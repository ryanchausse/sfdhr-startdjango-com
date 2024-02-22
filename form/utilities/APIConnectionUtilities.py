# The plan here is to implement the Token Bucket algorithm. The API
# Connection Manager is a singleton that can add and subtract tokens
# to rate limit outgoing API requests. Rates can differ by vendor.

# A celerybeat scheduled task adds "requests per second" tokens every second,
# but concurrent request tokens need to be updated by the caller.

class APIConnectionManager:
    _instance = None

    # For SmartRecruiters, published rate limits are:
    # 10 requests/s for each endpoint, generally
    # 8 concurrent requests, except for /candidates (only 1)
    # Rates can vary unpredictably through the day, especially at peak times
    sr_max_concurrent_requests = 8
    sr_max_concurrent_requests_candidates = 1
    sr_max_requests_per_second = 10
    # SR token bucket variables
    sr_current_concurrent_tokens = sr_max_concurrent_requests
    sr_current_concurrent_candidate_tokens = sr_max_concurrent_requests_candidates
    sr_current_requests_per_second_tokens = sr_max_requests_per_second

    # For AWS, rate limiting depends on a lot of factors.
    # Arbitrary numbers chosen here.
    aws_max_concurrent_requests = 10
    aws_max_requests_per_second = 100
    # AWS token bucket variables
    aws_current_concurrent_tokens = aws_max_concurrent_requests
    aws_current_requests_per_second_tokens = aws_max_requests_per_second

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    # SmartRecruiters
    def sr_consume_one_request_token(cls):
        # Not for /candidates endpoint. Remove a token from the bucket.
        if (cls.sr_current_concurrent_tokens > 0 and
            cls.sr_current_requests_per_second_tokens > 0):
            cls.sr_current_concurrent_tokens -= 1
            cls.sr_current_requests_per_second_tokens -= 1
            return True
        else:
            # Bucket empty, can't process request right now
            return False
    
    def sr_consume_one_request_token_candidate_endpoint(cls):
        # Do we also need to remove a "normal" concurrency token?
        # Unclear from SmartRecruiters docs.
        if (cls.sr_current_concurrent_candidate_tokens > 0 and
            cls.sr_current_requests_per_second_tokens > 0):
            cls.sr_current_concurrent_candidate_tokens -= 1
            cls.sr_current_requests_per_second_tokens -= 1
            return True
        else:
            # Bucket empty, can't process request right now
            return False
    
    def sr_finished_with_request_token(cls):
        # Not for /candidates endpoint. Use when request is complete to
        # update number of available concurrent tokens
        if (cls.sr_current_concurrent_tokens < cls.sr_max_concurrent_requests):
            cls.sr_current_concurrent_tokens += 1
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True
    
    def sr_finished_with_request_token_candidate_endpoint(cls):
        # For /candidates endpoint.
        if (cls.sr_current_concurrent_candidate_tokens < cls.sr_max_concurrent_requests_candidates):
            cls.sr_current_concurrent_candidate_tokens += 1
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True

    # AWS
    def aws_consume_one_request_token(cls):
        # Remove a token from the bucket.
        if (cls.aws_current_concurrent_tokens > 0 and
            cls.aws_current_requests_per_second_tokens > 0):
            cls.aws_current_concurrent_tokens -= 1
            cls.aws_current_requests_per_second_tokens -= 1
            return True
        else:
            # Bucket empty, can't process request right now
            return False
    
    def aws_finished_with_request_token(cls):
        # Use when request is complete to update number of available
        # concurrent tokens
        if (cls.aws_current_concurrent_tokens < cls.sr_max_concurrent_requests):
            cls.aws_current_concurrent_tokens += 1
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True
