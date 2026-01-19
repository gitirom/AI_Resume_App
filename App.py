import streamlit as st
import pandas as pd
import base64,random
import time,datetime
#libraries to parse the resume pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import pafy #for uploading youtube videos
import plotly.express as px #to create visualisations at the admin session
import nltk
from dotenv import load_dotenv
import os

nltk.download('stopwords')   #download stopwords for filltering out from resume content

# --- CONNECT TO DB ---
load_dotenv()  
db_password = os.getenv('DB_PASSWORD')

try:
    connection = pymysql.connect(  
        host='localhost',
        user='root',
        password= db_password,
        database='nlp_resume_app'
    )

    cursor = connection.cursor()
    #streamlit notification for successful connection
    st.success("Database connection successful!")
except Exception as e:
    st.error(f"Database connection failed: {e}")

def insert_user(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
    try:
        DB_table_name = 'user_data'
        insert_sql = "insert into " + DB_table_name + """ values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        rec_values = (name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses)
        cursor.execute(insert_sql, rec_values)
        connection.commit()
        st.success("User data inserted successfully!")
    except Exception as e:
        st.error(f"Failed to insert user data: {e}")

# --- STREAMLIT WEB PAGE CONFIG ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="./Logo/logo2.png",
)

def run():
    img = Image.open("./Logo/logo2.png")
    st.image(img,width=150)
    st.title("AI Resume Analyzer and Job Recommender System")
    st.sidebar.markdown("# Choose User Type")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

    