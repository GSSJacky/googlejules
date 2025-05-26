# LegalKnowledgeTool Design Document

## 1. Tool Name

`LegalKnowledgeTool`

## 2. Purpose

The `LegalKnowledgeTool` is designed to provide access to a comprehensive repository of Japanese and international legal information. This includes, but is not limited to, general legal principles, specific case law, statutory references, and legal precedents. It will serve as a callable tool for ADK (Agent Development Kit) agents, such as the `LegalConsultationAgent`, enabling them to retrieve factual legal data required to inform their advice, analysis, and responses.

## 3. ADK Tool Type

Within the Google ADK framework, the `LegalKnowledgeTool` would be implemented and registered as a **`FunctionTool`**. This classification is appropriate because the tool encapsulates a specific, callable functionality—retrieving legal information—that accepts defined inputs (parameters) and produces structured outputs (JSON). It does not manage a conversational flow itself but acts as a specialized service that other agents can invoke as needed.

## 4. Input Parameters

The `LegalKnowledgeTool` will accept the following parameters in its input schema, typically provided as a JSON object:

*   `query`: (string, required)
    *   Description: The specific legal question, topic, keyword(s), case citation, or legal concept the user or agent is inquiring about. This string will be the primary basis for the search.
    *   Example: "What are the criteria for 'fair use' in Japanese copyright law?" or "Landmark cases related to digital privacy in the European Union."
*   `jurisdiction`: (string, required, enum: `"japanese"`, `"international"`, `"both"`)
    *   Description: Specifies the legal and geographical context for the query.
    *   `"japanese"`: Focuses the search on Japanese laws, regulations, judicial precedents, and legal commentary.
    *   `"international"`: Focuses the search on international treaties, conventions, case law from international courts (e.g., ICJ, ICC, ECHR), and comparative legal analyses.
    *   `"both"`: Instructs the tool to consider both Japanese and international sources where applicable, potentially looking for interactions or comparisons.
*   `information_type`: (string, required, enum: `"general_overview"`, `"case_law"`, `"statute_reference"`)
    *   Description: Specifies the desired nature or format of the legal information to be retrieved.
    *   `"general_overview"`: Requests a summary, explanation, or discussion of a legal concept, area of law, or legal principle.
    *   `"case_law"`: Requests specific court cases, judicial decisions, precedents, or summaries thereof.
    *   `"statute_reference"`: Requests specific laws, articles, sections of legal codes, regulations, or treaties.
*   `max_results`: (integer, optional, default: 5)
    *   Description: The maximum number of distinct items (e.g., case law examples, statute references) to return. This parameter is primarily relevant when `information_type` is `"case_law"` or `"statute_reference"`. If omitted, a default value (e.g., 5) will be used.

## 5. Output Structure (JSON)

The tool will return a JSON object with a clearly defined structure to ensure predictable parsing by the calling agent.

```json
{
  "query_echo": {
    "query": "The original query string",
    "jurisdiction": "The specified jurisdiction",
    "information_type": "The specified information type",
    "max_results_requested": 5 // The max_results value used
  },
  "summary_section": { // Populated if information_type was 'general_overview', null otherwise
    "title": "General Overview of [Topic from Query]",
    "overview_text": "A synthesized textual summary of the legal topic...",
    "sources_consulted": ["Gemini General Knowledge", "LegalScholarlyDatabase"]
  },
  "results": [ // List of detailed findings. Empty if no results or error.
    {
      "id": "unique_result_identifier_string",
      "source": "e.g., Gemini General Knowledge, D1-Law API, courts.go.jp, ELaws API, Westlaw, LexisNexis",
      "type": "e.g., legal_principle, case_summary, statute_text, statute_citation, treaty_article",
      "title": "e.g., Relevant Case: Tanaka v. Suzuki (2023)",
      "content": "The actual legal information text. This could be a paragraph explaining a principle, a detailed summary of a case including key arguments and holdings, or the full text of a statute article.",
      "jurisdiction_specifics": "e.g., Japan - Patent Act Article 29, International - Berne Convention Article 10",
      "relevance_score": 0.91, // Optional: a score from 0.0 to 1.0
      "url": "Optional: URL to the source document if available (e.g., link to case on courts.go.jp or statute on e-Gov Japan)",
      "date_retrieved": "YYYY-MM-DDTHH:MM:SSZ",
      "metadata": { // Additional structured data based on 'type'
        // Example for 'case_summary'
        "case_number": "Heisei 30 (Wa) No. 12345",
        "court": "Tokyo District Court",
        "date_of_decision": "2023-03-15",
        "keywords": ["copyright", "software", "damages"],
        // Example for 'statute_reference'
        "statute_name": "Japanese Civil Code",
        "article_number": "Article 709",
        "chapter_section": "Chapter 5: Torts"
      }
    }
    // ... more results up to max_results
  ],
  "errors": [ // Optional: list of error objects if any part of the process failed
    {
      "code": "e.g., BACKEND_API_UNAVAILABLE, NO_RESULTS_FOUND, QUERY_AMBIGUOUS, INPUT_VALIDATION_ERROR",
      "message": "A descriptive error message for the agent or for logging.",
      "source_system": "e.g., D1-Law API" // Optional: which system reported the error
    }
  ],
  "disclaimer": "The information provided by LegalKnowledgeTool is for informational purposes only and does not constitute legal advice. Consult with a qualified legal professional for specific advice."
}
```

