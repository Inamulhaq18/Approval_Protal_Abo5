import streamlit as st
import requests
import base64
import base64
from PIL import Image
from io import BytesIO
import base64
import requests


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

def rembgapi(urls):
    imgs=get_as_base64(urls)
    imgs=str(imgs).replace("b'","")
    r = requests.post(url='https://hf.space/embed/eugenesiow/remove-bg/+/api/predict/', json={"data": ["data:image/jpeg;base64,"+imgs]})
    st.write(r.json())
    opimg=str(r.json()["data"][0]).replace("data:image/png;base64,","")
    im = Image.open(BytesIO(base64.b64decode(opimg)))
    st.image(im)
    
    
links=st.text_input("Link")
encoded_string=rembgapi(links)
