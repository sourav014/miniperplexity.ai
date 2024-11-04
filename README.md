# miniperplexity.ai
Minimal version of Q&amp;A system like Perplexity.ai

Setting Up the Repository Locally
=================================
Setting up this project is straightforward. Follow the steps below to prepare your local environment.
### Prerequisites
Ensure the following are installed and configured before proceeding:
1.  **Python** - [Download Python](https://www.python.org/downloads/)
    
2.  **API Keys**
    
    *   **OpenAI API Key** - [Generate here](https://platform.openai.com/account/api-keys)
        
    *   **Google Custom Search API Key** and **Search Engine ID** or **Bing API Key**
        
        *   For Google, create a Custom Search API Key and a Search Engine ID
            
        *   For Bing, [create a Bing Search API Key](https://www.microsoft.com/en-us/bing/apis/bing-search-api-v7)
            
### Steps to Set Up
1.  Clone the repository:
    ```
    git clone https://github.com/sourav014/miniperplexityAI.git
    ```
    
2.  Install dependencies: Navigate to the project directory and install required packages from requirements.txt:
    ```
    cd miniperplexityAI
    pip install -r requirements.txt
    ```
    
3.  Configure environment variables: Create a .env file in the project root and add your configuration values:
    ```
    SERVER_HOST="0.0.0.0"
    SERVER_PORT="8080"
    GOOGLE_CUSTOM_SEARCH_API_KEY="your-google-custom-search-api-key"
    SEARCH_ENGINE_ID="your-search-engine-id"
    BING_API_KEY="your-bing-api-key"
    OPENAI_API_KEY="your-openai-api-key"
    ```
    
4.  Start the server: Run the application:
    ```
    python3 app.py
    ```
