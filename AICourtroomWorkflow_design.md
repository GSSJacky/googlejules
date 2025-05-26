# AI Courtroom: Debate and Judgment Workflow

## 1. Title

AI Courtroom: Debate and Judgment Workflow

## 2. Introduction

This document outlines the step-by-step sequence of the AI Courtroom simulation, detailing the procedural flow from initial case input to the final delivery of a simulated judgment. The entire workflow is orchestrated by the `CourtroomSimulationManagerAgent`. Given the defined phases and ordered progression of events, this workflow is well-suited for implementation using an ADK (Agent Development Kit) `SequentialWorkflowAgent`, where each step or phase transition is managed in a controlled sequence.

## 3. Workflow Phases and Steps

The AI Courtroom simulation proceeds through the following distinct phases:

### Phase 1: Simulation Setup & Case Input

*   **Step 1.1: User Submits Case Details**
    *   The user interacts with an interface (e.g., a web form, chat input) to provide the foundational information for the simulation.
    *   **Required Inputs:**
        *   A brief summary of the dispute.
        *   The plaintiff's primary claim or desired outcome.
        *   The defendant's primary position or defense (if known by the user, otherwise can be more generally framed).
        *   (Optional) Any key facts or pieces of "evidence" (abstracted) the user wants to be considered for each side.
*   **Step 1.2: `CourtroomSimulationManagerAgent` Ingests and Distributes Input**
    *   The `CourtroomSimulationManagerAgent` (hereafter "Manager") receives the user's input.
    *   It parses this input and prepares tailored information packets for each participating agent:
        *   To `PlaintiffCounselAgent`: Case summary, plaintiff's claim/desired outcome, plaintiff-specific facts/evidence.
        *   To `DefendantCounselAgent`: Case summary, plaintiff's claim, defendant's position, defendant-specific facts/evidence.
        *   To `JudgeAgent`: Full case summary, plaintiff's claim, defendant's position, and any facts provided for both sides.
    *   The Manager then instantiates or initializes these agents with their respective information.

### Phase 2: Opening Statements

*   **Step 2.1: Manager Prompts `PlaintiffCounselAgent` for Opening Statement**
    *   The Manager signals the `PlaintiffCounselAgent` that it is its turn to deliver an opening statement.
*   **Step 2.2: `PlaintiffCounselAgent` Submits Statement; Manager Relays**
    *   The `PlaintiffCounselAgent` formulates its opening statement (based on its persona and initial information, potentially after consulting the `LegalKnowledgeTool` as per its role design).
    *   It sends the statement text to the Manager.
    *   The Manager relays this opening statement to the `JudgeAgent` (for listening) and to the `DefendantCounselAgent` (for information).
*   **Step 2.3: Manager Prompts `DefendantCounselAgent` for Opening Statement**
    *   After the plaintiff's statement, the Manager signals the `DefendantCounselAgent`.
*   **Step 2.4: `DefendantCounselAgent` Submits Statement; Manager Relays**
    *   The `DefendantCounselAgent` formulates its opening statement.
    *   It sends the statement text to the Manager.
    *   The Manager relays this opening statement to the `JudgeAgent` and to the `PlaintiffCounselAgent`.

### Phase 3: Plaintiff's Case Presentation

*   **Step 3.1: Manager Prompts `PlaintiffCounselAgent` to Present Main Arguments**
    *   The Manager signals the `PlaintiffCounselAgent` to present its primary arguments and refer to its (abstracted) evidence.
*   **Step 3.2: `PlaintiffCounselAgent` Submits Arguments; Manager Relays**
    *   The `PlaintiffCounselAgent` submits its structured arguments, potentially in one or more turns if the simulation design allows for iterative presentation. For simplicity, we'll assume one main submission here.
    *   The Manager relays these arguments to the `JudgeAgent` and the `DefendantCounselAgent`.

### Phase 4: Defendant's Case Presentation & Defense

