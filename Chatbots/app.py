import contextlib
import streamlit as st
import os

@contextlib.contextmanager
def no_ssl_verification():
    """Context manager to disable SSL verification on httpx Client.
    """
    import httpx

    # Save original Client constructor
    Client = httpx.Client

    # Disable SSL verification
    httpx.Client = lambda *args, **kwargs: Client(*args, verify=False, **kwargs)

    # Yield control to the caller
    yield

    # Restore original verify value
    httpx.Client = Client

chat_page = st.Page("chat.py", title="Chat")
rag_page = st.Page("rag.py", title="RAG")

pg = st.navigation([chat_page, rag_page], position="hidden")

st.set_page_config(
    page_title="Innovasjonslab-GPT",
    menu_items={
        "About": "## Innovasjonslab-GPT\n\nSnakk med ulike AI-modeller for å generere tekst. Velg modell og juster parametere for å se hvordan modellen responderer på ulike input.",
    },
    layout="wide",
)

pg.run()