# 🤖 AI Agent with LangChain

This project demonstrates how to build an AI agent using the **LangChain** library, integrating three key tools:

1. **CryptoPriceFetcher** – Fetches the USD price of any cryptocurrency using the CoinGecko API.  
2. **ResumeQA** – Answers questions based on the content of PDF resumes in the `PDFs/` folder.  
3. **SQLProductQuery** – Executes SQL queries on a local SQLite database (`data.db`).

---

## Requirements

- Python 3.8 or higher  
- OpenAI API Key (saved in a `.env` file)  
- PDF resumes placed in the `PDFs/` folder  
- SQLite database file named `data.db`

---

## Installation

```bash
git clone https://github.com/your-username/ai-agent-langchain.git
cd ai-agent-langchain
pip install langchain-openai requests python-dotenv pymupdf
```

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

---

## Project Structure

```
.
├── ai_agent.py        # Main script
├── data.db            # SQLite database
├── PDFs/              # Folder containing PDF resumes
│   ├── resume1.pdf
│   └── resume2.pdf
└── .env               # Environment variables file (not committed to version control)
```

---

## Create the Database

```sql
-- Run this in terminal using: sqlite3 data.db
python create_db.py
```
## Setting Up the Python Virtual Environment

To keep your dependencies organized and avoid conflicts with other projects, it's recommended to use a virtual environment.

1. **Create the virtual environment**  
   In the root of your project folder, run:

   ```bash
   python -m venv venv
   ```

   This will create a folder called `venv/` with an isolated Python environment.

2. **Activate the virtual environment**

   On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

   On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

   You’ll know it worked if you see `(venv)` in your terminal prompt.

3. **Install project dependencies**

   After activation, run:

   ```bash
   pip install -r requirements.txt
   ```

   Or, if you don’t have a `requirements.txt` yet, install manually:

   ```bash
   pip install langchain langchain-openai requests python-dotenv pymupdf
   ```

4. **Freeze the current environment (optional)**  
   If you want to save your installed packages:

   ```bash
   pip freeze > requirements.txt
   ```

5. **Deactivate when done**

   ```bash
   deactivate
   ```

---

### .env File Setup

You’ll need a `.env` file to store your OpenAI API key:

Create a `.env` file in the root directory with this content:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

This file will be loaded by `python-dotenv` to set environment variables for the agent to authenticate with OpenAI.

> ⚠️ **Important:** Never commit your `.env` file to version control (e.g., GitHub).
Add it to your `.gitignore`:

```gitignore
.env
```
---

## Run the Script

```bash
py ai_agent.py
```

## Available Tools

| Tool Name            | Description                                                                                     |
|----------------------|-------------------------------------------------------------------------------------------------|
| `CryptoPriceFetcher` | Fetches the current USD price of a cryptocurrency via the CoinGecko API                        |
| `ResumeQA`           | Reads and analyzes PDF files from the `PDFs/` folder to answer custom questions                |
| `SQLProductQuery`    | Runs SQL queries on the `data.db` SQLite database                                               |

---

## Example Prompts

```text
--- API TOOL EXAMPLE ---
What is the price of cardano?

--- PDF TOOL EXAMPLE ---
Who is the most experienced candidate in Streamlit?

--- PDF TOOL EXAMPLE ---
Make a list of all candidates with: Name | Experience Time (years) | Level | Main Skills

--- DATABASE TOOL EXAMPLE ---
List the name and price of all products.

--- DATABASE TOOL EXAMPLE ---
Which product is the most expensive?
```

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for more details.