*   **Step 4.1: Manager Prompts `DefendantCounselAgent` to Present Main Arguments and Defense**
    *   The Manager signals the `DefendantCounselAgent` to present its defense, counter-arguments, and refer to its (abstracted) evidence.
*   **Step 4.2: `DefendantCounselAgent` Submits Arguments; Manager Relays**
    *   The `DefendantCounselAgent` submits its structured arguments and defenses.
    *   The Manager relays these to the `JudgeAgent` and the `PlaintiffCounselAgent`.

### Phase 5: Rebuttal and Questioning (Optional, can be a loop)

This phase adds dynamism and allows for more direct interaction, mediated by the Judge.

*   **Step 5.1 (Optional): Manager Prompts `PlaintiffCounselAgent` for Rebuttal**
    *   The Manager may prompt the `PlaintiffCounselAgent` for a brief rebuttal to the defendant's case.
    *   If prompted, the `PlaintiffCounselAgent` submits its rebuttal; the Manager relays it to the `JudgeAgent` and `DefendantCounselAgent`.
*   **Step 5.2 (Optional): Manager Prompts `DefendantCounselAgent` for Rebuttal**
    *   Similarly, the Manager may prompt the `DefendantCounselAgent` for a rebuttal to the plaintiff's rebuttal or main case.
    *   If prompted, the `DefendantCounselAgent` submits its rebuttal; the Manager relays it to the `JudgeAgent` and `PlaintiffCounselAgent`.
*   **Step 5.3: Manager Prompts `JudgeAgent` for Questions**
    *   The Manager asks the `JudgeAgent` if it has any questions for either or both counsel based on the statements and arguments presented.
*   **Step 5.4: Judge-led Questioning Loop**
    *   If the `JudgeAgent` has questions:
        *   **Judge Submits Question:** The `JudgeAgent` formulates its question(s), specifying the target counsel (Plaintiff or Defendant), and sends it to the Manager.
        *   **Manager Relays Question:** The Manager relays the question to the specified counsel agent.
        *   **Counsel Submits Response:** The targeted counsel agent formulates its response and sends it to the Manager.
        *   **Manager Relays Response:** The Manager relays the counsel's response to the `JudgeAgent` and also to the other counsel agent (for awareness and potential follow-up in a more complex simulation).
        *   **Loop Continuation:** The Manager can then ask the `JudgeAgent` if it has further questions. This loop (Judge asks -> Counsel responds) can repeat a predefined number of times (e.g., 1-3 rounds) or until the `JudgeAgent` indicates it has no further questions. This allows for a focused examination of key points.

### Phase 6: Judge's Deliberation

*   **Step 6.1: Manager Signals `JudgeAgent` to Begin Deliberation**
    *   Once rebuttals and questioning are complete (or skipped), the Manager formally instructs the `JudgeAgent` to begin its deliberation process.
*   **Step 6.2: `JudgeAgent` Internal Processing**
    *   The `JudgeAgent` now enters its internal "deliberation" phase as defined in its role behavior (`AICourtroomRoleBehaviors_design.md`).
    *   This involves reviewing all case facts, arguments from both counsel, responses to questions, and making necessary calls to the `LegalKnowledgeTool` (as outlined in `AICourtroomKnowledgeIntegration_design.md`).
    *   This step is a "black box" from the Manager's immediate workflow perspective; the Manager simply awaits the `JudgeAgent`'s readiness to deliver a verdict. No other agent interactions occur during this time.

### Phase 7: Verdict Delivery

*   **Step 7.1: `JudgeAgent` Submits Verdict and Reasoning to Manager**
    *   Once deliberation is complete, the `JudgeAgent` formulates its final verdict (e.g., "Judgment for Plaintiff," "Judgment for Defendant") and a concise summary of its reasoning.
    *   It sends this information to the Manager.
*   **Step 7.2: Manager Relays Verdict and Reasoning**
    *   The Manager receives the verdict and reasoning.
    *   It relays this information to:
        *   The **User** (as the primary outcome of the simulation).
        *   The `PlaintiffCounselAgent` (for its "information").
        *   The `DefendantCounselAgent` (for its "information").

