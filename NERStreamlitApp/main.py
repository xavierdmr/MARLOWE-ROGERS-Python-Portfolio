# Load dependencies
import streamlit as st
import pandas as pd
import spacy 
from spacy import displacy
nlp = spacy.load("en_core_web_sm") # Loading in the English language model

# Title and description of app
st.title("Custom Named Entity Recognition App")
st.write("This app allows the user to upload or paste in text to")

# Text input/upload
file_upload = st.file_uploader("Upload a text file:", type=["txt"])
if file_upload: # If file is uploaded, read into and decode its context so that it is contained in the text variable
    text = file_upload.read().decode("utf-8")
else: # If file is not uploaded, simply take text from text input box into text variable
    text = st.text_area("Alternatively, paste your text here:","Example text: Jeff is from Charlotte, NC. He works at Home Depot.")
nlp.max_length = len(text) # Adjusting max length for the NLP to the length of the text

# Formatting instructions for adding in custom patterns to EntityRuler
st.subheader("Add your custom patterns:")
st.write("Follow the exact format given below:")
st.write("LABEL:PATTERN")
st.write("For example, WIZARD:Gandalf")
st.write("Each new pattern must be on its own line.")
patterns_input = st.text_area("")


patterns = [] # Initializing patterns as empty dictionary
# Breaking up the patterns input into
if patterns_input: 
    for line in patterns_input.splitlines(): # Splits the inputted text into individual lines
        if line and ":" in line: 
            label, pattern = line.split(":") # Splits each line at the ":", creating 2 parts - label and pattern
            # Appending patterns with the exact format required by spaCy's EntityRuler
            patterns.append({
                "label": label.strip(), # Stripping in case there are extra accidental spaces/punctuation
                "pattern": pattern.strip()
            })
        else:
            st.write("Error: Improperly formatted pattern") # If user input doesn't match the required format, prints error message

# Allow user to see their custom patterns
st.subheader("Your custom patterns:")
st.write(patterns)

# Adding in the EntityRuler
# Checking if the "ner" pipe exists, and adding in the EntityRuler before it if so
if "ner" in nlp.pipe_names:
    # Adds the patterns if the EntityRuler exists
    try:
        ruler = nlp.get_pipe("entity_ruler")
    # If it doesn't exist, add it in before "ner"
    except Exception:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    ruler.add_patterns(patterns)
else:
    # Add both the EntityRuler and the NER component if "ner" does not exist
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    ner = nlp.add_pipe("ner")

# Processing the text through the NLP
doc = nlp(text)

# Display recognized entities using displaCy
st.subheader("Your labeled text:")
# Displacy renders as html, so have to use st.components.v1.html to display it properly in streamlit
html = displacy.render(doc, style="ent", page=True) 
st.components.v1.html(html, scrolling=True) 

# Additional entity analysis table providing the top 10 most frequent patterns and their frequency
st.subheader("Analyzing the entity data:")

# New list of data that extracts the text and label from doc.ents, which stores the processed entity data
entities_data = []
for ent in doc.ents:
    entities_data.append({
        'text': ent.text,
        'label': ent.label_
    })

# Create dataframe with this data
ent_df = pd.DataFrame(entities_data)

# If that dataframe has data in it, prints a table of the top 10 combinations
if not ent_df.empty:
    st.write("Top 10 Text and Label Combinations:")
    st.write(ent_df[['text','label']].value_counts()[:10])
else:
    st.write("No entities found to analyze.")




