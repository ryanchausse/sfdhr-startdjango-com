# The plan here is to implement the Token Bucket algorithm. The API
# Connection Manager is a singleton that can add and subtract tokens
# to rate limit outgoing API requests. Rates can differ by vendor.

# A celerybeat scheduled task adds "requests per second" tokens every second,
# but concurrent request tokens need to be updated by the caller.

class APIConnectionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # For SmartRecruiters, published rate limits are:
        # 10 requests/s for each endpoint, generally
        # 8 concurrent requests, except for /candidates (only 1)
        # Rates can vary unpredictably through the day, especially at peak times
        self.sr_max_concurrent_requests = 8
        self.sr_max_concurrent_requests_candidates = 1
        self.sr_max_requests_per_second = 10

        # SR token bucket variables
        self.sr_current_concurrent_tokens = self.sr_max_concurrent_requests
        self.sr_current_concurrent_candidate_tokens = self.sr_max_concurrent_requests_candidates
        self.sr_current_requests_per_second_tokens = self.sr_max_requests_per_second

        # For AWS, rate limiting depends on a lot of factors.
        # Arbitrary numbers chosen here.
        self.aws_max_concurrent_requests = 10
        self.aws_max_requests_per_second = 100
        # AWS token bucket variables
        self.aws_current_concurrent_tokens = self.aws_max_concurrent_requests
        self.aws_current_requests_per_second_tokens = self.aws_max_requests_per_second

    # SmartRecruiters
    def sr_consume_one_request_token(self):
        # Not for /candidates endpoint. Remove a token from the bucket.
        if (self.sr_current_concurrent_tokens > 0 and
            self.sr_current_requests_per_second_tokens > 0):
            self.sr_current_concurrent_tokens -= 1
            self.sr_current_requests_per_second_tokens -= 1
            return True
        else:
            # Bucket empty, can't process request right now
            return False

    def sr_consume_one_request_token_candidate_endpoint(self):
        # Do we also need to remove a "normal" concurrency token?
        # Unclear from SmartRecruiters docs.
        if (self.sr_current_concurrent_candidate_tokens > 0 and
            self.sr_current_requests_per_second_tokens > 0):
            self.sr_current_concurrent_candidate_tokens -= 1
            self.sr_current_requests_per_second_tokens -= 1
            return True
        else:
            # Bucket empty, can't process request right now
            return False

    def sr_finished_with_request_token(self):
        # Not for /candidates endpoint. Use when request is complete to
        # update number of available concurrent tokens
        if (self.sr_current_concurrent_tokens < self.sr_max_concurrent_requests):
            self.sr_current_concurrent_tokens += 1
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True

    def sr_finished_with_request_token_candidate_endpoint(self):
        # For /candidates endpoint.
        if (self.sr_current_concurrent_candidate_tokens < self.sr_max_concurrent_requests_candidates):
            self.sr_current_concurrent_candidate_tokens += 1
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True

    def sr_add_token_for_requests_per_second(self):
        if self.sr_current_requests_per_second_tokens < self.sr_max_requests_per_second:
            self.sr_current_requests_per_second_tokens += 1
            return True

    def sr_get_current_requests_per_second_tokens(self):
        return self.sr_current_requests_per_second_tokens


    # AWS
    def aws_consume_one_request_token(self):
        # Remove a token from the bucket.
        if (self.aws_current_concurrent_tokens > 0 and
            self.aws_current_requests_per_second_tokens > 0):
            self.aws_current_concurrent_tokens -= 1
            self.aws_current_requests_per_second_tokens -= 1
            return True
        else:
            # Bucket empty, can't process request right now
            return False

    def aws_finished_with_request_token(self):
        # Use when request is complete to update number of available
        # concurrent tokens
        if (self.aws_current_concurrent_tokens < self.sr_max_concurrent_requests):
            self.aws_current_concurrent_tokens += 1
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True

    def aws_add_token_for_requests_per_second(self):
        if self.aws_current_requests_per_second_tokens < self.aws_max_requests_per_second:
            self.aws_current_requests_per_second_tokens += 1
            return True

    def aws_get_current_requests_per_second_tokens(self):
        return self.aws_current_requests_per_second_tokens
