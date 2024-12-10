import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO
from datetime import datetime

# Included Items
INCLUDED_ITEMS = [
    "Average dietary energy supply adequacy (percent) (3-year average)",
    "Average protein supply (g/cap/day) (3-year average)",
    "Coefficient of variation of habitual caloric consumption distribution (real number)",
    "Number of children under 5 years of age who are stunted (modeled estimates)",
    "Percentage of children under 5 years of age who are stunted (modelled estimates) (percent)",
    "Per capita food supply variability (kcal/cap/day)",
    "Percentage of population using at least basic sanitation services (percent)",
    "Percentage of population using safely managed drinking water services (percent)",
    "Prevalence of low birthweight (percent)",
    "Political stability and absence of violence/terrorism (index)",
    "Prevalence of obesity in the adult population (18 years and older) (percent)",
    "Prevalence of undernourishment (percent) (3-year average)",
    "Share of dietary energy supply derived from cereals, roots and tubers (percent) (3-year average)"
]

# Constants
FLAG_IMAGE_BASE_URL = "https://raw.githubusercontent.com/Manny735/Project-1/refs/heads/main/flags/"
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/Manny735/Project-1/refs/heads/main/path-to-datasets/"

DATASET_GLOB = [
    "suite-of-food-security-indicators_rus.csv",  # Russia
    "suite-of-food-security-indicators_can.csv",  # Canada
    "suite-of-food-security-indicators_chn.csv",  # China
    "suite-of-food-security-indicators_usa.csv",  # United States
    "suite-of-food-security-indicators_bra.csv",  # Brazil
    "suite-of-food-security-indicators_aus.csv",  # Australia
    "suite-of-food-security-indicators_ind.csv",  # India
    "suite-of-food-security-indicators_arg.csv",  # Argentina
    "suite-of-food-security-indicators_kaz.csv",  # Kazakhstan
    "suite-of-food-security-indicators_dza.csv",  # Algeria
    "suite-of-food-security-indicators_cod.csv",  # Congo (DR)
    "suite-of-food-security-indicators_sau.csv",  # Saudi Arabia
    "suite-of-food-security-indicators_mex.csv",  # Mexico
    "suite-of-food-security-indicators_idn.csv",  # Indonesia
    "suite-of-food-security-indicators_sdn.csv",  # Sudan
    "suite-of-food-security-indicators_lby.csv",  # Libya
    "suite-of-food-security-indicators_irn.csv",  # Iran
    "suite-of-food-security-indicators_mng.csv",  # Mongolia
    "suite-of-food-security-indicators_per.csv",  # Peru
    "suite-of-food-security-indicators_tcd.csv",  # Chad
    "suite-of-food-security-indicators_ner.csv",  # Niger
    "suite-of-food-security-indicators_ago.csv",  # Angola
    "suite-of-food-security-indicators_mli.csv",  # Mali
    "suite-of-food-security-indicators_zaf.csv",  # South Africa
    "suite-of-food-security-indicators_col.csv",  # Colombia
    "suite-of-food-security-indicators_eth.csv",  # Ethiopia
    "suite-of-food-security-indicators_bol.csv",  # Bolivia
    "suite-of-food-security-indicators_mrt.csv",  # Mauritania
    "suite-of-food-security-indicators_egy.csv",  # Egypt
    "suite-of-food-security-indicators_tza.csv",  # Tanzania
    "suite-of-food-security-indicators_nga.csv",  # Nigeria
    "suite-of-food-security-indicators_ven.csv",  # Venezuela
    "suite-of-food-security-indicators_pak.csv",  # Pakistan
    "suite-of-food-security-indicators_moz.csv",  # Mozambique
    "suite-of-food-security-indicators_tur.csv",  # Turkey
    "suite-of-food-security-indicators_chl.csv",  # Chile
    "suite-of-food-security-indicators_zmb.csv",  # Zambia
    "suite-of-food-security-indicators_mmr.csv",  # Myanmar (Burma)
    "suite-of-food-security-indicators_afg.csv",  # Afghanistan
    "suite-of-food-security-indicators_ssd.csv",  # South Sudan
    "suite-of-food-security-indicators_fra.csv",  # France (European part)
    "suite-of-food-security-indicators_som.csv",  # Somalia
    "suite-of-food-security-indicators_caf.csv",  # Central African Republic
    "suite-of-food-security-indicators_ukr.csv",  # Ukraine
    "suite-of-food-security-indicators_mdg.csv",  # Madagascar
    "suite-of-food-security-indicators_bwa.csv",  # Botswana
    "suite-of-food-security-indicators_ken.csv",  # Kenya
    "suite-of-food-security-indicators_yem.csv",  # Yemen
    "suite-of-food-security-indicators_tha.csv",  # Thailand
    "suite-of-food-security-indicators_esp.csv",  # Spain
    "suite-of-food-security-indicators_tkm.csv",  # Turkmenistan
    "suite-of-food-security-indicators_cmr.csv",  # Cameroon
    "suite-of-food-security-indicators_png.csv",  # Papua New Guinea
    "suite-of-food-security-indicators_swe.csv",  # Sweden
    "suite-of-food-security-indicators_uzb.csv",  # Uzbekistan
    "suite-of-food-security-indicators_mar.csv",  # Morocco
    "suite-of-food-security-indicators_irq.csv",  # Iraq
    "suite-of-food-security-indicators_pry.csv",  # Paraguay
    "suite-of-food-security-indicators_zwe.csv",  # Zimbabwe
    "suite-of-food-security-indicators_jpn.csv",  # Japan
    "suite-of-food-security-indicators_deu.csv",  # Germany
    "suite-of-food-security-indicators_cog.csv",  # Republic of the Congo
    "suite-of-food-security-indicators_fin.csv",  # Finland
    "suite-of-food-security-indicators_vnm.csv",  # Vietnam
    "suite-of-food-security-indicators_mys.csv",  # Malaysia
    "suite-of-food-security-indicators_nor.csv",  # Norway
    "suite-of-food-security-indicators_civ.csv",  # Ivory Coast
    "suite-of-food-security-indicators_pol.csv",  # Poland
    "suite-of-food-security-indicators_omn.csv",  # Oman
    "suite-of-food-security-indicators_ita.csv",  # Italy
    "suite-of-food-security-indicators_phl.csv",  # Philippines
    "suite-of-food-security-indicators_ecu.csv",  # Ecuador
    "suite-of-food-security-indicators_bfa.csv",  # Burkina Faso
    "suite-of-food-security-indicators_nzl.csv",  # New Zealand
    "suite-of-food-security-indicators_gab.csv",  # Gabon
    "suite-of-food-security-indicators_gin.csv",  # Guinea
    "suite-of-food-security-indicators_gbr.csv",  # United Kingdom
    "suite-of-food-security-indicators_uga.csv"   # Uganda
]

