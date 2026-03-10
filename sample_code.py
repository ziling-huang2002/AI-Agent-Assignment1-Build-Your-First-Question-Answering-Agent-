import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Setup & Security
# Make sure you have a .env file with GROQ_API_KEY=sk-...
load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), 
                base_url="https://api.groq.com/openai/v1")

# 2. Mock Functions (Reference for your Financial Functions)
def get_stock_price(symbol):
    """Mock function to get stock price."""
    print(f"[Mock] Getting stock price for {symbol}...")
    # In your assignment, you will look up Stock data here
    mock_prices = {
        "AAPL": {"symbol": "AAPL", "price": "260.00"},
        "TSLA": {"symbol": "TSLA", "price": "430.00"},
        "NVDA": {"symbol": "NVDA", "price": "190.00"}
    }
    if symbol.upper() in mock_prices:
        return json.dumps(mock_prices[symbol.upper()])
    else:
        return json.dumps({"error": "Data not found"})

def get_exchange_rate(currency_pair: str):
    """Mock function to get exchange rate."""
    print(f"[Mock] Getting exchange rate for {currency_pair}...")
    # In your assignment, you will look up exchange rate data here
    mock_rates = {
        "USD_TWD": {"currency_pair": "USD_TWD", "rate": 32.0},
        "JPY_TWD": {"currency_pair": "JPY_TWD", "rate": 0.2},
        "EUR_USD": {"currency_pair": "EUR_USD", "rate": 1.2}
    }
    if currency_pair.upper() in mock_rates:
        return json.dumps(mock_rates[currency_pair.upper()])
    else:
        return json.dumps({"error": "Data not found"})

# 3. Function Map (CRITICAL: Use this pattern)
# This allows dynamic execution without if-else chains
available_functions = {
    "get_stock_price": get_stock_price,
    "get_exchange_rate": get_exchange_rate,
}

# 4. Tool Schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get current stock price for a given symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL, TSLA, NVDA)"}
                },
                "required": ["symbol"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get current exchange rate for a currency pair",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_pair": {"type": "string", "description": "Currency pair (e.g., USD_TWD, EUR_USD, JPY_TWD)"}
                },
                "required": ["currency_pair"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

def run_agent():
    # 5. System Prompt (Persona)
    messages = [
        {"role": "system", "content": "You are a Financial Assistant. Use tools to look up information. "
            "If the user asks for an exchange rate, return ONLY the numerical rate (e.g., '32.0') "
            "or a very short sentence including the rate. "
            "If a tool returns 'Data not found', say 'Data not found'. "
            "When comparing stock prices, show the individual prices first, then the comparison. "
            "Do not guess or suggest other symbols."}
    ]
    
    print("Agent Started. Type 'exit' to quit.")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        messages.append({"role": "user", "content": user_input})

        # First API Call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Use a model that supports tool calls
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_msg = response.choices[0].message
        tool_calls = response_msg.tool_calls

        if tool_calls:
            # IMPORTANT: Add the assistant's "thought" (tool call request) to history
            messages.append(response_msg)
            
            # 6. Handle Parallel Tool Calls
            # The model might call multiple tools in one go (e.g. "Time in Taipei and NY")
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Dynamic Dispatch using Function Map
                function_to_call = available_functions.get(function_name)
                
                if function_to_call:
                    try:
                        tool_result = function_to_call(**function_args)
                    except Exception as e:
                        tool_result = json.dumps({"error": str(e)})
                else:
                    tool_result = json.dumps({"error": "Function not found"})
                
                # Append RESULT to history
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_result,
                })
            
            # Second API Call (Get final answer)
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            final_content = final_response.choices[0].message.content
            print(f"Agent: {final_content}")
            messages.append({"role": "assistant", "content": final_content})
            
        else:
            # No tool needed
            print(f"Agent: {response_msg.content}")
            messages.append({"role": "assistant", "content": response_msg.content})

        print()

if __name__ == "__main__":
    run_agent()