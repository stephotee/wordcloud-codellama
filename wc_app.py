import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import pandas as pd

# Set up the Streamlit app
st.title("Word Cloud Web App")

# Define the input text field and file uploader
text_field = st.text_input("Enter text:", "Type or paste text here")
file_uploader = st.file_uploader("Upload a .txt or .csv file:", type="txt,csv")

# Set up the generation button
generate_button = st.button("Generate Word Cloud")

# Set up the download button
download_button = st.button("Download PNG")

# Define the word cloud parameters
font_size = 8
font_color = "black"
text_case = "upper case"
stop_words = ["and", "the", "of", "it"]
additional_stop_words = []
num_words = 50

# Set up the word cloud data frame
word_cloud_data = pd.DataFrame()

# Define the tokenization function
def tokenize(text):
    return word_tokenize(text)

# Define the stop words removal function
def remove_stop_words(tokens):
    return [token for token in tokens if token not in stop_words and token.lower() not in additional_stop_words]

# Define the word cloud generation function
def generate_word_cloud():
    # Tokenize the text data
    tokens = tokenize(text_field)
    
    # Remove stop words from the text data
    filtered_tokens = remove_stop_words(tokens)
    
    # Count the frequency of each word in the text data
    counts = pd.Series(filtered_tokens).value_counts()
    
    # Sort the word cloud by frequency
    sorted_counts = counts.sort_values(ascending=False)
    
    # Trim the word cloud to the specified number of words
    trimmed_counts = sorted_counts[:num_words]
    
    # Create a new DataFrame with the top words from the word cloud
    word_cloud_data = pd.DataFrame({"word": trimmed_counts.index, "frequency": trimmed_counts.values})
    
    # Plot the word cloud
    plt.figure(figsize=(10, 8))
    plt.barh(x=word_cloud_data["word"], height=word_cloud_data["frequency"], color="black")
    plt.title("Word Cloud")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    
    # Set the font size and color for the word cloud
    plt.rcParams["font.size"] = font_size
    plt.rcParams["axes.labelcolor"] = font_color
    
    # Show the word cloud
    plt.show()
    
# Define the download PNG function
def download_png():
    # Create a new figure with the word cloud data
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot the word cloud on the new figure
    ax.barh(x=word_cloud_data["word"], height=word_cloud_data["frequency"], color="black")
    
    # Set the font size and color for the word cloud
    plt.rcParams["font.size"] = font_size
    plt.rcParams["axes.labelcolor"] = font_color
    
    # Save the figure as a PNG file
    fig.savefig("word_cloud.png")
    
# Set up the left side menu for additional controls to modify the word cloud after generation
left_menu = st.sidebar.expander("Additional Controls", expanded=False)
num_words_slider = left_menu.slider("Number of words:", 5, 100, 50)
color_selector = left_menu.selectbox("Text color:", ["black", "Colorful"])
text_case_selector = left_menu.radiobuttons("Text case:", ("upper case", "lower case"))
additional_stop_words_field = left_menu.text_input("Additional stop words (comma-separated):")

# Set up the event listeners for the input text field and file uploader
@st.experimental_memo
def memoized_tokenize(text):
    return tokenize(text)

@st.experimental_memo
def memoized_remove_stop_words(tokens):
    return remove_stop_words(tokens)

# Set up the event listeners for the left side menu controls
@st.experimental_memo
def memoized_num_words(value):
    return value

@st.experimental_memo
def memoized_color_selector(value):
    return value

@st.experimental_memo
def memoized_text_case_selector(value):
    return value

# Set up the event listeners for the download PNG button
@st.experimental_memo
def memoized_download_png():
    return True

# Set up the main content area
main = st.container()

# Set up the word cloud generation and download PNG buttons
main.button("Generate Word Cloud", generate_word_cloud)
main.button("Download PNG", download_png, disabled=memoized_download_png())

# Set up the left side menu for additional controls to modify the word cloud after generation
left = st.sidebar.expander("Additional Controls")
num_words = num_words_slider(left)
color_selector = color_selector(left)
text_case_selector = text_case_selector(left)
additional_stop_words_field = additional_stop_words_field(left)
