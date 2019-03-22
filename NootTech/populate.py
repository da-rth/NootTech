import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NootTech.settings')

import django
django.setup()
from backendAPI.models import *
from django.core.files.base import ContentFile
from backendAPI.utils import get_id_gen, get_upload_key

def populate():

    # Add error videos to database

    error_videos = [
        {
            "title": 'YEE',
            "url": 'https://www.youtube.com/watch?v=q6EoRBvdVPQ'
        },
        {
            "title": 'HEYYEYAAEYAAAEYAEYAA',
            "url": 'https://www.youtube.com/watch?v=ZZ5LpwO-An4'
        },
        {
            "title": 'Arf.mp4',
            "url": 'https://www.youtube.com/watch?v=4o5baMYWdtQ'
        }

    ]


    # Create 4 mock users with different information

    users = [
        {"username": 'anonymous',
         "email":    'admin@noot.tech',
         "colour":   '#00CCCC',
         "password": 'gC)uvR&7?<'},

        {"username": 'carrotman',
         "email": 'randomuser1@noot.tech',
         "colour": '#91829A',
         "password": 'Random1'},

        {"username": 'pizzaman',
         "email": 'randomuser2@noot.tech',
         "colour": '#FF00FF',
         "password": 'Random1'},

        {"username": 'bigmacman',
         "email": 'randomuser3@noot.tech',
         "colour": '#FFF1230',
         "password": 'Random1'},

        {"username": 'hotdogman',
         "email": 'randomuser4@noot.tech',
         "colour": '#7F2FFF',
         "password": 'Random1'},
    ]

    # Add a video to the dastabase given a dict of video info
    def add_video(video):
        v = ErrorVideo.objects.get_or_create(url=video['url'], title=video['title'])[0]
        if v:
            v.save()
        print('- New error video added to database: '+video['title'])

    # Add a user to the database given a dict of user info

    def add_user(user):
        u = User.objects.get_or_create(username=user["username"], colour=user["colour"], email=user["email"], upload_key=get_upload_key())[0]
        u.set_password(user["password"])
        u.save()
        print('- New user created/updated:', user['username'])
        return u

    # Upload a file to user's account given the user object and the file path

    def upload_file(user, filepath, private=False):
        try:
            myfile = open(filepath, 'rb')

            f = ContentFile(myfile.read())
            f.name = filepath.split("/")[1]
            f.size = os.path.getsize(filepath)

            ext = filepath.split(".")[-1]

            supported_thumbnail = ext.lower() in ["gif", "png", "jpg", "webm", "mp4", "jpeg"]

            f = File.objects.get_or_create(
                user=user,
                ip='127.0.0.1',
                file_content=f,
                file_thumbnail=f if supported_thumbnail else None,
                generated_filename=get_id_gen(),
                is_private=private
            )[0]

            f.save()
            if private:
                print('\t* New PRIVATE file uploaded by '+user.username+':', f.original_filename)
            else:
                print('\t* New file uploaded by '+user.username+':', f.original_filename)
        except Exception:
            print("\t* Could not upload file: "+filepath)

    for vid in error_videos:
        try:
            add_video(vid)
        except django.db.utils.IntegrityError:
            print("- Error video "+vid["title"]+" already exists.")

    for user in users:
        try:
            new_user = add_user(user)

            for entry in os.scandir('populate_files'):

                if entry.is_file():
                    # If file is hello.txt, upload it as a private file
                    if "hello.txt" in entry.path:
                        upload_file(new_user, entry.path, private=True)
                    else:
                        upload_file(new_user, entry.path)

        except django.db.utils.IntegrityError:
            print("- User "+user["username"]+" already exists.")


populate()