COUNTRY_MAPPING = {
    "rus": {"name": "Russia", "iso_alpha": "RUS", "iso_alpha_2": "ru", "flag": "🇷🇺"},
    "can": {"name": "Canada", "iso_alpha": "CAN", "iso_alpha_2": "ca", "flag": "🇨🇦"},
    "chn": {"name": "China", "iso_alpha": "CHN", "iso_alpha_2": "cn", "flag": "🇨🇳"},
    "usa": {"name": "United States", "iso_alpha": "USA", "iso_alpha_2": "us", "flag": "🇺🇸"},
    "bra": {"name": "Brazil", "iso_alpha": "BRA", "iso_alpha_2": "br", "flag": "🇧🇷"},
    "aus": {"name": "Australia", "iso_alpha": "AUS", "iso_alpha_2": "au", "flag": "🇦🇺"},
    "ind": {"name": "India", "iso_alpha": "IND", "iso_alpha_2": "in", "flag": "🇮🇳"},
    "arg": {"name": "Argentina", "iso_alpha": "ARG", "iso_alpha_2": "ar", "flag": "🇦🇷"},
    "kaz": {"name": "Kazakhstan", "iso_alpha": "KAZ", "iso_alpha_2": "kz", "flag": "🇰🇿"},
    "dza": {"name": "Algeria", "iso_alpha": "DZA", "iso_alpha_2": "dz", "flag": "🇩🇿"},
    "cod": {"name": "Congo (DR)", "iso_alpha": "COD", "iso_alpha_2": "cd", "flag": "🇨🇩"},
    "sau": {"name": "Saudi Arabia", "iso_alpha": "SAU", "iso_alpha_2": "sa", "flag": "🇸🇦"},
    "mex": {"name": "Mexico", "iso_alpha": "MEX", "iso_alpha_2": "mx", "flag": "🇲🇽"},
    "idn": {"name": "Indonesia", "iso_alpha": "IDN", "iso_alpha_2": "id", "flag": "🇮🇩"},
    "sdn": {"name": "Sudan", "iso_alpha": "SDN", "iso_alpha_2": "sd", "flag": "🇸🇩"},
    "lby": {"name": "Libya", "iso_alpha": "LBY", "iso_alpha_2": "ly", "flag": "🇱🇾"},
    "irn": {"name": "Iran", "iso_alpha": "IRN", "iso_alpha_2": "ir", "flag": "🇮🇷"},
    "mng": {"name": "Mongolia", "iso_alpha": "MNG", "iso_alpha_2": "mn", "flag": "🇲🇳"},
    "per": {"name": "Peru", "iso_alpha": "PER", "iso_alpha_2": "pe", "flag": "🇵🇪"},
    "tcd": {"name": "Chad", "iso_alpha": "TCD", "iso_alpha_2": "td", "flag": "🇹🇩"},
    "ner": {"name": "Niger", "iso_alpha": "NER", "iso_alpha_2": "ne", "flag": "🇳🇪"},
    "ago": {"name": "Angola", "iso_alpha": "AGO", "iso_alpha_2": "ao", "flag": "🇦🇴"},
    "mli": {"name": "Mali", "iso_alpha": "MLI", "iso_alpha_2": "ml", "flag": "🇲🇱"},
    "zaf": {"name": "South Africa", "iso_alpha": "ZAF", "iso_alpha_2": "za", "flag": "🇿🇦"},
    "col": {"name": "Colombia", "iso_alpha": "COL", "iso_alpha_2": "co", "flag": "🇨🇴"},
    "eth": {"name": "Ethiopia", "iso_alpha": "ETH", "iso_alpha_2": "et", "flag": "🇪🇹"},
    "bol": {"name": "Bolivia", "iso_alpha": "BOL", "iso_alpha_2": "bo", "flag": "🇧🇴"},
    "mrt": {"name": "Mauritania", "iso_alpha": "MRT", "iso_alpha_2": "mr", "flag": "🇲🇷"},
    "egy": {"name": "Egypt", "iso_alpha": "EGY", "iso_alpha_2": "eg", "flag": "🇪🇬"},
    "tza": {"name": "Tanzania", "iso_alpha": "TZA", "iso_alpha_2": "tz", "flag": "🇹🇿"},
    "nga": {"name": "Nigeria", "iso_alpha": "NGA", "iso_alpha_2": "ng", "flag": "🇳🇬"},
    "ven": {"name": "Venezuela", "iso_alpha": "VEN", "iso_alpha_2": "ve", "flag": "🇻🇪"},
    "nam": {"name": "Namibia", "iso_alpha": "NAM", "iso_alpha_2": "na", "flag": "🇳🇦"},
    "pak": {"name": "Pakistan", "iso_alpha": "PAK", "iso_alpha_2": "pk", "flag": "🇵🇰"},
    "moz": {"name": "Mozambique", "iso_alpha": "MOZ", "iso_alpha_2": "mz", "flag": "🇲🇿"},
    "tur": {"name": "Turkey", "iso_alpha": "TUR", "iso_alpha_2": "tr", "flag": "🇹🇷"},
    "chl": {"name": "Chile", "iso_alpha": "CHL", "iso_alpha_2": "cl", "flag": "🇨🇱"},
    "zmb": {"name": "Zambia", "iso_alpha": "ZMB", "iso_alpha_2": "zm", "flag": "🇿🇲"},
    "mmr": {"name": "Myanmar (Burma)", "iso_alpha": "MMR", "iso_alpha_2": "mm", "flag": "🇲🇲"},
    "afg": {"name": "Afghanistan", "iso_alpha": "AFG", "iso_alpha_2": "af", "flag": "🇦🇫"},
    "ssd": {"name": "South Sudan", "iso_alpha": "SSD", "iso_alpha_2": "ss", "flag": "🇸🇸"},
    "fra": {"name": "France (European part)", "iso_alpha": "FRA", "iso_alpha_2": "fr", "flag": "🇫🇷"},
    "som": {"name": "Somalia", "iso_alpha": "SOM", "iso_alpha_2": "so", "flag": "🇸🇴"},
    "caf": {"name": "Central African Republic", "iso_alpha": "CAF", "iso_alpha_2": "cf", "flag": "🇨🇫"},
    "ukr": {"name": "Ukraine", "iso_alpha": "UKR", "iso_alpha_2": "ua", "flag": "🇺🇦"},
    "mdg": {"name": "Madagascar", "iso_alpha": "MDG", "iso_alpha_2": "mg", "flag": "🇲🇬"},
    "bwa": {"name": "Botswana", "iso_alpha": "BWA", "iso_alpha_2": "bw", "flag": "🇧🇼"},
    "ken": {"name": "Kenya", "iso_alpha": "KEN", "iso_alpha_2": "ke", "flag": "🇰🇪"},
    "yem": {"name": "Yemen", "iso_alpha": "YEM", "iso_alpha_2": "ye", "flag": "🇾🇪"},
    "tha": {"name": "Thailand", "iso_alpha": "THA", "iso_alpha_2": "th", "flag": "🇹🇭"},
    "esp": {"name": "Spain", "iso_alpha": "ESP", "iso_alpha_2": "es", "flag": "🇪🇸"},
    "tkm": {"name": "Turkmenistan", "iso_alpha": "TKM", "iso_alpha_2": "tm", "flag": "🇹🇲"},
    "cmr": {"name": "Cameroon", "iso_alpha": "CMR", "iso_alpha_2": "cm", "flag": "🇨🇲"},
    "png": {"name": "Papua New Guinea", "iso_alpha": "PNG", "iso_alpha_2": "pg", "flag": "🇵🇬"},
    "swe": {"name": "Sweden", "iso_alpha": "SWE", "iso_alpha_2": "se", "flag": "🇸🇪"},
    "uzb": {"name": "Uzbekistan", "iso_alpha": "UZB", "iso_alpha_2": "uz", "flag": "🇺🇿"},
    "mar": {"name": "Morocco", "iso_alpha": "MAR", "iso_alpha_2": "ma", "flag": "🇲🇦"},
    "irq": {"name": "Iraq", "iso_alpha": "IRQ", "iso_alpha_2": "iq", "flag": "🇮🇶"},
    "pry": {"name": "Paraguay", "iso_alpha": "PRY", "iso_alpha_2": "py", "flag": "🇵🇾"},
    "zwe": {"name": "Zimbabwe", "iso_alpha": "ZWE", "iso_alpha_2": "zw", "flag": "🇿🇼"},
    "jpn": {"name": "Japan", "iso_alpha": "JPN", "iso_alpha_2": "jp", "flag": "🇯🇵"},
    "deu": {"name": "Germany", "iso_alpha": "DEU", "iso_alpha_2": "de", "flag": "🇩🇪"},
    "cog": {"name": "Republic of the Congo", "iso_alpha": "COG", "iso_alpha_2": "cg", "flag": "🇨🇬"},
    "fin": {"name": "Finland", "iso_alpha": "FIN", "iso_alpha_2": "fi", "flag": "🇫🇮"},
    "vnm": {"name": "Vietnam", "iso_alpha": "VNM", "iso_alpha_2": "vn", "flag": "🇻🇳"},
    "mys": {"name": "Malaysia", "iso_alpha": "MYS", "iso_alpha_2": "my", "flag": "🇲🇾"},
    "nor": {"name": "Norway", "iso_alpha": "NOR", "iso_alpha_2": "no", "flag": "🇳🇴"},
    "civ": {"name": "Ivory Coast", "iso_alpha": "CIV", "iso_alpha_2": "ci", "flag": "🇨🇮"},
    "pol": {"name": "Poland", "iso_alpha": "POL", "iso_alpha_2": "pl", "flag": "🇵🇱"},
    "omn": {"name": "Oman", "iso_alpha": "OMN", "iso_alpha_2": "om", "flag": "🇴🇲"},
    "ita": {"name": "Italy", "iso_alpha": "ITA", "iso_alpha_2": "it", "flag": "🇮🇹"},
    "phl": {"name": "Philippines", "iso_alpha": "PHL", "iso_alpha_2": "ph", "flag": "🇵🇭"},
    "ecu": {"name": "Ecuador", "iso_alpha": "ECU", "iso_alpha_2": "ec", "flag": "🇪🇨"},
    "bfa": {"name": "Burkina Faso", "iso_alpha": "BFA", "iso_alpha_2": "bf", "flag": "🇧🇫"},
    "nzl": {"name": "New Zealand", "iso_alpha": "NZL", "iso_alpha_2": "nz", "flag": "🇳🇿"},
    "gab": {"name": "Gabon", "iso_alpha": "GAB", "iso_alpha_2": "ga", "flag": "🇬🇦"},
    "gin": {"name": "Guinea", "iso_alpha": "GIN", "iso_alpha_2": "gn", "flag": "🇬🇳"},
    "gbr": {"name": "United Kingdom", "iso_alpha": "GBR", "iso_alpha_2": "gb", "flag": "🇬🇧"},
    "uga": {"name": "Uganda", "iso_alpha": "UGA", "iso_alpha_2": "ug", "flag": "🇺🇬"},
}


