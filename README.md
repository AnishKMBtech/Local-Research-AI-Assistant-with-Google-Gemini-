# Research AI Assistant with Google Gemini

This is a deep research AI assistant chatbot powered by Google's Gemini AI model with Tavily search integration. It allows you to ask research questions and get detailed, accurate responses even for topics the model might not have complete information about.

## Features

- Powered by Google Gemini 2.0 Flash model
- Integrated with Tavily search API for enhanced research capabilities
- Automatically determines when deep research is needed
- Clean, intuitive chat interface built with Streamlit
- Conversation history maintained during session
- Easy setup and deployment

## Setup Instructions

1. **Clone this repository**

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Get API keys**
   - Get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
   - Get a Tavily API key from [Tavily](https://tavily.com/)

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Replace `your_api_key_here` with your actual Gemini API key
   - Replace `your_tavily_api_key_here` with your actual Tavily API key

5. **Run the application**
   ```
   streamlit run app.py
   ```

6. **Open the application**
   - The app will be available at `http://localhost:8501` in your browser

## Usage

- Type your research question in the chat input
- The AI assistant will determine if it needs to perform deep research
- If research is needed, it will use Tavily to gather the latest information
- Your question will be answered using a combination of Gemini's knowledge and the research results
- Your conversation history is maintained throughout the session

## How It Works

The assistant follows this process for each question:
1. Analyzes your question to determine if research is needed
2. If needed, performs a web search using Tavily API to gather the latest information
3. Combines the research data with Gemini's knowledge to create a comprehensive answer
4. Presents the answer in a conversational format

## Requirements

- Python 3.7+
- Internet connection for API calls
- Google Gemini API key

- Tavily API key 
