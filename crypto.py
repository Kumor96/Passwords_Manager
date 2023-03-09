from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from os import environ, getenv
from dotenv import load_dotenv
load_dotenv()

SALT = getenv('SALT')

class Crypto:
    def __init__(self, text):
        self.text = text.encode('utf8')
    
    def create_key(self, password):
        salt = SALT.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf8')))
        return key

class Encrypt(Crypto):
    def execute(self, password):
        fernet = Fernet(self.create_key(password))
        encrypt_content = fernet.encrypt(self.text)
        return encrypt_content.decode('utf8')

class Decrypt(Crypto):
    def execute(self, password):
        fernet = Fernet(self.create_key(password))
        decrypt_content = fernet.decrypt(self.text)
        return decrypt_content.decode('utf8')

