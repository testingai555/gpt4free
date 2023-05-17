import requests
from uuid import uuid4
from browser_cookie3 import chrome

def get_session_auth_token():
    headers = {
        'authority': 'chat.openai.com',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://chat.openai.com/chat',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    response = requests.get('https://chat.openai.com/api/auth/session', headers=headers)
    return response.json()['accessToken']

session_token = get_session_auth_token()
headers = {
    'authority': 'chat.openai.com',
    'accept': 'text/event-stream',
    'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
    'authorization': 'Bearer ' + session_token,
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://chat.openai.com',
    'pragma': 'no-cache',
    'referer': 'https://chat.openai.com/chat',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

cookies = chrome(domain_name='chat.openai.com')
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie.name, cookie.value, domain=cookie.domain)

payload = {
    'action': 'next',
    'messages': [
        {
            'id': str(uuid4()),
            'role': 'system',
            'content': {
                'contentType': 'text',
                'content': 'hello world'
            }
        }
    ],
    'model': 'text-davinci-002',
    'timezoneOffset': -120
}

response = session.post('https://chat.openai.com/backend-api/conversation', headers=headers, json=payload)

print(response.text)