**Key Output Fields Explained:**

*   `query_echo`: Confirms the parameters received by the tool for traceability.
*   `summary_section`: If `information_type` was `"general_overview"`, this object will contain:
    *   `title`: A dynamically generated title reflecting the query topic.
    *   `overview_text`: The synthesized textual summary of the legal topic.
    *   `sources_consulted`: An array of strings listing the primary backends or knowledge bases used to generate the overview (e.g., "Gemini General Knowledge").
    This field will be `null` if `information_type` is not `"general_overview"`.
*   `results`: An array of objects, each representing a discrete piece of retrieved legal information.
    *   `id`: A unique identifier for the result item (e.g., a hash of key content or a DB ID).
    *   `source`: The primary origin of the data (e.g., "D1-Law API," "courts.go.jp," "Gemini General Knowledge").
    *   `type`: The category of legal information (e.g., `"legal_principle"`, `"case_summary"`, `"statute_text"`, `"statute_citation"`).
    *   `title`: A human-readable title for the result item, suitable for display (e.g., "Case: Tanaka v. Suzuki - Copyright Infringement").
    *   `content`: The core textual data. This could be an explanation of a legal principle, a summary of a case (including facts, arguments, holding, and reasoning), or the text of a statute.
    *   `jurisdiction_specifics`: Further details about the jurisdiction if applicable (e.g., "Japan - Patent Act Article 29," "International - Berne Convention Article 10").
    *   `relevance_score`: (Optional) A numerical value (e.g., 0.0 to 1.0) indicating the estimated relevance of this item to the input `query`.
    *   `url`: (Optional) A direct URL to the source document, case, or statute, if available and publicly accessible.
    *   `date_retrieved`: An ISO 8601 timestamp indicating when the information was fetched by the tool.
    *   `metadata`: A flexible object to hold additional structured data specific to the `type` of result. For example:
        *   If `type` is `"case_summary"`: `case_number`, `court`, `date_of_decision`, `keywords`.
        *   If `type` is `"statute_reference"`: `statute_name`, `article_number`, `chapter_section`.
*   `errors`: An array of error objects. This will be populated if any part of the information retrieval or processing failed. Each error object may contain:
    *   `code`: A machine-readable error code (e.g., `"BACKEND_API_UNAVAILABLE"`, `"NO_RESULTS_FOUND"`, `"INPUT_VALIDATION_ERROR"`).
    *   `message`: A human-readable description of the error.
    *   `source_system`: (Optional) The backend system or component that reported the error.
*   `disclaimer`: A standard legal disclaimer to be included in all responses, reminding the user that the tool's output is not legal advice.

## 6. Core Logic (Conceptual)

1.  **Input Validation & Initialization:**
    *   Validate all input parameters against their expected types, formats, and constraints (e.g., enum values, required fields). If validation fails, populate the `errors` array with an appropriate error object and return immediately.
    *   Initialize the response JSON structure with default empty values (e.g., `summary_section: null`, `results: []`, `errors: []`).

