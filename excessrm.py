#!/usr/bin/env python
# coding: utf-8

# In[21]:
import pandas as pd
import streamlit as st
import base64

def process_files(files):
    dataframes = []

    for file in files:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, skiprows=5)
            dataframes.append(df)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, skiprows=5)
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

uploaded_files = st.file_uploader("Upload the files:", accept_multiple_files=True)

if uploaded_files:
    try:
        combined_df_cleaned = process_files(uploaded_files)
        st.write("Appended and cleaned data:")
        st.dataframe(combined_df_cleaned)

        if st.button("Export to Excel"):
            output_file = "combined_data_cleaned.csv"
            st.markdown(get_table_download_link(combined_df_cleaned, output_file), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {str(e)}")


# In[ ]:




