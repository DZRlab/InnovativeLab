import streamlit as st
import json
from openai import AzureOpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os
import pyperclip
import uuid
import time

from chatbot.bedrock import generate_conversation
from chatbot.utils import (
    format_assistant, system_message, system_messages,
    download_json
)

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", None)
AZURE_OPENAI_APIKEY = os.getenv("AZURE_OPENAI_APIKEY", None)
AZURE_PHI_ENDPOINT = os.getenv("AZURE_PHI_ENDPOINT", None)
AZURE_PHI_APIKEY = os.getenv("AZURE_PHI_APIKEY", None)

AZURE_OPENAI_ENDPOINT = "https://revens-openai.openai.azure.com/"
AZURE_OPENAI_APIKEY = "2488b2f54fdb440a91b50d769b8481a0"
AZURE_PHI_ENDPOINT=""
AZURE_PHI_APIKEY=""


# Load data
with open("chat-config/models.json", "r") as f:
    model_config = json.load(f)

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

def format_model(key):
    return model_config[key]["display"]

def temp_change():
    print(temperature)

if "assistant" not in st.session_state:
    st.session_state.assistant = "assistant-standard"

if "system_prompt_value" not in st.session_state:
    st.session_state.system_prompt_value = system_message(
        system_messages, st.session_state.assistant
    )["content"]


def update_assistant():
    selected = st.session_state.assistant
    text = system_message(system_messages, selected)["content"]
    st.session_state.system_prompt_value = text


# Model endpoints

phi_client = ChatCompletionsClient(
    endpoint=AZURE_PHI_ENDPOINT, credential=AzureKeyCredential(AZURE_PHI_APIKEY)
)

oai_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01",
)

# Sidebar
temperature = st.sidebar.slider("Temperatur", 0.0, 1.0, value=0.9, step=0.1)

def set_chat_state():
    st.session_state.has_chat = True

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.has_chat = False
else:
    set_chat_state()


top_col1, top_col2 = st.columns([11, 1])

with top_col1:
    pass

with top_col2:
    if st.session_state.has_chat:
        if st.button(":material/Mop:", key="clear_chat"):
            st.session_state.messages = []
            st.session_state.has_chat = False


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if question_prompt := st.chat_input(
    "Hva har du lyst til å snakke om i dag?"
):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question_prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(question_prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Tenker på saken og jobber med et svar..."):
            config = {
                "messages": [
                    {"role": m["role"], "content": [{"text": m["content"]}]}
                    for m in st.session_state.messages
                ],
                "options": {
                    "temperature": temperature
                },
            }
            completion = generate_conversation(question_prompt, **config)
            # Helper function to stream response
            # https://discuss.streamlit.io/t/custom-write-stream/71366
            def generate_response():

                # format references
                formatted_references = ""
                for i, (key,value) in enumerate(completion[2].items(), start = 0):
                    formatted_references += f"**referanse {i+1}**:  \n\n{value}"

                # parts: answer, keywords, references
                response = completion[0]["output"]["text"] + "  \n\n**Nøkkelord**: " +  completion[1] + "  \n\n" + formatted_references

                for word in response:
                    yield word
                    time.sleep(0.005)
            response = st.write_stream(generate_response())

    # Add assistant response to chat history
    if response is not None:
        st.session_state.messages.append({"role": "assistant", "content": response})
        set_chat_state()


# Initialize chat buttons column
chat_col1, chat_col2 = st.columns(2)


# Copy chat history to clipboard
def copy_chat():
    chat = "\n".join([m["content"] for m in st.session_state.messages])
    pyperclip.copy(chat)
    st.toast("Kopiert til utklippstavlen")


with chat_col1:
    if st.session_state.messages:
        st.button(
            ":material/Content_Copy:", on_click=copy_chat, use_container_width=True
        )

with chat_col2:
    if st.session_state.messages:
        oid = uuid.uuid4()
        st.download_button(
            ":material/Save:",
            download_json(st.session_state.messages),
            f"chat-{str(oid)}.json",
            "application/json",
            key="download_chat",
            use_container_width=True,
        )
