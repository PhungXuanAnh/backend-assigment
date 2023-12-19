from rest_framework.throttling import UserRateThrottle


class UserRate2RequestsPer10SecondsThrottle(UserRateThrottle):
    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>

        So we always return a rate for 2 request per 10 seconds.

        Args:
            string: rate to be parsed, which we ignore.

        Returns:
            tuple:  <allowed number of requests>, <period of time in seconds>
        """
        return (2, 10)
