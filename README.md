# FullJSON

The package is for [JSON](https://www.json.org/json-en.html) conversion, based on Python enviroment.

Basic thought is using stack structure and recursive method.

## Installation
```bash
pip install fulljson 
```

## Examples

 - Convert a JSON string into a JSON object.

```python
from fulljson import JSON

value = '["foo", {"bar": ["baz", null, 1.0, 2, true]}]'
print(JSON.parse(value))
```

 - Convert JSON values to JSON strings.
```python
from fulljson import JSON

value = ["foo", {"bar": ["baz", None, 1.0, 2, True]}]
print(JSON.stringify(value))
```


