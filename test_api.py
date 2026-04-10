import httpx
import json

def test_chat_completion(streaming=False):
    url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "gemma-4-E2B-it",
        "messages": [
            {"role": "user", "content": "Merhaba, nasılsın?"}
        ],
        "stream": streaming
    }

    print(f"\n--- Testing {'Streaming' if streaming else 'Non-streaming'} ---")
    
    with httpx.Client() as client:
        if streaming:
            with client.stream("POST", url, headers=headers, json=payload, timeout=60.0) as response:
                for line in response.iter_lines():
                    if line:
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                print("\n[Stream Finished]")
                                break
                            try:
                                data = json.loads(data_str)
                                choices = data.get('choices', [])
                                if choices:
                                    content = choices[0].get('delta', {}).get('content', '')
                                    print(content, end="", flush=True)
                            except json.JSONDecodeError:
                                pass
        else:
            response = client.post(url, headers=headers, json=payload, timeout=60.0)
            if response.status_code == 200:
                data = response.json()
                print("AI Response:", data['choices'][0]['message']['content'])
            else:
                print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_chat_completion(streaming=False)
    test_chat_completion(streaming=True)
