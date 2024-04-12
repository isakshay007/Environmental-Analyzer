import os
from PIL import Image
from pathlib import Path
import streamlit as st
import pandas as pd  # Import pandas module
from utils import utils
from lyzr import DataConnector, DataAnalyzr

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]
# create directory if it doesn't exist
data = "data"
plot = 'plot'
os.makedirs(data, exist_ok=True)
os.makedirs(plot, exist_ok=True)

# Setup your config
st.set_page_config(
    page_title="Lyzr",
    layout="centered",  # or "wide" 
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Environmental Data Navigator🌐")
st.markdown("### Built using Lyzr🚀")
st.markdown("Explore environmental datasets effortlessly with our Environmental Data Navigator, powered by Lyzr. Upload your data, generate insights, and uncover valuable information to better understand environmental trends and make informed decisions for a sustainable future.")
# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

#Application

def data_uploader():
    st.subheader("Upload Data file")
    # Upload csv file
    uploaded_file = st.file_uploader("Choose csv file", type=["csv"])
    if uploaded_file is not None:
        utils.save_uploaded_file(uploaded_file)
    else:
        utils.remove_existing_files(data)
        utils.remove_existing_files(plot)

def analyzr():
    path = utils.get_files_in_directory(data)
    path = path[0]

    dataframe = DataConnector().fetch_dataframe_from_csv(file_path=Path(path))
    analyzr_instance = DataAnalyzr(df=dataframe, api_key=st.secrets["apikey"])

    return analyzr_instance

def file_checker():
    file = []
    for filename in os.listdir(data):
        file_path = os.path.join(data, filename)
        file.append(file_path)

    return file

# Function to display the dataset description
def display_description(analyzr):
    description = analyzr.dataset_description()
    if description is not None:
        st.subheader("Dataset Description:")
        st.write(description)

# Function to display queries
def display_queries(analyzr):
    queries = analyzr.ai_queries_df()
    if queries is not None:
        st.subheader("These Queries you can run on the data:")
        st.write(queries)

# Modify DataConnector class to specify encoding when reading CSV file
class DataConnector:
    def fetch_dataframe_from_csv(self, file_path):
        """
        Fetches a Pandas DataFrame from a CSV file.

        Parameters:
            file_path (Path): Path to the CSV file.

        Returns:
            dataframe (DataFrame): Pandas DataFrame containing the data from the CSV file.
        """
        try:
            # Specify encoding as 'latin1' when reading the CSV file
            dataframe = pd.read_csv(file_path, encoding='latin1')
            return dataframe
        except Exception as e:
            raise RuntimeError(f"Error occurred while reading CSV file '{file_path}': {str(e)}")

if __name__ == "__main__":
    style_app()
    st.sidebar.title("Environmental Data Navigator")
    selection = st.sidebar.radio("Go to", ["Data", "Analysis"])

    if selection == "Data":
        data_uploader()
    elif selection == "Analysis":
        file = file_checker()
        if len(file) > 0:
            analyzr = analyzr()

            # Create buttons for the options
            if st.button("Data Description"):
                display_description(analyzr)
            if st.button("Generate Queries"):
                display_queries(analyzr)
        
        else:
            st.error("Please upload a CSV file")
                
    
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr DataAnalyzr agent to generate analysis on data. With DataAnalyzr, you can streamline the complexity of data analytics into a powerful, intuitive, and conversational interface that lets you command data with ease. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)
