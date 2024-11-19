import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO
from datetime import datetime

# Define column names
item_column = "item"
time_column = "startdate"
value_column = "value"

# GitHub repository raw URL (replace `your-username`, `your-repo`, and `branch`)
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/Manny735/Project-1/refs/heads/main/path-to-datasets/"

# Preprocessing function to clean value column
def preprocess_value(value):
    """
    Remove < or > signs from the value and convert to float.
    """
    if isinstance(value, str) and (value.startswith("<") or value.startswith(">")):
        return float(value[1:].strip())
    try:
        return float(value)
    except ValueError:
        return None  # Return None for non-convertible values

# Preprocessing function to clean and validate dates
def clean_dates(date):
    """
    Clean and validate dates.
    Returns a properly formatted date object if valid, or None if invalid.
    """
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None  # Return None for invalid dates

# Fetch CSV from GitHub repository
def fetch_csv_from_github(file_name):
    """
    Fetch a CSV file from the GitHub repository.
    Returns a pandas DataFrame if successful, otherwise None.
    """
    url = GITHUB_RAW_BASE_URL + file_name
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return pd.read_csv(StringIO(response.text))
    except requests.RequestException as e:
        st.error(f"Failed to fetch {file_name}: {e}")
        return None

# App Title
st.title("Food Security Dashboard")
st.write("Explore food security indicators across countries.")

# List of available datasets (hardcoded or fetched dynamically)
dataset_files = [
    "suite-of-food-security-indicators_afg.csv",
    "suite-of-food-security-indicators_aze.csv",
    "suite-of-food-security-indicators_bra.csv",
    "suite-of-food-security-indicators_can.csv",
    "suite-of-food-security-indicators_chn.csv",
    "suite-of-food-security-indicators_dza.csv",
    "suite-of-food-security-indicators_egy.csv",
    "suite-of-food-security-indicators_esp.csv",
    "suite-of-food-security-indicators_gha.csv",
    "suite-of-food-security-indicators_ind.csv",
    "suite-of-food-security-indicators_irn.csv",
    "suite-of-food-security-indicators_ita.csv",
    "suite-of-food-security-indicators_jpn.csv",
    "suite-of-food-security-indicators_ken.csv",
    "suite-of-food-security-indicators_kor.csv",
    "suite-of-food-security-indicators_mng.csv",
    "suite-of-food-security-indicators_mys.csv",
    "suite-of-food-security-indicators_nga.csv",
    "suite-of-food-security-indicators_nld.csv",
    "suite-of-food-security-indicators_pak.csv",
    "suite-of-food-security-indicators_phl.csv",
    "suite-of-food-security-indicators_pol.csv",
    "suite-of-food-security-indicators_prt.csv",
    "suite-of-food-security-indicators_rus.csv",
    "suite-of-food-security-indicators_swe.csv",
    "suite-of-food-security-indicators_twn.csv",
    "suite-of-food-security-indicators_usa.csv",
    "suite-of-food-security-indicators_ven.csv",
    "suite-of-food-security-indicators_yem.csv",
    "suite-of-food-security-indicators_zmb.csv"
]

# Sidebar navigation for analysis type
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["Select", "Time Series Analysis", "Comparison Analysis", "Country Overview", "Global Analysis"]
)

# Dataset Selection (only for specific sections)
if analysis_type in ["Time Series Analysis", "Country Overview"]:
    selected_file = st.sidebar.selectbox(
        "Select a dataset",
        options=dataset_files,
        format_func=lambda x: x.replace('.csv', '').capitalize()
    )

    if selected_file:
        data = fetch_csv_from_github(selected_file)
        if data is not None:
            data.columns = data.columns.str.lower().str.strip()  # Standardize column names

            # Apply preprocessing to the value column
            if value_column in data.columns:
                data[value_column] = data[value_column].apply(preprocess_value)

# Time Series Analysis Section
if analysis_type == "Time Series Analysis":
    if data is not None and all(col in data.columns for col in [item_column, time_column, value_column]):
        # Clean and validate the time column
        data[time_column] = data[time_column].apply(clean_dates)
        data = data[data[time_column].notna()]  # Remove rows with invalid dates

        # Filter dates between 2000 and 2020
        valid_dates = sorted(date for date in data[time_column].unique() if 2000 <= date.year <= 2020)

        selected_item = st.selectbox("Select an item for Time Series", options=sorted(data[item_column].unique()))
        if selected_item:
            item_data = data[data[item_column] == selected_item]
            st.subheader(f"Time Series of {selected_item}")
            fig = px.line(item_data, x=time_column, y=value_column, title=f"Time Series of {selected_item}")
            st.plotly_chart(fig)
    else:
        st.error("The required columns are missing in the dataset.")

# Comparison Analysis Section
elif analysis_type == "Comparison Analysis":
    st.sidebar.write("Select two datasets for comparison:")
    dataset_1 = st.sidebar.selectbox("Select Dataset 1", dataset_files, key="comp_file_1")
    dataset_2 = st.sidebar.selectbox("Select Dataset 2", dataset_files, key="comp_file_2")

    if dataset_1 and dataset_2:
        data_1 = fetch_csv_from_github(dataset_1)
        data_2 = fetch_csv_from_github(dataset_2)
        if data_1 is not None and data_2 is not None:
            data_1.columns = data_1.columns.str.lower().str.strip()
            data_2.columns = data_2.columns.str.lower().str.strip()

            # Apply preprocessing to the value column in both datasets
            if value_column in data_1.columns:
                data_1[value_column] = data_1[value_column].apply(preprocess_value)
            if value_column in data_2.columns:
                data_2[value_column] = data_2[value_column].apply(preprocess_value)

            if all(col in data_1.columns for col in [item_column, time_column, value_column]) and \
               all(col in data_2.columns for col in [item_column, time_column, value_column]):
                # Clean and filter the time columns
                data_1[time_column] = data_1[time_column].apply(clean_dates)
                data_2[time_column] = data_2[time_column].apply(clean_dates)
                data_1 = data_1[data_1[time_column].notna()]
                data_2 = data_2[data_2[time_column].notna()]

                selected_item = st.selectbox("Select an item for Comparison", options=sorted(data_1[item_column].unique()))
                comparison_date = st.selectbox(
                    "Select a date for Comparison",
                    options=sorted(date for date in data_1[time_column].unique() if 2000 <= date.year <= 2020)
                )

                if selected_item and comparison_date:
                    value_1 = data_1[(data_1[item_column] == selected_item) & (data_1[time_column] == comparison_date)][value_column].values
                    value_2 = data_2[(data_2[item_column] == selected_item) & (data_2[time_column] == comparison_date)][value_column].values

                    if value_1.size > 0 and value_2.size > 0:
                        try:
                            value_1 = float(value_1[0])
                            value_2 = float(value_2[0])
                            st.subheader(f"Comparison of {selected_item} on {comparison_date}")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**{dataset_1.replace('.csv', '').capitalize()}:** {value_1:,.2f}")
                            with col2:
                                st.markdown(f"**{dataset_2.replace('.csv', '').capitalize()}:** {value_2:,.2f}")
                        except ValueError:
                            st.error("Comparison values are not numeric.")

