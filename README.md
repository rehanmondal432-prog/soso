# soso

Simple HTTP requests helper for Python.

A lightweight, zero-dependency alternative for basic HTTP requests using only the Python standard library.

## Install

```bash
pip install git+https://github.com/rehanmondal432-prog/soso.git
```

## Usage

```python
from soso import get, post

# GET request
r = get("https://httpbin.org/get", params={"foo": "bar"})
print(r.status_code)
print(r.json())

# POST with JSON
r = post("https://httpbin.org/post", json_data={"hello": "world"})
print(r.text)

# POST with form data
r = post("https://httpbin.org/post", data={"key": "value"})
print(r.ok)
```

## API

- `get(url, **kwargs)` – send a GET request
- `post(url, **kwargs)` – send a POST request
- `request(method, url, **kwargs)` – send any method

Keyword arguments:
- `params` – query string dict
- `data` – form body (dict) or raw body
- `json_data` – JSON body
- `headers` – extra headers
- `timeout` – seconds (default 30)

Returns a `Response` object with:
- `.status_code`
- `.ok`
- `.headers`
- `.content` / `.text`
- `.json()`
- `.url`
