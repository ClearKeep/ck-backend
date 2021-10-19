class DataUtils:
    @staticmethod
    def object_as_dict(obj):
        result = {}
        for key, value in obj.__dict__.items():
            if key == '_sa_instance_state':
                continue
            result[key] = value
        return result