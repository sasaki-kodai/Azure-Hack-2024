import os
from openai import AzureOpenAI
import json

dalle_client = AzureOpenAI(
    api_version="2024-02-01",
    api_key=os.environ["AZURE_DALLE_API_KEY"],
    azure_endpoint=os.environ["AZURE_DALLE_ENDPOINT"],
)


def genereate_image(prompt: str) -> str:
    result = dalle_client.images.generate(model="dall-e-3", prompt=prompt, n=1)
    json_response = json.loads(result.model_dump_json())
    storage_uri = json_response["data"][0]["url"]

    return storage_uri
