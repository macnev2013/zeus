import uuid


class GitProfile(dict):
    def __init__(self, profile_name, username, password):
        self['profile_id'] = str(uuid.uuid4())[0:8]
        self['profile_name'] = profile_name
        self['username'] = username
        self['password'] = password
