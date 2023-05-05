import sys
import subprocess 

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'stumpy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl'])

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
        # data = pd.read_csv(uploaded_file) if uploaded_file.type == "application/vnd.ms-excel" else pd.read_excel(uploaded_file)
        data = pd.read_csv(uploaded_file) if uploaded_file.type == "text/csv" else pd.read_excel(uploaded_file)

        # Let the user select the column for time-series analysis
        column = st.selectbox("Select a column for time-series analysis", data.columns)

        st.write("Visualizing the Time Series Data")
        
        # Plot the data graph
        st.line_chart(data[column], use_container_width=True)

        # Let the user choose the value of m for matrix profile analysis
        m = st.slider("Choose the value of m for matrix profile analysis", min_value=2, max_value=int(len(data[column]) / 2), value=30)

        # Let the user choose the maximum number of matches to display in the matrix profile graph
        max_matches = st.slider("Choose the maximum number of matches to display in the matrix profile graph", min_value=1, max_value=len(data[column]), value=10)

        # Let the user choose the maximum number of motifs to display
        max_motifs = st.slider("Choose the maximum number of motifs to display", min_value=1, max_value=10, value=5)

        # Compute the matrix profile using Stumpy's stump function
        matrix_profile = stumpy.stump(data[column], m)

        motif_idx = np.argsort(matrix_profile[:, 0])[0]
        nearest_neighbor_idx = matrix_profile[motif_idx, 1]

        st.write("Visualizing the Matrix Profile")

        fig, axs = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0}, figsize=(20,16))
        plt.suptitle('Motif (Pattern) Discovery', fontsize='30')

        axs[0].plot(data[column].values)
        axs[0].set_ylabel(column, fontsize='20')
        rect = Rectangle((motif_idx, 0), m, 40, facecolor='lightgrey')
        axs[0].add_patch(rect)
        rect = Rectangle((nearest_neighbor_idx, 0), m, 40, facecolor='lightgrey')
        axs[0].add_patch(rect)
        axs[1].set_xlabel('Time', fontsize ='20')
        axs[1].set_ylabel('Matrix Profile', fontsize='20')
        axs[1].axvline(x=motif_idx, linestyle="dashed")
        axs[1].axvline(x=nearest_neighbor_idx, linestyle="dashed")
        axs[1].plot(matrix_profile[:, 0])
        st.pyplot(fig)

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

app()
