# Passwords_Manager

A password manager is an app that stores your passwords, so you don't need to remember them. Once you've logged into the password manager using a 'master' password, it will remember your passwords for all your online accounts

## Packages Used


* sqlalchemy
* cryptography
* python-dotenv


## Run application

```bash
$ git clone https://github.com/Kumor96/Passwords_Manager.git
$ cd Passwords_Manager
$ pip install -r requirements.txt
```
* Create file .env
* into a .env file add this:
SALT = 'Your salt to encryption'
```bash
$ python main.py
```

<p><img src="Screenshots/add_credential.png"/></p>
<img src="Screenshots/load_credential.png"/>
<img src="Screenshots/password.png"/>
