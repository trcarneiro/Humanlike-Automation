import asyncio
import requests

# The send_prompt function, modified to remove the async for testing purposes.
def send_prompt(ip: str, port: int, endpoint: str, prompt: str, temperature: float = 0.7, max_tokens: int = 150) -> str:
    LLAMA_API_URL = f"http://{ip}:{port}{endpoint}"
    LLAMA_API_KEY = "lm-studio"
    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "model-identifier",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    response = requests.post(LLAMA_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json().get("choices")[0].get("text")

def test_questions(ip: str, port: int):
    endpoint = "/v1/completions"
    questions = [
        "What is your level of proficiency in English?",
        "How many years of work experience do you have with Linux?",
        "How many years of work experience do you have with continuous integration (CI)?",
        "How many years of work experience do you have with Bash?",
        "Can you understand C/C++ code enough to be able to help with merges and compilation issues?",
        "How many years of work experience do you have with Python scripting?",
        "How many years of work experience do you have with DevOps knowledge?",
    ]

    for question in questions:
        print(f"Question: {question}")
        response = send_prompt(ip, port, endpoint, question)
        print(f"Response: {response}\n")

if __name__ == "__main__":
    ip = "localhost"  # Replace with your API server IP
    port = 5555            # Replace with your API server port
    test_questions(ip, port)
