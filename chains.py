import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `company`, `role`, `experience`, `skills`, and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Tushar Khandelwal, a final-year Information & Technology student at NIT Jalandhar, with a strong passion for algorithmic problem-solving, data structures, and full-stack development. Tushar ranks among the top 0.01% of programmers in India, securing a top 100 spot in HackWithInfy, Infosys's national hackathon. 

            Write an email draft to X for a referral for the {role} role at {company}. Make it conversational and direct, without a formal tone. Limit the text to under 400 words. 

            Here are links to Tushar's portfolio: {links}, and here's the link to his CV: [https://drive.google.com/file/d/1_FSLJ3F3dLoG5wubVwDC1jwAd9Hu6PoG/view].

            ### LINKEDIN REFERRAL REQUEST (NO PREAMBLE):
            """
        )
        
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job.get('description', '')),
            "role": job.get('role', 'unspecified role'),
            "company": job.get('company', 'the company'),
            "links": links
        })
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
