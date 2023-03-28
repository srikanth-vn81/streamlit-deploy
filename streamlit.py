#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import streamlit as st


# In[3]:


df = pd.read_csv(r'C:\Users\srikanthve\Documents\Maria DB\week13.csv')


# In[4]:


df.head()


# In[5]:


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


# In[7]:


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)


# In[ ]:




