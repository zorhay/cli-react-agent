# ReAct AI Agent

This project implements an AI agent based on the **ReAct (Reasoning and Acting)** framework. The agent is designed to solve complex problems by breaking them down into a series of thoughts and actions, creating a transparent and auditable reasoning process. It can interact with a variety of tools to gather information and provide well-supported answers to user queries.

This agent's behavior is guided by a detailed system prompt that includes **few-shot exemplars**. This technique demonstrates the desired reasoning process, enabling the agent to handle complex, multi-step queries with good accuracy.

## Requirements

- **Python**: `3.13`
- **Dependencies**: All required packages are listed in `requirements.txt`.

## Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/zorhay/cli-react-agent.git
cd cli-react-agent
```

### 2. Install Dependencies

It is highly recommended to use a virtual environment.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

### 3. Set Environment Variables

This project requires API keys for Google Gemini and Tavily Search. Create a `.env` file in the project root:

```
touch .env
```

Now, add your API keys to the `.env` file:

```env
# .env
GOOGLE_API_KEY="your-google-api-key"
TAVILY_API_KEY="your-tavily-api-key"
```

### 4. Run the CLI Application

Once the setup is complete, you can run the interactive CLI:

```bash
python main.py
```

## Model Suggestions

This implementation is optimized for and performs best with **`gemini-2.5-pro`**. It is also compatible with **`gemini-2.5-flash`**, which offers a balance between performance and cost. These models can be configured in the `src/config.py` file.

## Documentation

### Project Structure

The project is organized into several key modules, each with a distinct responsibility:

```
cli-react-ai-agent/
├── main.py                # Main entry point for the application
├── requirements.txt         # Project dependencies
├── .env.example           # Example environment file
├── src/
│   ├── agent/             # Core agent logic
│   │   ├── agent.py       # Agent initialization and configuration
│   │   ├── prompt.py      # System prompt defining the agent's behavior
│   │   ├── store.py       # In-memory vector store for the agent (semantic search is configured)
│   │   └── tools/         # Directory for all agent tools
│   │       ├── __init__.py
│   │       ├── calculator.py
│   │       ├── store_wrapper.py
│   │       ├── web_reader.py
│   │       ├── web_search.py
│   │       └── wikipedia.py
│   ├── cli/               # Command-line interface components
│   │   ├── chat_session.py # Manages the interactive chat loop
│   │   ├── console.py     # Main console application class
│   │   ├── menu.py        # Main menu for the CLI
│   │   └── static.py      # Static text used in the CLI
│   ├── stream/            # Handles streaming and parsing of agent output
│   │   └── parser.py      # Parses agent messages into a structured format
│   └── config.py          # Application configuration settings
└── venv/                  # Virtual environment directory
```

### Module Explanations

-   **`src/agent`**: Contains the core logic for the ReAct agent, including its initialization, system prompt, and the tools it can use. The prompt now includes few-shot examples to guide the agent's reasoning.
-   **`src/cli`**: Manages the user-facing command-line interface, including menus, prompts, and the chat session display.
-   **`src/stream`**: Responsible for parsing the raw output stream from the agent and converting it into a structured format that the CLI can render.
-   **`src/config.py`**: Defines the configuration for the agent, such as the language model, temperature, and embedding models.
-   **`main.py`**: The main script that initializes and runs the agent and the CLI.

### Tools

The agent has access to a variety of tools to gather and process information:

-   **`search_web(query: str)`**: Searches the web for up-to-date information.
-   **`search_wikipedia(query: str)`**: Looks up topics on Wikipedia for encyclopedic knowledge.
-   **`read_web_page(url: str)`**: Reads the full text content from a URL, useful for parsing content from archive.org.
-   **`calculate(expression: str)`**: Evaluates mathematical expressions.
-   **`list_namespaces()`**: Lists all available data namespaces in the agent's memory.
-   **`search(namespace_prefix: list, query: str)`**: Searches for information within a given namespace in the agent's memory.
-   **`put(namespace: list, key: str, value: dict)`**: Stores a key-value pair in the agent's memory.
-   **`get(namespace: list, key: str)`**: Retrieves a value from the agent's memory using its exact key.

### How to Use the Agent

This project is designed to be run as an interactive CLI script. The agent's reasoning loop concludes when it has gathered enough information to answer the question, at which point it provides the answer.

```python
from src.agent import init_agent
from src.config import agent_settings

