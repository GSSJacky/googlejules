# Aroma Agent Project

## Overview

This project aims to develop an AI agent that provides personalized aroma suggestions. The agent takes user input regarding their mood or scent preferences (potentially in multiple languages) and suggests combinations of common household plants and preparation methods. If suitable plant-based options are not readily identifiable, it may suggest types of commercially available fragrance products.

The agent is designed to leverage information from sources like FlavorDB, user reviews of scents, and traditional botanical knowledge (e.g., from TCM databases). Interaction with a language model like Gemini is intended for input interpretation and suggestion generation.

## Current Status

This project includes two versions of the Aroma Agent:

1.  **Basic Agent (`src/agent.py` & `src/main.py`)**:
    *   A simpler version that uses `MockGeminiClient` and `DataLoader` with mock/simulated data.
    *   Provides a basic demonstration of suggestion logic.
    *   Launched via `python src/main.py`, which now guides users to the advanced agent.

2.  **Advanced Agent (`src/aroma_agent_advanced.py`)**:
    *   Uses `MockGeminiClient` and demonstrates a more sophisticated multi-step reasoning process:
        1.  **Intent Extraction**: User input is parsed into a structured context (mood, preferences, etc.) by the mock LLM.
        2.  **Local Candidate Search**: Data from local CSV files (`compounds_summary.csv`, `herb_flavordb_mapping.csv`) is searched for candidate aroma molecules and herbs based on extracted preferences. This step uses the `pandas` library.
        3.  **LLM-powered Recommendation**: The mock LLM "judges" these candidates against the user's full intent to generate a final, reasoned recommendation, potentially including commercial products if local matches are insufficient.
    *   Launched via the command line with a query.

Key components include:

*   **`src/agent.py`**: Defines the `AromaAgent` class for the basic demo (now mostly for reference).
*   **`src/main.py`**: Entry point that now directs users to the advanced agent script.
*   **`src/aroma_agent_advanced.py`**: The primary script for the advanced, multi-step agent with its own command-line interface.
*   **`src/utils/gemini_client.py`**: Contains `MockGeminiClient` to simulate LLM responses for both intent extraction and final recommendation.
*   **`src/utils/data_loader.py`**: Includes `DataLoader` for the basic agent's mock data (less relevant for the advanced agent).
*   **`src/compounds_summary.csv`**: Sample CSV data about aroma compounds, used by the advanced agent.
*   **`src/herb_flavordb_mapping.csv`**: Sample CSV data mapping herbs to compounds, used by the advanced agent.

## Running the Demos

### Basic Agent
The basic agent is now primarily for reference. Running `python src/main.py` will provide instructions to use the advanced agent.

### Advanced Agent Demo

1.  Ensure you are in the `aroma_agent` directory (the root of this project).
2.  **Dependency**: The advanced agent (`aroma_agent_advanced.py`) uses the `pandas` library. If you haven't already, install it:
    ```bash
    pip install pandas
    ```
3.  Execute the `aroma_agent_advanced.py` script with a `--query` argument. The query should be a string describing the user's need.
    Examples:
    ```bash
    python src/aroma_agent_advanced.py --query "I'm feeling stressed and need to relax, maybe something floral."
    ```
    ```bash
    python src/aroma_agent_advanced.py --query "我感到压力很大，需要放松"
    ```
    ```bash
    python src/aroma_agent_advanced.py --query "Quero um aroma energizante para começar o dia."
    ```
    The script will print the structured intent (as interpreted by the mock LLM), any matched candidates from local data, and the final suggestion.

## Project Structure

```
aroma_agent/
├── data/                 # Placeholder for future actual data files (currently unused)
│   └── .gitkeep
├── src/                  # Source code
│   ├── __init__.py
│   ├── agent.py          # Core agent logic (basic, for reference)
│   ├── aroma_agent_advanced.py # Advanced agent logic and CLI
│   ├── compounds_summary.csv   # Sample data for advanced agent
│   ├── herb_flavordb_mapping.csv # Sample data for advanced agent
│   ├── main.py           # Main entry point, directs to advanced agent
│   └── utils/            # Utility modules
│       ├── __init__.py
│       ├── data_loader.py # Mock data loading (for basic agent)
│       └── gemini_client.py # Mock Gemini client (used by advanced agent)
└── README.md             # This file
```

## Next Steps (Conceptual)

*   Integrate with a real Gemini API.
*   For `aroma_agent_advanced.py`:
    *   Refine the prompts for intent extraction and recommendation generation.
    *   Improve the scoring and candidate selection logic in `search_candidates`.
    *   Expand the local datasets (`compounds_summary.csv`, `herb_flavordb_mapping.csv`) with more comprehensive information.
*   Consider replacing mock CSVs with a more robust data storage/querying solution if data grows.
*   Expand language support for user inputs more robustly within the LLM prompts.
*   Structure the project according to Google ADK framework guidelines if/when available.
*   Add comprehensive unit and integration tests for each step of the advanced agent.
```