### Phase 8: Simulation End

*   **Step 8.1: Manager Presents Final Summary/Transcript (Optional)**
    *   The Manager may compile a brief summary or an abstract "transcript" of key interactions (e.g., opening statements, core arguments, verdict) and present this to the user.
    *   Mandatory disclaimers about the simulation's nature and non-binding outcome are reinforced here.
*   **Step 8.2: Simulation Concludes**
    *   The Manager finalizes the simulation state. All agents are dismissed or reset for potential new simulations.

## 4. ADK `SequentialWorkflowAgent` Fit

The described phases and steps map very well to the structure of an ADK `SequentialWorkflowAgent`:

*   **Sequential Nature:** The courtroom process, as outlined, is inherently sequential. Opening statements precede arguments, arguments precede deliberation, and deliberation precedes the verdict. Each phase logically follows the previous one.
*   **Defined Steps:** Each step within a phase (e.g., "Manager prompts Plaintiff," "Plaintiff submits statement," "Manager relays statement") can be implemented as a distinct operation or method call within the `SequentialWorkflowAgent`'s execution logic.
*   **Control Flow:** The `SequentialWorkflowAgent` naturally manages the control flow, ensuring that Step 2.2 only occurs after Step 2.1 is complete, and so on. The output of one step (e.g., a statement from an agent) becomes the input or trigger for subsequent steps (e.g., relaying that statement).
*   **State Management:** The Manager agent maintains the overall state of the simulation (e.g., current phase, whose turn it is), which is intrinsic to how a workflow agent progresses.
*   **Conditional Logic for Optional Phases:** Optional phases like "Rebuttal and Questioning" can be handled with conditional steps within the workflow. For example, the workflow can have a condition to check if "Questioning" is enabled or if the Judge has questions before entering that loop.

## 5. Handling of Agent Communication

As emphasized throughout the steps, the `CourtroomSimulationManagerAgent` acts as the **sole and central hub for all communications** between the child agents (`JudgeAgent`, `PlaintiffCounselAgent`, `DefendantCounselAgent`) and between the agents and the user.

*   Child agents do not communicate directly with each other.
*   All arguments, statements, questions, responses, and the final verdict are passed *through* the Manager.
*   This centralized communication model simplifies inter-agent interaction logic, allows the Manager to log all communications for potential transcript generation, and ensures the structured flow of the simulation is maintained.

## 6. Flexibility and Future Enhancements

This workflow provides a solid foundation that can be expanded upon:

*   **Detailed Rebuttals:** The rebuttal phase (5.1, 5.2) can be made more interactive, perhaps allowing multiple rounds or specific counter-arguments to individual points.
*   **Multiple Questioning Rounds:** The Judge's questioning loop (5.4) can be configured for more iterations or allow counsel to pose questions to each other (cross-examination, always mediated by the Judge and Manager).
*   **Evidence Presentation:** The concept of "abstracted evidence" can be made more concrete, with agents referring to specific (though still simulated) pieces of evidence, and the `LegalKnowledgeTool` potentially being used to verify or provide context for types of evidence.
*   **Witness Testimony:** A new phase for "Witness Testimony" could be inserted, where `WitnessAgent`s (a new role) provide statements, and counsel agents can "examine" them.
*   **Jury Deliberation:** For a more complex simulation, a "Jury Deliberation" phase could be added after the Judge's instructions, involving a `JuryAgent` or group of `JuryAgent`s.
*   **Dynamic Flow Adjustments:** While primarily sequential, more advanced implementations could allow the `JudgeAgent`, under certain conditions, to request modifications to the flow (e.g., requesting an additional piece of information before deliberation), which the Manager would then try to accommodate.

This workflow design ensures a structured yet adaptable progression for the AI Courtroom simulation, providing a clear path for interaction and decision-making among the AI agents.