agent = init_agent(agent_settings)  # agent initialization
res = agent.invoke({'messages': [{'role': 'user', 'content': 'How old is Noam Chomsky?'}]})  # query the agent

for r in res['messages']:  # printing the result
    r.pretty_print()
```

## Example Runs

The agent's reasoning is guided by few-shot examples in its prompt. Here is one such example to illustrate its process:

**Example 1**
```
Question: What is the name of the actor who starred alongside Brendan Gleeson in a film about two hitmen hiding in a small town?

THOUGHT: I need to identify the co-star of Brendan Gleeson in a film about two hitmen in a small town. I believe the film is "In Bruges" and will search for its cast to confirm and find the other actor, then draw a conclusion.
ACTION: search_web: {'query': 'actors in film with Brendan Gleeson two hitmen small town'}
OBSERVATION: [Large search log]
THOUGHT: The search results consistently point to the movie "In Bruges". The summaries mention that the film stars Brendan Gleeson and Colin Farrell as two hitmen hiding in Bruges, Belgium.
Final Answer:: The movie is "In Bruges" and the actor who starred alongside Brendan Gleeson is Colin Farrell.
```

**Example 2**
```
Question: What is the difference in height between the highest and third-highest peaks of the Armenian Highlands?

THOUGHT: I need to find the highest and third-highest peaks of the Armenian Highlands and then calculate the difference in their heights. I will start by searching for a list of the highest peaks in the Armenian Highlands.                                                                                                                                                          
ACTION: search_web: {'query': 'highest peaks of the Armenian Highlands'}                                                                                                            
OBSERVATION: [Large search log: just websites provide]
        "https://www.armgeo.am/en/the-5-highest-summits-of-armenian-highland/"
        "https://en.wikipedia.org/wiki/Armenian_highlands"
        "https://www.armgeo.am/en/the-highest-peaks-of-all-regions-of-armenia/"
        "https://thecascadetravel.com/blog/highest-mountains-to-hike-in-amenia/"
        "https://en.wikipedia.org/wiki/Mountains_of_Armenia"                                                 
THOUGHT: I have identified the highest and third-highest peaks of the Armenian Highlands from a reliable source. The highest peak is Masis at 5165m, and the third-highest is Jilo at 4168m. My next step is to calculate the difference in their heights.                                                                                                                               
ACTION: calculate: {'expression': '5165 - 4168'}                                                                                                                                    
OBSERVATION: 997                                                                                                                                                                    
THOUGHT: I have identified the highest and third-highest peaks of the Armenian Highlands and calculated the difference in their heights. The highest peak is Mount Masis (5165m) and the third highest is Mount Jilo (4168m). The difference is 997m. I will now store this information and provide the final answer.                                                                  
ACTION: put: {                                                                                                                                                                                                     
             "namespace": ["user_data", "facts"],                                                                                                                                                                
             "key": "height_difference_armenian_highlands",                                                                                                                                                      
             "value": {                                                                                                                                                                                          
               "highest_peak": {                                                                                                                                                                                 
                 "name": "Mount Masis",                                                                                                                                                                          
                 "height": 5165                                                                                                                                                                                  
               },                                                                                                                                                                                                
               "third_highest_peak": {                                                                                                                                                                           
                 "name": "Mount Jilo",                                                                                                                                                                           
                 "height": 4168                                                                                                                                                                                  
               },                                                                                                                                                                                                
               "difference_in_height": 997                                                                                                                                                                       
             }                                                                                                                                                                                                   
           }                                                                                                                
OBSERVATION: null
Final Answer: The difference in height between the highest peak of the Armenian Highlands, Mount Masis (5165m), and the third-highest peak, Mount Jilo (4168m), is 997 meters.
```

---

*A note on configuration: Some settings are currently hardcoded. For more advanced use cases, these could be migrated to a more robust configuration system to improve flexibility.* 