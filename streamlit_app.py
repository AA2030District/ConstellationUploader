import streamlit as st
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth 
import xml.etree.ElementTree as et
import xmltodict
from PIL import Image

st.set_page_config(
     page_title='2030 District Constellation Uploader',
     layout="wide",)

image = Image.open("logo.jpg")
st.logo(image,size="large")
st.title("2030 District Constellation Uploader")
upload,errors,console=st.columns([.4,.3,.3])
upload.subheader("Upload your files here.")
errors.subheader("Errors:")
console.subheader("Console Messages:")
espmfile   = upload.file_uploader("Upload your download of properties you wish to address here", type="xlsx")
inputfile = upload.file_uploader("Upload your constellation file here", type="xlsx")
user = upload.text_input("Energy Star Username",type="password")
password = upload.text_input("Energy Star Password",type="password")

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
    return espmdict

def customidfinder(espmdict):       
    condf = pd.read_excel(inputfile)
    meteriddict={}
    meterlist={}
    faillist=[]
    #iterates through the constellation file and creates a dictionary of all the unique constellation meter ID's removing duplicates
    for conid in condf['MeterNumber']:
        meteriddict[conid]=()
    for item in meteriddict.keys():
        try:
            meterlist.update({item:espmdict[str(item)]})
            console.write(item)
        except KeyError:
            faillist.append(item)
        except Exception as error:
            errors.write("An Error Occured:",type(error).__name__)
            exit()
    totaldf=pd.DataFrame
    dflist=[]
    counter=0
    for entry in meterlist: 
        newdf = condf.loc[condf['MeterNumber']==entry]
        id=str(meterlist[entry][1])
        id2=str(meterlist[entry][0])
        response=requests.get('https://portfoliomanager.energystar.gov/ws/meter/'+id+'/consumptionData',auth=HTTPBasicAuth(user,password))
        dict_data = xmltodict.parse(response.content)
        try:
            for item in dict_data['meterData']['meterConsumption']:
                df_dict=pd.DataFrame([item])
                dflist.append(df_dict)
            totaldf=pd.concat(dflist)
        except KeyError:
             print("meternotfound")
             print(id)
        if totaldf.empty == False:
            for number in totaldf['startDate']:
                newdf = newdf.drop(newdf[newdf['CycleStartDate'] == number].index)
        headers = {'Content-Type': 'application/xml'}
        for index,row in newdf.iterrows():
            if pd.isna(row['TotalCharges']) == True:
                row['TotalCharges'] =0
            xml = """<?xml version="1.0" encoding="UTF-8"?>
            <meterData>
            <meterConsumption>
                <usage>{usage}</usage>
                <startDate>{date1}</startDate>
                <endDate>{date2}</endDate>
                <cost>{price}</cost>
            </meterConsumption></meterData>"""
            xml = xml.format(usage=str(row['FeeVolume']),date1=str(row['CycleStartDate']).rsplit(' ',1)[0],date2=str(row['CycleEndDate']).rsplit(' ',1)[0],price=str(row['TotalCharges']))
            url='https://portfoliomanager.energystar.gov/ws/meter/{meterid}/consumptionData'
            url=url.format(meterid=id)
            print(requests.post(url,auth=HTTPBasicAuth(user,password), data=xml, headers=headers).text)

    return faillist
def failaddressfinder(faillist):
    condict={}
    if len(faillist)>=1:
        errors.write("The Following Constellation ID's do not have an ESPM meter equivalent: - Check if the building is in Energy Star or if the meters have constellation ID in the 1st custom ID slot. Otherwise try updating your input files.:")
        condf = pd.read_excel(inputfile)
        for index,row in condf.iterrows():
            if row['MeterNumber'] not in faillist:
                condf.drop(index,inplace=True)
        for index,row in condf.iterrows():
            try:
                condict.update({row['MeterNumber']:row['street']})
            except:
                condict.update({row['MeterNumber']:"No Street Found"})
        for item in condict:
            str="Address:{address}, Constellation ID:{conid}"
            errors.write(str.format(address=condict[item],conid=item))

if st.button("Run Program"):
    console.write("Beginning Upload of Meters:")
    idmatchlist=espmidmatcher()
    faillist=customidfinder(idmatchlist)
    failaddressfinder(faillist)
    console.write("Finished!")

with st.expander(label="Tutorial :open_book:"):
    st.write("To begin, you will need a custom ESPM download of all the properties you want to upload gas data to and the constellation file containing the data you want to upload.")
    st.write("To get this ESPM custom download, go to Energy Star - custom download, select the properties you wish to upload data to and then include basic property information AND Meters")
    st.write("Upload both files to their places in the uploader, enter your username and password and press run! Any errors or console messages should appear to the right. ")
    st.write("contact bros@2030districts.org with any questions!")