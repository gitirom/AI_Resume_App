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

connection = pymysql.connect(  
                                host='localhost',
                                user='root',
                                password='db_password',
                                database='nlp_resume_app'
                            )

cursor = connection.cursor()