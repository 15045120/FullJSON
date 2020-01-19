# -*- coding: UTF-8 -*-
from .collections import Stack
from .util import JSONStrUtil, KeyValue, TypeValue, CLASS_ARRAY, CLASS_OBJECT, JSONIllegalChar, JSONEmptyChar
from .errors import JSONDecoderError

EMPTY_CHARS = [' ', '\t', '\r', '\n']
ENABLED_FRONT = ['[', ',', ':']

class FullJSONDecoder(object):
    def __init__(self, value):
        self.value = value

    def decode(self):
        stack = Stack()
        class_stack = Stack()
        keyvalue_stack = Stack()
        
        i = 0
        while i < len(self.value):
            ch = self.value[i]
            if ch == '"':
                stack.push(ch)
                end = i+1
                while end < len(self.value) and self.value[end] != '"':
                    ch = self.value[end]
                    stack.push(ch)
                    end = end + 1
                if end == len(self.value):
                    error_msg = 'Expecting " delimiter: column {}'.format(end)
                    raise JSONDecoderError(error_msg)
                else:
                    stack.push('"')
                    i = end
            elif ch == '{':
                # remove character in [' ', '\t', '\r', '\n']
                while not stack.is_empty()  and stack.top in EMPTY_CHARS:
                    stack.pop()
                # normal status
                stack.push(ch)
                class_stack.push(TypeValue(CLASS_OBJECT,{}))
                # push border object to stack
                keyvalue_stack.push(KeyValue('', '', border=True))
            elif ch == '[':
                # remove character in [' ', '\n', '\t']
                while not stack.is_empty() and stack.top in EMPTY_CHARS:
                    stack.pop()
                # normal status
                stack.push(ch)
                class_stack.push(TypeValue(CLASS_ARRAY,[]))
            elif ch == ',':
                # remove character in [' ', '\n', '\t']
                while not stack.is_empty() and stack.top in EMPTY_CHARS:
                    stack.pop()
                if class_stack.top.type == CLASS_ARRAY:
                    primary_str = ''.join(stack.pop_all(end='['))
                    primary = JSONStrUtil.valueOf(primary_str)
                    
                    # add the primary value left
                    if type(primary) == JSONEmptyChar:
                        if len(class_stack.top.value) == 0:
                            error_msg = 'Missing element after "," delimiter: column {}'.format(i)
                            raise JSONDecoderError(error_msg)
                        else:
                            pass
                    elif type(primary) != JSONIllegalChar:
                        class_stack.top.value.append(primary)
                    else:
                        error_msg = 'Illeagal json character sequence {}: column {}'.format(primary_str, i)
                        raise JSONDecoderError()
                        
                elif class_stack.top.type == CLASS_OBJECT:
                    primary_str = ''.join(stack.pop_all(end='{'))
                    primary = JSONStrUtil.valueOf(primary_str)
                    
                    # add the primary value left
                    if type(primary) == JSONEmptyChar:
                        if keyvalue_stack.size() <= 1:
                            error_msg = 'Missing element after "," delimiter: column {}'.format(i)
                            raise JSONDecoderError(error_msg)
                        else:
                            pass
                    elif type(primary) != JSONIllegalChar:
                        keyvalue_stack.top.value = primary
                    else:
                        error_msg = 'Illeagal json character sequence {}: column {}'.format(primary_str, i)
                        raise JSONDecoderError(error_msg)
                else:
                    error_msg = 'Missing "[" or "{" before "," delimiter: column {}'.format(i)
                    raise JSONDecoderError()
            elif ch == ']':
                if class_stack.is_empty():
                    error_msg = 'Missing "[" delimiter: column {}'.format(i)
                    raise JSONDecoderError(error_msg)
                # is array
                if class_stack.top.type == CLASS_ARRAY:
                    primary_str = ''.join(stack.pop_all(end='['))
                    primary = JSONStrUtil.valueOf(primary_str)
                    
                    # add the primary value left
                    if type(primary) == JSONEmptyChar:
                        # not found last element in array
                        pass
                    elif type(primary) != JSONIllegalChar:
                        class_stack.top.value.append(primary)
                    else:
                        error_msg = 'Illeagal json character sequence {}: column {}'.format(primary_str, i)
                        raise JSONDecoderError(error_msg)
                    
                    top_value = class_stack.pop()
                    if class_stack.is_empty():
                        class_stack.push(top_value)
                    elif not class_stack.is_empty() and class_stack.top.type == CLASS_ARRAY:
                        class_stack.top.value.append(top_value.value)
                    elif not class_stack.is_empty() and class_stack.top.type == CLASS_OBJECT:
                        keyvalue_stack.top.value = top_value.value
                        
                    # remove '['
                    stack.pop()
                else:
                    error_msg = 'Missing "[" delimiter: column {}'.format(i)
                    raise JSONDecoderError(error_msg)
            elif ch == '}':
                if class_stack.is_empty():
                    error_msg = 'Missing "{" delimiter: column {}'.format(i)
                    raise JSONDecoderError(error_msg)
                # is object
                if class_stack.top.type == CLASS_OBJECT:
                    primary_str = ''.join(stack.pop_all(end='{'))
                    primary = JSONStrUtil.valueOf(primary_str)
                    # add the primary value left
                    if type(primary) == JSONEmptyChar:
                        pass
                    elif type(primary) != JSONIllegalChar:
                        keyvalue_stack.top.value = primary
                    else:
                        error_msg = 'Illeagal json character sequence {}: column {}'.format(primary_str, i)
                        raise JSONDecoderError(error_msg)
                        
                    while not keyvalue_stack.is_empty() and not keyvalue_stack.top.isBorder():
                        kv = keyvalue_stack.pop()
                        class_stack.top.value[kv.key] =  kv.value
                        
                    # remove border
                    keyvalue_stack.pop()
                    
                    top_value = class_stack.pop()
                    if class_stack.is_empty():
                        class_stack.push(top_value)
                    elif not class_stack.is_empty() and class_stack.top.type == CLASS_ARRAY:
                        class_stack.top.value.append(top_value.value)
                    elif not class_stack.is_empty() and class_stack.top.type == CLASS_OBJECT:
                        keyvalue_stack.top.value = top_value.value
                    
                    # remove '{'
                    stack.pop()
                else:
                    error_msg = 'Missing "{" delimiter: column {}'.format(i)
                    raise JSONDecoderError(error_msg)
            elif ch == ':':
                primary = ''.join(stack.pop_all(end='{'))
                if JSONStrUtil.isStr(primary):
                    keyvalue_stack.push(KeyValue(JSONStrUtil.valueOf(primary), None))
                else:
                    error_msg = 'Illeagal json character sequence {}: column {}'.format(primary, i)
                    raise JSONDecoderError(error_msg)
            else:
                stack.push(ch)
            i = i + 1
        # is array or object
        if type(class_stack.top) == TypeValue:
            return class_stack.top.value
        # is primary json type
        else:
            primary_str = ''.join(stack.pop_all())
            primary = JSONStrUtil.valueOf(primary_str)
            if type(primary) != JSONIllegalChar:
                class_stack.push(primary)
            else:
                error_msg = 'Illeagal json character sequence {}: in {}'.format(primary_str, primary_str)
                raise JSONDecoderError(error_msg)
            return class_stack.top