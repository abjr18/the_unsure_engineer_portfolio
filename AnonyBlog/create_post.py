import time
import runpy
from pathlib import Path

import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import dotenv
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
from supabase import create_client, Client
import random

load_dotenv()
def get_creds():
    # 1. Declare variables as global INSIDE the function
    global ACCESS_KEY, SECRET_KEY, BUCKET_NAME, REGION, url, key, supabase

    # 2. Assign the values
    ACCESS_KEY = st.secrets["AWS_KEY"]
    SECRET_KEY = st.secrets["AWS_SECRET"]
    BUCKET_NAME = 'the-unscripted-analtical'
    REGION = 'us-east-1'
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

# 3. Call the function first to populate the global variables
get_creds()

# 4. Now the variables exist and can be safely used here
s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)


def upload_image_to_s3(file_data, file_name):
    try:
        # Uploading the file
        s3_client.upload_fileobj(
            file_data,
            BUCKET_NAME,
            file_name,
            ExtraArgs={'ContentType': file_data.type}  # Ensures it opens in browser
        )

        # Construct the URL
        url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file_name}"
        return url
    except NoCredentialsError:
        return None


def generate_funny_username():
    # Lists of funny words to mix and match
    adjectives = ["Vanzotya", "Zapatlela", "Boka", "Nalla", "Yetrapindi", "Caffeinated", "LactoseFree", "Majestic"]
    nouns = ["Burrito", "bakri", "Toaster", "Gladiator", "Sausage", "Potato", "Ke dil me", "dev", "dada"]

    # Randomly pick one from each list
    adj = random.choice(adjectives)
    noun = random.choice(nouns)

    # Add a random number for uniqueness
    number = random.randint(10, 99)

    return f"{adj}{noun}{number}"


if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
st.title("Abhi's Anonymous Blog Space 📝 ")
if st.button("View posts"):
    runpy.run_path(str(Path(__file__).resolve().parent / "view_posts.py"), run_name="__main__")
    st.stop()
with st.expander(label='Add image for your post?', width=250):

    uploaded_file = st.file_uploader("Drag file below, or click upload to choose a file from your device", type=["jpg", "jpeg", "png"], key=st.session_state.uploader_key)
    if uploaded_file:
        st.image(uploaded_file, caption="Preview")
# Using a form helps group the inputs and only triggers a rerun
# once the user clicks the "Post" button.
with st.form("blog_post_form", clear_on_submit=True):
    st.subheader("Write a new post")

    title = st.text_input("Blog Title")
    content = st.text_area("What's on your mind?", height=200)

    submit_button = st.form_submit_button("Post Anonymously")

if submit_button:
    if title and content:
        imgurl = None
        if uploaded_file:
            extension = os.path.splitext(uploaded_file.name)[1]
            filename = title + "_" + str(uuid.uuid4()) + "_"+extension
            imgurl = upload_image_to_s3(uploaded_file, file_name=filename)

        blog = {
            "title":title,
            "content":content,
            "image_url":imgurl,
            "created_at":datetime.now().isoformat(),
            "username":generate_funny_username()
        }

        try:
            response = supabase.table('posts').insert(blog).execute()
            st.success(f"Post '{title}' has been created!")
        except Exception as e:
            st.error(f"error saving post {e}")
    else:
        st.error("Please provide both a title and content.")
    st.session_state.uploader_key += 1
    st.rerun()



