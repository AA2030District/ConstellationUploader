import streamlit as st
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth 
import xml.etree.ElementTree as et
import xmltodict

st.title("2030 District Constellation Uploader")
st.write(
    "go my minions!"
     uploaded_file = st.file_uploader("Upload an excel file of constellation here", type="xls")
     
)