# Column Names
ITEM_COLUMN = "item"
TIME_COLUMN = "startdate"
VALUE_COLUMN = "value"

# Functions
def format_dataset_name(file_name):
    country_code = file_name.split('_')[-1].split('.')[0].lower()
    country_info = COUNTRY_MAPPING.get(country_code)
    if country_info:
        return f"{country_info['name']} {country_info['flag']}"
    return file_name.replace('.csv', '').capitalize()

def get_country_code_by_name(display_name):
    for code, info in COUNTRY_MAPPING.items():
        if info['name'] in display_name:
            return code
    return None

def preprocess_value(value):
    if isinstance(value, str) and (value.startswith('<') or value.startswith('>')):
        return float(value[1:].strip())
    try:
        return float(value)
    except ValueError:
        return None

def clean_dates(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

@st.cache_data
def fetch_csv_from_github(file_name):
    url = GITHUB_RAW_BASE_URL + file_name
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))
    except requests.RequestException as e:
        st.error(f"Error fetching {file_name}: {e}")
        return None
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV from {file_name}: {e}")
        return None

def preprocess_data(data):
    data.columns = data.columns.str.lower().str.strip()
    if TIME_COLUMN in data.columns:
        data[TIME_COLUMN] = data[TIME_COLUMN].apply(clean_dates)
        data = data[data[TIME_COLUMN].notna()]
    if VALUE_COLUMN in data.columns:
        data[VALUE_COLUMN] = data[VALUE_COLUMN].apply(preprocess_value)
    if ITEM_COLUMN in data.columns:
        data = data[data[ITEM_COLUMN].isin(INCLUDED_ITEMS)]  # Filter only included items
    return data

