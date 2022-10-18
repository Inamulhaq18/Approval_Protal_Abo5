import streamlit as st
import requests
import base64
import base64
from PIL import Image
from io import BytesIO
import base64
import requests

links=st.text_input("Link")


a=base64.b64encode(requests.get(links).content)
st.write("Converstion to B64 done!")
imgs=str(a).replace("b'","")
r = requests.post(url='https://hf.space/embed/eugenesiow/remove-bg/+/api/predict/', json={"data": ["data:image/jpeg;base64,"+imgs]})
st.write(r.json())
opimg=str(r.json()["data"][0]).replace("data:image/png;base64,","")
st.img(opimg)

'''def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

def rembgapi(urls):
    imgs=get_as_base64(urls)
    imgs=str(imgs).replace("b'","")
    st.write(imgs)
    

    im = Image.open(BytesIO(base64.b64decode(opimg)))
    st.image(im)
    '''
    
