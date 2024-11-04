# Cold Referral Generator

## Overview

**Cold Referral Generator** is an end-to-end tool that generates personalized referral messages to enhance networking and outreach efforts. Built with **Llama 3.1** (an open-source Large Language Model), **ChromaDB** (vector store for efficient data retrieval), **LangChain** (for orchestrating LLM interactions), and **Streamlit** (for a user-friendly interface), this project automates the process of creating high-quality referral messages tailored to your contacts and context.

## Installation

### Prerequisites

- Python 3.x
- [Other dependencies as needed]

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cold-referral-generator.git
   cd cold-referral-generator
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Streamlit App**:

   ```bash
   streamlit run app.py
   ```

2. **Enter Input**: Provide details about the contact and desired referral.

3. **Generate Referral**: The tool will generate a personalized cold referral message, which you can further edit as needed.

## Configuration

- **ChromaDB**: Set up ChromaDB for vector storage by updating the `config.py` file.
- **Llama 3.1 and LangChain**: Configure model details and LangChain parameters to optimize referral generation.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

