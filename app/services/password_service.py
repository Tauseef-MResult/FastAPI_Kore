import bcrypt
import secrets
import string

def generate_password(length=10):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def encrypt_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def decrypt_password(hashed_password: str, password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)