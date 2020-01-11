from .decoder import FullJSONDecoder
from .encoder import FullJSONEncoder

'''
https://www.json.org/json-en.html

JSON (JavaScript Object Notation) is a lightweight data-interchange format. 
It is easy for humans to read and write. It is easy for machines to parse and generate. 
It is based on a subset of the JavaScript Programming Language Standard ECMA-262 3rd Edition - December 1999.

JSON is built on two structures:
    A collection of name/value pairs. In various languages, this is realized as an object, record, 
    struct, dictionary, hash table, keyed list, or associative array.
    
    An ordered list of values. In most languages, this is realized as an array, vector, list, or sequence.

In JSON, they take on these forms:
    object
    array
    string
    number
    true
    false
    null
'''


__all__=['JSON']

class JSON(object):
    @staticmethod
    def parse(str):
        decoder = FullJSONDecoder(str)
        return decoder.decode()

    @staticmethod
    def stringify(obj):
        encoder = FullJSONEncoder(obj)
        return encoder.encode()