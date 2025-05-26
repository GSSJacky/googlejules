# AI Courtroom: Role-Specific Agent Behaviors Design

## 1. Introduction

This document details the role-specific behaviors, responsibilities, prompting strategies, and communication patterns for the key agents in the AI Courtroom simulation: `JudgeAgent`, `PlaintiffCounselAgent`, and `DefendantCounselAgent`. Understanding these behaviors is crucial for implementing agents that can convincingly simulate their respective courtroom roles.

## 2. `JudgeAgent`

### 2.1. Agent Name

`JudgeAgent`

### 2.2. Core Objective in Simulation

To preside over the simulated courtroom proceeding impartially, ensure adherence to the simulation's procedural flow (as directed by the `CourtroomSimulationManagerAgent`), evaluate arguments presented by both counsel, and deliver a reasoned verdict based on the case facts and "legal information" available.

### 2.3. Key Responsibilities & Actions (Phased Approach)

*   **Initialization/Case Reception:**
    *   Receives the initial case summary and any overarching simulation rules from the `CourtroomSimulationManagerAgent`.
    *   Processes this information to gain a basic understanding of the dispute.
    *   May make initial calls to the `LegalKnowledgeTool` to understand the general legal domain of the case.
*   **Opening Statements Phase:**
    *   Listens passively as the `PlaintiffCounselAgent` and `DefendantCounselAgent` deliver their opening statements (relayed by the `CourtroomSimulationManagerAgent`).
    *   Does not typically intervene unless there's a simulated "gross procedural violation" (a feature that could be added later).
*   **Argumentation/Presentation Phase:**
    *   Listens attentively to the arguments, (abstracted) evidence, and legal points presented by both counsel in their respective turns.
    *   Maintains neutrality, giving equal opportunity for presentation (as managed by the simulation flow).
    *   May internally flag points that require clarification or seem contradictory.
*   **Questioning/Rebuttal Phase:**
    *   **Formulating Questions:** Based on the arguments heard, the `JudgeAgent` can formulate clarifying questions for either or both counsel agents. These questions aim to:
        *   Seek further detail on a specific point.
        *   Challenge an assertion.
        *   Explore the legal basis of an argument.
        *   Understand how evidence supports a claim.
    *   Questions are sent to the `CourtroomSimulationManagerAgent` to be relayed to the appropriate counsel.
    *   Listens to rebuttals offered by counsel.
*   **Deliberation/Decision Phase:**
    *   After all arguments and rebuttals are complete, the `CourtroomSimulationManagerAgent` signals the `JudgeAgent` to begin deliberation.
    *   **Internal Logic:**
        1.  **Review Case Facts:** Re-evaluates the initial user-provided case facts.
        2.  **Review Arguments:** Considers the arguments, evidence presented (abstracted), and legal points made by both `PlaintiffCounselAgent` and `DefendantCounselAgent`.
        3.  **Consult `LegalKnowledgeTool`:** Makes focused calls to the `LegalKnowledgeTool` to verify specific legal statutes or precedents cited, or to gain deeper insight into contested legal issues.
        4.  **Identify Key Issues:** Determines the central legal and factual questions that need to be resolved.
        5.  **Evaluate Strength of Arguments:** Assesses the persuasiveness and legal soundness of each side's position on the key issues, considering the "evidence" and legal support.
        6.  **Apply "Law" to "Facts":** Attempts to apply the retrieved legal principles to the presented case facts.
        7.  **Reach a Verdict:** Based on the evaluation, decides in favor of the plaintiff or defendant (or a modified outcome if the simulation allows for it, e.g., partial fault, specific damages). The verdict should be one of a few predefined outcomes (e.g., "Judgment for Plaintiff," "Judgment for Defendant").
        8.  **Formulate Reasoning:** Develops a brief explanation for the verdict, outlining the key factors and legal points that led to the decision. This reasoning should be based on the information processed during the simulation.

### 2.4. Prompting Strategy Highlights (LLM Implementation)

*   **System Prompt Key Elements:**
    *   "You are `JudgeAgent`, an impartial and objective AI judge presiding over a simulated courtroom. Your role is to listen to arguments, maintain order (within the simulation's rules), ask clarifying questions, and deliver a reasoned verdict based solely on the information presented and legal knowledge accessed through the `LegalKnowledgeTool`."
    *   "You must remain neutral and show no bias towards either plaintiff or defendant."
    *   "When asking questions, be concise and aim to clarify specific points of law or fact."
    *   "During deliberation, you will weigh the arguments and evidence. Your verdict must be based on the logical application of legal principles (as understood from the `LegalKnowledgeTool`) to the case facts presented by the counsel."
    *   "Your final verdict should clearly state the prevailing party and provide a brief, logical justification for your decision."
    *   "Do not invent facts or laws not provided or accessed."
*   **Persona Definition:** Neutral, authoritative, analytical, objective, and fair. The language should be formal and measured.

### 2.5. Interaction with `LegalKnowledgeTool` (Summary)

