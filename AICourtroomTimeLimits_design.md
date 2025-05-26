# AI Courtroom: Incorporating Time Limits

## 1. Title

AI Courtroom: Incorporating Time Limits

## 2. Introduction

The purpose of incorporating time limits into the AI Courtroom simulation is multi-faceted:

*   **Conciseness:** To ensure the simulation remains engaging and does not become overly lengthy, respecting the user's time and attention.
*   **Urgency/Realism (Simulated):** While not perfectly replicating real courtroom pressures, time limits can add a slight sense of urgency, encouraging more direct and focused arguments from the AI agents.
*   **Resource Management:** In a cloud-hosted environment, limiting the duration of complex AI agent interactions helps manage computational resource usage and associated costs.
*   **User Expectation:** The user's initial request mentioned a target of approximately **10 minutes** for the overall simulation. This document outlines strategies to work towards this target and manage time effectively.

## 3. Overall Simulation Time Limit

*   **Tracking by `CourtroomSimulationManagerAgent`:**
    *   The `CourtroomSimulationManagerAgent` (hereafter "Manager") will be responsible for tracking the total elapsed time from the moment the simulation officially begins (e.g., after case input is processed and the first phase starts).
    *   It will start a master timer at the beginning of Phase 2 (Opening Statements).
*   **Handling Exceeding Overall Limit (e.g., 10 minutes):**
    *   If the overall configurable time limit (e.g., 10 minutes) is approached (e.g., at 90% elapsed):
        *   The Manager might issue a "hurry up" signal internally, which could adjust the time allocated for remaining phases (making them shorter).
        *   It could also notify the user: "Approaching overall time limit. The simulation will conclude shortly."
    *   If the overall limit is exceeded:
        *   **Graceful Conclusion (Preferred):**
            1.  The Manager will prevent new phases or extensive interactions from starting.
            2.  It will immediately move to the Judge's Deliberation phase (Phase 6), instructing the `JudgeAgent` to make a decision based on the information gathered *so far*. The `JudgeAgent`'s deliberation time itself might also be curtailed.
            3.  The simulation then proceeds directly to Verdict Delivery (Phase 7) and Simulation End (Phase 8).
        *   **Hard Stop (Less Ideal):** If graceful conclusion is too complex initially, the simulation might just end with a message like: "Overall simulation time limit reached. The simulation has concluded. A verdict could not be reached in the allotted time." (This is less desirable as it lacks closure).
    *   The primary goal is to always reach a verdict, even if based on an abbreviated process, to fulfill the simulation's purpose.

## 4. Time Limits for Specific Phases/Turns (Optional but Recommended)

Introducing granular time limits for specific phases or agent turns is highly recommended to manage the overall time effectively and ensure each part of the simulation receives appropriate attention.

*   **Possible Phases for Time Limits:**
    *   **Opening Statements:** e.g., 30-60 seconds per counsel.
    *   **Main Argument Presentation:** e.g., 90-120 seconds per counsel.
    *   **Rebuttal Phases:** e.g., 45-75 seconds per counsel.
    *   **Judge's Questioning Rounds:** e.g., 60-90 seconds for the `JudgeAgent` to ask a question and counsel to respond (per question-answer cycle). The number of cycles could also be limited.
    *   **Judge's Deliberation:** e.g., 60-120 seconds. This is a critical phase and needs sufficient time, but cannot be indefinite.
*   **Configuration of Granular Limits:**
    *   **Fixed Durations (Simpler Initial Approach):** Assign a fixed, predetermined duration for each phase (as exemplified above). The sum of these, plus some buffer, should align with the overall simulation time limit.
    *   **Percentage of Overall Time (More Dynamic):** Allocate a percentage of the remaining overall time to the current phase. This is more complex to implement as it requires dynamic recalculation but can adapt better if earlier phases finish quickly.
    *   A hybrid approach could also be used: fixed times for initial phases, with later phases becoming more dynamic if time is running short.
    *   For the initial design, **fixed durations** are recommended for simplicity.

## 5. Implementation within `CourtroomSimulationManagerAgent`

The Manager agent, as the orchestrator, is central to implementing and enforcing these time limits.

*   **Monitoring and Enforcement:**
    *   For each step in its workflow that involves waiting for another agent (e.g., waiting for `PlaintiffCounselAgent` to submit an opening statement), the Manager will start an internal timer specific to that step/phase.
    *   This timer will be set to the configured duration for that phase.
