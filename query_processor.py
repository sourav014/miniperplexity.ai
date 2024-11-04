
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SEARCH_TIME_LIMIT = 3
LLM_MODEL = 'gpt-4o-mini'
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

system_prompt_cited_answer = """You are a helpful assistant who is expert at answering user's queries based on the cited context."""
cited_answer_prompt = """
Provide a relevant, informative response to the user's query using the given context (search results with [citation number](website link) and brief descriptions).

- Answer directly without referring the user to any external links.
- Use an unbiased, journalistic tone and avoid repeating text.
- Format your response in markdown with bullet points for clarity.
- Cite all information using [citation number](website link) notation, matching each part of your answer to its source.

Context Block:
{context_block}

User Query:
{query}
"""


class QueryProcessor:
    def __init__(self, handlers) -> None:
        self.handlers = handlers
    

    def search_query(self, query: str):
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(handler.fetch, query): handler for handler in self.handlers}
            for future in as_completed(future_to_url):
                handler = future_to_url[future]
                try:
                    result = future.result()
                    results.append((handler.__class__.__name__, result))
                except Exception as e:
                    print(f"{handler.__class__.__name__} generated an exception: {e}")

        return results
    
    def fetch_webpages(self, url, timeout):
        try:
            print(f"Fetching content from link: {url}")
            response = requests.get(url=url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            paragraphs = soup.find_all('p')
            page_text = ' '.join([para.get_text() for para in paragraphs])
            return url, page_text
        except (requests.exceptions.RequestException, TimeoutError) as e:
            print(f"Error fetching {url}: {e}")
        return url, None
    
    def process_urls(self, urls):
        results = dict()
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(self.fetch_webpages, url, SEARCH_TIME_LIMIT): url for url in urls}
            for future in future_to_url:
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        url = result[0]
                        page_text = result[1]
                        if url and page_text:
                            results[url] = page_text
                except Exception as e:
                    print(e)
            return results
        
    def llm_call(self, query, searc_dic, llm_model=LLM_MODEL):
        client = OpenAI(api_key=OPENAI_API_KEY)
        context_block = "\n".join([f"[{index+1}]({url}): {content}" for index, (url, content) in enumerate(searc_dic.items())])
        prompt = cited_answer_prompt.format(context_block=context_block, query=query)
        system_prompt = system_prompt_cited_answer
        msg = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=llm_model,
            messages=[{"role": "system", "content": system_prompt}, *msg]
        )
        llm_answer = response.choices[0].message.content
        return llm_answer

    def process_query(self, query: str):
        final_respose = None
        search_results = self.search_query(query=query)
        for search_result in search_results:
            _, web_page_urls = search_result
            results = self.process_urls(urls=web_page_urls)
            sources = "\n".join([f"{number+1}. {link}" for number, link in enumerate(results.keys())])
            llm_answer = self.llm_call(query=query, searc_dic=results)
            if sources and llm_answer:
                final_respose = sources + "\n \n" + llm_answer

        return final_respose



