# -*- coding: UTF-8 -*-
from .collections import Stack
from .util import JSONStrUtil, KeyValue, TypeValue, CLASS_ARRAY, CLASS_OBJECT, CLASS_STRING, CLASS_BOOL, CLASS_NULL, PRIMARY_CLASS4JSON
from .errors import JSONEncoderError

class FullJSONEncoder(object):
    def __init__(self, obj):
        self.obj = obj

    def encode(self):
        if type(self.obj) != CLASS_ARRAY and type(self.obj) != CLASS_OBJECT:
            raise JSONEncoderError()
        return self.__do_encode(self.obj)
        
    def __do_encode(self, target):
        __type = type(target)
        if __type in PRIMARY_CLASS4JSON:
            if __type == CLASS_NULL:
                return 'null'
            elif __type == CLASS_BOOL:
                if target == True:
                    return 'true'
                else:
                    return 'false'
            elif __type == CLASS_STRING:
                return '"{}"'.format(target)
            else:
                return str(target)
        elif type(target) == CLASS_ARRAY:
            res = '['
            if len(target) < 2:
                for list_item in target:
                    res = res + self.__do_encode(list_item)
            else:
                for list_item in target:
                    res = res + self.__do_encode(list_item) + ','
                res = res[0:len(res)-1]
            res = res + ']'
            return res
        elif type(target) == CLASS_OBJECT:
            res = '{'
            if len(target) < 2:
                for k, v in target.items():
                    res = res + '"{}":{}'.format(k, self.__do_encode(v))
            else:
                for k, v in target.items():
                    res = res + '"{}":{},'.format(k, self.__do_encode(v))
                res = res[0:len(res)-1]
            res = res + '}'
            return res
        else:
            res = '{'
            # get class member
            members = vars(target)
            if len(members) < 2:
                for name, value in members.items():
                    res = res + '"{}":{}'.format(name, self.__do_encode(value))
            else:
                for name, value in members.items():
                    res = res + '"{}":{},'.format(name, self.__do_encode(value))
                res = res[0:len(res)-1]
            res = res + '}'
            return res