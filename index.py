from config import API_KEY, GROQ_MODEL_NAME, MAX_TRIES, TEMPERATURE 
import streamlit as st  
from langchain_groq import ChatGroq  
from langchain_core.prompts import PromptTemplate  
from langchain.chains import LLMChain 

st.title("Restaurant Generator")  # Set the title for the Streamlit app.

# Sidebar input to select a country.
country = st.sidebar.selectbox("Select a country", ("India", "America", "Italy")) 

# Dictionary mapping countries to their states.
states_by_country = {
    "India": ["Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka"],
    "America": ["California", "Texas", "New York", "Florida"],
    "Italy": ["Rome", "Milan", "Venice", "Florence"]
}

# Sidebar input to select a state based on the selected country.
state = st.sidebar.selectbox("Select a state", states_by_country[country])

# Text input field to specify the type of cuisine.
cuisine_input = st.text_input("Enter the type of cuisine (e.g., Italian, Mexican, etc.):")

# Initialize the AI model with configuration parameters.
llm = ChatGroq(
    model=GROQ_MODEL_NAME,
    temperature=TEMPERATURE,
    max_retries=MAX_TRIES,
    api_key=API_KEY
)

# Define a prompt template for generating restaurant names based on cuisine.
restaurant_input_template = PromptTemplate(
    input_variables=['cuisine'],
    template="I want to open a hotel, suggest one name for {cuisine} cuisine."
)

# Create a chain for generating restaurant names.
restaurant_input_chain = LLMChain(llm=llm, prompt=restaurant_input_template)

# Define a prompt template for generating menu items based on cuisine and state.
cusine_input_template = PromptTemplate(
    input_variables=['cuisine', 'state'],
    template="Suggest some menu items specific to {cuisine} cuisine in {state} for a restaurant."
)

# Create a chain for generating menu items.
cusine_input_chain = LLMChain(llm=llm, prompt=cusine_input_template)

# Save the selected state to a variable for clarity.
state_input = state

# Save the selected country to a variable for clarity.
country_input = country

# Check if all inputs (cuisine, state, and country) are provided.
if cuisine_input and state_input and country_input:
    # Display a button to trigger the generation process.
    if st.button("Generate"):
        # Generate a restaurant name based on the cuisine input.
        hotel_name_response = restaurant_input_chain.run(cuisine_input)
        st.write(f"**Suggested Restaurant Name:** {hotel_name_response}")

        # Generate menu items based on cuisine and state inputs.
        menu_items_response = cusine_input_chain.run(cuisine=cuisine_input, state=state_input)
        st.write("**Suggested Menu Items for your restaurant:**")
        st.write(menu_items_response)
else:
    # Display a message if required inputs are missing.
    st.write("Please select country, state, and cuisine type to proceed.")
