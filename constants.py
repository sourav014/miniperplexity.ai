import os
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3
RETRY_DELAY = 2
SEARCH_TIME_LIMIT = 3
LLM_MODEL = 'gpt-4o-mini'
BING_API_KEY=os.getenv('BING_API_KEY')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
SEARCH_ENGINE_ID=os.getenv('SEARCH_ENGINE_ID')
GOOGLE_CUSTOM_SEARCH_API_KEY=os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')

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