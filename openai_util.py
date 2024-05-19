from openai import OpenAI
from config_secrets import OPENAI
import base64
import requests

# Function to encode the image
def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def image_diff(file_img_1, file_img_2):
    api_key = OPENAI['api_token']

    # Getting the base64 string
    base64_image_a = encode_image(file_img_1)
    base64_image_b = encode_image(file_img_2)

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
    }

    payload = {
    'model': 'gpt-4o',
    'messages': [
        {
        'role': 'user',
        'content': [
            {
            'type': 'text',
            'text': 'What item is missing in the second image? Only tell me the name of the item. Do not include any other information.'
            },
            {
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/jpeg;base64,{base64_image_a}'
            }
            },
            {
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/jpeg;base64,{base64_image_b}'
            }
            }
        ]
        }
    ],
    'max_tokens': 300
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)

    response_payload_dict = response.json();
    return response_payload_dict;



