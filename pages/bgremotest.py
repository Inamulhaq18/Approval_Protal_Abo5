import requests
import base64
import base64
from PIL import Image
from io import BytesIO
import base64
import requests
import streamlit as st 

def resizeimage(img):
    fixed_height = 1000
    height_percent = (fixed_height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    image = img.resize((width_size, fixed_height), Image.NEAREST)
    return(image)

def removebgapi(links):
    a=base64.b64encode(requests.get(links).content)
    imgs=str(a).replace("b'","")
    base64_str = imgs
    buffer = BytesIO()
    imgdata = base64.b64decode(base64_str)
    img = Image.open(BytesIO(imgdata))
    new_img = resizeimage(img)
    new_img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue())
    imgs=img_b64
    imgs=str(imgs).replace("b'","")
    payloaddata={"data": ["data:image/jpeg;base64,"+imgs,10,"alpha matting"]}
    #https://hf.space/embed/eugenesiow/remove-bg/+/api/predict/

    r = requests.post(url='https://hf.space/embed/KenjieDec/RemBG/+/api/predict', json=payloaddata)
    st.write(r.json()["data"][0].replace("data:image/png;base64,",""))
    opimg=str(r.json()["data"][0]).replace("data:image/png;base64,","")
    
    im = Image.open(BytesIO(base64.b64decode(opimg)))
    return(im)
  
link=st.text_input("enter link")
removebgapi(link)
