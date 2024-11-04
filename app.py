import os
    
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS
from search import GoogleCustomSearchHandler, BingSearchHandler
from query_processor import QueryProcessor

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/health")
def health_check():
    return "Server is up!"

@app.route("/api/search", methods=['POST'])
def resolve_search_query():
    data = request.get_json()
    # print(data)
    user_query = data.get('query')
    print(user_query)
    # handlers = [GoogleCustomSearchHandler(), BingSearchHandler()]
    handlers = [GoogleCustomSearchHandler()]
    query_processor = QueryProcessor(handlers=handlers)
    search_results = query_processor.process_query(query=user_query)
    # print(urls)
    res = None
    for search_result in search_results:
        search_handler, web_page_urls = search_result
        # print(search_handler)
        # print(web_page_urls)
        results = query_processor.process_urls(urls=web_page_urls)
        sources = "\n".join([f"{number+1}. {link}" for number, link in enumerate(results.keys())])
        # print(sources)
        # print(results)
        res = sources
        llm_answer = query_processor.llm_call(query=user_query, searc_dic=results)
        res += "\n \n" + llm_answer
    print(res)
    return jsonify({'response': res})

if __name__ == "__main__":
    app.run(host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT"))