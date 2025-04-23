import os
import boto3
import json
import logging
import re

# Model ID
model_id = "anthropic.claude-3-5-haiku-20241022-v1:0"

boto3.setup_default_session(
    aws_access_key_id=os.environ.get("blabla"),
    aws_secret_access_key=os.environ.get("blabla"),
    region_name=
    os.environ.get("blabla", "us-east-1"),
)

s3_session = boto3.Session(
    region_name="us-east-1"
)

# Set up the Amazon Bedrock client
bedrock_client_untrained = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

bedrock_agent_runtime_client = s3_session.client(service_name = "bedrock-agent-runtime", region_name="us-east-1")

class InferenceConfig(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__allowed_keys = ["maxTokens", "temperature", "topP", "stopSequences"]
        for key in self.keys():
            self._check_key(key)

    def _check_key(self, key):
        if key not in self.__allowed_keys:
            raise KeyError(
                f"Key '{key}' is not allowed. Allowed keys are: {self.__allowed_keys}"
            )

    def __setitem__(self, key, value):
        self._check_key(key)
        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        for key in dict(*args, **kwargs).keys():
            self._check_key(key)
        super().update(*args, **kwargs)


def generate_conversation(
    question_prompt: str, messages: list, options: dict | None = None
) -> dict:
    # Config
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html
    # https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html
    inference_config = InferenceConfig(
        {"maxTokens": 2000, "temperature": 0.7, "topP": 0.999}
    )
    top_k = 200

    # If the user has added options, we merge our dicts
    if isinstance(options, dict):
        inference_config.update(options)
        # If we have empty stop sentences, we must remove them
        if "stopSequences" in inference_config.keys():
            if not all(inference_config["stopSequences"]):
                _ = inference_config.pop("stopSequences")

    # Additional inference parameters to use.
    additional_model_fields = {"top_k": top_k}

    # Step 1: ask a question
    answer = bedrock_agent_runtime_client.retrieve_and_generate(
        input={
            'text': question_prompt
        },
        retrieveAndGenerateConfiguration={
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": BUCKET_ID,
                "modelArn": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            },
            'type': 'KNOWLEDGE_BASE'
        }
    )

    # Step 2: formulate a couple of keywords based on the above query
    # Prompt
    keyword_prompt_user_part = "Based on the exchange below, formulate maximum 5 keywords that pertain to the topic as hand as a python list \n" + "question:\n" + question_prompt + "\nanswer:\n" + str(answer["output"]["text"]) + "\n"
    keyword_prompt_system_part = "You are an expert on audit. Questions will be in Norwegian. You should answer in Norwegian. For the question at hand, your job is to create keywords that can be used to match the questions to a potential answer. You will generate keywords that describes the topic of the question, as many as needed, but keep it terse. Keywords may contain underscores. In particular, if the question is answered by an ISA, the name of the document should be a keyword\n"
    keyword_prompt = keyword_prompt_user_part + keyword_prompt_system_part

    # Configure an unspecialized claude
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "temperature": 0.9,
        "top_k": 250,
        "top_p": 1,
        "messages": [{"role": "user","content": [{"type": "text","text": keyword_prompt}]}]
    }

    # Call
    keywords = bedrock_client_untrained.invoke_model(
        modelId=model_id,
        body=json.dumps(payload)
    )
    # create keywords
    keywords = json.loads(keywords["body"].read())
    keywords = f"  \n\n**Nøkkelord**: {keywords["content"][0]["text"]}"

    # create references
    pattern = r"\w\/(.*?\.pdf)"
    references = {}
    for i,v in enumerate(answer["citations"][0]["retrievedReferences"]):
        references[f"reference_{i+1}"] = (f" -- filnavn: '{re.findall(pattern, v["metadata"]["x-amz-bedrock-kb-source-uri"])[0]}'  \n\n**kildetekst**: '...{v["content"]["text"]}...' ")


    ###1 delete this chunk -- I don't know where the correct data is
    ###1 token_usage = response["usage"]
    ###1 logging.info(f"Token usage: {token_usage}")
    ###1 print(f"Token usage: {token_usage}")
    ###1 cost = calculate_cost(
    ###1     (token_usage["inputTokens"], config["input_token_price"]),
    ###1     (token_usage["outputTokens"], config["output_token_price"])
    ###1 )
    ###1 print(f"Estimated cost in $: {cost}")

    return answer,keywords,references


def calculate_cost(*args: tuple[int, float]) -> float:
    """
        Calculate the total cost based on multiple unit counts and their respective prices.

    Args:
        *args: Variable number of (units, price) tuples.

    Returns:
        float: The total cost of all units.

    Examples:
        >>> calculate_cost((5, 10.0), (3, 15.0))
        95.0
        >>> calculate_cost((2, 3.5), (4, 2.75), (1, 5.0))
        23.0
    """
    total_cost = sum(units * (price / 1000) for units, price in args)
    return round(total_cost, 6)
