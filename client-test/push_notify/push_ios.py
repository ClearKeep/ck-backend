import asyncio

from kalyke.client import VoIPClient, APNsClient
from kalyke.payload import PayloadAlert, Payload
# from kalyke.client import APNsClient
# from kalyke.payload import PayloadAlert, Payload




# def ios_data_notification():
#     alert = {'title': 'title',
#              'body': 'message'
#              }
#     # token = registration_tokens
#     token = '16D6F8F928B7A1315DCB65E78AA1666CA6AF83EB37ACC5A3F9F4332517CC7552'
#     try:
#         res = client1.send(token,
#                                alert,
#                                expiration=int(time.time() + 604800),
#                                error_timeout=5,
#                                batch_size=200)
#
#         print(res.tokens)
#         print(res.errors)
#         print(res.token_errors)
#     except Exception as e:
#         print(e)
#
#     client1.close()


# def ios_data_notification_test():
#     alert = 'request_call'
#     # token = registration_tokens
#     token = '16D6F8F928B7A1315DCB65E78AA1666CA6AF83EB37ACC5A3F9F4332517CC7552'
#     f = open("/configs/apns/Certificates_voip.pem", "r")
#     pemfile = f.read()
#     try:
#         beams_client = PushNotifications(
#             instance_id=token,
#             secret_key=pemfile,
#         )
#
#         response = beams_client.publish_to_interests(interests=['hello'],
#                                                      publish_body={
#                                                          'apns': {
#                                                              'aps': {
#                                                                  'alert': {
#                                                                      'title': 'title',
#                                                                      'body': 'message'
#                                                                  },
#                                                              },
#                                                          },
#                                                      },
#                                                      )
#         print(response['publishId'])
#
#     except Exception as e:
#         print(e)


# def test1():
#     # sslcontext.load_cert_chain(cert, keyfile=ca_cert)
#     cli = apnsclient(mode=apnsclient.MODE_DEV, client_cert='/home/global/Ductn/ck-backend/src/services/Certificates_voip.pem')
#     alert = IOSPayloadAlert(body='body!', title='title!')
#     payload = IOSPayload(alert=alert)
#     notification = IOSNotification(payload=payload, priority=IOSNotification.PRIORITY_LOW)
#     token = '16D6F8F928B7A1315DCB65E78AA1666CA6AF83EB37ACC5A3F9F4332517CC7552'
#     try:
#         cli.push(notification=notification, device_token=token)
#     except APNSException as e:
#         if e.is_device_error:
#             if isinstance(e, UnregisteredException):
#                 # device is unregistered, compare timestamp (e.timestamp_datetime) and remove from db
#                 pass
#             else:
#                 # flag the device as potentially invalid
#                 pass
#         elif e.is_apns_error:
#             # try again later
#             pass
#         elif e.is_programming_error:
#             # check your code
#             # try again later
#             pass
#     else:
#         # everything is ok
#         pass

def voip():

    client = VoIPClient(
    auth_key_filepath="/configs/apns/Certificates_voip.pem",
    bundle_id= "com.telred.clearkeep3.ios.dev",
    use_sandbox=True
    )
    alert = {
        "key": "value"
    }

    # Send single VoIP notification

    registration_id = "16D6F8F928B7A1315DCB65E78AA1666CA6AF83EB37ACC5A3F9F4332517CC7552"

    result = client.send_message(registration_id, alert)
    print(result)
    # Send multiple VoIP notifications

    # registration_ids = [
    #     "16D6F8F928B7A1315DCB65E78AA1666CA6AF83EB37ACC5A3F9F4332517CC7552",
    # ]

    # try:
    #     registration_ids = [
    #         "16D6F8F928B7A1315DCB65E78AA1666CA6AF83EB37ACC5A3F9F4332517CC7552",
    #     ]
    #
    #     results = client.send_bulk_message(registration_ids, alert)
    #
    #     print(results)
    # except Exception as e:
    #     print(e)


def text():
    try:
        client_chat = APNsClient(
            team_id="H4C7478UQW",
            auth_key_id="LRKZJ6859V",
            auth_key_filepath='/home/global/Ductn/ck-backend/configs/apns/Certificates_apns.p8',
            bundle_id="com.telred.clearkeep3.ios.dev",
            use_sandbox=True,
            force_proto="h2",
            apns_push_type="alert"
        )
        payload_alert = PayloadAlert(title="Ductn", body="A New Message")
        alert = Payload(alert=payload_alert, badge=1, sound="default",custom={
        "group_id": 1,
        "from_client_id": '123',
        "client_id": '234',
        "message": "1234"
    })

        registration_id = "4cb6e7eee9e141003345d56e9e9d2ef7b162d6f884a718ee4ada6ef06ac0565c"

        result = client_chat.send_message(registration_id, alert)
        print(result)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    # ios_data_notification()
    # ios_data_notification_test()

    text()