# Country Overview Section
elif analysis_type == "Country Overview":
    if data is not None and time_column in data.columns and value_column in data.columns:
        # Clean and validate the time column
        data[time_column] = data[time_column].apply(clean_dates)
        data = data[data[time_column].notna()]  # Remove invalid dates

        # Filter valid dates
        valid_dates = sorted(date for date in data[time_column].unique() if 2000 <= date.year <= 2020)

        selected_overview_date = st.sidebar.selectbox("Select a date for Overview", options=valid_dates)
        if selected_overview_date:
            st.subheader(f"Country Overview on {selected_overview_date}")
            date_data = data[(data[time_column] == selected_overview_date) & data[value_column].notna()]
            if not date_data.empty:
                for _, row in date_data.iterrows():
                    item_name = row[item_column]
                    try:
                        item_value = float(row[value_column])
                        st.markdown(
                            f"<div style='font-size: 1.5em; font-weight: bold; margin-top: 1em;'>{item_name}</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='font-size: 2.5em; font-weight: bold; color: #007bff;'>{item_value:,.2f}</div>",
                            unsafe_allow_html=True
                        )
                    except ValueError:
                        st.markdown(
                            f"<div style='font-size: 1.5em; font-weight: bold; margin-top: 1em;'>{item_name}</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='font-size: 2.5em; font-weight: bold; color: #007bff;'>{row[value_column]}</div>",
                            unsafe_allow_html=True
                        )
            else:
                st.error("No data available for the selected date.")
        else:
            st.error("Please select a valid date.")

# Global Analysis Section
elif analysis_type == "Global Analysis":
    # Collect all unique items and dates across datasets
    unique_items = set()
    all_dates = set()

    for file in dataset_files:
        global_data = fetch_csv_from_github(file)
        if global_data is not None:
            global_data.columns = global_data.columns.str.lower().str.strip()
            if item_column in global_data.columns:
                unique_items.update(global_data[item_column].unique())
            if time_column in global_data.columns:
                global_data[time_column] = global_data[time_column].apply(clean_dates)
                all_dates.update(global_data[time_column].dropna().unique())

    valid_dates = sorted(date for date in all_dates if 2000 <= date.year <= 2020)

    # User selects a date and an item for global analysis
    selected_date = st.sidebar.selectbox("Select a date for Global Analysis", options=valid_dates)
    selected_item = st.sidebar.selectbox("Select an item for Global Analysis", options=sorted(unique_items))

    # Main content area: Display data for the selected item and date
    if selected_date and selected_item:
        st.subheader(f"Global Analysis for {selected_item} on {selected_date}")
        for file in dataset_files:
            country_data = fetch_csv_from_github(file)
            if country_data is not None:
                country_data.columns = country_data.columns.str.lower().str.strip()
                if item_column in country_data.columns and time_column in country_data.columns and value_column in country_data.columns:
                    # Clean and filter dates for each dataset
                    country_data[time_column] = country_data[time_column].apply(clean_dates)
                    country_data = country_data[country_data[time_column].notna()]

                    # Filter data for the selected date and item
                    filtered_data = country_data[
                        (country_data[time_column] == selected_date) & 
                        (country_data[item_column] == selected_item)
                    ]

                    if not filtered_data.empty:
                        # Use the dataset name (without extension) as country name
                        country_name = file.replace('.csv', '').capitalize()
                        try:
                            # Extract value
                            value = float(filtered_data.iloc[0][value_column])
                            st.markdown(
                                f"""
                                <div style='display: flex; align-items: center; margin-top: 1em;'>
                                    <div style='font-size: 1.5em; font-weight: bold; margin-right: 1em;'>{country_name}</div>
                                    <div style='font-size: 1.5em; font-weight: bold; color: #007bff;'>{value:,.2f}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        except ValueError:
                            # If value is not numeric
                            st.markdown(
                                f"""
                                <div style='display: flex; align-items: center; margin-top: 1em;'>
                                    <div style='font-size: 1.5em; font-weight: bold; margin-right: 1em;'>{country_name}</div>
                                    <div style='font-size: 1.5em; font-weight: bold; color: #007bff;'>{filtered_data.iloc[0][value_column]}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    else:
                        # No data found for the selected date and item
                        st.markdown(
                            f"""
                            <div style='display: flex; align-items: center; margin-top: 1em;'>
                                <div style='font-size: 1.5em; font-weight: bold; margin-right: 1em;'>{file.replace('.csv', '').capitalize()}</div>
                                <div style='font-size: 1.5em; font-weight: bold; color: #ff0000;'>No data available</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

