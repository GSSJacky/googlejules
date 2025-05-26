# AI Lawyer Interaction Flow Design Document

## 1. Title

AI Lawyer Interaction Flow

## 2. Overview

This document outlines the step-by-step process managed by the `LegalConsultationAgent`, detailing the interaction flow from the moment a user submits a legal query to the final presentation of synthesized advice. It describes how the `LegalConsultationAgent` orchestrates calls to the `LegalKnowledgeTool` and the various AI Lawyer Personas to generate a comprehensive and multi-faceted response, inspired by the clarity and structured presentation of legal opinions seen on platforms like `bengo4.com`.

## 3. ADK Workflow Type

*   **ADK Workflow Agent:** The `LegalConsultationAgent` is best implemented as a **`SequentialWorkflowAgent`**. While the core path (Query -> Knowledge Retrieval -> Persona Invocation -> Aggregation -> Presentation) is sequential, specific steps within this sequence will handle more complex operations, including parallel processing.
*   **Parallelism for Persona Agents:**
    *   Within the `SequentialWorkflowAgent`'s structure, one of the steps will be responsible for invoking the multiple AI Lawyer Persona agents. This step will execute these invocations **in parallel**.
    *   This can be achieved by the `LegalConsultationAgent` making asynchronous calls to each persona `LlmAgent` and then awaiting all responses. Alternatively, if the ADK framework provides a specific construct for parallel agent execution (e.g., a "Parallel" step type or a utility function for concurrent agent calls), that would be leveraged. The key is that the personas process their inputs and generate advice concurrently to optimize response time.

## 4. Interaction Steps (Detailed)

### Step 1: User Query Input

*   **How User Submits Query:**
    *   The user submits their legal question or describes their situation via a textual input interface (e.g., a chat window, a text box on a web page).
    *   (Future enhancements could include voice input, which would be transcribed to text before reaching the `LegalConsultationAgent`).
*   **`LegalConsultationAgent` Ingestion:**
    *   The `LegalConsultationAgent`, being the primary interface, receives this raw text query as its initial input.
    *   It may perform initial basic validation (e.g., checking for non-empty input).

### Step 2: Legal Knowledge Retrieval

*   **Invocation of `LegalKnowledgeTool`:**
    *   The `LegalConsultationAgent` (as part of its sequential workflow) invokes the `LegalKnowledgeTool`.
*   **Inputs to `LegalKnowledgeTool`:**
    *   `query`: The user's original textual query.
    *   `jurisdiction`: This could be:
        *   Explicitly asked from the user in a prior step or as part of an initial form.
        *   Inferred from the query text if possible (e.g., "What are tenant rights in Japan?").
        *   Defaulted to a primary jurisdiction (e.g., "japanese") if not specified, with a clarification to the user.
        *   For this flow, we'll assume it's either explicitly provided or a default is used.
    *   `information_type`: The `LegalConsultationAgent` might initially request a `"general_overview"` or a combination. For a typical first pass, it might request multiple types or start with `"general_overview"` and `"case_law"`. The exact strategy can be refined. Let's assume it requests `"case_law"` and `"statute_reference"` to get specific data for the personas.
    *   `max_results`: A sensible default, e.g., 3-5 per information type.
*   **Expected Output from `LegalKnowledgeTool`:**
    *   A structured JSON object as defined in `LegalKnowledgeTool_design.md`. This will include:
        *   `query_echo`
        *   `results`: A list of found legal information items (case summaries, statute texts/citations).
        *   `errors` (if any).
        *   `disclaimer`.

### Step 3: Parallel Persona Invocation

*   **`LegalConsultationAgent` Invokes Personas:**
    *   After receiving the output from the `LegalKnowledgeTool` (and checking for critical errors), the `LegalConsultationAgent` proceeds to invoke the defined AI Lawyer Persona agents:
        *   `Cautious Advisor` (`LlmAgent`)
        *   `Zealous Advocate` (`LlmAgent`)
        *   `Pragmatic Negotiator` (`LlmAgent`)
*   **Parallel Invocation Confirmed:**
    *   This invocation is performed **in parallel**. The `LegalConsultationAgent` makes three separate, concurrent calls to these persona agents.
*   **Inputs to Each Persona Agent:** Each persona agent receives the same set of information:
    1.  **User's Original Query:** The raw textual query initially submitted by the user.
    2.  **Output from `LegalKnowledgeTool`:** The full JSON output (or a relevant, structured subset) from the `LegalKnowledgeTool`. This provides the factual legal context for the personas to analyze.

### Step 4: Persona Response Generation

*   **Concurrent Processing:**
    *   Each of the three AI Lawyer Persona `LlmAgent`s processes its inputs concurrently.
    *   Guided by their unique system prompts (defining their objectives, tone, and approach), each persona analyzes the user's query and the legal information from the `LegalKnowledgeTool`.
