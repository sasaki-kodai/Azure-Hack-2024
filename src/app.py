# flaskでapiを作成する
# http://sj-dirac:7778/
import logging
import re
from azure.monitor.opentelemetry import configure_azure_monitor
from flask import Flask, request, jsonify

from chat import generate_word_storyboard
from cosmos import write_generate_history
from image import generate_image

app = Flask(__name__)
configure_azure_monitor()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def extract_scene_prompt(message):
    return re.findall(r'scene_prompt_\d+\s*:\s*"(.*?)"', message)


@app.route("/chat", methods=["POST"])
def chat():
    logger.info("Received chat request")

    data = request.get_json()
    logger.info(f"Get request data: {data}")
    message = data.get("message", None)

    if message is None:
        logger.warning("No message received")
        return jsonify({"error": "Message is required"}), 400

    try:
        generate_result = generate_word_storyboard(message=message)
    except Exception as e:
        logger.exception(f"Failed to generate word storyboard. {e}")
        return jsonify({"error": f"Failed to generate word storyboard."}), 400

    logger.info(f"Response: {generate_result}")

    try:
        write_generate_history(message, generate_result)
    except Exception as e:
        logger.exception(f"Failed to write generation history. {e}")

    return (
        jsonify(
            {
                "message": generate_result,
                "image_generate_prompt": extract_scene_prompt(generate_result),
            }
        ),
        200,
    )


@app.route("/image", methods=["POST"])
def image():
    logger.info("Received image request")

    data = request.get_json()
    logger.info(f"Get request data: {data}")
    message = data.get("message", None)

    if message is None:
        logger.warning("No message received")
        return jsonify({"error": "Message is required"}), 400

    try:
        # urlが返却される
        generate_result = generate_image(message=message)
    except Exception as e:
        logger.exception(f"Failed to generate image. {e}")
        return jsonify({"error": f"Failed to generate image."}), 400

    logger.info(generate_result)

    return (
        jsonify(
            {
                "message": generate_result,
            }
        ),
        200,
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7778)
    # app.run()
    # ローカル環境でpython ./src/app.pyを立ち上げて下記を投げると返ってくる
    # curl -X POST http://sj-dirac:7778/chat -H "Content-Type: application/json" -d '{"message": "advertiser_name : 株式会社トライト promotion_name : 保育士ワーカー promotion_details : 「転職成功者1万人」をテーマに専門職種の転職サイトを手掛ける会社の保育士専門の転職サイト、「全ての保育士さんが満足、安心して働ける理想の職場を」がモットー。 kpi : サイト来訪"}'
    # curl -X POST http://sj-dirac:7778/chat -H "Content-Type: application/json" -d '{"message": "advertiser_name : Microsoft Corporation promotion_name : Azure promotion_details : クラウドコンピューティングプラットフォームおよびサービス、生成AIをOfficeとの連携することで業務効率化を目指している。 kpi : 認知度の向上"}'
    # curl -X POST http://sj-dirac:7778/image -H "Content-Type: application/json" -d '{"message": "Young woman entering bathroom in the morning, looking sleepy"}'