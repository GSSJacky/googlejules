import json
import os
import datetime

# Adjust import paths based on your project structure.
# This assumes 'ai_exam_simulator' is in the Python path or script is run from project root.
from ai_exam_simulator.core.gemini_client import GeminiClient
from ai_exam_simulator.agents.candidate_agent import CandidateAgent
from ai_exam_simulator.agents.examiner_agent import ExaminerAgent

def load_questions(filepath: str) -> list:
    """Loads questions from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Question file not found at {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return []

def save_results(results: dict, output_dir: str = "../results"):
    """Saves the simulation results to a JSON file in the specified directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    results_filename = f"simulation_results_{timestamp}.json"
    filepath = os.path.join(output_dir, results_filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {filepath}")
    except IOError:
        print(f"Error: Could not write results to {filepath}")

def run_simulation():
    print("Starting AI Exam Simulation...")

    # --- Configuration ---
    # Relative path from run_simulation.py to the questions file
    questions_filepath = os.path.join(os.path.dirname(__file__), "../questions/sample_questions.json")
    # Relative path from run_simulation.py to the results directory
    results_output_dir = os.path.join(os.path.dirname(__file__), "../results")

    num_candidate_agents = 2 # Let's simulate with 2 candidates
    num_examiner_agents = 1  # And 1 examiner (can be expanded)

    # --- Initialize Gemini Client (using placeholder) ---
    # In a real scenario, you might pass an API key here
    gemini_client = GeminiClient() 

    # --- Load Questions ---
    questions = load_questions(questions_filepath)
    if not questions:
        print("No questions loaded. Exiting simulation.")
        return

    print(f"Loaded {len(questions)} questions.")

    # --- Instantiate Candidate Agents ---
    candidate_agents = [
        CandidateAgent(agent_id=f"candidate_{i+1}", gemini_client=gemini_client)
        for i in range(num_candidate_agents)
    ]
    print(f"Initialized {len(candidate_agents)} candidate agents.")

    # --- Candidate Agents Answer Questions ---
    all_submitted_answers = []
    print("\n--- Candidates Answering ---")
    for question in questions:
        print(f"Processing Question ID: {question['id']} - '{question['question_text'][:50]}...'")
        for candidate in candidate_agents:
            print(f"  Agent {candidate.agent_id} is answering...")
            submitted_answer = candidate.answer_question(
                question_id=question['id'],
                question_text=question['question_text']
            )
            all_submitted_answers.append({
                "question_id": question['id'],
                "question_text": question['question_text'],
                "model_answer_text": question.get('model_answer'), # Include model answer for examiner
                "agent_id": candidate.agent_id,
                "answer_text": submitted_answer['answer_text'] # Extract text from dict
            })
            print(f"    Agent {candidate.agent_id} answered.")
    
    print(f"\nTotal submitted answers: {len(all_submitted_answers)}")

    # --- Instantiate Examiner Agents ---
    examiner_agents = [
        ExaminerAgent(agent_id=f"examiner_{i+1}", gemini_client=gemini_client)
        for i in range(num_examiner_agents)
    ]
    print(f"Initialized {len(examiner_agents)} examiner agents.")

    # --- Examiner Agents Evaluate Answers ---
    all_evaluations = []
    print("\n--- Examiners Evaluating ---")
    if not examiner_agents:
        print("No examiner agents available to evaluate. Skipping evaluation.")
    else:
        for i, submission in enumerate(all_submitted_answers):
            # Simple round-robin assignment of examiners
            examiner = examiner_agents[i % len(examiner_agents)] 
            print(f"  Examiner {examiner.agent_id} evaluating answer from {submission['agent_id']} for Q: {submission['question_id']}")
            
            evaluation = examiner.evaluate_answer(
                question_id=submission['question_id'],
                question_text=submission['question_text'],
                candidate_answer_text=submission['answer_text'],
                model_answer_text=submission['model_answer_text']
            )
            all_evaluations.append({
                "question_id": submission['question_id'],
                "question_text": submission['question_text'],
                "candidate_agent_id": submission['agent_id'],
                "candidate_answer_text": submission['answer_text'],
                "examiner_agent_id": examiner.agent_id,
                "evaluation_details": evaluation['evaluation'] # This is the dict from GeminiClient
            })
            print(f"    Evaluation complete by {examiner.agent_id}.")

    print(f"\nTotal evaluations: {len(all_evaluations)}")

    # --- Compile and Save Results ---
    final_results = {
        "simulation_timestamp": datetime.datetime.now().isoformat(),
        "questions_used": questions_filepath,
        "num_candidate_agents": num_candidate_agents,
        "num_examiner_agents": num_examiner_agents,
        "evaluated_answers": all_evaluations
    }
    
    # For now, just print the results to console
    # print("\n--- Simulation Results ---")
    # print(json.dumps(final_results, indent=2)) # Pretty print

    save_results(final_results, results_output_dir)

    print("\nSimulation finished.")

if __name__ == "__main__":
    # This allows the script to be run directly.
    # Ensure that Python can find the 'ai_exam_simulator' package.
    # One way is to run this script from the root directory of the project:
    # python -m ai_exam_simulator.simulations.run_simulation
    # Or, ensure 'ai_exam_simulator' parent directory is in PYTHONPATH.

    # For direct execution from anywhere, you might need to adjust sys.path:
    # import sys
    # import os
    # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    # if project_root not in sys.path:
    #    sys.path.insert(0, project_root)
        
    run_simulation()