2.  **Query Augmentation & Understanding (Optional LLM Step):**
    *   The raw `query` string might be processed by an internal LLM (e.g., Gemini) to:
        *   **Expand:** Add relevant legal synonyms, related terms, or common phrasings.
        *   **Identify Entities:** Extract key legal concepts, names, jurisdictions, or date ranges mentioned in the query.
        *   **Translate:** If the query language differs from the target database language (e.g., English query for Japanese databases), translate keywords or the entire query.
        *   **Clarify:** If the query is ambiguous, the LLM might attempt to formulate a clearer version or identify areas needing clarification (though the tool itself won't ask back; it would note ambiguity).

3.  **Backend Source Selection & Query Dispatch Strategy:**
    *   A sophisticated routing mechanism (rule-based, or potentially a small, specialized LLM) determines the most appropriate backend data source(s) to query based on `jurisdiction`, `information_type`, and insights from the query understanding step.
    *   **If `information_type` is `"general_overview"`:**
        *   Primarily query a large language model (e.g., Gemini) using a carefully crafted prompt that includes the user's `query` and the specified `jurisdiction`. The aim is to generate a comprehensive, explanatory text.
        *   Optionally, this can be supplemented by querying curated legal encyclopedias or scholarly databases if APIs are available, and their content can be summarized.
    *   **If `information_type` is `"case_law"`:**
        *   If `jurisdiction` is `"japanese"` or `"both"`:
            *   Prioritize querying specialized Japanese legal databases via API (e.g., D1-Law, Lexis AS ONE, TKC Law Library - assuming API access).
            *   Query publicly accessible Japanese court websites (e.g., `courts.go.jp`). This might involve web scraping if no official API exists, which requires careful design for politeness (rate limiting, user-agent strings) and robustness against website structure changes.
        *   If `jurisdiction` is `"international"` or `"both"`:
            *   Query databases for international law (e.g., WorldLII, HUDOC for ECHR, UN Treaty Series databases, specific international tribunal websites like ICC, ICJ).
            *   Utilize APIs of commercial legal research platforms (e.g., Westlaw, LexisNexis, Bloomberg Law) if the deployment environment has subscriptions and API access.
    *   **If `information_type` is `"statute_reference"`:**
        *   If `jurisdiction` is `"japanese"` or `"both"`:
            *   Query the Japanese e-Government Law Search (e-Gov法令検索) – ideally via an API if one exists, or by constructing targeted search URLs for scraping specific statutes or articles.
        *   If `jurisdiction` is `"international"` or `"both"`:
            *   Query databases of international treaties (e.g., UN Treaty Collection).
            *   Access national legislative databases of key foreign countries if relevant and accessible via API.
    *   The (potentially augmented) `query` is adapted to the specific query syntax, language, and parameter requirements of each selected backend API or search mechanism.
    *   Queries to multiple backends might be dispatched in parallel to optimize response time.

4.  **Information Retrieval, Parsing, and Normalization:**
    *   Fetch data from the targeted backend(s). Handle timeouts and connection errors gracefully.
    *   For each piece of data retrieved:
        *   Parse it from its native format (e.g., XML from an API, HTML from a webpage, JSON from another service).
        *   Normalize the parsed data into the standardized `results` object structure defined in Section 5. This involves:
            *   Extracting and mapping fields like `source`, `type`, `title`, `content`, `url`.
            *   Populating the `metadata` object with specific details (e.g., case numbers for case law).
            *   Setting `jurisdiction_specifics`.
            *   Recording the `date_retrieved`.
        *   Attempt to calculate or retrieve a `relevance_score`. If provided by the backend, use it. Otherwise, a simple heuristic (e.g., keyword match density) or an LLM-based assessment could be applied.

5.  **Content Synthesis & Summary Generation (for "general_overview"):**
    *   If `information_type` was `"general_overview"`, the text generated by the LLM (or aggregated and summarized texts from other sources) is placed into `summary_section.overview_text`.
    *   The `summary_section.title` is generated based on the input `query`.
    *   `summary_section.sources_consulted` is populated.

6.  **Result Aggregation, Deduplication, and Ranking:**
    *   Combine results from all queried backends into a single list.
    *   (Optional but recommended) Deduplicate results if multiple sources return substantially the same information (e.g., the same case summary from different databases). This can be done by comparing key fields like case numbers, URLs, or content hashes.
    *   Rank the aggregated results based on `relevance_score` (primary), date of information (e.g., newer cases might be preferred), source reliability, or other domain-specific heuristics.
    *   Enforce the `max_results` limit for `case_law` and `statute_reference` types by selecting the top-N ranked items.

7.  **Error Handling & Finalization:**
    *   If any backend API call failed or returned errors, these are logged internally and also added as structured objects to the `errors` array in the output JSON. The tool should aim to return partial results if some sources succeed while others fail.
    *   If no relevant information is found after querying all appropriate sources, this is indicated by an empty `results` list and potentially a specific error object in the `errors` array (e.g., code: `"NO_RESULTS_FOUND"`).
    *   The standard `disclaimer` is added to the output JSON.

## 7. Example Usage (Conceptual)

**Scenario:** The `LegalConsultationAgent` needs to find information about the "Statute of Limitations for contract disputes in Japan."

**1. Agent Invokes the `LegalKnowledgeTool`:**

The agent, upon receiving or inferring this need, would formulate a call to the `LegalKnowledgeTool`. Conceptually, within an ADK Python environment:

```python
# Conceptual ADK agent code snippet
try:
    tool_response_json = adk.tools.call_tool(
        tool_name="LegalKnowledgeTool",
        parameters={
            "query": "Statute of Limitations for contract disputes in Japan",
            "jurisdiction": "japanese",
            "information_type": "statute_reference", // Could also be "general_overview"
            "max_results": 2
        }
    )
    # The agent would then parse tool_response_json (which is a Python dict/list)
    # For example, to access results:
    # if tool_response_json.get("results"):
    #     for item in tool_response_json["results"]:
    #         print(f"Title: {item.get('title')}, Content: {item.get('content')[:100]}...")
    # elif tool_response_json.get("errors"):
    #     print(f"LegalKnowledgeTool reported errors: {tool_response_json['errors']}")

except adk.ToolError as e:
    # Handle exceptions if the tool call itself fails (e.g., tool not found, network issue)
    print(f"Error calling LegalKnowledgeTool: {e}")
```

**2. Example of Expected JSON Output from `LegalKnowledgeTool`:**

```json
{
  "query_echo": {
    "query": "Statute of Limitations for contract disputes in Japan",
    "jurisdiction": "japanese",
    "information_type": "statute_reference",
    "max_results_requested": 2
  },
  "summary_section": null,
  "results": [
    {
      "id": "statute_jcc_art166_20240728",
      "source": "ELaws API", // (e-Gov法令検索)
      "type": "statute_reference",
      "title": "Japanese Civil Code - Article 166 (Extinctive Prescription - General)",
      "content": "Article 166 (1) A claim shall be extinguished by prescription if the obligee does not exercise the right for five years from the time when the obligee became aware that the right could be exercised, or for ten years from the time when the right could be exercised. (2) With regard to a claim for damages for loss or damage arising from a tort, the provisions of the preceding paragraph shall apply if the victim or the legal representative thereof does not exercise the right within three years from the time when the victim or legal representative became aware of such loss or damage and of the identity of the person who caused it, or within twenty years from the time when the tort was committed.",
      "jurisdiction_specifics": "Japan - Civil Code (Act No. 89 of 1896)",
      "relevance_score": 0.95,
      "url": "https://elaws.e-gov.go.jp/document?lawid=129AC0000000089_20230401_503AC0000000034", // Example URL
      "date_retrieved": "2024-07-28T11:00:00Z",
      "metadata": {
        "statute_name": "Civil Code (Act No. 89 of 1896)",
        "article_number": "Article 166",
        "chapter_section": "Part I General Provisions, Chapter V Juristic Acts, Section 5 Extinctive Prescription"
      }
    },
    {
      "id": "statute_jcc_art167_20240728",
      "source": "ELaws API",
      "type": "statute_reference",
      "title": "Japanese Civil Code - Article 167 (Extinctive Prescription of Claims other than those based on Juristic Act)",
      "content": "Article 167 (1) A claim other than one based on a juristic act shall be extinguished by prescription if it is not exercised for ten years from the time when the right could be exercised. (2) The provisions of the preceding paragraph shall also apply to a claim for the return of unjust enrichment.",
      "jurisdiction_specifics": "Japan - Civil Code (Act No. 89 of 1896)",
      "relevance_score": 0.88,
      "url": "https://elaws.e-gov.go.jp/document?lawid=129AC0000000089_20230401_503AC0000000034", // Example URL
      "date_retrieved": "2024-07-28T11:00:00Z",
      "metadata": {
        "statute_name": "Civil Code (Act No. 89 of 1896)",
        "article_number": "Article 167",
        "chapter_section": "Part I General Provisions, Chapter V Juristic Acts, Section 5 Extinctive Prescription"
      }
    }
  ],
  "errors": [],
  "disclaimer": "The information provided by LegalKnowledgeTool is for informational purposes only and does not constitute legal advice. Consult with a qualified legal professional for specific advice."
}
```

This comprehensive design document provides a solid foundation for the development and integration of the `LegalKnowledgeTool` within an ADK-based legal AI system.Okay, I have created the `LegalKnowledgeTool_design.md` file with the detailed design specifications as requested.
