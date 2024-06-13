import json
import os
import openai

dalle_client = openai.AzureOpenAI(
    api_version="2024-02-01",
    api_key=os.environ["AZURE_DALLE_API_KEY"],
    azure_endpoint=os.environ["AZURE_DALLE_ENDPOINT"],
)


def generate_image(message):
    result = dalle_client.images.generate(model="dall-e-3", prompt=message, n=1)
    json_response = json.loads(result.model_dump_json())
    return json_response["data"][0]["url"]