def calculate_global_averages(date):
    averages = {}
    for file in dataset_files:
        country_data = preprocess_data(fetch_csv_from_github(file["file"]))
        if country_data is not None and not country_data.empty:
            filtered_data = country_data[country_data[TIME_COLUMN] == date]
            for _, row in filtered_data.iterrows():
                item = row[ITEM_COLUMN]
                value = row[VALUE_COLUMN]
                if pd.notna(value):
                    if item not in averages:
                        averages[item] = []
                    averages[item].append(value)
    # Calculate average for each item
    return {item: sum(values) / len(values) for item, values in averages.items()}
# App Layout
st.title("Food Security Analysis Dashboard")
st.write("Explore food security indicators across countries. 
\n All the data was collected from the HDX 
\n M.Mandakhbayar ")

# Dataset List
dataset_files = [{"file": file, "display": format_dataset_name(file)} for file in DATASET_GLOB]

# Sidebar Navigation
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["Select", "Time Series Analysis", "Comparison Analysis", "Country Overview", "Global Analysis"]
)

# Dataset Selection for relevant analyses
selected_dataset = None
if analysis_type in ["Time Series Analysis", "Country Overview"]:
    selected_display = st.sidebar.selectbox(
        "Select a dataset", options=[d["display"] for d in dataset_files]
    )
    selected_dataset = next(d["file"] for d in dataset_files if d["display"] == selected_display)
    selected_country_code = get_country_code_by_name(selected_display)

