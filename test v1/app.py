import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key="AIzaSyAG2TeiQcu0wPl-iLr1D60RI_1ylfSYnZM")

# Set up the Tavily client
tavily_client = TavilyClient(api_key="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")

# Set up the model
model = genai.GenerativeModel('gemini-2.0-flash')

def perform_research(query):
    """Use Tavily to perform deep research on a query"""
    try:
        search_results = tavily_client.search(query=query)
        research_data = []
        
        # Format search results
        for result in search_results.get("results", []):
            research_data.append(f"Title: {result.get('title')}")
            research_data.append(f"Content: {result.get('content')}")
            research_data.append(f"URL: {result.get('url')}")
            research_data.append("---")
        
        if research_data:
            return "\n".join(research_data)
        return "No research results found."
    except Exception as e:
        return f"Error performing research: {str(e)}"

def should_use_research(question):
    """Determine if deep research is needed based on question analysis"""
    # Ask Gemini if it needs additional information
    research_prompt = f"""
    Analyze this question: "{question}"
    
    Do you have enough information to provide a complete, accurate, and up-to-date answer?
    Reply with just "Yes" if you can answer confidently, or "No" if external research would help.
    """
    
    research_decision = model.generate_content(research_prompt).text.strip().lower()
    return "no" in research_decision

def get_gemini_response(question, chat_history=[]):
    """Get response from Gemini AI model with research enhancement if needed"""
    # Check if we need to do deep research
    research_data = ""
    if should_use_research(question):
        st.info("Performing deep research to enhance the answer...")
        research_data = perform_research(question)
    
    # Prepare the enhanced prompt
    if research_data:
        enhanced_prompt = f"""
        Question: {question}
        
        Additional research information to help you provide the most accurate answer:
        {research_data}
        
        Based on this information and your knowledge, please provide a comprehensive answer to the question.
        """
    else:
        enhanced_prompt = question
    
    # Initialize chat if this is a new conversation
    if not chat_history:
        chat = model.start_chat(history=[])
    else:
        # Convert history to format expected by Gemini
        formatted_history = []
        for entry in chat_history:
            if entry["role"] == "user":
                formatted_history.append({"role": "user", "parts": [entry["content"]]})
            else:
                formatted_history.append({"role": "model", "parts": [entry["content"]]})
        chat = model.start_chat(history=formatted_history)
    
    # Get response
    response = chat.send_message(enhanced_prompt)
    return response.text

# Streamlit UI
st.title("Research Assistant powered by Google Gemini")
st.subheader("Ask me anything about your research topic!")

# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input for user question
user_question = st.chat_input("Ask a research question...")
if user_question:
    # Add user question to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    
    # Display user question
    with st.chat_message("user"):
        st.write(user_question)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            response = get_gemini_response(user_question, st.session_state.chat_history)
            st.write(response)
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response}) 