import requests
import time
from constants import SEARCH_ENGINE_ID, GOOGLE_CUSTOM_SEARCH_API_KEY, MAX_RETRIES, RETRY_DELAY, BING_API_KEY

class SearchHandler:
    def fetch(self, query: str) -> list:
        raise NotImplementedError("Subclasses must implement this method.")
    

class GoogleCustomSearchHandler(SearchHandler):
    def fetch(self, query: str) -> list:
        for attempt in range(MAX_RETRIES):
            try:
                urls = []
                response = requests.get(f'https://customsearch.googleapis.com/customsearch/v1?cx={SEARCH_ENGINE_ID}&key={GOOGLE_CUSTOM_SEARCH_API_KEY}&q={query}')
                response.raise_for_status()
                response_json = response.json()
                resonse_items = response_json.get('items')
                if resonse_items:
                    for response_item in resonse_items:
                        if response_item.get('link'):
                            urls.append(response_item.get('link'))

                return urls
            except requests.RequestException as e:
                print(f"GoogleCustomSearchHandler Error: {e}. Attempt {attempt + 1} of {MAX_RETRIES}.")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)

        print(f"GoogleCustomSearchHandler Error: Failed to fetch results after several attempts for query {query}")
        return []
    
class BingSearchHandler(SearchHandler): 
    def fetch(self, query: str) -> list:
        endpoint = "https://api.bing.microsoft.com/v7.0/search"
        params = { 'q': query}
        headers = { 'Ocp-Apim-Subscription-Key': BING_API_KEY }
        for attempt in range(MAX_RETRIES):
            try:
                urls = []
                response = requests.get(endpoint, headers=headers, params=params)
                response.raise_for_status()
                response_json = response.json()
                web_pages = response_json.get('webPages')
                if web_pages:
                    response_values = web_pages.get('value')
                    if response_values:
                        for response_value in response_values:
                            if response_value.get('url'):
                                urls.append(response_value.get('url'))

                return urls
            except requests.RequestException as e:
                print(f"BingSearchHandler Error: {e}. Attempt {attempt + 1} of {MAX_RETRIES}.")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
        
        print(f"BingSearchHandler Error: Failed to fetch results after several attempts for query {query}")
        return []