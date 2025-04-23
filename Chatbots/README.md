# README

## Set up

In order for the streamlit app to run as expexted, you need to set configuration options and secrets in the hidden directory `.streamlit`.

It it does not exist already, create the `.streamlit` directory and create the files `config.toml` and `secrets.toml` inside this directory. The contents of the `config.toml` file should be as follows:

```
[logger]

level = "info"

[client]

toolbarMode = "viewer"

[browser]

gatherUsageStats = false
```

The contents of the `secrets.toml` file should be as follows (insert your API-keys where applicable):

```
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_APIKEY=""
AZURE_PHI_ENDPOINT=""
AZURE_PHI_APIKEY=""
ES_ENDPOINT=""
ES_INDEX=""
ES_KEY=""
AWS_BEDROCK_ACCESS_KEY_ID=""
AWS_BEDROCK_SECRET_ACCESS_KEY=""
```

## Run the app

Run the app by executing the following command in your terminal window:

```shell
streamlit run app.py
```
