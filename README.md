# Assignment 1: Build Your First Question Answering Agent
### Project Overview
This project implements a Financial Question Answering Agent from scratch using Python and the OpenAI Python SDK. The agent can provide real-time (mocked) stock prices and exchange rates using Function Calling and supports Parallel Tool Calls and Contextual Memory.

### Technical Stack
- **LLM Engine:** Groq (Llama-3.3-70b-versatile) - Used as an OpenAI-compatible API.
- **Language:** Python 3.10
- **Libraries:** `openai`, `python-dotenv`
- **Environment Management:** Conda

### Key Features & Implementation
- **Function Calling:** Implemented `get_stock_price` and `get_exchange_rate` with standardized mock data.
- **Structured Outputs:** Defined JSON schemas with "strict": true and "additionalProperties": false.
  - Note: While the schema follows the strict requirements, some compatible APIs (like Groq) may have limitations with the strict parameter; the code is structured to be 100% compliant with OpenAI's format.
- **Parallel Tool Calling:** The agent loop can handle multiple function calls in a single turn (e.g., comparing two stocks).
- **Conversation Memory:** Maintains a `messages` list to remember user information (e.g., name).
- **Security:** API keys are managed via `.env` and excluded from version control via `.gitignore`.

### Setup Instructions
1. Clone the repository
```
git clone https://github.com/ziling-huang2002/AI-Agent-Assignment1-Build-Your-First-Question-Answering-Agent-.git
cd https://github.com/ziling-huang2002/AI-Agent-Assignment1-Build-Your-First-Question-Answering-Agent-.git
```

2. Create Conda environment
```
conda create -n financial_agent python=3.10 -y
conda activate financial_agent
```
 
3. Install dependencies
```
pip install -r requirements.txt
```

4. Configure environment variables  
Create a `.env` file in the root directory
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Benchmark Task Demos  
Task A (Persona): Verified as "Financial Assistant".  
Task B (Single Tool): NVDA price returns 190.00.  
Task C (Parallel Tools): Simultaneous lookup for AAPL and TSLA.  
Task D (Memory): Successfully remembers user name.  
Task E (Error Handling): Gracefully handles unknown symbols (e.g., GOOG) with "Data not found".

### Demo Video
[Watch the Demo](https://www.youtube.com/watch?v=MCEw-hbgzpM&feature=youtu.be)
