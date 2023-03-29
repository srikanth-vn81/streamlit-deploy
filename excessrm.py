#!/usr/bin/env python
# coding: utf-8

# In[21]:

import os
import pandas as pd
import streamlit as st
import base64
from pathlib import Path

def process_files(folder_path):
    all_files = os.listdir(folder_path)
    dataframes = []

    for file in all_files:
        file_path = os.path.join(folder_path, file)
        if file.endswith('.csv'):
            df = pd.read_csv(file_path, skiprows=5)
            dataframes.append(df)
        elif file.endswith('.xlsx'):
            df = pd.read_excel(file_path, skiprows=5)
            dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    # Remove 'Unnamed' columns
    unnamed_columns = combined_df.filter(like='Unnamed', axis=1).columns
    combined_df_cleaned = combined_df.drop(columns=unnamed_columns)

    return combined_df_cleaned

def get_table_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" target="_blank">Download file</a>'
    return href

st.title("File Appender")

folder_path = st.text_input("Enter folder path:", "")

if folder_path:
    folder_path = Path(folder_path)
    if folder_path.exists() and folder_path.is_dir():
        try:
            combined_df_cleaned = process_files(str(folder_path))
            st.write("Appended and cleaned data:")
            st.dataframe(combined_df_cleaned)

            if st.button("Export to Excel"):
                output_file = "combined_data_cleaned.csv"
                st.markdown(get_table_download_link(combined_df_cleaned, output_file), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Invalid folder path. Please make sure the path is correct.")



# In[ ]:




