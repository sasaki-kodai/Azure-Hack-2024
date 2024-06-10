import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

def create_vectorindex(input):
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
    )

    response = client.embeddings.create(
        input=input,
        model="text-embedding-ada-002"
    ).data[0].embedding

    return response
