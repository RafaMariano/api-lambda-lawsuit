import requests

API_ENDPOINT = "https://ij3hepb6ck.execute-api.sa-east-1.amazonaws.com/v2/save-html"
API_KEY = "API-KEY-HERE"

with open("../data/processo1.html", "rb") as html_file:
    encoded_html = html_file.read()

r = requests.post(url=API_ENDPOINT, data=encoded_html, headers={'x-api-key': API_KEY,
                                                                'Content-Type': 'text/html'})

print(r.text)
