# -*- coding: UTF-8 -*-
from .collections import Stack
from .util import JSONStrUtil, KeyValue, TypeValue, CLASS_ARRAY,CLASS_OBJECT
from .errors import JSONDecoderError

class FullJSONDecoder(object):
    def __init__(self, value):
        self.value = value

    def decode(self):
        stack = Stack()
        class_stack = Stack()
        keyvalue_stack = Stack()
        
        for i,ch in enumerate(self.value):
            if ch == '{':
                stack.push(ch)
                class_stack.push(TypeValue(CLASS_OBJECT,{}))
                # push border object to stack
                keyvalue_stack.push(KeyValue('', '', border=True))
            elif ch == '[':
                stack.push(ch)
                class_stack.push(TypeValue(CLASS_ARRAY,[]))
            elif ch == ',':
                if class_stack.top.type == CLASS_ARRAY:
                    primary = ''.join(stack.pop_all(end='['))
                    primary = JSONStrUtil.valueOf(primary)
                    
                    class_stack.top.value.append(primary)
                elif class_stack.top.type == CLASS_OBJECT:
                    primary = ''.join(stack.pop_all(end='{'))
                    primary = JSONStrUtil.valueOf(primary)
                    
                    keyvalue_stack.top.value = primary
                else:
                    raise JSONDecoderError()
            elif ch == ']':
                if class_stack.is_empty():
                    raise JSONDecoderError()
                # is array
                if class_stack.top.type == CLASS_ARRAY:
                    primary = ''.join(stack.pop_all(end='['))
                    primary = JSONStrUtil.valueOf(primary)
                    
                    # add the primary value left
                    if primary != '':
                        class_stack.top.value.append(primary)
                    
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
                    raise JSONDecoderError()
            elif ch == '}':
                if class_stack.is_empty():
                    raise JSONDecoderError()
                # is object
                if class_stack.top.type == CLASS_OBJECT:
                    primary = ''.join(stack.pop_all(end='{'))
                    primary = JSONStrUtil.valueOf(primary)
                    
                    # add the primary value left
                    if primary != '':
                        class_stack.top.value = primary
                    
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
                    raise JSONDecoderError()
            elif ch == ':':
                primary = ''.join(stack.pop_all(end='{'))
                if JSONStrUtil.isStr(primary):
                    keyvalue_stack.push(KeyValue(JSONStrUtil.valueOf(primary), None))
                else:
                    raise JSONDecoderError()
            else:
                stack.push(ch)
        return class_stack.top.value