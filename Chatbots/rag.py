import streamlit as st
import os
import httpx
import json
import pyperclip
import uuid

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", None)
AZURE_OPENAI_APIKEY = os.getenv("AZURE_OPENAI_APIKEY", None)
ES_ENDPOINT = os.getenv("ES_ENDPOINT", None)

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# Create a custom httpx client with SSL verification disabled
httpx_client = httpx.Client(verify=False)

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview",
    transport=httpx_client  # This is where the custom transport goes,
)

# Set global variables

with open("models.json", "r") as f:
    model_config = json.load(f)

# Only OpenAI is supported, so we filter out any other models
model_config = {k: v for k, v in model_config.items() if v["client"] == "openai"}

# Initialize

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize citations
if "citations" not in st.session_state:
    st.session_state.citations = []

# Initialize chat state
if "has_chat" not in st.session_state:
    st.session_state.has_chat = None

# Initialize Elasticsearch defaults
if "es_connection" not in st.session_state:
    st.session_state.es_connection = None

if "es_content_field" not in st.session_state:
    st.session_state.es_content_field = "text"

if "es_infer_field" not in st.session_state:
    st.session_state.es_infer_field = "text_infer"

# Sidebar


@st.dialog("Legg til datakilde")
def es_connection():
    st.write(
        "Her kan du legge til informasjon om indeks og API-nøkkel. Ta kontakt med SUVDS for å få dette"
    )
    st.write("Søkeindeks")
    # Default values
    index = (
        st.session_state.es_connection["index"]
        if st.session_state.es_connection is not None
        else ""
    )
    api_key = (
        st.session_state.es_connection["api_key"]
        if st.session_state.es_connection is not None
        else ""
    )
    es_index = st.text_input("Navn på indeks", value=index)
    es_key = st.text_input("API-nøkkel", value=api_key)
    es_content_field = st.text_input(
        "Feltnavn for tekstinnhold", value=st.session_state.es_content_field
    )
    es_infer_field = st.text_input(
        "Feltnavn for vektorsøk", value=st.session_state.es_infer_field
    )
    if st.button("Lagre"):
        st.session_state.es_connection = {"index": es_index, "api_key": es_key}
        st.session_state.es_content_field = es_content_field
        st.session_state.es_infer_field = es_infer_field
        st.rerun()


if st.session_state.es_connection is not None:

    if (
        st.session_state.es_connection["index"] is None
        or len(st.session_state.es_connection["index"]) == 0
    ):
        st.error("Mangler indeks", icon=":material/error:")
    else:
        st.sidebar.info(
            f"Søker nå i data fra **{st.session_state.es_connection['index']}**",
            icon=":material/info:",
        )

    if (
        st.session_state.es_connection["api_key"] is None
        or len(st.session_state.es_connection["api_key"]) == 0
    ):
        st.error("Mangler API-nøkkel", icon=":material/error:")

    def format_model(key):
        return model_config[key]["display"]

    model = st.sidebar.selectbox(
        "Velg modell", options=list(model_config.keys()), format_func=format_model
    )

    n_docs = st.sidebar.number_input(
        "Antall dokumenter", min_value=1, max_value=20, value=4, step=1
    )

    temperature = st.sidebar.slider(
        "Temperatur", min_value=0.0, max_value=1.0, value=0.7, step=0.1
    )

if st.sidebar.button("Bruk egne data"):
    es_connection()


# Main page

top_col1, top_col2 = st.columns([11, 1])

with top_col1:
    pass

with top_col2:
    if st.session_state.has_chat:
        if st.button(":material/Mop:", key="clear_chat"):
            st.session_state.messages = []
            st.session_state.has_chat = False


def set_chat_state():
    chat_status = 0 if not st.session_state.has_chat else st.session_state.has_chat
    st.session_state.has_chat = chat_status + 1


if st.session_state.es_connection is None:
    st.warning(
        "Du må velge en datakilde før du kan gå videre", icon=":material/warning:"
    )
else:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        icon = (
            ":material/robot:"
            if message["role"] == "assistant"
            else ":material/person:"
        )
        with st.chat_message(message["role"], avatar=icon):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(
        "Hva har du lyst til å snakke om i dag?",
        max_chars=1024 * 16,
        on_submit=set_chat_state,
    ):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Vent litt, jeg jobber med saken..."):
                messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
                print(st.session_state.has_chat)
                params = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                }
                if st.session_state.has_chat == 1:
                    params["extra_body"] = {
                        "data_sources": [
                            {
                                "type": "elasticsearch",
                                "parameters": {
                                    "endpoint": ES_ENDPOINT,
                                    "index_name": st.session_state.es_connection[
                                        "index"
                                    ],
                                    "query_type": "vector",
                                    "fields_mapping": {
                                        "title_field": "name",
                                        "content_fields": st.session_state.es_content_field.split(
                                            ","
                                        ),
                                        "vector_fields": st.session_state.es_infer_field.split(
                                            ","
                                        ),
                                    },
                                    "embedding_dependency": {
                                        "type": "model_id",
                                        "model_id": ".multilingual-e5-small_linux-x86_64",
                                    },
                                    "top_n_documents": n_docs,
                                    "authentication": {
                                        "type": "encoded_api_key",
                                        "encoded_api_key": st.session_state.es_connection[
                                            "api_key"
                                        ],
                                    },
                                },
                            }
                        ]
                    }
                completion = client.chat.completions.create(**params)
                response = completion.choices[0].message.content
                st.session_state.citations = completion.choices[0].message.context[
                    "citations"
                ]
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.write(response)


# Check if we have citations and add buttons to display them
if st.session_state.citations is not None and len(st.session_state.citations) > 0:
    for idx, citation in enumerate(st.session_state.citations):

        @st.dialog("Kilde", width="large")
        def citation_dialog():
            st.write(citation["content"])

        if st.button(f"Vis kilde {idx+1}", key=f"citation_button{idx}"):
            citation_dialog()


# Copy chat history to clipboard
def copy_chat():
    chat = "\n".join([m["content"] for m in st.session_state.messages])
    pyperclip.copy(chat)
    st.toast("Kopiert til utklippstavlen")


# Convert chat history to JSON-data for download
def download_json(data):
    json_data = json.dumps(data)
    json_bytes = json_data.encode("utf-8")

    return json_bytes


# Initialize chat buttons column
chat_col1, chat_col2 = st.columns(2)

with chat_col1:
    if st.session_state.has_chat:
        st.button(
            ":material/Content_Copy:", on_click=copy_chat, use_container_width=True
        )

with chat_col2:
    if st.session_state.has_chat:
        oid = uuid.uuid4()
        st.download_button(
            ":material/Save:",
            download_json(
                [
                    {"chat": st.session_state.messages},
                    {"citations": st.session_state.citations},
                ]
            ),
            f"rag-{str(oid)}.json",
            "application/json",
            key="download_chat",
            use_container_width=True,
        )