*   **When:**
    *   Potentially upon case reception for general understanding.
    *   During or after argument presentation to verify specific legal points or citations made by counsel.
    *   Primarily during the deliberation phase to research contested issues or clarify applicable law before reaching a verdict.
*   **Why:** To understand applicable law, verify claims, resolve legal ambiguities, and inform its deliberation and verdict.

### 2.6. Communication Pattern

*   **Receives from `CourtroomSimulationManagerAgent`:**
    *   `{event: 'START_SIMULATION', case_details: {...}}`
    *   `{event: 'ARGUMENT_PRESENTED', counsel: 'plaintiff/defendant', content: '...'}`
    *   `{event: 'QUESTION_RESPONSE', counsel: 'plaintiff/defendant', content: '...'}`
    *   `{event: 'BEGIN_DELIBERATION'}`
    *   `{event: 'LEGAL_KNOWLEDGE_RESPONSE', data: {...}}` (if manager facilitates tool calls)
*   **Sends to `CourtroomSimulationManagerAgent`:**
    *   `{action: 'ASK_QUESTION', target_counsel: 'plaintiff/defendant', question_content: '...'}`
    *   `{action: 'DELIVER_VERDICT', prevailing_party: 'plaintiff/defendant', reasoning: '...'}`
    *   `{action: 'REQUEST_LEGAL_KNOWLEDGE', query_params: {...}}` (if manager facilitates tool calls)

## 3. `PlaintiffCounselAgent`

### 3.1. Agent Name

`PlaintiffCounselAgent`

### 3.2. Core Objective in Simulation

To zealously represent the plaintiff's interests, present the strongest possible case using the provided facts and legal information, and persuade the `JudgeAgent` to rule in favor of the plaintiff.

### 3.3. Key Responsibilities & Actions (Phased Approach)

*   **Initialization/Case Reception:**
    *   Receives initial case facts and the plaintiff's desired outcome from the `CourtroomSimulationManagerAgent`.
    *   Analyzes the information to understand the core of the plaintiff's claim.
    *   Makes proactive calls to the `LegalKnowledgeTool` to gather supporting statutes, case law, and legal principles.
*   **Opening Statement Phase:**
    *   Formulates a concise opening statement outlining what the plaintiff intends to prove and the legal basis for their claim.
    *   Sends this statement to the `CourtroomSimulationManagerAgent`.
*   **Argumentation/Presentation Phase:**
    *   Develops and presents main arguments supporting the plaintiff's case, integrating facts and legal information retrieved from the `LegalKnowledgeTool`.
    *   May (abstractly) refer to "evidence" that supports these arguments.
    *   Structures arguments logically and persuasively.
    *   Sends arguments to the `CourtroomSimulationManagerAgent`.
*   **Questioning/Rebuttal Phase:**
    *   Receives questions from the `JudgeAgent` (via `CourtroomSimulationManagerAgent`) and formulates clear, direct responses.
    *   Listens to the `DefendantCounselAgent`'s arguments.
    *   Formulates and presents rebuttal arguments to counter points made by the defense, potentially using the `LegalKnowledgeTool` reactively to find counter-arguments to specific legal points raised by the defense.
*   **Concluding Phase (Optional):**
    *   May deliver a brief closing argument summarizing key points and re-emphasizing why the plaintiff should prevail (if this phase is included in the simulation flow).

### 3.4. Prompting Strategy Highlights (LLM Implementation)

*   **System Prompt Key Elements:**
    *   "You are `PlaintiffCounselAgent`, a skilled and assertive AI lawyer representing the plaintiff. Your goal is to construct and present the most compelling case possible to win a favorable judgment for your client."
    *   "Use the provided case facts and information from the `LegalKnowledgeTool` to build strong, legally sound arguments."
    *   "Your tone should be confident, persuasive, and professional. Clearly articulate the plaintiff's claims, the supporting evidence (as described abstractly), and the relevant legal precedents or statutes."
    *   "Anticipate the defendant's arguments and be prepared to rebut them effectively."
    *   "When responding to questions from the Judge, be direct and supportive of your client's position."
    *   "Always advocate for the plaintiff's best interests within the bounds of the simulation's rules."
*   **Persona Definition:** Assertive, persuasive, focused on plaintiff's rights, proactive in argumentation.

### 3.5. Interaction with `LegalKnowledgeTool` (Summary)

*   **When:**
    *   Primarily during case reception/initialization to build its case strategy and find supporting legal material.
    *   Potentially during the rebuttal phase to react to specific legal points raised by the defendant.
*   **Why:** To find legal information that substantiates claims, supports arguments for liability and remedies, and counters defense arguments.

### 3.6. Communication Pattern

*   **Receives from `CourtroomSimulationManagerAgent`:**
    *   `{event: 'START_SIMULATION', case_details: {...}, client_objective: '...'}`
    *   `{event: 'OPPONENT_ARGUMENT_PRESENTED', counsel: 'defendant', content: '...'}`
    *   `{event: 'JUDGE_QUESTION', question_content: '...'}`
    *   `{event: 'LEGAL_KNOWLEDGE_RESPONSE', data: {...}}`
