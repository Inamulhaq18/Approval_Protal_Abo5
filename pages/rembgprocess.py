import streamlit as st
import requests
import base64

with open("best-skincare-products-1656081764.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
st.write((encoded_string.replace("b'","")))


r = requests.post(url='https://hf.space/embed/eugenesiow/remove-bg/+/api/predict/', json={"data": ["data:image/jpeg;base64,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"]})
r.json()

