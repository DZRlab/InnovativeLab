# chatbot_app.py
import streamlit as st
import boto3
import botocore
from botocore.exceptions import NoCredentialsError, BotoCoreError

# Config
KNOWLEDGE_BASE_NAME = "knowledge-base-quick-start-4f76g-data-source-chatbot"
KNOWLEDGE_BASE_ID = "UDZE28IZ9X"
REGION = "us-east-1"

# Initialize client (when trying from Goran's setup, try without verify argument)
try:
    client = boto3.client("bedrock-agent-runtime", region_name=REGION, verify=False)
except NoCredentialsError:
    st.error("AWS credentials not found.")
    st.stop()

# UI
st.title("Macedonian Financial Standards Chatbot")
question = st.text_input("Ask a question:")

if question:
    try:
        response = client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
                },
                "type": "KNOWLEDGE_BASE"
            }
        )
        answer = response.get("output", {}).get("text", "[No response]")
        st.markdown(f"**Answer:** {answer}")
    except BotoCoreError as e:
        st.error(f"AWS error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")