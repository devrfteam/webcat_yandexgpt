import aiohttp
import json
from bs4 import BeautifulSoup
from config import YANDEX_API_URL, YANDEX_API_HEADERS, instr

async def fetch_content(url, cookies=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    session_timeout = aiohttp.ClientTimeout(sock_connect=5)
    async with aiohttp.ClientSession(headers=headers, cookies=cookies, timeout=session_timeout) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            return html

async def extract_text(html, max_length=2000):
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.stripped_strings
    content = ' '.join(texts)
    return content[:max_length]

async def classify_text(text):
    prompt = {
        "modelUri": "gpt://ID/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": f"{instr}"
            },
            {
                "role": "user",
                "text": text
            },
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(YANDEX_API_URL, headers=YANDEX_API_HEADERS, json=prompt) as response:
            if response.status == 200:
                response_text = await response.text()
                result = json.loads(response_text)
                return result
            else:
                error_message = f"Error: Received status code {response.status}"
                return {"error": error_message}
