import os
from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain
import json
import streamlit as st

# Assuming CPSC.json contains relevant data for the conversation
course_data = json.load(open("CPSC.json"))


def get_llm():
    # Initialize Bedrock with only the necessary parameters
    llm = Bedrock(
        credentials_profile_name=os.environ.get(
            "BWB_PROFILE_NAME"
        ),  # Optional: specify AWS credentials profile name
        region_name=os.environ.get(
            "BWB_REGION_NAME"
        ),  # Optional: specify the AWS region
        endpoint_url=os.environ.get(
            "BWB_ENDPOINT_URL"
        ),  # Optional: specify the endpoint URL
        model_id="anthropic.claude-v2:1",  # Specify the model ID directly without `model_kwargs`
    )
    return llm


def get_memory():
    # Initialize memory for the chat session
    llm = get_llm()
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=20000,  # Maintain a summary of previous messages up to a token limit
    )
    return memory


def get_chat_response(input_text, memory):
    courses_taken = " "
    if "courses_taken" in st.session_state:
        # Access the saved courses_taken from the session state
        courses_taken = st.session_state["courses_taken"]

    # Build the chat response
    prompt = f"This is course data for courses at UBC: {course_data} This is my question:, ({input_text} I have only taken these courses: {courses_taken})"
    llm = get_llm()
    conversation_with_summary = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True,  # Print internal states of the chain while running
    )
    chat_response = conversation_with_summary.predict(input=prompt)
    return chat_response
