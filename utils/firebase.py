import firebase_admin
from firebase_admin import credentials

def init_firebase_app():
    cred = credentials.Certificate("configs/ck-3-test-firebase-adminsdk-gszn7-fc1b46d732.json")
    default_app = firebase_admin.initialize_app(cred)