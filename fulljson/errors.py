# -*- coding: UTF-8 -*-
class Error(Exception):
    pass

class JSONEncoderError(Error):
    def __init__(self, message='cannot stringify JSON object'):
        self.message = message
    def __str__(self):
        return repr(self.message)

class JSONDecoderError(Error):
    def __init__(self, message='cannot parse JSON string'):
        self.message = message
    def __str__(self):
        return repr(self.message)