import requests
import base64
import base64
from PIL import Image
from io import BytesIO
import base64
import requests
import streamlit as st 


def removebgapi(links):
    st.write("inside removebgapi")
    st.write(links)
    st.write("-1")
    a=base64.b64encode(requests.get(links).content)
    st.write("-2")
    imgs=str(a).replace("b'","")
    st.write("-3")
    base64_str = imgs
    st.write("-4")
    buffer = BytesIO()
    st.write("-5")
    imgdata = base64.b64decode(base64_str)
    st.write("-6")
    img = Image.open(BytesIO(imgdata))
    st.write("-7")
    st.write(img.size)
    st.write("-8")
    img.thumbnail((350, 350))
    st.write("-9")
    st.write(img.size)
    st.image(img)
    st.write(type(img))
    img.save(buffer, format="PNG")
    st.write(img)
    st.write("-11")
    img_b64 = base64.b64encode(buffer.getvalue())
    st.write("-12")
    imgs=img_b64
    st.write("-13")
    imgs=str(imgs).replace("b'","")
    st.write("-14")
    imgdatacheck = base64.b64decode(img_b64)
    imcheck = Image.open(io.BytesIO(imgdatacheck))
    st.write(imcheck)
    payloaddata={"data": ["data:image/jpeg;base64,"+imgs,10,"alpha matting"]}
    st.write("-15")
    st.write(payloaddata)
    r = requests.post(url='https://hf.space/embed/KenjieDec/RemBG/+/api/predict', json=payloaddata)
    st.write("-16")
    st.write(r)
    opimg=str(r.json()["data"][0]).replace("data:image/png;base64,","")
    st.write("-17")
    st.write("opimg")
    st.write("-18")
    imot = Image.open(BytesIO(base64.b64decode(opimg)))
    st.write("-19")
    return(imot)
