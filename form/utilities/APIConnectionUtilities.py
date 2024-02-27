# The plan here is to implement the Token Bucket algorithm. The API
# Connection Manager can add and subtract tokens to rate limit outgoing
# API requests. Rates can differ by vendor.

# A celerybeat scheduled task adds "requests per second" tokens every second,
# but concurrent request tokens need to be updated by the caller.
from form.models import APIRateLimiter

class APIConnectionManager:
    # For SmartRecruiters, published rate limits are:
    # 10 requests/s for each endpoint, generally
    # 8 concurrent requests, except for /candidates (only 1)
    # Rates can vary unpredictably through the day, especially at peak times
    SR_MAX_CONCURRENT_REQUESTS = 8
    SR_MAX_CONCURRENT_REQUESTS_CANDIDATES = 1
    SR_MAX_REQUESTS_PER_SECOND = 10

    # For AWS, rate limiting depends on a lot of factors.
    # Arbitrary numbers chosen here.
    AWS_MAX_CONCURRENT_REQUESTS = 10
    AWS_MAX_REQUESTS_PER_SECOND = 100

    # SmartRecruiters
    def sr_consume_one_request_token():
        # Not for /candidates endpoint. Remove a token from the bucket.
        api_rate_limiter = APIRateLimiter.objects.get()
        if (api_rate_limiter.sr_current_concurrent_tokens > 0 and
            api_rate_limiter.sr_current_requests_per_second_tokens > 0):
            api_rate_limiter.sr_current_concurrent_tokens -= 1
            api_rate_limiter.sr_current_requests_per_second_tokens -= 1
            api_rate_limiter.save()
            return True
        else:
            # Bucket empty, can't process request right now
            return False

    def sr_consume_one_request_token_candidate_endpoint():
        # Do we also need to remove a "normal" concurrency token?
        # Unclear from SmartRecruiters docs.
        api_rate_limiter = APIRateLimiter.objects.get()
        if (api_rate_limiter.sr_current_concurrent_candidate_tokens > 0 and
            api_rate_limiter.sr_current_requests_per_second_tokens > 0):
            api_rate_limiter.sr_current_concurrent_candidate_tokens -= 1
            api_rate_limiter.sr_current_requests_per_second_tokens -= 1
            api_rate_limiter.save()
            return True
        else:
            # Bucket empty, can't process request right now
            return False

    def sr_finished_with_request_token(self):
        # Not for /candidates endpoint. Use when request is complete to
        # update number of available concurrent tokens
        api_rate_limiter = APIRateLimiter.objects.get()
        if (api_rate_limiter.sr_current_concurrent_tokens < self.SR_MAX_CONCURRENT_REQUESTS):
            api_rate_limiter.sr_current_concurrent_tokens += 1
            api_rate_limiter.save()
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True

    def sr_finished_with_request_token_candidate_endpoint(self):
        # For /candidates endpoint.
        api_rate_limiter = APIRateLimiter.objects.get()
        if (api_rate_limiter.sr_current_concurrent_candidate_tokens < self.SR_MAX_CONCURRENT_REQUESTS_CANDIDATES):
            api_rate_limiter.sr_current_concurrent_candidate_tokens += 1
            api_rate_limiter.save()
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True

    def sr_add_token_for_requests_per_second(self):
        api_rate_limiter = APIRateLimiter.objects.get()
        if api_rate_limiter.sr_current_requests_per_second_tokens < self.SR_MAX_REQUESTS_PER_SECOND:
            api_rate_limiter.sr_current_requests_per_second_tokens += 1
            api_rate_limiter.save()
            return True

    def sr_get_current_requests_per_second_tokens(self):
        api_rate_limiter = APIRateLimiter.objects.get()
        return api_rate_limiter.sr_current_requests_per_second_tokens


    # AWS
    def aws_consume_one_request_token():
        # Remove a token from the bucket.
        api_rate_limiter = APIRateLimiter.objects.get()
        if (api_rate_limiter.aws_current_concurrent_tokens > 0 and
            api_rate_limiter.aws_current_requests_per_second_tokens > 0):
            api_rate_limiter.aws_current_concurrent_tokens -= 1
            api_rate_limiter.aws_current_requests_per_second_tokens -= 1
            api_rate_limiter.save()
            return True
        else:
            # Bucket empty, can't process request right now
            return False

    def aws_finished_with_request_token(self):
        # Use when request is complete to update number of available
        # concurrent tokens
        api_rate_limiter = APIRateLimiter.objects.get()
        if (api_rate_limiter.aws_current_concurrent_tokens < self.AWS_MAX_CONCURRENT_REQUESTS):
            api_rate_limiter.aws_current_concurrent_tokens += 1
            api_rate_limiter.save()
            return True
        else:
            # Bucket is full, so we don't have to do anything
            return True

    def aws_add_token_for_requests_per_second(self):
        api_rate_limiter = APIRateLimiter.objects.get()
        if api_rate_limiter.aws_current_requests_per_second_tokens < self.AWS_MAX_REQUESTS_PER_SECOND:
            api_rate_limiter.aws_current_requests_per_second_tokens += 1
            api_rate_limiter.save()
            return True

    def aws_get_current_requests_per_second_tokens():
        api_rate_limiter = APIRateLimiter.objects.get()
        return api_rate_limiter.aws_current_requests_per_second_tokens
