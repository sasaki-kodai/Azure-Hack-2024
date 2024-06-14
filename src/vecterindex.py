import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
import re

def modify_query(query):
    pattern = "advertiser_name : |promotion_name : |promotion_details : |kpi : "
    modified_query = re.sub(pattern, '', query)
    return modified_query

def get_embedding(input):
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

def hybrid_search(query):
    """
    Azure AI SearchのIndexに検索クエリを渡し、HybridSearchの結果を取得する
    """
    search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    search_index_name = "fism-brand-rag-index-2"#os.environ["AZURE_SEARCH_INDEX_NAME"]
    search_api_key = os.environ["AZURE_SEARCH_API_KEY"]
    search_client = SearchClient(
        search_endpoint, 
        search_index_name, 
        AzureKeyCredential(search_api_key)
    )
    vector_query = VectorizedQuery(
        vector=get_embedding(query), 
        k_nearest_neighbors=1, 
        fields="contentVector"
    )

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=["content"],
        top=1,
    )

    return results

if __name__ == "__main__":
    q = 'advertiser_name : 株式会社 AIoTクラウド promotion_name : スリーゼロ promotion_details : アルコールチェック管理サービス、アルコールゼロ・検査漏れゼロ・飲酒事故ゼロを目指すクラウドサービス kpi : 認知度の向上'
    _q = modify_query(q)
    r = hybrid_search(_q)
    result = r.next()['content']
    print({"role": "system", "content": '下記は検索結果です。\nもし過去に同じpromotion_nameの企画があればそれを参考にして考えてください。\n検索結果 :\n'+result})
    #for i in r:
        #print(i['content'])
