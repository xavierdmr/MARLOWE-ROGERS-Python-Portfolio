import streamlit as st
import pandas as pd

# ================================
# Step 1: Displaying a Simple DataFrame in Streamlit
# ================================

st.subheader("Now, let's look at some data!")

# Creating a simple DataFrame manually
# This helps students understand how to display tabular data in Streamlit.
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
})

# Displaying the table in Streamlit
# st.dataframe() makes it interactive (sortable, scrollable)
st.write("Here's a simple table:")
st.dataframe(df)

# ================================
# Step 2: Adding User Interaction with Widgets
# ================================

# Using a selectbox to allow users to filter data by city
# Students learn how to use widgets in Streamlit for interactivity
city = st.selectbox("Select a city", df["City"].unique())

# Filtering the DataFrame based on user selection
st.write(f"People in {city}")
st.dataframe(df[df['City'] == city])
# Display the filtered results


# ================================
# Step 3: Importing Data Using a Relative Path
# ================================

# Now, instead of creating a DataFrame manually, we load a CSV file
# This teaches students how to work with external data in Streamlit
# # Ensure the "data" folder exists with the CSV file
# Display the imported dataset
df2 = pd.read_csv("data/sample_data.csv")
st.dataframe(df2)


# Using a selectbox to allow users to filter data by city
# Students learn how to use widgets in Streamlit for interactivity
salary = st.slider("Choose a maximum salary", min_value=df2['Salary'].min(), max_value = df2['Salary'].max())


st.write(f"Salaries under {salary}")
st.dataframe(df2[df2['Salary'] <= salary])
# Filtering the DataFrame based on user selection




# Display the filtered results

# ================================
# Summary of Learning Progression:
# 1️⃣ Displaying a basic DataFrame in Streamlit.
# 2️⃣ Adding user interaction with selectbox widgets.
# 3️⃣ Importing real-world datasets using a relative path.
# ================================