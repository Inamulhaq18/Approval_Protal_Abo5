import requests
import base64
import base64
from PIL import Image
from io import BytesIO
import base64
import requests
import streamlit as st 
from rembg import remove



def removebgapi(links):
    st.write(links)
    responses = requests.get(links)
    img = Image.open(BytesIO(responses.content))
    st.write(links)
    st.write("-1")
    img.thumbnail((500, 500))
    st.write("-9")
    st.write(img.size)
    st.write("-10")
    st.write(type(img))
    st.write("-11")
    st.write(type(img))
    imot=remove(img)
    st.write("done:D")
    st.write("-19")
    return(imot)
intttt=st.text_input('Movie title', 'Life of Brian')
removebgapi(intttt)