# Load Data
data = fetch_csv_from_github(selected_dataset) if selected_dataset else None
if data is not None:
    data = preprocess_data(data)



# Time Series Analysis
if analysis_type == "Time Series Analysis" and selected_country_code:
    st.image(f"{FLAG_IMAGE_BASE_URL}{COUNTRY_MAPPING[selected_country_code]['iso_alpha_2']}.svg", 
         width=150, caption=COUNTRY_MAPPING[selected_country_code]['name'])


    if data is not None and all(col in data.columns for col in [ITEM_COLUMN, TIME_COLUMN, VALUE_COLUMN]):
        # Filter dates between 2000 and 2020
        valid_dates = sorted([date for date in data[TIME_COLUMN].unique() if 2000 <= date.year <= 2020])

        # Add date range selection
        st.sidebar.subheader("Percentage change calculator")
        starting_date = st.sidebar.selectbox("Starting Date", options=valid_dates)
        ending_date = st.sidebar.selectbox("Ending Date", options=valid_dates[::-1])  # Reverse order for Ending Date

        if starting_date and ending_date:
            st.subheader("Time Series Analysis for All Items")
            
            # Ensure the dates are valid
            if starting_date > ending_date:
                st.error("Starting Date must be earlier than Ending Date.")
            else:
                # Loop through all unique items
                for item in sorted(data[ITEM_COLUMN].unique()):
                    # Filter data for the specific item
                    item_data = data[data[ITEM_COLUMN] == item]
                    
                    # Calculate percentage change
                    starting_value = item_data[item_data[TIME_COLUMN] == starting_date][VALUE_COLUMN].values
                    ending_value = item_data[item_data[TIME_COLUMN] == ending_date][VALUE_COLUMN].values

                    if starting_value.size > 0 and ending_value.size > 0:
                        percentage_change = ((ending_value[0] - starting_value[0]) / starting_value[0]) * 100
                        if percentage_change > 0:
                            change_text = f"**<span style='color:lime;'>Percentage change from {starting_date} to {ending_date}: +{percentage_change:.2f}% ↑</span>**"
                        else:
                            change_text = f"**<span style='color:red;'>Percentage change from {starting_date} to {ending_date}: {percentage_change:.2f}% ↓</span>**"
                    else:
                        change_text = "**Change: N/A (Data Missing)**"

                    # Create and display the chart
                    fig = px.line(
                        item_data,
                        x=TIME_COLUMN,
                        y=VALUE_COLUMN,
                        title=f"Time Series of {item}",
                        labels={TIME_COLUMN: "Date", VALUE_COLUMN: "Value"},
                    )
                    fig.update_yaxes(range=[0, item_data[VALUE_COLUMN].max() * 1.1])  # Start Y-axis at 0
                    
                    # Display the chart and percentage change
                    st.plotly_chart(fig)
                    st.markdown(change_text, unsafe_allow_html=True)
    else:
        st.error("The dataset is missing required columns.")



