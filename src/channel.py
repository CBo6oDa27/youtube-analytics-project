import os
from googleapiclient.discovery import build
import json


class Channel:

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        youtube = self.get_service()
        channel = youtube.channels().list(
            id=self.channel_id, part='snippet,statistics').execute()
        channel_info = channel['items'][0]
        channel_snippet = channel_info['snippet']
        self.id = channel_info['id']
        self.title = channel_snippet['title']
        self.description = channel_snippet['description']
        self.url = 'https://www.youtube.com/channel/' + self.id
        self.subscriberCount = channel_info['statistics']['subscriberCount']
        self.video_count = channel_info['statistics']['videoCount']
        self.view_count = channel_info['statistics']['viewCount']
        self.channel = channel

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        return int(self.subscribers) - int(other.subscribers)

    def __gt__(self, other):
        return int(self.subscribers) > int(other.subscribers)

    def __ge__(self, other):
        return int(self.subscribers) >= int(other.subscribers)

    def __lt__(self, other):
        return int(self.subscribers) < int(other.subscribers)

    def __le__(self, other):
        return int(self.subscribers) <= int(other.subscribers)

    def __eq__(self, other):
        return int(self.subscribers) == int(other.subscribers)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(
            id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.channel, file)
