# AI Courtroom: Legal Knowledge Tool Integration

## 1. Title

AI Courtroom: Legal Knowledge Tool Integration

## 2. Introduction

The purpose of this document is to outline how the specialized AI agents within the AI Courtroom simulation (`JudgeAgent`, `PlaintiffCounselAgent`, `DefendantCounselAgent`) will integrate and utilize the `LegalKnowledgeTool`. Access to relevant legal information is crucial for these agents to perform their roles effectively, construct coherent arguments, and make informed decisions within the simulated legal environment. The `LegalKnowledgeTool` (as previously designed) serves as the primary repository for this legal information.

## 3. Orchestration of Access

The method by which courtroom agents access the `LegalKnowledgeTool` needs to ensure both flexibility and controlled information flow, managed primarily by the `CourtroomSimulationManagerAgent`.

*   **Facilitated Tool Calls by `CourtroomSimulationManagerAgent` (Primary Method):**
    *   The `CourtroomSimulationManagerAgent` will generally act as the facilitator for `LegalKnowledgeTool` calls. When a child agent (`PlaintiffCounselAgent`, `DefendantCounselAgent`, or `JudgeAgent`) requires legal information, it will formulate a request (or a set of parameters for a query) and pass it to the `CourtroomSimulationManagerAgent`.
    *   The `CourtroomSimulationManagerAgent` then executes the actual call to the `LegalKnowledgeTool` using the provided parameters.
    *   Upon receiving the JSON response from the `LegalKnowledgeTool`, the `CourtroomSimulationManagerAgent` forwards this information back to the requesting child agent.
    *   **Rationale:** This approach maintains centralized control over tool usage, allows for logging and monitoring of tool interactions at the manager level, and simplifies the child agents' direct responsibilities. It also aligns well with a `SequentialWorkflowAgent` structure for the manager.

*   **Direct Access Permissions (Secondary/Conditional Method):**
    *   If the ADK framework supports secure and granular permissioning for tools on a per-agent basis, direct access could be granted to child agents.
    *   In this scenario, an agent like `PlaintiffCounselAgent` could directly call `adk.tools.call_tool("LegalKnowledgeTool", params={...})`.
    *   **Rationale:** This might be slightly more efficient for highly interactive agents that need rapid, iterative lookups. However, it requires more sophisticated access control within the ADK and potentially more complex error handling within each child agent. For the initial design, facilitated access is preferred.

*   **Timing of Tool Calls:**
    *   **Proactive Calls (During Preparation/Strategy Phases):**
        *   Counsel agents (`PlaintiffCounselAgent`, `DefendantCounselAgent`) are likely to make proactive calls during their initial "case preparation" or "argument generation" phases. Before presenting their opening statements or main arguments, they would query the `LegalKnowledgeTool` to gather supporting legal precedents, statutes, or relevant legal principles.
        *   The `JudgeAgent` might make proactive calls if, upon receiving the initial case details, it identifies specific legal areas it needs to refresh its "understanding" on.
    *   **Reactive Calls (In Response to Simulation Events):**
        *   During the course of the simulation, agents might need to make calls in reaction to arguments raised by opposing counsel or questions posed by the `JudgeAgent`. For example, if opposing counsel cites an unexpected case, an agent might request a lookup on that case.
        *   The `JudgeAgent` is particularly likely to make reactive calls during its "deliberation" phase, after all arguments have been presented, to verify specific points of law or compare conflicting interpretations offered by the counsel agents.

## 4. Agent-Specific Usage Scenarios

### 4.1. `PlaintiffCounselAgent`

