# 🐧 Pick A Penguin – Interactive Streamlit App

This beginner-level Streamlit app allows users to explore a dataset of 344 penguins by filtering based on species, sex, and body mass. The app is designed to help users discover and "select" a penguin that fits their criteria.

---

## Project Overview

"Pick A Penguin" introduces interactive web app development using Streamlit and pandas. By providing dropdown filters and sliders, users can dynamically narrow the dataset and view the details of their chosen penguin.

---

## Setup & Run Instructions

1. Clone this repository.
2. Navigate to the project directory: cd basicstreamlitapp
3. Install dependencies: 
    - pip install streamlit
    - pip install pandas
4. Run the app: streamlit run main.py

---

## App Features

- View a dataset of 344 penguins with various biological characteristics.
- Filter by:
    - Species (e.g.,  Adelie, Chinstrap, Gentoo)
    - Sex (Male or Female)
    - Body Mass (grams)
- Select a penguin by ID to view detailed information about it.
- Display a penguin image after selection.

---

## Dataset

- Source: [**Palmer Penguins Dataset**](data/penguins.csv)
- Contains species, island of origin, bill size, flipper length, body mass, sex, and year

---

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)