# Comparison Analysis
elif analysis_type == "Comparison Analysis":
    st.subheader("Comparison Analysis")
    dataset_1_display = st.sidebar.selectbox(
        "Select Dataset 1", options=[d["display"] for d in dataset_files]
    )
    dataset_2_display = st.sidebar.selectbox(
        "Select Dataset 2", options=[d["display"] for d in dataset_files]
    )

    if dataset_1_display and dataset_2_display:
        dataset_1_file = next(d["file"] for d in dataset_files if d["display"] == dataset_1_display)
        dataset_2_file = next(d["file"] for d in dataset_files if d["display"] == dataset_2_display)
        country_1_code = get_country_code_by_name(dataset_1_display)
        country_2_code = get_country_code_by_name(dataset_2_display)

        data_1 = preprocess_data(fetch_csv_from_github(dataset_1_file))
        data_2 = preprocess_data(fetch_csv_from_github(dataset_2_file))

        if data_1 is not None and data_2 is not None:
            selected_item = st.selectbox("Select an item for Comparison", options=sorted(data_1[ITEM_COLUMN].unique()))
            comparison_date = st.selectbox(
                "Select a date for Comparison",
                options=sorted(date for date in data_1[TIME_COLUMN].unique() if 2000 <= date.year <= 2020)
            )

            if selected_item and comparison_date:
                # Dynamic title showing the selected item and date
                st.write(f"### {selected_item} in {comparison_date}:")

                value_1 = data_1[(data_1[ITEM_COLUMN] == selected_item) & (data_1[TIME_COLUMN] == comparison_date)][VALUE_COLUMN].values
                value_2 = data_2[(data_2[ITEM_COLUMN] == selected_item) & (data_2[TIME_COLUMN] == comparison_date)][VALUE_COLUMN].values

                col1, col2 = st.columns(2)

                if value_1.size > 0 and value_2.size > 0:
                    # Display flag, metric, and time series for country 1
                    with col1:
                        st.image(f"{FLAG_IMAGE_BASE_URL}{COUNTRY_MAPPING[country_1_code]['iso_alpha_2']}.svg", 
         width=100, caption="")
                        st.metric(f"{COUNTRY_MAPPING[country_1_code]['name']} {COUNTRY_MAPPING[country_1_code]['flag']}",
                                  f"{value_1[0]:,.2f}")

                        # Time series for Dataset 1
                        country_1_item_data = data_1[data_1[ITEM_COLUMN] == selected_item]
                        fig_1 = px.line(
                            country_1_item_data,
                            x=TIME_COLUMN,
                            y=VALUE_COLUMN,
                            title=f"{COUNTRY_MAPPING[country_1_code]['name']} {selected_item} Time Series",
                            labels={TIME_COLUMN: "Date", VALUE_COLUMN: "Value"}
                        )
                        fig_1.update_yaxes(range=[0, country_1_item_data[VALUE_COLUMN].max() * 1.1])  # Start Y-axis at 0
                        st.plotly_chart(fig_1, use_container_width=True)

                    # Display flag, metric, and time series for country 2
                    with col2:
                        st.image(f"{FLAG_IMAGE_BASE_URL}{COUNTRY_MAPPING[country_2_code]['iso_alpha_2']}.svg", 
         width=100, caption="")

                        st.metric(f"{COUNTRY_MAPPING[country_2_code]['name']} {COUNTRY_MAPPING[country_2_code]['flag']}",
                                  f"{value_2[0]:,.2f}")

                        # Time series for Dataset 2
                        country_2_item_data = data_2[data_2[ITEM_COLUMN] == selected_item]
                        fig_2 = px.line(
                            country_2_item_data,
                            x=TIME_COLUMN,
                            y=VALUE_COLUMN,
                            title=f"{COUNTRY_MAPPING[country_2_code]['name']} {selected_item} Time Series",
                            labels={TIME_COLUMN: "Date", VALUE_COLUMN: "Value"}
                        )
                        fig_2.update_yaxes(range=[0, country_2_item_data[VALUE_COLUMN].max() * 1.1])  # Start Y-axis at 0
                        st.plotly_chart(fig_2, use_container_width=True)
                else:
                    st.warning("Data not available for the selected date or item.")

