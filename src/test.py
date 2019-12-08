from urllib.request import urlopen

import requests
import base64

API_ENDPOINT = "https://ij3hepb6ck.execute-api.sa-east-1.amazonaws.com/v1/save-html"
API_KEY = "CfF2caw5FG81BOqiGZcFLiyrnztt71Q3gPaTKCq4"

with open("../data/processo1.html", "rb") as html_file:
    encoded_html = base64.b64encode(html_file.read())

data = {'content': encoded_html.decode('utf-8')}

r = requests.post(url=API_ENDPOINT, json=data, headers={'x-api-key': API_KEY})

print(r.text)

# image_url = "https://st.depositphotos.com/1787196/1326/i/450/depositphotos_13269196-stock-photo-3d-alien.jpg"
# img_file = urlopen(image_url)
#
# print(img_file.read())
