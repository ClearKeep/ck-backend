class SignalKey:
    def __init__(self, client_id, registration_id, device_id, identity_key_public, prekey_id, prekey, signed_prekey_id, signed_prekey, signed_prekey_signature):
        self.client_id = client_id
        self.registration_id = registration_id
        self.device_id = device_id
        self.identity_key_public = identity_key_public
        self.prekey_id = prekey_id
        self.prekey = prekey
        self.signed_prekey_id = signed_prekey_id
        self.signed_prekey = signed_prekey
        self.signed_prekey_signature = signed_prekey_signature
