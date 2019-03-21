from django.test import TestCase
from django.core.files.base import ContentFile
from .utils import get_id_gen, get_upload_key
from .models import *
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
import os
    
class APITestCase(TestCase):

    def setUp(self):
        u = User.objects.create(username="testx", email="testx@noot.tech")
        u.set_password("testPassword123")
        u.save()

        u = User.objects.create(username="testy", email="testy@noot.tech")
        u.set_password("testPassword123")
        u.save()
        
        filepath = os.getcwd()+'/populate_files/hello.txt'
        mf = open(filepath, 'rb')
        f = ContentFile(mf.read())
        f.size = os.path.getsize(filepath)
        f.name = "test_public.txt"

        File.objects.create(user=u, file_content=f, generated_filename=get_id_gen(),)
        
        ErrorVideo.objects.create(title="YEE", url="https://www.youtube.com/watch?v=q6EoRBvdVPQ")


    def test_user_unauthenticated_cant_get_settings(self):
        """
        Check if an unauthenticated user gets 401 when trying to view settings api
        """
        response = self.client.get(reverse('GetSetSettings'))
        self.assertEqual(response.status_code, 401)
    
    def test_authenticated_user_view_settings(self):
        """
        Check if an authenicated user can view their settings
        """
        self.client.login(username="testx", password="testPassword123")
        response = self.client.get(reverse('GetSetSettings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "colour")
    
    def test_user_can_create_account(self):
        """
        Check if a user can create an account
        """
        response = self.client.get(reverse('CreateUser'))
        # OK: 200
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('CreateUser'), {
            'username': 'testerino', 
            'password': 'TestPassword123', 
            'email': 'test@noot.tech', 
            'colour': '#00CCCC'}
        )
        # Account created: code 201
        self.assertEqual(response.status_code, 201)
    
    def test_user_can_view_error_videos(self):
        """
        Check if an unauthenticated user can view the error videos list
        """
        response = self.client.get(reverse('ErrorVideos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "YEE")
        self.assertContains(response, "youtube")
    
    def test_auth_user_can_favourite_file(self):
        """
        Check if an auth user can favourite a file and then view their favourites
        """
        self.client.login(username="testx", password="testPassword123")
        # File with ID 1 is test_public.txt
        response = self.client.post(reverse('AddFavourite', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200) # created
        # Check if user now has 1 favourite
        response = self.client.get(reverse('ListFavourites'))
        self.assertContains(response, "test_public.txt")
    
    def test_auth_user_can_view_files(self):
        """
        Test if authenticated user can view their own files
        testy has 1 file
        """
        self.client.login(username="testy", password="testPassword123")
        response = self.client.get(reverse('ListFiles'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "generated_filename")
    
    def test_user_can_report_file(self):
        """
        Test if anonymous user can add a report
        """
        response = self.client.get(reverse('ReportAdd'))

        # No get requests allowed, only POST.
        self.assertEqual(response.status_code, 405)

        response = self.client.post(reverse('ReportAdd'), {
            'reason_title': 'Copyright Infringement', 
            'reason_body': 'This file belongs to me!!s', 
            'reported_by': 1, 
            'reported_file': 1
            }
        )
        
        # Account created: code 201
        self.assertEqual(response.status_code, 201)
    
    def test_upload_file_responds_accordingly(self):
        """
        Test if the upload API responds with a bad request if the user doesnt provide correct credentials
        """
        # Try upload a file with missing POST Parameters to get response message

        response = self.client.post(reverse('Upload'), {
            'username': 'testx', 
            'upload_key': 'wrong_key'
            }
        )
        
        # If missing credentials or wrong credentials, Upload should respond with Bad Request (400)
        self.assertEqual(response.status_code, 400)

class UserFileTestCase(TestCase):

    def setUp(self):
        # Give user john 0 warnings (default)
        u = User.objects.create(username="johnsmith", email="johnsmith@noot.tech", colour="#00FF00", upload_key=get_upload_key())
        u.set_password("MyP@$$w0rd!")
        u.save()

        # Give user jane 3 warnings
        u = User.objects.create(username="janedoe", email="jonedoe@noot.tech", colour="#FFFF00", upload_key=get_upload_key(), warnings=3)
        u.set_password("MyP@$$w0rd!")
        u.save()

        # Have user jane upload 2 files, 1 public, 1 private.
        filepath = os.getcwd()+'/populate_files/hello.txt'
        mf = open(filepath, 'rb')
        f = ContentFile(mf.read())
        f.size = os.path.getsize(filepath)
        f.name = "test_public.txt"
        
        File.objects.create(
            user=u, 
            file_content=f,
            generated_filename=get_id_gen(),
            is_private=False
        )

        f.name = "test_private.txt"

        File.objects.create(
            user=u, 
            file_content=f,
            generated_filename=get_id_gen(),
            is_private=True
        )

        filepath = os.getcwd()+'/populate_files/ER.png'
        mf = open(filepath, 'rb')
        f = ContentFile(mf.read())
        f.size = os.path.getsize(filepath)
        f.name = "ER.png"
        File.objects.create(
            user=u, 
            file_content=f,
            file_thumbnail=f,
            generated_filename=get_id_gen(),
        )
    
    def test_warnings_are_correct(self):
        """
        Test if default warning is 0
        """
        john = User.objects.get(username="johnsmith")
        jane = User.objects.get(username="janedoe")
        self.assertEqual(john.warnings, 0)
        self.assertEqual(jane.warnings, 3)
    
    def test_file_is_private(self):
        """
        test if default privacy status for files is False
        """
        # Checks if a file is private or public. id=1 is Private, id=2 is Public.
        private = File.objects.get(id=1)
        public = File.objects.get(id=2)
        self.assertEqual(private.is_private, False)
        self.assertEqual(public.is_private, True)
    
    def test_file_mime_type(self):
        """
        Check if file mimetype is generated on file upload
        """
        # Checks if a text file has correct mimetype
        jane = User.objects.get(username="janedoe")
        f = File.objects.get(id=1)
        self.assertEqual(f.file_mime_type, 'text/plain')
    
    def test_textfile_textinfo_generated(self):
        """
        Check if textinfo is generated for text-files and not image files
        """
        f = File.objects.get(id=1) #text
        i = File.objects.get(id=3) #image
        self.assertNotEqual(f.file_text, None)
        self.assertEqual(f.file_text, None)
    
    def test_textfile_has_no_imageinfo(self):
        """
        Check that a text file has no image_info attribute
        """
        f = File.objects.get(id=1)
        self.assertEqual(f.file_image, None)

    def test_imagefile_imageinfo_generated(self):
        """
        Check that an image file has image_info auto-generated
        """
        f = File.objects.get(id=3)
        self.assertNotEqual(f.file_image, None)
    
    def test_imagefile_imageinfo_deleted_if_imagefile_deleted(self):

        f = File.objects.get(id=3)
        imgid = f.file_image.id
        f.delete()

        with self.assertRaises(Http404):
            get_object_or_404(Image, id=imgid)
    
    def test_files_favs_deleted_if_user_deleted(self):
        
        u = User.objects.get(username="janedoe")
        u.delete()

        with self.assertRaises(Http404):
            get_list_or_404(File, user=u)
        
        with self.assertRaises(Http404):
            get_list_or_404(FavouritedFile, user=u)
