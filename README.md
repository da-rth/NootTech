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
$ (venv) python manage.py makemigrations 
$ (venv) python manage.py migrate
$ (venv) python manage.py createsuperuser
$ (venv) python manage.py runserver

# Start VueJS dev server or build it
$ (venv) cd frontend
$ (venv) npm install
$ (venv) npm run dev (or npm run build)

Visit localhost:8000 
???????
Profit
```

