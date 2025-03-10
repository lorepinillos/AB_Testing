import streamlit as st
import seaborn as sns
import pandas as pd
import random
import matplotlib.pyplot as plt
import time

# Page title
st.title("A/B Testing for Data Visualization")

# Business Question 
st.subheader("Which month has the highest number of passengers?")

# Function to load data from Google Sheets
def load_data_from_google_sheets():
    """Fetch data from Google Sheets using direct CSV export"""
    try:
        url = "https://docs.google.com/spreadsheets/d/1aB9onEXYl_BcBZC9mqzj0preEaniv93O296voHw9PpI/export?format=csv"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {e}")
        return None

# Try to load data from Google Sheets, otherwise use seaborn dataset
try:
    df = load_data_from_google_sheets()
    if df is None:
        raise Exception("Unable to load data from Google Sheets")
    st.success("Successfully loaded data from Google Sheets!")
except:
    st.warning("Using default Seaborn dataset (Google Sheets not connected).")
    df = sns.load_dataset("flights")

# Display raw data in an expandable section
with st.expander("View Raw Data"):
    st.dataframe(df)

# Initialize session state variables if they don't exist
if "selected_chart" not in st.session_state:
    st.session_state.selected_chart = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "response_time" not in st.session_state:
    st.session_state.response_time = None
if "showing_result" not in st.session_state:
    st.session_state.showing_result = False

# Button to start the test and show a random chart
if st.session_state.selected_chart is None:
    if st.button("Show Chart"):
        # Randomly select chart A or B
        st.session_state.selected_chart = random.choice(["A", "B"])
        # Start timer
        st.session_state.start_time = time.time()

# Display the randomly selected chart
if st.session_state.selected_chart:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if st.session_state.selected_chart == "A":
        # Chart A: Bar chart
        sns.barplot(x="month", y="passengers", data=df, ax=ax)
        plt.title("Chart A: Bar Chart of Passengers per Month", fontsize=16)
    else:
        # Chart B: Line chart
        sns.lineplot(x="month", y="passengers", data=df, marker="o", ax=ax)
        plt.title("Chart B: Line Chart of Passengers per Month", fontsize=16)
    
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Number of Passengers", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Show "I answered your question" button
    if not st.session_state.showing_result:
        if st.button("I answered your question :)"):
            # Calculate response time
            end_time = time.time()
            st.session_state.response_time = round(end_time - st.session_state.start_time, 2)
            st.session_state.showing_result = True

# Display the response time if available
if st.session_state.showing_result and st.session_state.response_time is not None:
    st.success(f"Response Time: {st.session_state.response_time} seconds")
    st.write(f"You were shown Chart {st.session_state.selected_chart}")
    
    # Reset button
    if st.button("Reset Test"):
        # Reset all session state variables
        st.session_state.selected_chart = None
        st.session_state.start_time = None
        st.session_state.response_time = None
        st.session_state.showing_result = False