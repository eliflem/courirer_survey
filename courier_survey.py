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


st.title("Banabikurye'de Daha Fazla Kazanç Elde Etmek İster Misiniz?")
st.subheader("Vereceğiniz bilgileri size daha uygun gönderiler sağlayabilmek için kullanacağız.")


phone = st.text_input("Telefon numaranız:")

def external_id(phone):
    while True:
        try:
            phone = phone.replace(" ", "")
            phone = phone.replace("-", "")
            phone = phone.replace("(", "")
            phone = phone.replace(")", "")
            phone = phone.replace("+", "")
            if len(phone) == 11:
                phone = phone[1:11]
            else:
                phone = phone  
            query = {
            "query" : {
                "field" : "phone",
                "operator" : "=",
                "value" : phone
            } } 
            url = "https://api.intercom.io/contacts/search"
            result = r.post(url, headers=headers, json=query)
            result = result.json()
            return(result["data"][0]["id"])
        except IndexError:
            return("not exist")

if not phone:
    st.subheader("Lütfen sisteme kayıtlı telefon numaranızı girip formu doldurunuz.")
elif external_id(phone) == "not exist":
    st.subheader("Lütfen sistemde kayıtlı olan telefon numaranızı giriniz.")
else:
    with st.form(key='my_form'):
        st.text("Hangi bölgelerde çalışmayı tercih edersiniz? Birden fazla seçim yapabilirsiniz.")
        avp1 = st.checkbox('AVP1 (Beşiktaş, Şişli, Kağıthane)')
        avp2 = st.checkbox('AVP2 (Fatih, Zeytinburnu)')
        avp3 = st.checkbox('AVP3 (Alibeyköy, Sarıyer, Sultangazi)')
        avp4 = st.checkbox('AVP4 (Gaziosmanpaşa, Esenler, Bayrampaşa, Bağcılar)')
        avp5 = st.checkbox('AVP5 (Bakırköy, Bahçelievler, Güngören, Küçükçekmece)')
        avp6 = st.checkbox('AVP6 (Başakşehir, Arnavutköy)')
        avp7 = st.checkbox('AVP7 (Avcılar, Beylikdüzü, Esenyurt, Büyükçekmece)')
        and1 = st.checkbox('AND1 (Kadıköy, Üsküdar, Ümraniye, Ataşehir)')
        and2 = st.checkbox('AND2 (Beykoz, Çekmeköy, Sancaktepe, Sultanbeyli)')
        and3 = st.checkbox('AND3 (Maltepe, Kartal, Pendik, Tuzla)')
        schedule = st.radio("Banabikurye'de çalışmak için haftada ne kadar zaman ayırabilirsiniz?", ('Haftada 20 saatten az çalışabilirim', 'Haftada 20 ila 30 saat arası çalışabilirim', 'Haftada 30 saatten fazla çalışabilirim'))
        has_company = st.radio('Kazancınıza karşılık fatura kesebileceğiniz bir şirketiniz var mı?', ('Evet', 'Hayır'))
        submit_button = st.form_submit_button(label='Gönder')


    if submit_button:
        st.subheader("Vermiş olduğunuz cevaplar için teşekkür ederiz.")
        
    courier_id = external_id(phone)
    
    
    preferred_regions = {}
    preferred_regions["avp1"] = avp1
    preferred_regions["avp2"] = avp2
    preferred_regions["avp3"] = avp3
    preferred_regions["avp4"] = avp4
    preferred_regions["avp5"] = avp5
    preferred_regions["avp6"] = avp6
    preferred_regions["avp7"] = avp7
    preferred_regions["and1"] = and1
    preferred_regions["and2"] = and2
    preferred_regions["and3"] = and3

    regions = []
    for key, value in preferred_regions.items():
             if value == True:
                regions.append(key)
        
    update_1 = {"type": "contact",
            "id": courier_id,
            "custom_attributes" : {
                               "preferred_regions": ' '.join(x for x in regions)
            }}


    # In[12]:


    update = r.put("https://api.intercom.io/contacts/"+courier_id+"", headers=headers, json=update_1)





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
