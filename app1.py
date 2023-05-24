import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# Load API key from secrets.toml
api_key = st.secrets["api_key"]

# Set your API key
openai.api_key = api_key

def generate_response(user_input):
    user_role = "User: " + user_input
    system_role = "System: Make a picture that feels like Disney. You should make it into a Disney cartoon style. Make a sentence around 80 characters."

    prompt = f"{user_role}\n{system_role}\nSystem:"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def generate_image(prompt):
    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
        json={'model': 'image-alpha-001', 'prompt': prompt, 'num_images': 1, 'size': '512x512'}
    )
    return response.json()['data'][0]['url']

def display_response(response):
    if response:
        st.markdown(response)

# 타이틀
st.title("GPT plus DALL-E (feat. Disney)")

# 텍스트 필드
st.markdown("#### prompt")
prompt_input = st.text_input("")

if len(prompt_input) > 2:
    # 서브밋 버튼
    if st.button("시작"):
        with st.spinner("GPT가 열심히 일하고 있어요!"):
            response = generate_response(prompt_input)
            display_response(response)
            
            with st.spinner("DALL-E가 이미지를 생성하고 있어요!"):
                image_url = generate_image(response)
                image_response = requests.get(image_url)
                img = Image.open(BytesIO(image_response.content))
                st.image(img, caption='DALLE-generated image', use_column_width=True)
else:
    if st.button("시작"):
        st.markdown("3글자 이상 써 주세요!")