*   **Actions When a Specific Phase/Turn Limit is Up:**
    *   **Counsel Speaking Turn (Opening Statement, Main Argument, Rebuttal):**
        *   If the counsel agent has not submitted its content within the allotted time, the Manager will send a "time's up" signal to that agent (if the agent is designed to handle it by, for example, truncating its response).
        *   More practically for an initial implementation, the Manager will simply cease waiting for that agent's input.
        *   The Manager then immediately prompts the next agent in the sequence or moves to the next phase. For example, if `PlaintiffCounselAgent`'s time for argument is up, the Manager proceeds to prompt `DefendantCounselAgent`. The `JudgeAgent` would be informed that the previous speaker was cut short.
    *   **Judge's Questioning Round:**
        *   If a counsel agent takes too long to respond to a judge's question, the Manager prompts the `JudgeAgent` to either ask another question (if overall questioning time allows) or conclude questioning.
        *   If the `JudgeAgent` takes too long to formulate a question, the Manager might prompt it to conclude questioning.
    *   **Judge's Deliberation:**
        *   If the `JudgeAgent` exceeds its deliberation time, the Manager will instruct it to provide a verdict based on its current state of deliberation immediately.

## 6. Communicating Time Limits to Agents (and User)

*   **Informing AI Agents:**
    *   **Yes, it is highly recommended.** When the Manager prompts an AI agent to perform an action (e.g., deliver an opening statement), it should include the allotted time in the prompt.
    *   **Example Prompt Snippet (to `PlaintiffCounselAgent`):**
        ```
        System: You are PlaintiffCounselAgent.
        User (from CourtroomSimulationManagerAgent):
        It is your turn to deliver your opening statement.
        Case Details: [...]
        You have 60 seconds to formulate and provide your statement. Please be concise and impactful.
        ```
    *   This allows the LLM to potentially adjust the length and detail of its response to fit the constraint.
*   **Informing the User:**
    *   **Overall Time Limit:** Yes, at the beginning of the simulation, the user could be informed: "This courtroom simulation has an approximate total duration of 10 minutes."
    *   **Current Phase Time Limit (Optional):** Displaying a countdown timer for the current phase or agent's turn could be a UI feature. This adds transparency but also complexity to the UI. For a text-based or simpler interface, it might be omitted, with the Manager just enforcing limits implicitly.
    *   If a speaker is cut off, the Manager could output a message like: "Counsel [Name]'s time for opening statements has elapsed. We now move to..."

## 7. Flexibility and Configuration

*   **Configurable Parameters:**
    *   The overall simulation time limit (e.g., 10 minutes) should be an easily configurable parameter when initiating the simulation.
    *   The specific time limits for each phase (opening statements, arguments, deliberation, etc.) should also be configurable. This allows for tuning the simulation's pacing and focus.
    *   These configurations could be part of the `CourtroomSimulationManagerAgent`'s initial setup.

## 8. Impact on Agent Behavior

*   **Conciseness:** Ideally, making LLM agents aware of time limits (via prompting) should encourage them to generate more concise and focused responses. They might prioritize key points and omit verbose elaborations.
*   **Prompt Engineering:** This requires careful prompt engineering. The LLM needs to understand the instruction to "be concise within X seconds/minutes" and act on it. The effectiveness of this will depend on the LLM's capabilities.
*   **Graceful Truncation (Advanced):** A more advanced agent might be designed to provide a summary or key takeaways if it realizes it's running out of time, rather than just stopping abruptly. This is a complex behavior to implement reliably. Initially, the Manager's enforcement will be the primary mechanism.

## 9. Technical Considerations for ADK

*   **ADK Workflow Timeouts:**
    *   If the ADK's `SequentialWorkflowAgent` or other workflow constructs offer built-in support for step timeouts or timed operations, these should be leveraged. This would simplify the Manager's implementation, as the ADK framework itself could handle the timer logic and trigger actions upon timeout.
*   **Custom Timer Implementation:**
    *   If ADK does not have native robust support for granular step timeouts within a workflow agent, the `CourtroomSimulationManagerAgent` would need to implement this logic itself. This typically involves:
        *   Recording a start time when a timed operation begins.
        *   Periodically checking the elapsed time against the allocated duration.
        *   Using asynchronous programming patterns (e.g., `asyncio` in Python if ADK is Python-based) to manage these timers without blocking the agent's main execution thread.
    *   This would require careful implementation to ensure timers are accurate and that timeout actions are triggered reliably.

By implementing these time limit strategies, the AI Courtroom simulation can become a more focused, manageable, and user-friendly experience, aligning with the desired operational constraints.
