import os
import time
    
from flask import Flask, request, render_template, Response, stream_with_context
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
    return Response(query_processor.process_query_stream(query=user_query), mimetype='text/plain')

if __name__ == "__main__":
    app.run(port=os.getenv("SERVER_PORT"))