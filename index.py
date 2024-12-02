from config import API_KEY, GROQ_MODEL_NAME, MAX_TRIES, TEMPERATURE
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

st.title("Restaurant Generator")

country = st.sidebar.selectbox("Select a country", ("India", "America", "Italy"))
states_by_country = {
    "India": ["Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka"],
    "America": ["California", "Texas", "New York", "Florida"],
    "Italy": ["Rome", "Milan", "Venice", "Florence"]
}
state = st.sidebar.selectbox("Select a state", states_by_country[country])
cuisine_input = st.text_input("Enter the type of cuisine (e.g., Italian, Mexican, etc.):")
llm = ChatGroq(
    model=GROQ_MODEL_NAME,
    temperature=TEMPERATURE,
    max_retries=MAX_TRIES,
    api_key=API_KEY
)
restaurant_input_template = PromptTemplate(
    input_variables=['cuisine'],
    template="I want to open a hotel, suggest one name for {cuisine} cuisine."
)
restaurant_input_chain = LLMChain(llm=llm, prompt=restaurant_input_template)
cusine_input_template = PromptTemplate(
    input_variables=['cuisine', 'state'],
    template="Suggest some menu items specific to {cuisine} cuisine in {state} for a restaurant."
)

cusine_input_chain = LLMChain(llm=llm, prompt=cusine_input_template)

state_input = state
country_input = country

if cuisine_input and state_input and country_input:
    if st.button("Generate"):
        hotel_name_response = restaurant_input_chain.run(cuisine_input)
        st.write(f"**Suggested Restaurant Name:** {hotel_name_response}")

        menu_items_response = cusine_input_chain.run(cuisine=cuisine_input, state=state_input)
        st.write("**Suggested Menu Items for your restaurant:**")
        st.write(menu_items_response)
else:
    st.write("Please select country, state, and cuisine type to proceed.")