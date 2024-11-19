import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

# Use a securely stored key
SECRET_KEY = os.getenv("MY_KEY")
cipher = Fernet(SECRET_KEY)

def encrypt_content(content: str) -> str:
    return cipher.encrypt(content.encode())

def decrypt_content(content: str) -> str:
    return cipher.decrypt(content).decode()