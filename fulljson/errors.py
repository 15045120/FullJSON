# -*- coding: UTF-8 -*-
class JSONError(Exception):
    pass

class JSONEncoderError(JSONError):
    def __init__(self, message='cannot stringify JSON object'):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return repr(self.message)

class JSONDecoderError(JSONError):
    def __init__(self, message='cannot parse JSON string'):
        self.message = message

    def __str__(self):
        return repr(self.message)

    def __repr__(self):
        return repr(self.message)