*   **Advice Generation:**
    *   Each persona generates a textual response string reflecting its specialized viewpoint, advice, and potential follow-up questions.

### Step 5: Aggregation and Formatting

*   **Collection of Responses:**
    *   The `LegalConsultationAgent` waits for all three persona agents to return their respective textual responses.
*   **Preparation for Presentation:**
    *   The `LegalConsultationAgent` collates these individual responses.
    *   It may add an introductory statement (e.g., "Here are a few perspectives on your situation:") and a concluding remark.
    *   The responses from each persona should be clearly demarcated and attributed (e.g., "Cautious Advisor suggests:", "Zealous Advocate advises:", "Pragmatic Negotiator recommends:").
    *   **Styling (bengo4.com inspiration):**
        *   The presentation should aim for clarity and structure, similar to how `bengo4.com` presents answers from multiple lawyers.
        *   Each persona's advice should be a distinct block of text.
        *   Headings for each persona's section should be clear.
        *   Use of formatting (like bullet points or bolding within each persona's advice, if generated by the persona or applied by the `LegalConsultationAgent`) can enhance readability.
        *   The overall layout should be clean and easy to navigate, allowing the user to compare the different opinions effectively.

### Step 6: Presentation to User

*   **Delivery of Combined Advice:**
    *   The `LegalConsultationAgent` delivers the final, aggregated, and formatted multi-perspective advice to the user through the output interface (e.g., displaying it in the chat window or on the web page).
*   **Disclaimers:**
    *   Crucially, a clear and prominent disclaimer must be included with the response. This disclaimer should state:
        *   That the information provided is generated by AI and is for informational purposes only.
        *   That it does not constitute legal advice from a qualified human legal professional.
        *   That the user should consult with a qualified lawyer for advice tailored to their specific situation.
        *   This disclaimer might be appended by the `LegalConsultationAgent` to the aggregated response, or each persona might include a version in its own output. A system-level appended disclaimer by `LegalConsultationAgent` is more reliable.

## 5. Data Flow Diagram (Conceptual - Textual Description)

1.  **User Query (Text)**
    `-->` **LegalConsultationAgent (LCA)**
2.  **LCA** `-->` (sends `query`, `jurisdiction`, `information_type`)
    `-->` **LegalKnowledgeTool (LKT)**
3.  **LKT** `-->` (returns `structured JSON legal_info`)
    `-->` **LCA**
4.  **LCA** `-->` (sends `user_query`, `legal_info` in parallel to each)
    *   `-->` **PersonaAgent1 (`Cautious Advisor`)**
    *   `-->` **PersonaAgent2 (`Zealous Advocate`)**
    *   `-->` **PersonaAgent3 (`Pragmatic Negotiator`)**
5.  **PersonaAgent1** `-->` (returns `persona1_advice_text`) `-->` **LCA**
    **PersonaAgent2** `-->` (returns `persona2_advice_text`) `-->` **LCA**
    **PersonaAgent3** `-->` (returns `persona3_advice_text`) `-->` **LCA**
    *(These return concurrently, LCA collects all)*
6.  **LCA** `-->` (formats and aggregates `persona1_advice_text`, `persona2_advice_text`, `persona3_advice_text` + disclaimers)
    `-->` **User Response (Formatted Text)**

## 6. Error Handling (Briefly)

The `LegalConsultationAgent` must be prepared to handle potential errors gracefully:

*   **`LegalKnowledgeTool` Failure:**
    *   If the `LegalKnowledgeTool` returns a significant error (e.g., API unavailable, no results found for a critical query) or fails to respond:
        *   The `LegalConsultationAgent` might inform the user that it's unable to retrieve necessary legal information at this time.
        *   It could offer the user the option to try again later or to proceed without comprehensive legal data (in which case the personas would have to rely solely on the user's query, which should be flagged).
*   **Persona Agent Failure:**
    *   If one or more persona agents fail to generate a response (e.g., due to an internal LLM error or timeout):
        *   The `LegalConsultationAgent` could present the advice from the successful personas, with a note that some perspectives are currently unavailable (e.g., "We have advice from Cautious Advisor and Pragmatic Negotiator, but Zealous Advocate's input could not be retrieved at this time.").
        *   If all personas fail, a general error message should be provided to the user.
*   **Input Validation Errors:**
    *   If the initial user query is invalid (e.g., empty, too short, unintelligible), the `LegalConsultationAgent` should prompt the user to provide a clearer or more detailed query.
*   **Timeouts:**
    *   The `LegalConsultationAgent` should have timeouts for calls to the `LegalKnowledgeTool` and persona agents to prevent indefinite waiting. If a timeout occurs, it should be handled similarly to a failure of that component.

By addressing these potential failure points, the `LegalConsultationAgent` can provide a more robust and user-friendly experience.
