import os
from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain


import json

course_data = json.load(open("CPSC.json"))


def get_llm():
    model_kwargs = {
        "modelId": "anthropic.claude-v2:1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": '{"prompt":"\\n\\nHuman: Hello world\\n\\nAssistant:","max_tokens_to_sample":300,"temperature":0.5,"top_k":250,"top_p":1,"stop_sequences":["\\n\\nHuman:"],"anthropic_version":"bedrock-2023-05-31"}',
    }

    llm = Bedrock(
        credentials_profile_name=os.environ.get(
            "BWB_PROFILE_NAME"
        ),  # sets the profile name to use for AWS credentials (if not the default)
        region_name=os.environ.get(
            "BWB_REGION_NAME"
        ),  # sets the region name (if not the default)
        endpoint_url=os.environ.get(
            "BWB_ENDPOINT_URL"
        ),  # sets the endpoint URL (if necessary)
        model_id="anthropic.claude-v2:1",  # set the foundation model
        model_kwargs=model_kwargs,
    )  # configure the properties for Claude

    return llm


def get_memory():  # create memory for this chat session
    # ConversationSummaryBufferMemory requires an LLM for summarizing older messages
    # this allows us to maintain the "big picture" of a long-running conversation
    llm = get_llm()

    memory = ConversationSummaryBufferMemory(
        llm=llm, max_token_limit=1024
    )  # Maintains a summary of previous messages

    return memory


def get_chat_response(input_text, memory):  # chat client function
    prompt = f"{course_data} + {input_text}"

    llm = get_llm()

    conversation_with_summary = ConversationChain(  # create a chat client
        llm=llm,  # using the Bedrock LLM
        memory=memory,  # with the summarization memory
        verbose=True,  # print out some of the internal states of the chain while running
    )

    chat_response = conversation_with_summary.predict(
        input=prompt
    )  # pass the user message and summary to the model

    return chat_response
