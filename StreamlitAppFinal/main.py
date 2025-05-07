# Install dependencies
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Main title of the app
st.title("🌍 Country Comparison App 🌍")
st.write("Welcome to the Country Comparison App! With this app, you can upload indicator data from the World Bank Database, and visualize how different countries compare with each other across various metrics.")

### SIDEBAR: Upload + Options

# Section header
st.sidebar.header("Data Input")

# Allow user to upload a file if they don't want to use the default World Bank data included in the app
st.sidebar.write("If you would prefer to upload a new dataset with different countries and indicators, download your desired data from this [World Bank Database](https://databank.worldbank.org/source/world-development-indicators).")
uploaded_file = st.sidebar.file_uploader("Upload a World Bank-style CSV here:", type=["csv"])

# Use uploaded file if available, otherwise load sample data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded.") # Give green message confirming that user data was uploaded
else:
    df = pd.read_csv("data/wdi_data.csv")
    st.sidebar.info("Currently using sample dataset.") # Indicate that the data being used is the sample dataset

# To prevent crashing if user uploads a random file with unrelated data, shows an error message and stops the app if the required columns for the dropdowns aren't present.
required_cols = ["Country Name", "Country Code", "Series Name", "Series Code"]
if not all(col in df.columns for col in required_cols):
    st.error("Missing required columns. Please upload a valid World Bank-style dataset.")
    st.stop()

# The World Bank data downloads include some irrelevant information below the tables in the csv, so this drops these rows where each of the necessary four columns aren't empty.
# Also drops rows in the actual data where a country may not have data on a certain series (e.g. variable like GDP) for whatever reason.
df = df.dropna(subset=required_cols)

# Rename year columns from, for example, "2000 [YR2000]" to just "2000".
year_cols = [col for col in df.columns if "YR" in col] # Creating list of the column names that contain "YR", identifying the year columns (there is a column for each year in the wide format).
rename_dict = {col: col.split(" ")[0] for col in year_cols} # Creating a dictionary defining each column name as just the year number
df = df.rename(columns=rename_dict)

# Melt into long format (originally in wide) 
df_long = pd.melt(df, id_vars=["Country Name", "Series Name"], value_vars=rename_dict.values(), var_name="Year", value_name="Value")

# Convert year and value to numeric (initially read as strings from CSV)
df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce") # errors="coerce" ignores bad rows that can't be converted for whatever reason
df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce") 
df_long = df_long.dropna(subset=["Year", "Value"]) # Drop missing values

### SIDEBAR: User Selections

st.sidebar.header("Comparison Selections")

# Dynamic country and indicator lists from the dataset
available_countries = sorted(df_long["Country Name"].unique()) # Gets all of the unique country names from the dataset and puts them in alphabetical order
available_indicators = sorted(df_long["Series Name"].unique()) # Gets all of the unique indicators from the dataset and puts them in alphabetical order

# Multi-select for countries - allow user to select any number of countries to compare against each other
selected_countries = st.sidebar.multiselect("Select countries to compare", available_countries, default=available_countries[:2]) # By default selecting the first 2 countries in the list so that there isn't just an empty display when the app is launched

# Selectbox for indicator
selected_indicator = st.sidebar.selectbox("Select indicator", available_indicators)

# Year range slider based on available data, allowing user to limit year range in the comparison
min_year = int(df_long["Year"].min())
max_year = int(df_long["Year"].max())
selected_years = st.sidebar.slider("Select year range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

### MAIN DISPLAY AREA

#  Filter for selected data, creating a new dataframe containing only the selected countries, indicator, and year range
filtered = df_long[
    (df_long["Country Name"].isin(selected_countries)) &
    (df_long["Series Name"] == selected_indicator) &
    (df_long["Year"] >= selected_years[0]) &
    (df_long["Year"] <= selected_years[1])
]

# Line chart section

# Determine appropriate scaling factor based on largest value
max_val = filtered["Value"].max()

if max_val >= 1_000_000_000_000:
    scale = 1_000_000_000_000
    y_label = "Value (Trillions)"
elif max_val >= 1_000_000_000:
    scale = 1_000_000_000
    y_label = "Value (Billions)"
elif max_val >= 1_000_000:
    scale = 1_000_000
    y_label = "Value (Millions)"
else:
    scale = 1
    y_label = "Value"

# Plotting the actual chart
st.header(f"📈 Line Chart: {selected_indicator}") # Chart title with selected indicator
st.write(f"This line chart displays trends in **{selected_indicator}** from **{selected_years[0]}** to **{selected_years[1]}** " + f"for: **{', '.join(selected_countries)}**."
)
# Only plot chart if at least 1 country is selected and there is data available for that country/countries in the given indicator/years
if filtered.empty or len(selected_countries) == 0:
    st.warning("Please select at least one country and an indicator with available data.")
else:
    fig, ax = plt.subplots()
    for country in selected_countries: # Plotting a line for each selected country
        country_data = filtered[filtered["Country Name"] == country] # Getting a dataframe including the data for a specific country for the selected indicator/years... filtering the already filtered df
        scaled_values = country_data["Value"] / scale # Ensuring the values that show up on the axis are scaled to match the scale indicated in the axis label
        ax.plot(country_data["Year"], scaled_values, marker="o", label=country) # Plot the values

    ax.set_title(selected_indicator)
    ax.set_xlabel("Year")
    ax.set_ylabel(y_label)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Bar chart section

st.header("📊 Bar Chart (Most Recent Year)")

# Get the most recent year in the filtered data
most_recent_year = filtered["Year"].max()
recent_data = filtered[filtered["Year"] == most_recent_year]

st.write(f"This bar chart compares **{selected_indicator}** in the year **{most_recent_year}** " + f"between: **{', '.join(selected_countries)}**.")

if not recent_data.empty: # Only graph if there is data from the most recent year for any of the selected countries
    
    # Determine appropriate scaling (same as in line graph)
    max_val_bar = recent_data["Value"].max() # Grab max value of the bar

    # Adjust scale depending on max value, re-label y-axis to reflect this
    if max_val_bar >= 1_000_000_000_000:
        scale_bar = 1_000_000_000_000
        y_label_bar = "Value (Trillions)"
    elif max_val_bar >= 1_000_000_000:
        scale_bar = 1_000_000_000
        y_label_bar = "Value (Billions)"
    elif max_val_bar >= 1_000_000:
        scale_bar = 1_000_000
        y_label_bar = "Value (Millions)"
    else:
        scale_bar = 1
        y_label_bar = "Value"

    # Scale the data 
    recent_data_scaled = recent_data.copy()
    recent_data_scaled["Scaled Value"] = recent_data_scaled["Value"] / scale_bar # divide the value by the scale (e.g., 1 trillion/1 trillion = 1, will display as 1)

    # Plot the graph
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(recent_data_scaled["Country Name"], recent_data_scaled["Scaled Value"], color="green") # defining "bars" so that I can add value labels
    ax2.set_ylabel(y_label_bar)
    ax2.set_title(f"{selected_indicator} in {int(most_recent_year)}")
    # Add value labels above bars
    ax2.bar_label(bars, fmt="%.2f", label_type="edge")

    st.pyplot(fig2)
else:
    st.warning("No data available for the most recent year.") # Display this message if the selected countries don't have data from the most recent available year

# Show filtered data as a table
st.header("Filtered Data Table")
filtered_display = filtered.copy()
filtered_display["Year"] = filtered_display["Year"].astype(str) # astype(str) so that year displays without comma
st.dataframe(filtered_display)