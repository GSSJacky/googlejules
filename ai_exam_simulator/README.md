# AI Exam Simulator 🎓

## Project Description

This project simulates an examination environment using AI agents built with a conceptual Google ADK framework and powered by Google Gemini (currently using placeholder implementations). It features:

*   **Candidate Agents:** AI agents that generate answers to exam questions.
*   **Examiner Agents:** AI agents that evaluate the candidates' answers, provide scores, qualitative feedback, and suggestions for improvement.
*   **Question Bank:** Ability to use a collection of questions (currently from a sample JSON file).

The goal is to explore the capabilities of LLMs in reasoning, learning, and teaching, demonstrating agents in dual roles.

## Project Structure

```
ai_exam_simulator/
├── agents/                 # Contains agent definitions
│   ├── __init__.py
│   ├── candidate_agent.py  # Logic for agent answering questions
│   └── examiner_agent.py   # Logic for agent evaluating answers
├── core/                   # Core components like the Gemini client
│   ├── __init__.py
│   └── gemini_client.py    # Placeholder for Gemini API interaction
├── questions/              # Stores question bank files
│   ├── __init__.py
│   └── sample_questions.json # Sample questions for the simulation
├── results/                # Default directory for storing simulation results
│   └── __init__.py
├── simulations/            # Scripts to run simulations
│   ├── __init__.py
│   └── run_simulation.py   # Main script to orchestrate the exam simulation
├── tests/                  # Unit and integration tests
│   ├── __init__.py
│   ├── test_candidate_agent.py
│   └── test_examiner_agent.py
└── README.md               # This file
```

## Setup

Currently, the project uses standard Python libraries. No external package installations are strictly required to run the placeholder version.

If you were to connect to the actual Google Gemini API, you would need to install the appropriate Google client libraries:

```bash
# Example:
# pip install google-generativeai
```

Ensure your Python environment is set up to resolve imports from the `ai_exam_simulator` root directory.

## How to Run a Simulation

1.  Navigate to the root directory of the project (`ai_exam_simulator`).
2.  You can run the simulation using the Python module execution option:

    ```bash
    python -m simulations.run_simulation
    ```

    Alternatively, if your `PYTHONPATH` includes the project's parent directory, you might be able to run:

    ```bash
    python ai_exam_simulator/simulations/run_simulation.py
    ```
    
    The first method is generally more robust for package-like structures.

3.  The simulation will:
    *   Load questions from `questions/sample_questions.json`.
    *   Instantiate Candidate Agents to answer these questions.
    *   Instantiate Examiner Agents to evaluate the answers.
    *   Print progress to the console.
    *   Save a detailed JSON report of the simulation in the `results/` directory, named with a timestamp (e.g., `simulation_results_YYYYMMDD_HHMMSS.json`).

## How to Run Tests

1.  Navigate to the root directory of the project (`ai_exam_simulator`).
2.  To run all tests discovered in the `tests` directory:

    ```bash
    python -m unittest discover -s tests -p "test_*.py"
    ```
    (If your project root `ai_exam_simulator` is not directly in PYTHONPATH, you might need to run from one level up: `python -m unittest discover -s ai_exam_simulator/tests -p "test_*.py"`)

3.  To run a specific test file:

    ```bash
    python -m unittest tests.test_candidate_agent
    python -m unittest tests.test_examiner_agent
    ```

## Further Development Ideas

*   Integrate with a real Gemini API.
*   Expand the question bank and support different formats.
*   Implement more sophisticated agent behaviors and personas.
*   Develop a web interface for easier interaction.
*   Add more detailed analytics of agent performance.
*   Allow configuration of different LLM models for agents.
