# WAD2 Group Project

### Team Members:

- [Daniel Arthur - 2086380a](mailto:2086380a@student.gla.ac.uk)
- [Lorenzo Roccato - 2265986r](mailto:2265986r@student.gla.ac.uk)
- [Jonathan Sumner - 2268242s](mailto:2268242s@student.gla.ac.uk)
- [Enrico Maria Trombetta - 2396702t](mailto:2396702t@student.gla.ac.uk)

### WAD2 Tutor:

- [Francesco Perrone](http://mailto:f.perrone.1@research.gla.ac.uk)



## Important:

Do **not** push directly to the master branch! You may cause conflicts with someone elses work, or even break the project. 

What should you do instead?

```sh
$ git checkout -b [name_of_your_new_branch]
$ git commit -m "Your message"
$ git push origin [name_of_your_branch]
```

This will create a new branch of the project (with your changes) which we can then merge with the master branch via GitHub after your code has been double-checked by another team member for any conflicts!

'''Check Working Branch 
    git rev-parse --abbrev-ref HEAD
'''

## Setup:

```sh
# Setup repo and virtual environment
$ git clone https://github.com/denBot/WAD2-Group-Project.git
$ cd WAD2-Group-project
$ virtualenv -p python3 venv

# Activate virtual environment
$ source venv/bin/activate
$ .\venv\Scripts\activate.bat

# Configure and run django server
$ (venv) cd NootTech

# create a settings.json in ~/WAD2-Group-Project/NootTech/NootTech
$ (venv) cd NootTech
$ (venv) cp settings-example.json settings.json
$ (venv) vim settings.json # or any editor you like

# create a config.json in ~/WAD2-Group-Project/NootTech/frontend/src
$ (venv) cd .. # go back to ~/WAD2-Group-Project/NootTech/
$ (venv) cd frontend/src
$ (venv) cp config_example.json config.json
$ (venv) vim config.json # or any editor you like

# change settings.json
$ (venv) cd ../../
$ (venv) cp NootTech/settings{-example,}.json
$ (venv) vim NootTech/settings.json

# start django
$ (venv) python manage.py makemigrations 
$ (venv) python manage.py migrate
# (venv) python populate.py # populate the database with error videos and mock-users
$ (venv) python manage.py createsuperuser
$ (venv) python manage.py collectstatic
$ (venv) python manage.py runserver

# By now the back-end will be running. If the front-end JS has been pre-built and you can see the website, you can stop here.
# If you get a blank page, you will need to build the front-end JavaScript:

# Start VueJS dev server or build it
$ (venv) cd frontend
$ (venv) npm install
$ (venv) npm run build
$ (venv) cd ..
$ (venv) python manage.py collectstatic

Visit localhost:8000 
???????
Profit
```

## Django Dependencies
* Django Dependancies
* Django 1.11.18
* Django Rest Framework
* Django REST Framework - simplejwt
* Django Cors Headers
* Django Model Admin Reorder
* Django Webpack Loader
* Easy Thumbnails
* Easy Thumbnails FFMPEG
* hurry.filesize
* MailChecker
* MoviePy
* Pillow
* virustotal-api

## Vue Dependencies
* VueJS
* Vue FontAwesome
* Axios
* Bootstrap Vue
* highlight.js
* jwt-decode
* Video.js
* VueJS
* vue-color
* vue-github-api
* vue-notification
* vue-paginate
* vue-router
* vue-video-player
* vuex
* vue-password-strength-meter
* wavesurfer.js

