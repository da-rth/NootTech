os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NootTech.settings')

import django
django.setup()
from backendAPI.models import *

def populate():

    error_videos = [
        {"title": 'random video 1',
         "url": 'https://www.youtube.com/watch?v=hI8j0nkfNrM%27%7D,
        {"title": 'random video 2',
         "url": 'https://www.youtube.com/watch?v=TpQvlxwsp3o%27%7D,
        {"title": 'random video 3',
         "url": 'https://www.youtube.com/watch?v=28LdsO-_UcQ%27%7D,

    ]

    def add_video(video):
        v = ErrorVideo.objects.get_or_create(url=video['url'], title=video['title'])
        v.save()
        return v

    for video in error_videos:
        add_video(video)