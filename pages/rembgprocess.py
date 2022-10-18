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
opimg=str(r.json()["data"][0]).replace("data:image/png;base64,","")

im = Image.open(BytesIO(base64.b64decode(opimg)))
st.image(im)