*   **Objective:** To find legal information that substantiates the plaintiff's claims, establishes the defendant's liability, and supports requests for specific remedies.
*   **Usage:**
    *   **Argument Preparation:** Before constructing its core arguments, the agent will query for laws, regulations, and case law that affirm the plaintiff's rights and the defendant's obligations in the context of the case facts.
    *   **Supporting Claims:** It will look for precedents where similar factual scenarios led to favorable outcomes for the plaintiff.
    *   **Identifying Elements of Proof:** The tool can help identify the necessary legal elements the plaintiff must prove for each claim (e.g., duty, breach, causation, damages in a negligence case).
    *   **Rebuttal Preparation:** If the defendant raises specific legal defenses, the `PlaintiffCounselAgent` might use the tool to find counter-arguments or limitations to those defenses.
*   **Example Queries (sent to `CourtroomSimulationManagerAgent` or directly):**
    *   `{"query": "Case law supporting breach of contract for failure to deliver goods by agreed date in Japan", "jurisdiction": "japanese", "information_type": "case_law", "max_results": 3}`
    *   `{"query": "Statutory basis for claiming damages for emotional distress in online defamation cases, international examples", "jurisdiction": "international", "information_type": "statute_reference", "max_results": 2}`
    *   `{"query": "Elements required to prove 'unjust enrichment' in commercial disputes", "jurisdiction": "japanese", "information_type": "general_overview"}`

### 4.2. `DefendantCounselAgent`

*   **Objective:** To find legal information that supports defenses, refutes the plaintiff's claims, establishes counterclaims, or mitigates the defendant's liability.
*   **Usage:**
    *   **Defense Strategy:** Queries for affirmative defenses applicable to the plaintiff's claims (e.g., statute of limitations, contributory negligence, contractual disclaimers).
    *   **Challenging Plaintiff's Case:** Looks for precedents where similar claims by plaintiffs were dismissed or limited.
    *   **Supporting Counterclaims:** If the defendant has counterclaims, the agent uses the tool to find legal support for these.
    *   **Mitigating Damages:** Researches legal principles or cases that might limit the scope or amount of damages if liability is found.
*   **Example Queries:**
    *   `{"query": "Affirmative defenses to copyright infringement claims regarding software in Japan", "jurisdiction": "japanese", "information_type": "case_law", "max_results": 3}`
    *   `{"query": "Case law where 'force majeure' clause excused non-performance of contract", "jurisdiction": "international", "information_type": "case_law", "max_results": 2}`
    *   `{"query": "Legal definition and application of 'reasonable care' for service providers", "jurisdiction": "japanese", "information_type": "general_overview"}`

### 4.3. `JudgeAgent`

*   **Objective:** To ensure a fair trial based on law, clarify legal ambiguities, verify claims made by counsel, and make an informed judgment.
*   **Usage:**
    *   **Understanding Applicable Law:** If the case involves complex or niche areas of law, the `JudgeAgent` might use the tool to get a general overview or specific statute details.
    *   **Verifying Citations:** If counsel agents cite specific statutes or cases, the `JudgeAgent` can use the tool to retrieve and "review" these sources.
    *   **Resolving Legal Discrepancies:** If plaintiff and defendant counsel offer conflicting interpretations of a law or precedent, the `JudgeAgent` can seek clarification from the tool.
    *   **Informing Deliberation:** During the "deliberation" phase, after all arguments are heard, the `JudgeAgent` uses the tool to research any remaining legal questions that are critical to reaching a verdict. This helps simulate a judge's independent research or consultation of legal texts.
*   **Example Queries:**
    *   `{"query": "Interpretation of 'good faith' under Japanese contract law", "jurisdiction": "japanese", "information_type": "general_overview"}`
    *   `{"query": "Full text of Patent Act Article 70, Japan", "jurisdiction": "japanese", "information_type": "statute_reference"}`
    *   `{"query": "Landmark international cases on 'state responsibility for transboundary harm'", "jurisdiction": "international", "information_type": "case_law", "max_results": 1}`
    *   `{"query": "Legal standard for 'admissibility of digital evidence' in Japanese courts", "jurisdiction": "japanese", "information_type": "general_overview"}`

## 5. Information Flow

