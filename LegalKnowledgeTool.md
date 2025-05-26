# LegalKnowledgeTool Design Document

## 1. Tool Name

`LegalKnowledgeTool`

## 2. Purpose

The `LegalKnowledgeTool` is designed to provide access to a wide range of Japanese and international legal information. This includes general legal principles, specific case law, and statutory references. It will serve as a callable tool for ADK agents, such as the `LegalConsultationAgent`, to retrieve factual legal data needed to inform their advice and responses.

## 3. ADK Tool Type

Within the ADK framework, the `LegalKnowledgeTool` would be implemented and registered as a **`FunctionTool`**. This is because it encapsulates a specific functionality (retrieving legal information) that takes defined inputs and produces structured outputs. It does not manage a conversation flow itself but acts as a service that other agents can call.

## 4. Input Parameters

The `LegalKnowledgeTool` will accept the following parameters in its input schema:

*   `query`: (string, required)
    *   Description: The specific legal question, topic, keyword(s), or case citation the user or agent is inquiring about.
    *   Example: "What are the requirements for patent eligibility in Japan?" or "Cases related to copyright infringement in software in international law."
*   `jurisdiction`: (string, required, enum: `"japanese"`, `"international"`, `"both"`)
    *   Description: Specifies the legal context for the query.
    *   `"japanese"`: Focuses on Japanese laws, regulations, and case law.
    *   `"international"`: Focuses on international treaties, conventions, and case law from international courts or comparative law.
    *   `"both"`: Considers both Japanese and international sources where applicable.
*   `information_type`: (string, required, enum: `"general_overview"`, `"case_law"`, `"statute_reference"`)
    *   Description: Specifies the type of legal information requested.
    *   `"general_overview"`: Requests a summary or explanation of a legal concept or area.
    *   `"case_law"`: Requests specific court cases, precedents, or judicial decisions.
    *   `"statute_reference"`: Requests specific laws, articles, or sections of legal code.
*   `max_results`: (integer, optional, default: 5)
    *   Description: The maximum number of distinct case law examples or statute references to return. This parameter is primarily relevant when `information_type` is `"case_law"` or `"statute_reference"`.

## 5. Output Structure (JSON)

The tool will return a JSON object with the following structure:

```json
{
  "query_received": {
    "query": "...",
    "jurisdiction": "...",
    "information_type": "...",
    "max_results": 0 // value provided or default
  },
  "summary": "Optional: A textual summary if information_type was 'general_overview'. Null otherwise.",
  "results": [
    {
      "source": "e.g., Gemini General Knowledge, D1-Law API, courts.go.jp, ELaws API",
      "type": "e.g., legal_principle, case_summary, statute_text, statute_citation",
      "content": "The actual legal information text. This could be a paragraph explaining a principle, a summary of a case, or the text of a statute article.",
      "jurisdiction_details": "e.g., Japan - Patent Act Article 29, International - Berne Convention",
      "relevance_score": 0.85, // Optional, a hypothetical score
      "url": "Optional: URL to the source if available (e.g., link to case on courts.go.jp or statute on e-Gov Japan)",
      "case_details": { // Optional, present if type is 'case_summary'
        "case_number": "...",
        "court": "...",
        "date_of_decision": "YYYY-MM-DD"
      },
      "statute_details": { // Optional, present if type is 'statute_text' or 'statute_citation'
        "statute_name": "e.g., Patent Act",
        "article_number": "e.g., Article 29, Paragraph 1"
      }
    }
    // ... more results
  ],
  "errors": [ // Optional, contains error messages if any occurred
    {
      "code": "e.g., DATABASE_UNAVAILABLE, NO_RESULTS_FOUND",
      "message": "Descriptive error message"
    }
  ]
}
```

**Field Descriptions:**

*   `query_received`: An echo of the input parameters for traceability.
*   `summary`: A string containing a synthesized overview if `information_type` was `"general_overview"`. Otherwise, this field will be `null`.
*   `results`: A list of objects, each representing a piece of retrieved legal information.
    *   `source`: The origin of the information (e.g., "Gemini General Knowledge" for general principles, "D1-Law API" for specific Japanese case law, "courts.go.jp" for publicly available Japanese case law, "ELaws API" for Japanese statutes).
    *   `type`: The nature of the content (e.g., `"legal_principle"`, `"case_summary"`, `"statute_text"`, `"statute_citation"`).
    *   `content`: The core textual information.
    *   `jurisdiction_details`: Specifics about the jurisdiction and legal instrument (e.g., "Japan - Civil Code Article 709").
    *   `relevance_score`: (Optional) A numerical value (e.g., 0.0 to 1.0) indicating the estimated relevance of the result to the input `query`. This might be derived from the search algorithms of the backend systems.
    *   `url`: (Optional) A direct URL to the source document or case, if available.
    *   `case_details`: (Optional) Contains structured information if the result is a case summary.
        *   `case_number`: Official case identifier.
        *   `court`: Name of the court that issued the decision.
        *   `date_of_decision`: The date the judgment was rendered.
    *   `statute_details`: (Optional) Contains structured information if the result is about a statute.
        *   `statute_name`: The official name of the law or act.
        *   `article_number`: Specific article, section, or paragraph number.
*   `errors`: A list of error objects if any part of the information retrieval failed.

## 6. Core Logic (Conceptual)

1.  **Input Validation:**
    *   Validate the input parameters (e.g., ensure `jurisdiction` and `information_type` are within the allowed enum values, `query` is not empty).
    *   Return an error if validation fails.

2.  **Query Preprocessing & Normalization:**
    *   The input `query` string might undergo some preprocessing:
        *   Keyword extraction.
        *   Expansion with synonyms or related legal terms (potentially using a small legal thesaurus or an LLM).
        *   Translation if necessary (e.g., if the query is in English but needs to target Japanese databases with Japanese terms).

