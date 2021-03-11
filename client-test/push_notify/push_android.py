from firebase_admin import credentials, messaging
import firebase_admin

cred = credentials.Certificate("/home/global/Ductn/ck-backend/configs/ck-3-test-firebase-adminsdk-gszn7-fc1b46d732.json")
default_app = firebase_admin.initialize_app(cred)

registration_tokens =["fhIqfm_HRbm_thXMpVD2Bu:APA91bHNAnAvm44nfUjUE4P1TNGrtnt3ykFikpo1yjXV_lhoSAffa0LuMB2fQNIiwB8hFb41q_PNp3vHTEgCm8lwf055F4LZXssibeZeXMtteBNVK144JTDgFt3zrC_zEeotrDkfbDQB"]
payload = messaging.Notification(title="ductn", body="A new message")

message = messaging.MulticastMessage(
    tokens=registration_tokens,
    notification=payload,
    data={
        "group_id": "1",
        "from_client_id": '123',
        "client_id": '234',
        "message": "1234"
    }

)
response = messaging.send_multicast(message)
print(response)