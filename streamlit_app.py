import streamlit as st
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth 
import xml.etree.ElementTree as et
import xmltodict

st.title("2030 District Constellation Uploader")
st.write(
    "go my minions!")
uploaded_file = st.file_uploader("Upload your download of properties you wish to address here", type="xlsx")
uploaded_file2 = st.file_uploader("Upload your constellation file here", type="xlsx")