3.  **Backend Source Selection & Querying Strategy:**
    *   The tool will use a rule-based or model-based strategy to decide which backend(s) to query based on `jurisdiction` and `information_type`.
    *   **If `information_type` is `"general_overview"`:**
        *   Primarily query a general knowledge base (e.g., a large language model like Gemini, appropriately prompted for legal context).
        *   `jurisdiction` will guide the LLM's focus (e.g., "Provide a general overview of contract law in Japan.").
    *   **If `information_type` is `"case_law"`:**
        *   If `jurisdiction` is `"japanese"` or `"both"`:
            *   Query specialized Japanese legal databases (e.g., D1-Law API, if available and integrated).
            *   Query publicly accessible Japanese court websites (e.g., `courts.go.jp` via scraping or a dedicated API if one exists).
        *   If `jurisdiction` is `"international"` or `"both"`:
            *   Query international law databases or search engines that index international tribunal decisions (e.g., WorldLII, HUDOC for ECHR, specific UN databases).
            *   Potentially use general web search targeted at legal academic resources or international court websites.
    *   **If `information_type` is `"statute_reference"`:**
        *   If `jurisdiction` is `"japanese"` or `"both"`:
            *   Query Japanese e-Government Law Search (e-Gov法令検索) via its API (if available) or by constructing targeted search URLs.
        *   If `jurisdiction` is `"international"` or `"both"`:
            *   Query databases of international treaties (e.g., UN Treaty Collection).
            *   Search for specific national statutes of other countries if relevant to "international" context (this might be limited in scope).
    *   The `query` string (possibly preprocessed) will be adapted to the specific API or search mechanism of the selected backend.
    *   Multiple backends might be queried in parallel or sequentially.

4.  **Information Retrieval and Normalization:**
    *   Retrieve data from the selected backend(s).
    *   Transform the retrieved data into the standardized `results` list format defined in the "Output Structure" section. This involves mapping fields, extracting relevant text snippets, and identifying URLs.
    *   Populate `source`, `type`, `content`, `url`, `case_details`, and `statute_details` as applicable.
    *   If a relevance score is provided by the backend, include it. Otherwise, it can be omitted or a simple heuristic can be applied.

5.  **Summary Generation (for "general_overview"):**
    *   If `information_type` was `"general_overview"`, and the primary source was an LLM, its response can directly form the `summary`.
    *   If multiple sources contributed, the `summary` might be a concatenation or a further LLM-powered summarization of the collected `content` from various results.

6.  **Result Aggregation and Ranking:**
    *   Combine results from different backends.
    *   (Optional) Results can be ranked based on `relevance_score` (if available) or other heuristics (e.g., source reliability, date of case).
    *   Apply `max_results` to limit the number of returned items for `case_law` and `statute_reference`.

7.  **Error Handling:**
    *   If a backend API is unreachable, log the error and attempt to continue with other sources if possible. Include an error object in the `errors` list in the output.
    *   If no relevant information is found after querying all appropriate sources, return an empty `results` list and potentially an error object indicating "NO_RESULTS_FOUND".
    *   Handle timeouts and other API-specific errors gracefully.

## 7. Example Usage (Conceptual)

**Hypothetical Call from `LegalConsultationAgent`:**

Imagine the `LegalConsultationAgent` needs to find Japanese case law related to "software copyright infringement damages."

```python
# This is a conceptual Python snippet showing how an agent might call the tool
try:
    legal_info = adk.tools.call_tool(
        tool_name="LegalKnowledgeTool",
        parameters={
            "query": "Damages awarded in software copyright infringement cases",
            "jurisdiction": "japanese",
            "information_type": "case_law",
            "max_results": 3
        }
    )
    # Process the legal_info (which will be a Python dict parsed from the JSON output)
except adk.ToolError as e:
    # Handle tool execution errors
    print(f"Error calling LegalKnowledgeTool: {e}")

```

**Example of Expected JSON Output:**

```json
{
  "query_received": {
    "query": "Damages awarded in software copyright infringement cases",
    "jurisdiction": "japanese",
    "information_type": "case_law",
    "max_results": 3
  },
  "summary": null,
  "results": [
    {
      "source": "D1-Law API",
      "type": "case_summary",
      "content": "The Tokyo District Court awarded JPY 10,000,000 in damages for copyright infringement related to unauthorized duplication and distribution of proprietary business software. The court considered the defendant's profits and the plaintiff's lost licensing revenue.",
      "jurisdiction_details": "Japan - Copyright Act",
      "relevance_score": 0.92,
      "url": "https://example.d1-law.com/case/xyz123",
      "case_details": {
        "case_number": "XYZ123-2022",
        "court": "Tokyo District Court",
        "date_of_decision": "2022-08-15"
      }
    },
    {
      "source": "courts.go.jp",
      "type": "case_summary",
      "content": "Osaka High Court upheld a lower court decision awarding damages based on the number of illegal downloads of a copyrighted game. The calculation method for damages was a key point of contention.",
      "jurisdiction_details": "Japan - Copyright Act",
      "relevance_score": 0.88,
      "url": "https://www.courts.go.jp/app/hanrei_jp/detail2?id=abc987",
      "case_details": {
        "case_number": "ABC987-2021",
        "court": "Osaka High Court",
        "date_of_decision": "2021-11-05"
      }
    }
  ],
  "errors": []
}
```
This output provides structured information that the `LegalConsultationAgent` can then use to formulate its advice, potentially citing these cases.
If `information_type` were `"general_overview"`, the `summary` field would be populated, and `results` might contain broader principles. If it were `"statute_reference"`, `results` would list specific articles from relevant laws.
