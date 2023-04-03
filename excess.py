#!/usr/bin/env python
# coding: utf-8

# In[11]:

import pandas as pd
import streamlit as st

# Function to append the uploaded Excel files into a single DataFrame
def append_excel_files(input_files):
    appended_df = pd.DataFrame()

    for input_file in input_files:
        # Read the input Excel file into a DataFrame
        input_df = pd.read_excel(input_file, skiprows=5)

        # Remove columns with the name 'Unnamed'
        input_df = input_df.loc[:, ~input_df.columns.str.contains('^Unnamed')]

        # Rename columns as needed
        input_df = input_df.rename(columns={
            'Buyer Division': 'Buyer Division',
            'Warehouse': 'Warehouse',
            'Item Group': 'Item Group',
            'Item Code': 'Item Code',
            # Add the rest of the columns as needed, updating the names accordingly
        })

        # Append the DataFrame to the overall DataFrame
        appended_df = appended_df.append(input_df, ignore_index=True)

    return appended_df

# Set the title and page layout
st.set_page_config(page_title="Excel Processing App")
st.title("Excel Processing App")

# Allow the user to upload multiple Excel files
st.header("Upload Excel Files")
uploaded_files = st.file_uploader("Choose Excel files", type=["xlsx"], accept_multiple_files=True)

# If Excel files were uploaded, append them into a single DataFrame and display the result
if uploaded_files:
    st.header("Processing Results")

    # Call the appending function
    appended_df = append_excel_files(uploaded_files)

    # Display the appended DataFrame
    st.write("Appended file:")
    st.write(appended_df)

    # Save the appended DataFrame as an Excel file without the index column
    output_file = 'appended_output.xlsx'
    appended_df.to_excel(output_file, index=False)

    # Display the download button for the output Excel file
    st.download_button(
        label=f"Download appended file",
        data=open(output_file, 'rb').read(),
        file_name=output_file,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.warning("Please upload Excel files to get started.")






























































# In[ ]:




