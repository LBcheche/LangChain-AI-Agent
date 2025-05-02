# INSTALL: pip install langchain-openai requests python-dotenv pymupdf


from langchain_openai import ChatOpenAI # Import the ChatOpenAI class to interact with OpenAI’s chat-based models
from langchain.agents import initialize_agent, AgentType # Import functions to initialize an agent and specify its type
from langchain.tools import Tool # Import the Tool wrapper to turn Python functions into LangChain tools
import requests, sqlite3, os # Import the requests library for HTTP requests, sqlite3 for database access, and os for environment operations
from dotenv import load_dotenv # Import load_dotenv to load environment variables from a .env file
import fitz  # Import PyMuPDF (fitz) to read text from PDF files


load_dotenv() # Load environment variables from a .env file into the process’s environment
os.environ["OPENAI_API_KEY"] # Ensure the OPENAI_API_KEY environment variable is set for API authentication

# Instantiate the ChatOpenAI language model with a specific model and deterministic output
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# TOOL 1: Define a function to fetch the USD price of a cryptocurrency via CoinGecko API
def get_crypto_price(crypto: str) -> str:
    # Build the API URL with the specified cryptocurrency ID
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    # Send a GET request to the CoinGecko API
    res = requests.get(url)
    print(res.json)
    # If the response is successful (HTTP 200), parse the JSON for the USD price
    if res.status_code == 200:
        price = res.json().get(crypto, {}).get("usd", "not found")
        # Return a formatted string with the price
        return f"The price of {crypto} is ${price} USD."
    # If the request failed, return an error message
    return "Failed to access the API."

# Wrap the get_crypto_price function as a LangChain tool named “CryptoPriceFetcher”
api_tool = Tool.from_function(
    name="CryptoPriceFetcher",
    description=(
        "Uses an API to fetch the current price of a cryptocurrency."
        "Example: bitcoin, ethereum. Answer with just the number: $0.00001 USD"
    ),
    func=get_crypto_price
)

# TOOL 2: Define a function to answer questions based on all resumes (PDFs) in the 'PDFs/' folder
def ask_about_resumes(question: str) -> str:
    # Set the folder path containing PDF resumes
    folder_path = "PDFs"
    # Initialize an empty string to accumulate all extracted text
    corpus = ""
    # Iterate over each file in the specified folder
    for filename in os.listdir(folder_path):
        # Process only PDF files (case-insensitive check)
        if filename.lower().endswith(".pdf"):
            # Open the PDF file with PyMuPDF
            with fitz.open(os.path.join(folder_path, filename)) as doc:
                # Extract text from each page and append to the corpus
                corpus += "".join(page.get_text() for page in doc)
    # If no text was extracted, inform the user
    if not corpus.strip():
        return "No text could be extracted from the resumes."
    try:
        # Use the language model to answer the question based on the combined resume text
        return llm.invoke(
            f"Based on the following resumes:\n\n{corpus}\n\nAnswer this question: {question}"
        )
    except Exception as e:
        # If an error occurs, return the exception message
        return f"Error processing CVs: {str(e)}"

# Wrap the ask_about_resumes function as a LangChain tool named “ResumeQA”
resume_tool = Tool.from_function(
    name="ResumeQA",
    description=(
        "Answer any question based on the content of CVs located in the 'PDFs/' folder. "
        "You can answer about skills, experiences, technologies, or candidate profiles."
    ),
    func=ask_about_resumes
)

# TOOL 3: Define a function to run arbitrary SQL queries against a SQLite database
def query_products(sql: str) -> str:
    try:
        # Connect to the SQLite database file “data.db”
        with sqlite3.connect("data.db") as conn:
            # Execute the provided SQL query
            cursor = conn.execute(sql)
            # Fetch all resulting rows
            rows = cursor.fetchall()
        # Return the rows as a string, or indicate no data was found
        return str(rows) if rows else "No data found."
    except Exception as e:
        # Return an error message if the query fails
        return f"Query error: {str(e)}"

# Wrap the query_products function as a LangChain tool named “SQLProductQuery”
db_tool = Tool.from_function(
    name="SQLProductQuery",
    description="Run SQL queries on a SQLite database. Example: SELECT name, price FROM products;",
    func=query_products
)

# Initialize the LangChain agent with the three tools defined above
tools = [api_tool, resume_tool, db_tool]
agent = initialize_agent(
    tools=tools,                                  # List of tools available to the agent
    llm=llm,                                      # Language model instance
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent reasoning strategy
    verbose=False                                 # Disable verbose logging
)

# Define example prompts to demonstrate each tool’s usage
examples = [
    ("\n--- API TOOL EXAMPLE ---\n", "What's the current price of cardano?"),
    ("\n--- PDF TOOL EXAMPLE ---\n", 
     "What is the name of the most experienced professional in Streamlit? "),
    ("\n--- PDF TOOL EXAMPLE ---\n",
    "Make a list of all professionals and order by experience time?.\n "
    "The list must contain Name, Time Of Experience (years), "
    "Level (Specialist, Senior, Mid-level, Junior) and Main Skills.\n "
    "Show the list in a formatted table like excel with rows and cols. "
    ),
    ("\n--- DATABASE TOOL EXAMPLE ---\n", "List the name and price of all products in the products table. "
    "Show the list in a formatted table"),
    ("\n--- DATABASE TOOL EXAMPLE ---\n", "Which one is the most expensive product?")
]

# Iterate over each example: print the header, invoke the agent, and display the response
for header, prompt in examples:
    print(header)
    response = agent.invoke(prompt)
    print(response["input"] + "\n")
    print(response["output"])
