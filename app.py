# flaskでapiを作成する
# http://sj-dirac:7778/
from flask import Flask, request, jsonify
from openai import AzureOpenAI
import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01"
)

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler())

@app.route('/chat', methods=['POST'])
def chat():
    logger.info("Received request")
    data = request.get_json()

    logger.info(f"Received {data}")

    if 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    user_message = data['message']
    response = client.chat.completions.create(model="gpt-4",
                                        messages=[
                                            {"role": "system", "content": "あなたは優秀な広告クリエイターです。"},
                                            {"role": "user", "content": user_message}],
                                        max_tokens=150)
    chat_response = response.choices[0].message.content

    return chat_response


@app.route('/test', methods=['GET'])
def test():
    logger.info("Received request")

    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
    # ローカル環境でpython ./src/app.pyを立ち上げて下記を投げると返ってくる
    # curl -X POST http://sj-dirac:7778/chat -H "Content-Type: application/json" -d '{"message": "こんにちは、元気ですか？"}'