1.  **Request Formulation:** The courtroom agent (e.g., `PlaintiffCounselAgent`) identifies a need for legal information. It formulates a set of parameters for the `LegalKnowledgeTool` query (as per the tool's input schema).
2.  **Request to Manager:** This request is sent to the `CourtroomSimulationManagerAgent`.
3.  **Tool Call:** The `CourtroomSimulationManagerAgent` makes the actual call to the `LegalKnowledgeTool` with the received parameters.
4.  **Tool Response:** The `LegalKnowledgeTool` returns a structured JSON response (containing `summary`, `results` array with `source`, `type`, `content`, `url`, `metadata`, etc., and `errors`).
5.  **Response Forwarding:** The `CourtroomSimulationManagerAgent` forwards this JSON response back to the original requesting agent.
6.  **Information Extraction & Processing by Agent:**
    *   The receiving agent (e.g., `PlaintiffCounselAgent`) parses the JSON.
    *   It extracts relevant pieces of information from the `results` array – typically the `content` (text snippets, case summaries, statute text), `title`, `source`, and any relevant `metadata` (like case numbers or statute articles).
7.  **Influence on Agent's Reasoning and Response Generation:**
    *   **Prompt Augmentation:** The extracted legal information is then incorporated into the context provided to the agent's underlying LLM. This is typically done by adding the information to the system prompt or as part of the user/history input for the LLM's next generation step.
    *   **Example Prompt Snippet (for `PlaintiffCounselAgent`'s LLM):**
        ```
        System: You are Plaintiff's Counsel.
        User (from CourtroomSimulationManagerAgent):
        Your current task is to formulate your opening statement.
        Case Details: [User-provided case summary]
        Supporting Legal Information from LegalKnowledgeTool:
        1. Case: Tanaka v. Yamada (Tokyo District Court, 2022) - Summary: [Summary of Tanaka v. Yamada where similar breach was found...] - Source: D1-Law API
        2. Statute: Civil Code Article XXX - Text: [Text of relevant Civil Code article...] - Source: ELaws API
        ---
        Now, generate your opening statement.
        ```
    *   **Content Generation:** The LLM uses this augmented context to:
        *   Cite specific laws or cases in its arguments (e.g., "As established in Tanaka v. Yamada...").
        *   Frame its arguments based on the legal principles found (e.g., "The defendant's actions clearly violate Civil Code Article XXX, which states...").
        *   For the `JudgeAgent`, the information helps in formulating its reasoning for the verdict (e.g., "Considering Civil Code Article YYY and the precedent set in ZZZ v. AAA, the court finds...").

## 6. Assumptions and Limitations

*   **Tool Capability:** The effectiveness of this integration heavily relies on the `LegalKnowledgeTool`'s ability to:
    *   Accurately interpret queries.
    *   Access a comprehensive and relevant database of Japanese and international law.
    *   Return precise, concise, and relevant information in its JSON output. Overly verbose or irrelevant results will be less useful for the LLM agents.
*   **LLM Reasoning:** The "depth" of legal understanding and application by the courtroom agents is dependent on:
    *   The quality and relevance of information provided by the `LegalKnowledgeTool`.
    *   The underlying LLM's ability to reason over and correctly apply the provided legal context in its response generation. LLMs are not legal experts and may misinterpret or misapply information.
*   **Conciseness of Information:** The `LegalKnowledgeTool` should ideally provide summaries or specific relevant snippets rather than entire lengthy documents, as LLMs have context window limitations and process concise information more effectively.
*   **No Real Legal Expertise:** It must be continually emphasized (in system design and user presentation) that this is a simulation. The agents and the tool do not possess genuine legal expertise or consciousness.
*   **Simplified Interaction:** The process of legal research and application is highly complex. This integration represents a simplified model of how legal professionals might access and use legal knowledge.

This integration design aims to provide a foundational layer of "legal knowledge" for the AI Courtroom agents, enabling them to engage in more informed and contextually relevant simulated legal proceedings. Continuous refinement of the `LegalKnowledgeTool` and the agents' prompting strategies will be key to improving the quality of the simulation.
