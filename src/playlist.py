import os
from googleapiclient.discovery import build
import isodate
from datetime import timedelta

class PlayList:
    def __init__(self, playlist_id):

        self.__youtube = self.get_service()
        self.__playlist_id = playlist_id
        self.playlist_videos = self.__youtube.playlistItems().list(
            playlistId=self.__playlist_id, part="contentDetails,snippet", maxResults=50,).execute()
        self.channel_id = self.playlist_videos['items'][0]['snippet']['channelId']
        self.title = self.get_title(self.channel_id, self.__playlist_id, self.__youtube)
        self.__url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'
        self.__video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.__video_response = self.__youtube.videos().list(
            part='contentDetails,statistics',id=','.join(self.__video_ids)).execute()

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def show_best_video(self):

        likes = 0
        video_url = str()
        for video in self.__video_response['items']:
            if int(video['statistics']['likeCount']) > likes:
                video_url = video['id']
                likes = int(video['statistics']['likeCount'])
        return f'https://youtu.be/{video_url}'

    @staticmethod
    def get_title(channel_id, playlist_id, youtube):
        playlists = youtube.playlists().list(
            channelId=channel_id, part='contentDetails,snippet', maxResults=50,).execute()
        for playlist in playlists['items']:
            if playlist['id'] == playlist_id:
                title = playlist['snippet']['title']
                return title

    @property
    def url(self):
        return self.__url

    @property
    def total_duration(self):

        duration_list = []
        for video in self.__video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)
        return timedelta(seconds=sum(td.total_seconds() for td in duration_list))
