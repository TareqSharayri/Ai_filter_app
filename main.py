#user add a text to conversion

#image conversion model
#show the image
#install libary in terminal
#import libary with pyip web

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64


st.set_page_config(page_title="AI Image Generator")
st.title(" AI Image with Text")
st.write("AI image with text created by Tareq Sharayri ")
prompt = st.text_input("Write the image description here:")
token = st.secrets["token"]

headers = {"Authorization": f"Bearer {token}"}
api_model= "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_image(prompt_text):
    payload = {"inputs": prompt_text, "options": {"wait_for_model": True}}
    response = requests.post(api_model, headers=headers, json=payload)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None


if st.button("Create image"):
    if not prompt.strip():
        st.warning("Please enter a description first!")
    else:
        with st.spinner("Generating your masterpiece... "):
            image = generate_image(prompt)
            if image:
                st.image(image, caption=f"Generated: {prompt}", use_container_width=True)

                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(label="Download Image", data=byte_im, file_name="ai_image.png", mime="image/png")