import streamlit as st
import requests
from transformers import pipeline

# Load the conversational model
chatbot = pipeline('conversational', model='microsoft/DialoGPT-medium')

# Define function to get crypto data from CoinGecko API
def get_crypto_data(crypto_id):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data

# Streamlit application
st.title('Real-Time Crypto Information and Chatbot')

# Section for cryptocurrency information
st.header('Crypto Information')
crypto_id = st.text_input('Enter the cryptocurrency ID (e.g., bitcoin, ethereum)')

if crypto_id:
    data = get_crypto_data(crypto_id)
    if data:
        st.write(f"**{crypto_id.capitalize()}**")
        st.write(f"Price (USD): ${data[crypto_id]['usd']}")
    else:
        st.write("Cryptocurrency not found.")

# Section for chatbot conversation
st.header('Chat with our Bot')
user_input = st.text_input('You:', '')

if user_input:
    response = chatbot(user_input)
    st.write('Bot:', response[0]['generated_text'])
