import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NootTech.settings')

import django
django.setup()
from backendAPI.models import *
from django.core.files import File as F
from backendAPI.utils import get_id_gen

def populate():

    error_videos = [
        {"title": 'random video 1',
         "url": 'https://www.youtube.com/watch?v=hI8j0nkfNrM%27%7D',},
        {"title": 'random video 2',
         "url": 'https://www.youtube.com/watch?v=TpQvlxwsp3o%27%7D'},
        {"title": 'random video 3',
         "url": 'https://www.youtube.com/watch?v=28LdsO-_UcQ%27%7D'}

    ]

    users = [
        {"username": 'randomuser1',
         "email": 'randomuser1@noot.com',
         "colour": '#91829A',
         "password": 'Random1'},

        {"username": 'randomuser2',
         "email": 'randomuser2@noot.com',
         "colour": '#FFFFFF',
         "password": 'Random1'},

        {"username": 'randomuser3',
         "email": 'randomuser3@noot.com',
         "colour": '#FFF123',
         "password": 'Random1'},

        {"username": 'randomuser4',
         "email": 'randomuser4@noot.com',
         "colour": '#7F2FFF',
         "password": 'Random1'},
    ]

    def add_video(video):
        v = ErrorVideo.objects.get_or_create(url=video['url'], title=video['title'])[0]
        v.save()
        return v

    for vid in error_videos:
        add_video(vid)

    def add_user(user):
        u = User.objects.get_or_create(username=user["username"],
                                       colour=user["colour"], email=user["email"])[0]
        u.set_password(user["password"])
        u.save()
        return u


    for us in users:
        U = add_user(us)
        myfile = open('populate_files/test.jpg', encoding='utf8')
        myfile = F(myfile)
        f = File.objects.get_or_create(user=U, ip='127.1.4.2', file_content=myfile, file_thumbnail=myfile, generated_filename=get_id_gen())[0]
        print('New user created', 'Username:', us['username'])
        print('New file added', 'filename:', f.original_filename)
        f.save()

populate()