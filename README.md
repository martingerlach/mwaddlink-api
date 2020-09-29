# mwaddlink-api

## Quickstart

### Installation

``` sh
# Clone repo, then cd mwaddlink-api
python3 -m venv .
source bin/activate
pip install -r requirements.txt
python -m nltk.downloader punkt
```

### Running the application

``` sh
python app.py
```

You can then visit http://127.0.0.1:5000/api/v1/addlink?title=Leipzig in your browser. You can pass in titles from [Simple Wikipedia](https://simple.wikipedia.org) for testing.
