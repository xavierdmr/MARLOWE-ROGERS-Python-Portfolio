import streamlit as st
import pandas as pd

st.title("Pick A Penguin!")
st.write("Welcome to Pick A Penguin! This app allows you to view details about hundreds of different penguins and select one of them that is right for you.")
st.write("Below is a table documenting 344 penguins of various species, islands of origin, and sizes.")

# Brings in penguins.csv dataset from  data folder. Important that the user has this dataset downloaded in a "data" folder as well
df = pd.read_csv("data/penguins.csv")

# First data table (full and unfiltered)
st.dataframe(df)

st.subheader("Filter by species, sex, and body mass to find the penguin that is right for you!")

# Filters by species, sex, and body mass to narrow down the selection of penguins to choose from
species = st.selectbox("Select a species", df['species'].unique())
sex = st.selectbox("Select a sex", ['male','female']) # I don't do df['sex'] because it includes a "nan" option for the penguins without a listed sex 
mass = st.slider("Choose a maximum body mass (grams)", min_value=df['body_mass_g'].min(), max_value = df['body_mass_g'].max())

# Creates and shows filtered dataframe containing only the penguins that match the selected criteria
filtered_df = df[(df['species'] == species) & (df['sex'] == sex) & (df['body_mass_g'] <= mass)]
st.write(f"Here are the {sex} {species} penguins weighing under {mass} grams:")
st.dataframe(filtered_df)

# Prompts the user to select a penguin by ID number out of the filtered dataframe 
if not filtered_df.empty:
    id = st.selectbox("Pick a penguin by its ID number", filtered_df['id'].unique())
    # Creates a dataframe to show the user the details of the penguin that they selected
    selected_penguin = filtered_df[filtered_df['id'] == id]
    st.write("Congrats! Here are the details of your selected penguin:")
    st.dataframe(selected_penguin)
    st.image("https://transforms.stlzoo.org/production/animals/king-penguin-hero.jpg?w=800&h=950&auto=compress%2Cformat&fit=crop&dm=1643681906&s=a256b3b584f978fd6bff00921617ff49")
#If there are no penguins that match the criteria, the user will be notified. Otherwise, the user will select a penguin and be shown a stock image of a penguin along with their penguin's details
else:
    st.write("No penguins match the selected criteria. Consider increasing the body mass range or selecting a different species or sex.")