# Country Overview
elif analysis_type == "Country Overview" and selected_country_code:
    st.image(f"{FLAG_IMAGE_BASE_URL}{COUNTRY_MAPPING[selected_country_code]['iso_alpha_2']}.svg", 
         width=150, caption=COUNTRY_MAPPING[selected_country_code]['name'])

    if data is not None:
        selected_date = st.sidebar.selectbox(
            "Select a date for Overview", 
            options=sorted(date for date in data[TIME_COLUMN].unique() if 2000 <= date.year <= 2020)
        )
        if selected_date:
            st.subheader(f"Country Overview on {selected_date}")
            
            # Get the country's data for the selected date
            overview_data = data[data[TIME_COLUMN] == selected_date]
            
            # Calculate global averages for the selected date
            global_averages = calculate_global_averages(selected_date)
            
            # Prepare the table data
            table_data = []
            for _, row in overview_data.iterrows():
                item = row[ITEM_COLUMN]
                value = row[VALUE_COLUMN]
                global_average = global_averages.get(item, None)
                relative_to_average = (
                    f"{((value - global_average) / global_average) * 100:.2f}%" if global_average else "N/A"
                )
                table_data.append({
                    "Item": item,
                    "Value": f"{value:,.2f}" if pd.notna(value) else "N/A",
                    "Relative to Average": relative_to_average
                })
            
            # Convert to DataFrame and display as a table
            table_df = pd.DataFrame(table_data)
            st.write(table_df)



