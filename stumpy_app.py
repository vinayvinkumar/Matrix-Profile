import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'stumpy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])

import streamlit as st
import pandas as pd
import numpy as np
import stumpy
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.patches import Rectangle

# Define the Streamlit app
def app():
    # Add a title
    st.title("Time-series analysis using Stumpy")

    # Add a file uploader
    uploaded_file = st.file_uploader("Upload your time-series data (CSV or Excel file)", type=["csv", "xlsx"])

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Load the data into a Pandas dataframe
        data = pd.read_csv(uploaded_file) if uploaded_file.type == "text/csv" else pd.read_excel(uploaded_file)

        # Let the user select the column for time-series analysis
        column = st.selectbox("Select a column for time-series analysis", data.columns)

        # Let the user choose the value of m for matrix profile analysis
        m = st.slider("Choose the value of m for matrix profile analysis", min_value=2, max_value=int(len(data[column]) / 2), value=30)

        # Let the user choose the maximum number of matches to display in the matrix profile graph
        max_matches = st.slider("Choose the maximum number of matches to display in the matrix profile graph", min_value=1, max_value=len(data[column]), value=10)

        # Let the user choose the maximum number of motifs to display
        max_motifs = st.slider("Choose the maximum number of motifs to display", min_value=1, max_value=10, value=5)

        # Plot the matrix profile graph
        st.line_chart(data[column], use_container_width=True)

        # Compute the matrix profile using Stumpy's stump function
        matrix_profile = stumpy.stump(data[column], m)

        # Plot the matrix profile graph
        st.line_chart(matrix_profile[:, 0], use_container_width=True)

        # Compute the univariate motif using Stumpy's motifs function
        motifs = stumpy.motifs(data[column].values,matrix_profile[:, 0],max_matches=max_matches, max_motifs=max_motifs)

        # Display the univariate motif(s)
        if len(motifs) > 0:
            st.write(f"Found {len(motifs)} univariate motif(s):")
            for motif in motifs:
                st.write(motif)
        else:
            st.write("No univariate motifs found.")

        conc_motifs = pd.DataFrame()
        for i in motifs[1][0]:
            conc_motifs[i] = data[column].iloc[i:i+m].values

        if not conc_motifs.empty:
            st.write(f"Top {max_motifs} motifs:")
            st.line_chart(conc_motifs,use_container_width=True)
        else:
             st.write("No motifs found.")

        # Plot the top 10 motifs
        # if len(top_motifs) > 0:
        #     st.write(f"Top 10 motifs:")
        #     for i, motif in enumerate(top_motifs):
        #         fig, ax = plt.subplots()
        #         ax.plot(motif["indices"], motif["values"])
        #         ax.set_title(f"Motif {i+1}")
        #         st.pyplot(fig)
        # else:
        #     st.write("No motifs found.")

app()
