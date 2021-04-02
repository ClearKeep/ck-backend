class JanusService(object):
    def __init__(self, janus_url, token, stransaction):
        self.token = token
        self.transaction = stransaction
        self.janus_url = janus_url
        self.janus_sesion = None
        self.janus_plugin = None
        self.janus_plugin_url = None
        self.janus_create_room_url = None
        self.janus_room = None

    def set_janus_plugin_url(self, janus_sesion):
        self.janus_plugin_url = self.janus_url + "/" + str(janus_sesion)

    def set_janus_create_room_url(self, janus_plugin):
        self.janus_create_room_url = self.janus_url + "/" + str(self.janus_sesion) + "/" + str(janus_plugin)

    def get_janus_data(self, group_id):
        return {
            "janus": 'create',
            "id": group_id,
            "token": self.token,
            "transaction": self.transaction
        }

    def get_janus_data_plugin(self):
        return {
            "janus": 'attach',
            "plugin": "janus.plugin.videoroom",
            "token": self.token,
            "transaction": self.transaction
        }

    def get_janus_create_room(self, group_id):
        return {
            "janus": 'message',
            "body": {
                "request": "create",
                "room": group_id,
                "publishers": 6
            },
            "token": self.token,
            "transaction": self.transaction
        }

    def check_janus_create_room(self, group_id):
        return {
            "janus": 'message',
            "body": {
                "request": "create",
                "room": group_id,
                "publishers": 6
            },
            "token": self.token,
            "transaction": self.transaction
        }
