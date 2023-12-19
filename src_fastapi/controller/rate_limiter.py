import time
import json
import os
import redis as python_redis

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS


class RateLimiter:
    def __init__(self, redis_url, times, period_second):
        self.times = times
        self.period = period_second
        self.redis = python_redis.from_url(redis_url)
        self.history = None

    async def _check(self, request):
        self.key = await self.get_identifier(request)
        if self.key is None:
            return True

        history = self.redis.get(self.key)
        self.history = json.loads(history) if history else []
        self.now = time.time()

        while self.history and self.history[-1] <= self.now - self.period:
            self.history.pop()
        if len(self.history) >= self.times:
            wait_time = await self.wait()
        else:
            self.history.insert(0, self.now)
            self.redis.setex(self.key, self.period, json.dumps(self.history))
            wait_time = 0

        self.redis.close()
        return wait_time

    async def wait(self):
        """
        Returns wait time to retry call API.
        """
        if self.history:
            remaining_time = self.period - (self.now - self.history[-1])
        else:
            remaining_time = self.period

        available_requests = self.times - len(self.history) + 1
        if available_requests <= 0:
            return None

        return int(remaining_time / available_requests)

    async def get_identifier(self, request: Request):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.client.host
        return ip + ":" + request.scope["path"]

    async def __call__(self, request: Request, response: Response):
        if os.environ.get("ENVIRONMENT") == "pytest":
            return
        wait_time = await self._check(request)
        if wait_time != 0:
            raise HTTPException(
                HTTP_429_TOO_MANY_REQUESTS,
                f"Too Many Requests, Retry after {wait_time} seconds",
                headers={"Retry-After": str(wait_time)},
            )
