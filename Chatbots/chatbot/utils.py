__all__ = ["format_assistant", "system_message", "download_json"]

import json

with open("chat-config/system-messages.json", "r") as f:
    system_messages = json.load(f)


def format_assistant(name):
    assistant_names = dict(
        zip(
            [x["assistant"] for x in system_messages],
            [x["display"] for x in system_messages],
        )
    )
    return assistant_names[name]


def system_message(assistants, name):
    default = "Du er en hjelpsom assistent som svarer på spørsmål så korrekt du kan"
    message = next(
        (x["content"] for x in assistants if x["assistant"] == name), default
    )
    return {"role": "system", "content": message}


# Convert chat history to JSON-data for download
def download_json(data):
    json_data = json.dumps(data, ensure_ascii=False)
    json_bytes = json_data.encode("utf-8")

    return json_bytes
