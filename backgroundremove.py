import requests
import base64
import base64
from PIL import Image
from io import BytesIO
import base64
import requests
import streamlit as st 


def removebgapi(links):
    a=base64.b64encode(requests.get(links).content)
    imgs=str(a).replace("b'","")
    base64_str = imgs
    buffer = BytesIO()
    imgdata = base64.b64decode(base64_str)
    img = Image.open(BytesIO(imgdata))
    st.write(img.size)
    img.thumbnail((500, 500))
    st.write(img.size)
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue())
    imgs=img_b64
    imgs=str(imgs).replace("b'","")
    payloaddata={"data": ["data:image/jpeg;base64,"+imgs,10,"alpha matting"]}

    r = requests.post(url='https://hf.space/embed/KenjieDec/RemBG/+/api/predict', json=payloaddata)
    opimg=str(r.json()["data"][0]).replace("data:image/png;base64,","")
    imot = Image.open(BytesIO(base64.b64decode(opimg)))
    return(imot)
