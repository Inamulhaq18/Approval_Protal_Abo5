import streamlit as st
import requests
import base64
import base64
from PIL import Image
from io import BytesIO


with open("best-skincare-products-1656081764.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
encoded_string=str(encoded_string).replace("b'","")


r = requests.post(url='https://hf.space/embed/eugenesiow/remove-bg/+/api/predict/', json={"data": ["data:image/jpeg;base64,"+encoded_string]})


st.write(r.json()["data"][0])
'''
f = open('C:\\Users\\pc\\Desktop\\base64.txt','r')
data = f.read()
im = Image.open(BytesIO(base64.b64decode(data)))
im.save('C:\\Users\\pc\\Desktop\\image.png', 'PNG')
'''
