import requests
import time
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
VIDEO_ID = os.getenv('VIDEO_ID')

producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
headers = {
    "Connection": "close"  # Disable keep-alive
}

def get_live_chat_id(api_key, video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={video_id}&key={api_key}'
    response = requests.get(url, headers=headers).json()
    try:
        live_chat_id = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
        return live_chat_id
    except KeyError:
        print("No live chat found or video is not live.")
        return None

def fetch_live_chat_messages(api_key, live_chat_id, next_page_token=None):
    url = f'https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={live_chat_id}&part=snippet,authorDetails&key={api_key}'
    if next_page_token:
        url += f"&pageToken={next_page_token}"
    response = requests.get(url).json()
    messages = response.get('items', [])
    next_page_token = response.get('nextPageToken')
    return messages, next_page_token

def send_data(messages):
    for message in messages:
        author = message['authorDetails']['displayName']
        text = message['snippet']['displayMessage']
        profile_image = message['authorDetails']['profileImageUrl']
        timestamp = message['snippet']['publishedAt']
        data = {
            'author': author,
            'comment': text,
            'profile_image': profile_image,
        }
        try:
            producer.send("RAW_DATA", data)
            producer.flush()
        except Exception as e:
            print(f"An error occurred: {e}")
        print(f"{author}: {text}")

def monitor_live_chat(api_key, video_id, interval=5):
    live_chat_id = get_live_chat_id(api_key, video_id)
    if not live_chat_id:
        return
    
    next_page_token = None

    while True:
        messages, next_page_token = fetch_live_chat_messages(api_key, live_chat_id, next_page_token)
        send_data(messages)
        time.sleep(interval)

# Run the live chat monitor
monitor_live_chat(API_KEY, VIDEO_ID, interval=5)
