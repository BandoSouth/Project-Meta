import requests
import json
from string import Template

# 서버 정보
url = "http://127.0.0.1:1234/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}

request_template = Template("$user_input")


# 요청 데이터 생성 함수
def create_request_data(user_input):
    # 사용자가 입력한 값을 템플릿에 삽입
    user_message = request_template.substitute(user_input=user_input)

    data = {
        "model": "MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf:2",
        "messages": [
            {
                "role": "system",
                "content": "Answer user requests."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "answer_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "answer": {
                            "type": "string"
                        }
                    },
                    "required": ["answer"]
                }
            }
        },
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": True
    }

    return data


# API 요청 함수
def request_dial(user_input):
    data = create_request_data(user_input)
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=300)

    # 응답 확인 및 출력
    if response.status_code == 200:
        response_json = response.json()

        # message.content를 추출하고 JSON 파싱
        message_content = response_json["choices"][0]["message"]["content"]
        content_json = json.loads(message_content)  # content를 다시 JSON으로 파싱

        joke = content_json.get("joke", "No joke found")

        print("생성된 응답:", joke)

    else:
        print(f"오류 발생: {response.status_code}, {response.text}")


# 메인 함수
def main():
    print("원하는 명령을 입력하십시오.")
    user_input = input()

    request_dial(user_input)

main()

