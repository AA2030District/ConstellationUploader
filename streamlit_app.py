import streamlit as st
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth 
import xml.etree.ElementTree as et
import xmltodict

st.title("2030 District Constellation Uploader")
st.write(
    "go my minions!")
espmfile   = st.file_uploader("Upload your download of properties you wish to address here", type="xlsx")
inputfile = st.file_uploader("Upload your constellation file here", type="xlsx")

def espmidmatcher():
    esdf = pd.read_excel(espmfile,'Meters')
    esdf = esdf.iloc[4:]
    new_header = esdf.iloc[0] #grab the first row for the header
    esdf = esdf[1:] #take the data less the header row
    esdf.columns = new_header #set the header row as the df header
    espmdict={}
    counter=5
    newdictionary={}
    failedlist=[]
    #CUSTOM ID SHOULD BE FIRST OEN!
    counter=4   
    for property in esdf.iloc:
        espmdict.update({property['Custom Meter ID 1 Value']:[property['Portfolio Manager ID'],property['Portfolio Manager Meter ID']]})
        counter+=1
    st.write(espmdict)
    return espmdict



if st.button("Run Program"):
    espmidmatcher()

