from fasthtml.common import *
from starlette.requests import Request
from monsterui.all import *
import requests
from typing import Dict, Any
import json

# Get frankenui and tailwind headers via CDN
hdrs = Theme.blue.headers()

# Initialize the app
app, rt = fast_app(hdrs=hdrs)

# Agent configurations
AGENT_CONFIGS = {
    "Alpaca Trader": {"streaming": False, "url": "https://alpaca-agent.fly.dev"},
    "CEX Aggregator": {"streaming": False, "url": "https://cex-aggregator-agent.fly.dev"},
    "Polymarket Agent": {"streaming": True, "url": "https://zuvu-polymarket-agent.fly.dev"},
    "NewsX": {"streaming": False, "url": "https://x-posting-agent.fly.dev"}
}

# Example questions for each agent
EXAMPLE_QUESTIONS = {
    "Alpaca Trader": [
        "What can you help me with?",
        "Back test trend following for TSLA last week",
        "Show me my account information",
        "Show me my current positions",
        "Place a market order to buy 1 share of INTL",
        "Place a limit order to buy 1 share of AAPL at $150"
    ],
    "CEX Aggregator": [
        "What exchanges are available?",
        "Show me my balance on Binance",
        "What is the price of BTC/USDC on Bybit?",
        "Show me arbitrage opportunities for BTC/USDC between Binance and Bybit",
        "Run a mean reversion backtest for BTC/USDT on Binance",
        "Run a trend following backtest for ETH/USDT on Bybit"
    ],
    "Polymarket Agent": [
        "What can you help me with?",
        "What markets are available on Polymarket right now?",
        "Tell me about upcoming election markets",
        "Show me market with most volume and liquidity",
        "Show me the markets ending today"
    ],
    "NewsX": []
}

def send_message(message: str, endpoint_url: str, selected_endpoint: str) -> Dict[Any, Any]:
    """Send message to the selected API endpoint"""
    streaming = AGENT_CONFIGS[selected_endpoint]["streaming"]
    
    if selected_endpoint == "Polymarket Agent":
        payload = {"input": message}
    else:
        payload = {
            "input": message,
            "history": [],
            "config": {
                "streaming": streaming,
                "thread_id": "test_thread"
            }
        }
    
    try:
        response = requests.post(endpoint_url + "/chat", json=payload, stream=streaming)
        response.raise_for_status()
        
        if streaming:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            content = line_str[6:]
                            if content.strip():
                                full_response += content
                    except Exception as e:
                        return {"response": f"Error processing response: {str(e)}"}
            
            if not full_response:
                return {"response": "Error: No response received from the server"}
                
            return {"response": full_response}
        else:
            return response.json()
            
    except requests.exceptions.RequestException as e:
        return {"response": f"Error: Failed to get response from the server - {str(e)}"}

def ChatMessage(role: str, content: str):
    """Render a chat message with appropriate styling"""
    return Div(
        cls="p-4 rounded-lg mb-4 " + 
            ("bg-blue-100" if role == "user" else "bg-gray-100"),
        children=[
            P(cls="font-bold", children=[role.capitalize()]),
            P(cls="mt-2", children=[content])
        ]
    )

def ExampleQuestionButton(question: str, selected_endpoint: str):
    """Render an example question button"""
    return Button(
        question,
        cls=(ButtonT.secondary, "w-full mb-2"),
        hx_post="/chat",
        hx_vals=json.dumps({
            "message": question,
            "endpoint": selected_endpoint
        }),
        hx_target="#chat-messages",
        hx_swap="beforeend"
    )

@rt
def index():
    return Titled(
        "🤖 Agentic AI Demo",
        Grid(
            # Sidebar
            Div(
                H3("Select Agent", cls="mb-4"),
                *[
                    Button(
                        agent,
                        cls=(ButtonT.primary if agent == "Alpaca Trader" else ButtonT.secondary, "w-full mb-2"),
                        hx_get=f"/select-agent/{agent}",
                        hx_target="#agent-content"
                    )
                    for agent in AGENT_CONFIGS.keys()
                ],
                Hr(cls="my-4"),
                Button(
                    "🔄 Refresh Chat",
                    cls=(ButtonT.secondary, "w-full"),
                    hx_get="/refresh-chat",
                    hx_target="#chat-messages"
                ),
                id="agent-content"
            ),
            # Main chat area
            Div(
                Div(
                    ChatMessage("assistant", "Hello! How can I help you today?"),
                    id="chat-messages"
                ),
                Form(
                    Input(
                        type="text",
                        name="message",
                        placeholder="What would you like to know?",
                        cls="flex-1"
                    ),
                    Button("Send", cls=ButtonT.primary),
                    hx_post="/chat",
                    hx_target="#chat-messages",
                    hx_swap="beforeend"
                ),
                Div(
                    H3("Example Questions", cls="mb-4"),
                    Grid(
                        *[ExampleQuestionButton(q, "Alpaca Trader") for q in EXAMPLE_QUESTIONS["Alpaca Trader"][:6]],
                        cols_lg=3
                    )
                )
            ),
            cols_lg=2
        )
    )

@rt
async def chat(request: Request):
    form = await request.form()
    message = form.get("message")
    endpoint = form.get("endpoint", "Alpaca Trader")
    user_message = ChatMessage("user", message)
    response = send_message(
        message,
        AGENT_CONFIGS[endpoint]["url"],
        endpoint
    )
    assistant_message = ChatMessage("assistant", response.get("response", "Error: No response"))
    return user_message + assistant_message

@rt
def select_agent(request: Request, agent_name: str):
    return Div(
        H2(f"🤖 {agent_name}", cls="mb-4"),
        Grid(
            *[ExampleQuestionButton(q, agent_name) for q in EXAMPLE_QUESTIONS[agent_name][:6]],
            cols_lg=3
        ),
        id="agent-content"
    )

@rt
def refresh_chat(request: Request):
    return Div(
        ChatMessage("assistant", "Chat refreshed. How can I help you?"),
        id="chat-messages"
    )

if __name__ == '__main__':
    serve() 