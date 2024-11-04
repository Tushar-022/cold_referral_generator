import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Custom web loader function to replace WebBaseLoader
def custom_web_loader(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        page_content = soup.get_text(separator=" ")  # Extracts all text with space as separator
        return page_content
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching content: {e}")
        return None

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("🤝🏻 Referral Request Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.apple.com/en-us/details/200554363/machine-learning-ai-internships")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Fetch data from the URL using the custom web loader
            data = custom_web_loader(url_input)
            
            # Check if data is loaded
            if not data:
                st.error("No content found at the provided URL.")
                return
            
            # Clean the text using the provided clean_text function
            data = clean_text(data)
            portfolio.load_portfolio()
            
            # Extract jobs and check if any jobs are found
            jobs = llm.extract_jobs(data)
            if not jobs:
                st.error("No job postings found in the extracted data.")
                return

            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                
                # Verify that there are links to include in the email
                if not links:
                    st.error("No portfolio links found for the required skills.")
                    return
                
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
                
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    # Initialize instances of Chain and Portfolio
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Referral Generator", page_icon="🤝🏻")
    create_streamlit_app(chain, portfolio, clean_text)