# Global Analysis
elif analysis_type == "Global Analysis":
    selected_item = st.sidebar.selectbox(
        "Select an Item for Global Analysis",
        options=[""] + sorted({
            item
            for file in dataset_files
            for item in preprocess_data(fetch_csv_from_github(file["file"]))[ITEM_COLUMN].unique()
        })
    )
    selected_date = st.sidebar.selectbox(
        "Select a Date for Global Analysis",
        options=[""] + sorted({
            date for file in dataset_files
            for date in preprocess_data(fetch_csv_from_github(file["file"]))[TIME_COLUMN].unique()
            if 2000 <= date.year <= 2020  # Restrict to dates between 2000 and 2020
        })
    )

    if selected_item and selected_date:
        map_data = []

        for file in dataset_files:
            country_key = file["file"].split('_')[-1].split('.')[0].lower()
            if country_key in COUNTRY_MAPPING:
                country_info = COUNTRY_MAPPING[country_key]
                country_data = preprocess_data(fetch_csv_from_github(file["file"]))
                if country_data is not None and not country_data.empty:
                    filtered_data = country_data[
                        (country_data[TIME_COLUMN] == selected_date) &
                        (country_data[ITEM_COLUMN] == selected_item)
                    ]

                    if not filtered_data.empty:
                        try:
                            value = float(filtered_data.iloc[0][VALUE_COLUMN])
                            map_data.append({
                                "iso_alpha": country_info["iso_alpha"],
                                "country": country_info["name"],
                                "flag": country_info["flag"],
                                "value": value
                            })
                        except ValueError:
                            pass

        if map_data:
            map_df = pd.DataFrame(map_data)

            st.subheader(f"Global Analysis of {selected_item} on {selected_date}")
            fig = px.choropleth(
                map_df,
                locations="iso_alpha",
                color="value",
                hover_name="country",
                title=f"Global Map of {selected_item} ({selected_date})",
                color_continuous_scale="Viridis",
                hover_data={"iso_alpha": False, "value": True}  # Exclude 'iso_alpha' from hover
            )
            st.plotly_chart(fig)
            for _, row in map_df.iterrows():
                st.write(f"{row['country']} {row['flag']}: {row['value']}")
        else:
            st.warning("No data available for the selected item or date.")
    else:
        st.warning("Please select both an item and a date.")
