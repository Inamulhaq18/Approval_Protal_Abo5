import streamlit as st
import requests
import base64
import base64
from PIL import Image
from io import BytesIO
import base64
import requests

def resizeimage(img):
    fixed_height = 1000
    height_percent = (fixed_height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    image = img.resize((width_size, fixed_height), Image.NEAREST)
    return(image)


links=st.text_input("Link")




a=base64.b64encode(requests.get(links).content)
st.write("Converstion to B64 done!")
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
r = requests.post(url='https://hf.space/embed/eugenesiow/remove-bg/+/api/predict/', json={"data": ["data:image/jpeg;base64,"+imgs]})
st.write(r.json())
opimg=str(r.json()["data"][0]).replace("data:image/png;base64,","")
im = Image.open(BytesIO(base64.b64decode(opimg)))
st.image(im)



'''def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

def rembgapi(urls):
    imgs=get_as_base64(urls)
    imgs=str(imgs).replace("b'","")
    st.write(imgs)
    

    
    st.image(im)
    '''
    
