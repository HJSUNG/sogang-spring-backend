import requests
import json
from flask import current_app

def chat_gpt_query(query_text):
    # OpenAI API 키
    api_key = current_app.config['CHAT_GPT_API_KEY']

    # API 엔드포인트
    url = 'https://api.openai.com/v1/chat/completions'

    # 요청 헤더
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # 요청 본문
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [

            {"role": "user", "content": query_text}
        ]
    }
    # {"role": "system", "content": "You are a helpful assistant."},

    # POST 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 응답 확인
    if response.status_code == 200:
        result = response.json()
        print("Response:", result['choices'][0]['message']['content'])
        return result['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code, response.text)
        return ''
