# import streamlit as st
# from langchain_community.document_loaders import WebBaseLoader
# from chains import Chain
# from portfolio import Portfolio
# from utils import clean_text

# def create_streamlit_app(llm, portfolio, clean_text):
#     st.title("🤝🏻 Referral Request Generator")
#     url_input = st.text_input("Enter a URL:", value="https://www.amazon.jobs/en/jobs/2750545/sde-i-intern-6m-july-dec")
#     submit_button = st.button("Submit")

#     if submit_button:
#         try:
#             loader = WebBaseLoader([url_input])
#             loaded_data = loader.load()
            
#             # Check if data is loaded
#             if not loaded_data:
#                 st.error("No content found at the provided URL.")
#                 return
            
#             data = clean_text(loaded_data.pop().page_content)
#             portfolio.load_portfolio()
            
#             # Extract jobs and check if any jobs are found
#             jobs = llm.extract_jobs(data)
#             if not jobs:
#                 st.error("No job postings found in the extracted data.")
#                 return

#             for job in jobs:
#                 skills = job.get('skills', [])
#                 links = portfolio.query_links(skills)
#                 email = llm.write_mail(job, links)
#                 st.code(email, language='markdown')
                
#         except Exception as e:
#             st.error(f"An Error Occurred: {e}")

# if __name__ == "__main__":
#     chain = Chain()
#     portfolio = Portfolio()
#     st.set_page_config(layout="wide", page_title="Cold Referral Generator", page_icon="🤝🏻")
#     create_streamlit_app(chain, portfolio, clean_text)

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("🤝🏻 Referral Request Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.amazon.jobs/en/jobs/2750545/sde-i-intern-6m-july-dec")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            loaded_data = loader.load()
            
            # Check if data is loaded
            if not loaded_data:
                st.error("No content found at the provided URL.")
                return
            
            data = clean_text(loaded_data.pop().page_content)
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
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Referral Generator", page_icon="🤝🏻")
    create_streamlit_app(chain, portfolio, clean_text)
