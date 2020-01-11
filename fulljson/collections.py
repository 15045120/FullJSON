# -*- coding: UTF-8 -*-
class StackEmptyError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class Stack(object):
    def __init__(self):
        self.__values = []
        self.__index = -1
        self.top = None

    def push(self, value):
        self.__values.append(value)
        self.__index = self.__index + 1
        self.top = self.__values[-1]

    def pop(self):
        if self.__index == -1:
            raise StackEmptyError('Stack is empty')
        value = self.__values.pop()
        
        self.__index = self.__index - 1
        if self.__index == -1:
            self.top = None
        else:
            self.top = self.__values[self.__index]
        return value

    def is_empty(self):
        return self.__index == -1

    def pop_all(self, end=None):
        list = []
        while not self.is_empty() and self.top != end:
            value = self.pop()
            list.insert(0, value) 
        return list

    def print_stack(self):
        if self.__index == -1:
            print('<>')
        else:
            __values_str = str(self.__values)
            print('<{}>'.format(__values_str[1:len(__values_str)-1]))

class QueueEmptyError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class Queue(object):
    def __init__(self):
        self.__values = []

    def in_queue(self, value):
        self.__values.append(value)

    def out_queue(self):
        if len(self.__values) == 0:
            raise QueueEmptyError('Queue is empty')
        self.__values.pop(0)

    def is_empty(self):
        return len(self.__values) == 0

    def queue_head(self):
        if len(self.__values) == 0:
            raise QueueEmptyError('Queue is empty')
        return self.__values[0]

    def queue_tail(self):
        if len(self.__values) == 0:
            raise QueueEmptyError('Queue is empty')
        return self.__values[-1]

    def print_queue(self):
        if len(self.__values) == 0:
            print('<>')
        else:
            __values_str = str(self.__values)
            print('<{}>'.format(__values_str[1:len(__values_str)-1]))