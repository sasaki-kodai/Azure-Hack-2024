# flaskでapiを作成する
# http://sj-dirac:7778/
from flask import Flask, request, jsonify
import re
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from src.image import genereate_image
from src.chat import genereate_text

app = Flask(__name__)
configure_azure_monitor()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def extract_scene_prompt(message):
    return re.findall(r'scene_prompt_\d+\s*:\s*"(.*?)"', message)


@app.route("/chat", methods=["POST"])
def chat():
    logger.info("Received chat request")
    message = request.get_json("message", None)

    if message is None:
        logger.warning("No message received")
        return jsonify({"error": "Message is required"}), 400

    try:
        genereate_result = genereate_text(message)
    except Exception as e:
        logger.exception(f"Failed to generate text. {e}")
        return jsonify({"error": f"Failed to generate text."}), 400

    return jsonify(
        {
            "message": genereate_result,
            "image_generate_prompt": extract_scene_prompt(genereate_result),
        }
    ), 200


@app.route("/image", methods=["POST"])
def image():
    logger.info("Received image request")
    data = request.get_json()
    logger.info(f"Get request data: {data}")
    message = data.get("message", None)

    if "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    try:
        storage_uri = genereate_image(message)
    except Exception as e:
        logger.exception(f"Failed to generate image. {e}")
        return jsonify({"error": f"Failed to generate image."}), 400

    return jsonify({"message": storage_uri}), 200


if __name__ == "__main__":
    app.run(debug=True)
    # ローカル環境でpython ./src/app.pyを立ち上げて下記を投げると返ってくる
    # curl -X POST http://sj-dirac:7778/chat -H "Content-Type: application/json" -d '{"message": "こんにちは、元気ですか？"}'
