#!/usr/bin/env python
# coding: utf-8

# In[23]:


import streamlit as st
import requests as r
import pandas as pd
import time


# In[3]:


headers = {'Authorization': st.secrets["token"], 'Accept': 'application/json', 'Content-Type': 'application/json'}


# In[2]:


st.title("Help us to get to know you better")
st.text("We will use your answers to provide you the most suitable jobs")


# In[3]:


phone = st.text_input("Phone number:")

if not phone:
    st.write("please enter your phone")
else:
    query = {
    "query" : {
    "field" : "phone",
    "operator" : "=",
    "value" : phone
    } } 
    url = "https://api.intercom.io/contacts/search"
    result = r.post(url, headers=headers, json=query)
    result = result.json()
    courier_id = result["data"][0]["id"]


    # In[ ]:


    st.text("Please select the regions that you prefer to work in. You can choose more than one region.")
    regions = st.multiselect('Choose your regions', ['R1', 'R2', 'R3', 'R4'])


    # In[ ]:


    update_1 = {"type": "contact",
            "id": courier_id,
            "custom_attributes" : {
                               "regions": regions
            }}


    # In[12]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_1)


    # In[ ]:


    st.text("Please select how will be your weekly working schedule")

    schedule = st.radio('Choose your daily working schedule', ('I will work whole work', 'I will work half week', 'I will work whenever I find time'))


    # In[2]:


    update_2 = {"type": "contact",
     "id": courier_id,
      "custom_attributes" : {
                           "schedule": schedule
    }}


    # In[ ]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_2)


    # In[ ]:


    st.text("Please select if you have a company")

    has_company = st.selectbox('Do you have a company', ('Yes', 'No'))


    # In[22]:


    update_3 = {"type": "contact",
     "id": courier_id,
      "custom_attributes" : {
                           "has_company": has_company
    }}


    # In[ ]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_3)

