import sys
sys.path.append('./')
from app import app  # Flaskアプリをインポート
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_chat_route(client):
    test_chat = "advertiser_name : 株式会社トライト promotion_name : 保育士ワーカー promotion_details : 「転職成功者1万人」をテーマに専門職種の転職サイトを手掛ける会社の保育士専門の転職サイト、「全ての保育士さんが満足、安心して働ける理想の職場を」がモットー。 kpi : サイト来訪"
    # JSONペイロードを含むPOSTリクエストを送信
    response = client.post("/chat", json={"message": test_chat})
    assert response.status_code == 200
    # 正しいメッセージが含まれているか確認
    assert response.headers['Content-Type'] == 'application/json'