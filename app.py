import streamlit as st
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

st.title("Crypto Information Chatbot")
st.write("Ask anything about cryptocurrency!")

# Set up Streamlit UI
input_text = st.text_input("You: ", "")
response_container = st.empty()

# CoinGecko API call function
def get_crypto_info(crypto_name):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if crypto_name in data:
            price = data[crypto_name]["usd"]
            return f"The current price of {crypto_name} is ${price} USD."
        else:
            return f"Sorry, I couldn't find the price for {crypto_name}."
    else:
        return "Sorry, I couldn't fetch the information at the moment."

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Handle user input
if input_text:
    st.session_state.chat_history.append(f"You: {input_text}")

    # Generate response using DialoGPT
    new_user_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = new_user_input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Decode response and append to chat history
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    st.session_state.chat_history.append(f"Bot: {response}")

    # Check if the input is a crypto query and append the crypto info to the response
    if "price" in input_text.lower() and any(crypto in input_text.lower() for crypto in ["bitcoin", "ethereum", "dogecoin", "litecoin"]):
        crypto_name = input_text.lower().split("price of ")[-1].strip()
        crypto_info = get_crypto_info(crypto_name)
        st.session_state.chat_history.append(f"Bot: {crypto_info}")

# Display chat history
response_container.text("\n".join(st.session_state.chat_history))