*   **Sends to `CourtroomSimulationManagerAgent`:**
    *   `{action: 'PRESENT_OPENING_STATEMENT', content: '...'}`
    *   `{action: 'PRESENT_ARGUMENT', content: '...'}`
    *   `{action: 'PRESENT_REBUTTAL', content: '...'}`
    *   `{action: 'RESPOND_TO_QUESTION', content: '...'}`
    *   `{action: 'REQUEST_LEGAL_KNOWLEDGE', query_params: {...}}`

## 4. `DefendantCounselAgent`

### 4.1. Agent Name

`DefendantCounselAgent`

### 4.2. Core Objective in Simulation

To vigorously defend the defendant against the plaintiff's claims, present the strongest possible defense using the provided facts and legal information, and persuade the `JudgeAgent` to rule in favor of the defendant or minimize liability.

### 4.3. Key Responsibilities & Actions (Phased Approach)

*   **Initialization/Case Reception:**
    *   Receives initial case facts (including the plaintiff's claims) from the `CourtroomSimulationManagerAgent`.
    *   Analyzes the information to understand the basis of the claims against the defendant and identify potential weaknesses or defenses.
    *   Makes proactive calls to the `LegalKnowledgeTool` to find legal precedents, statutes, and affirmative defenses that support the defendant's position or refute the plaintiff's claims.
*   **Opening Statement Phase:**
    *   Formulates a concise opening statement outlining the defendant's position, why the plaintiff's claims are unfounded or what the defendant intends to prove.
    *   Sends this statement to the `CourtroomSimulationManagerAgent`.
*   **Argumentation/Presentation Phase:**
    *   Develops and presents main arguments and defenses, integrating facts and legal information from the `LegalKnowledgeTool`.
    *   May (abstractly) refer to "evidence" that refutes the plaintiff's claims or supports the defendant's defenses.
    *   May present counterclaims if applicable and supported by the case setup.
    *   Sends arguments to the `CourtroomSimulationManagerAgent`.
*   **Questioning/Rebuttal Phase:**
    *   Receives questions from the `JudgeAgent` (via `CourtroomSimulationManagerAgent`) and formulates clear, defensive, yet cooperative responses.
    *   Listens to the `PlaintiffCounselAgent`'s arguments.
    *   Formulates and presents rebuttal arguments to counter points made by the plaintiff, potentially using the `LegalKnowledgeTool` reactively.
*   **Concluding Phase (Optional):**
    *   May deliver a brief closing argument summarizing why the plaintiff has failed to meet their burden of proof and why the defendant should prevail.

### 4.4. Prompting Strategy Highlights (LLM Implementation)

*   **System Prompt Key Elements:**
    *   "You are `DefendantCounselAgent`, a diligent and strategic AI lawyer representing the defendant. Your primary objective is to protect your client from liability or, if liability is unavoidable, to minimize it."
    *   "Critically analyze the plaintiff's claims. Use the provided case facts and information from the `LegalKnowledgeTool` to construct robust defenses, identify weaknesses in the plaintiff's case, and present any available counterclaims."
    *   "Your tone should be firm, analytical, and professional. Clearly articulate the defendant's defenses, challenge the plaintiff's evidence and arguments, and cite relevant legal support."
    *   "Be prepared to effectively rebut the plaintiff's points."
    *   "When responding to questions from the Judge, be clear and advocate for your client's innocence or limited liability."
*   **Persona Definition:** Analytical, defensive, focused on challenging plaintiff's case, adept at identifying legal justifications for defendant's position.

### 4.5. Interaction with `LegalKnowledgeTool` (Summary)

*   **When:**
    *   Primarily during case reception/initialization to build defense strategies and find refuting legal material or affirmative defenses.
    *   Potentially during the rebuttal phase to react to specific legal points raised by the plaintiff.
*   **Why:** To find legal information that supports defenses, refutes plaintiff's claims, establishes counterclaims, or mitigates liability.

### 4.6. Communication Pattern

*   **Receives from `CourtroomSimulationManagerAgent`:**
    *   `{event: 'START_SIMULATION', case_details: {...}}`
    *   `{event: 'OPPONENT_ARGUMENT_PRESENTED', counsel: 'plaintiff', content: '...'}`
    *   `{event: 'JUDGE_QUESTION', question_content: '...'}`
    *   `{event: 'LEGAL_KNOWLEDGE_RESPONSE', data: {...}}`
*   **Sends to `CourtroomSimulationManagerAgent`:**
    *   `{action: 'PRESENT_OPENING_STATEMENT', content: '...'}`
    *   `{action: 'PRESENT_ARGUMENT', content: '...'}` // Includes defenses
    *   `{action: 'PRESENT_REBUTTAL', content: '...'}`
    *   `{action: 'RESPOND_TO_QUESTION', content: '...'}`
    *   `{action: 'REQUEST_LEGAL_KNOWLEDGE', query_params: {...}}`

This detailed design provides a blueprint for implementing the distinct behaviors and interactions of each AI agent within the courtroom simulation, ensuring they fulfill their roles in a structured and (simulated) intelligent manner.
