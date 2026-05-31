import time

import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import dotenv
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
from supabase import create_client, Client

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



def allposts():
    response = supabase.table("posts").select("*").execute()
    posts = response.data
    return posts


def get_presigned_url(s3_url):
    file_key = s3_url.split('/')[-1]
    try:

        url = s3_client.generate_presigned_url('get_object',Params={'Bucket': os.getenv("S3_BUCKET"), 'Key': file_key},ExpiresIn=300)  # URL valid for 5 minutes

        return url
    except Exception as e:
        return e


def _parse_created_at(item):
    try:
        return datetime.fromisoformat(item.get("created_at", ""))
    except Exception:
        return datetime.min


def _format_posted_at(created_at):
    try:
        dt = datetime.fromisoformat(created_at)
        return dt.strftime("%A, %b %d %Y at %I:%M %p")
    except Exception:
        return created_at or "Unknown time"


allpostData = sorted(allposts(), key=_parse_created_at, reverse=True)
totalposts = len(allpostData)

for i in range(totalposts):
    with st.container(border=True):
        
        col1, col2 = st.columns([1, 1], gap="xxsmall", vertical_alignment="bottom")
        postTitle = allpostData[i]["title"]
        
        with col1:
            st.subheader(postTitle)
            st.caption(f"Posted at: {_format_posted_at(allpostData[i].get('created_at', ''))}")
        with col2:
            st.caption(f"By {allpostData[i]['username']}")
            
        # FIX: Removed the key parameter entirely
        with st.expander(label='Read full post'):
            
            if allpostData[i].get('image_url'):
                url = get_presigned_url(allpostData[i]['image_url'])
                st.image(url)
                
            st.write(allpostData[i]['content'])





