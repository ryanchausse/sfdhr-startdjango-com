from form.utilities.APIConnectionUtilities import APIConnectionManager
import time
import requests

class SmartRecruitersAPI:
    def __init__(self, request, api_request_details):
        self.request = request
        self.api_request_details = api_request_details
        self.retry_delay = 1 # seconds, by default
        self.retries = 20

    def retry_token_with_backoff(self, uri, candidate_endpoint = False):
        if self.retries == 0:
            raise TimeoutError('Max retries for SR API request tokens reached')
        self.retries -= 1
        time.sleep(self.retry_delay)
        self.retry_delay = self.retry_delay * 1.2
        if not candidate_endpoint:
            self.api_request(uri=uri)
        else:
            self.api_request_candidate_endpoint(uri=uri)

    def retry_sr_api_with_backoff(self, uri, retry_after = 0, candidate_endpoint = False):
        if self.retries == 0:
            raise TimeoutError('Max retries for SR API request reached')
        self.retries -= 1
        if not retry_after:
            time.sleep(self.retry_delay)
        else:
            time.sleep(float(retry_after) + float(0.2))
        if not candidate_endpoint:
            self.api_request()
        else:
            self.api_request_candidate_endpoint()

    def api_request(self, uri):
        api_mgr = APIConnectionManager()
        if not api_mgr.sr_consume_one_request_token():
            self.retry_token_with_backoff()

        # Query SR API
        response = requests.get(
            url='https://api.smartrecruiters.com/' + uri)

        # If HTTP status code 429 returned, or if 'Retry-After' header
        # included in response, retry with delay.
        if (response.headers['status_code'] == 429 or
           'Retry-After' in response.headers):
            if 'Retry-After' in response.headers:
                # Maybe verify here that value is a float
                self.retry_sr_api_with_backoff(
                    uri=uri,
                    retry_after=response.headers['Retry-After'])
            else:
                self.retry_sr_api_with_backoff(uri=uri)

        if not api_mgr.sr_finished_with_request_token():
            raise ValueError('Was not able to put token back into'
                             'concurrency bucket for SR API')
        return response
    
    def api_request_candidate_endpoint(self, uri):
        api_mgr = APIConnectionManager()
        if not api_mgr.sr_consume_one_request_token_candidate_endpoint():
            self.retry_token_with_backoff(uri=uri, candidate_endpoint=True)

        # Query SR API
        response = requests.get(
            url='https://api.smartrecruiters.com/' + uri)

        # If HTTP status code 429 returned, or if 'Retry-After' header
        # included in response, retry with delay.
        if (response.headers['status_code'] == 429 or
           'Retry-After' in response.headers):
            if 'Retry-After' in response.headers:
                # Maybe verify here that value is a float
                self.retry_sr_api_with_backoff(
                    uri=uri,
                    retry_after=response.headers['Retry-After'],
                    candidate_endpoint=True)
            else:
                self.retry_sr_api_with_backoff(uri=uri, candidate_endpoint=True)

        if not api_mgr.sr_finished_with_request_token_candidate_endpoint():
            raise ValueError('Was not able to put token back into'
                             '/candidate concurrency bucket for SR API')
        return response

    def get_candidate(self):
        uri = f"candidate/{self.api_request_details['candidate_uuid']}"
        response = self.api_request_candidate_endpoint(uri=uri)
        if ('status_code' in response.headers and
            response.headers['status_code'] == '200'):
            return response.text
        else:
            print('Request for candidate details failed')
            # Add info here from response, perhaps
            return False
