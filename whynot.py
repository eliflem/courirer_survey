#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import requests as r
import pandas as pd
import time


# In[50]:


headers = {'Authorization': st.secrets["token"] , 'Accept': 'application/json', 'Content-Type': 'application/json'}



# In[2]:


st.title("Sizi Daha İyi Tanımamıza Yardımcı Olur Musunuz")
st.text("Vereceğiniz bilgileri size daha uygun gönderiler sağlayabilmek için kullanacağız.")


# In[ ]:


with st.form(key='my_form'):
    st.text("Lütfen sistemde kayıtlı olan telefon numaranızı giriniz")
    phone = st.text_input("Telefon numaranız:")
    st.text("Çalışmak istediğiniz bölgeleri seçiniz")
    preferred_regions = st.multiselect('Çalışmak istediğiniz bölgeleri seçiniz', ['R1', 'R2', 'R3', 'R4'])
    st.text("Banabikurye'de çalışmaya haftada ne kadar zaman ayırabilirsiniz?")
    schedule = st.radio('Haftalık çalışma uygunluğunuzu belirtiniz', ('Haftada 20 saatten az çalışabilirim', 'Haftada 20 ila 30 saat arası çalışabilirim', 'Haftada 30 saatten fazla çalışabilirim'))
    has_company = st.radio('Kazancınıza karşılık fatura kesebileceğiniz bir şirketiniz var mı?', ('Evet', 'Hayır'))
    submit_button = st.form_submit_button(label='Submit')


# In[21]:
if submit_button:
    st.write("Vermiş olduğunuz cevaplar için teşekkür ederiz.")


phone = phone.replace(" ", "")
phone = phone.replace("-", "")
if len(phone) == 11:
    phone = phone[1:11]
else:
    phone = phone


# #get phone number remove spaces and 0 from mthe beginning
# phone = phone.replace(" ", "")

# if len(phone) == 11:
#     phone = phone[1:11]
# else:
#     phone = phone

# In[3]:


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


# st.text("Please select the regions that you prefer to work in. You can choose more than one region.")
# regions = st.multiselect('Choose your regions', ['R1', 'R2', 'R3', 'R4'])

# In[ ]:


update_1 = {"type": "contact",
        "id": courier_id,
        "custom_attributes" : {
                           "preferred_regions": ' '.join(str(x) for x in preferred_regions)
        }}


# In[12]:


update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_1)


# st.text("Please select how will be your weekly working schedule")
# 
#     schedule = st.radio('Choose your daily working schedule', ('I will work whole work', 'I will work half week', 'I will work whenever I find time'))

# In[2]:


update_2 = {"type": "contact",
 "id": courier_id,
  "custom_attributes" : {
                       "schedule": schedule
}}


# In[ ]:


update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_2)


# st.text("Please select if you have a company")
# 
# has_company = st.selectbox('Do you have a company', ('Yes', 'No'))

# In[22]:


update_3 = {"type": "contact",
 "id": courier_id,
  "custom_attributes" : {
                       "has_company": has_company
}}


# In[ ]:


update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_3)

