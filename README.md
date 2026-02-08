<h1 align="center">Agentic Vector RAG</h1>

<p align="center">
  <strong>A personal Agentic Vector RAG system which uses LangGraph, LangChain, conversation history, and question clarification from human feedback. It's best suitable for understanding and summarizing personal PDF documents.</strong>
</p>

## Overview

This repository showcases a practical implementation of an **Agentic RAG (Retrieval-Augmented Generation)** system built with LangGraph, designed to stay lightweight while demonstrating powerful agent-driven behaviors. The system goes beyond basic RAG by introducing reasoning, coordination, and self-improvement mechanisms. Currently, the system supports PDF documents only as input for conversational interactions. It uses Qdrant as the vector storage for efficient similarity search. It implements:

- **Multi-Agent Map-Reduce**: Breaks complex user questions into smaller sub-queries that can be processed in parallel by multiple agents, then aggregates the results to produce more complete and well-reasoned final answers.
- **Agent Orchestration**: Leverages LangGraph to coordinate multiple agent steps—such as retrieval, evaluation, and refinement—into a structured, traceable workflow instead of a linear pipeline.
- **Intelligent Evaluation**: Evaluates the relevance and usefulness of retrieved information at the individual chunk level, ensuring that only high-quality context is passed to the generation step.
- **Hierarchical Indexing**: Combines fine-grained and coarse-grained retrieval by searching over small, focused child chunks for precision, then expanding to larger parent chunks to provide richer contextual grounding for generation.
- **Hybrid Search**: Integrates dense semantic embeddings with sparse BM25 scoring to balance semantic relevance and keyword matching.
- **Conversation Memory**: Preserves dialogue history across multiple user interactions, allowing the system to maintain context and respond coherently in ongoing conversations rather than treating each query in isolation.
- **Query Clarification**: Detects vague or underspecified user queries and either reformulates them into clearer search queries or explicitly asks the user for clarification, improving retrieval accuracy from the start.
- **Self-Correction**: Monitors the adequacy of retrieved results and automatically triggers follow-up searches or alternative strategies when the initial retrieval does not meet quality thresholds.
- **Modular architecture**: Designed with interchangeable components, allowing you to easily replace or extend individual parts of the system (such as the LLM, retriever, or evaluator) without impacting the overall workflow.
- **Simple web UI**: Includes a complete, end-to-end Gradio application that supports document upload, indexing, and querying, making it easy to interact with and manage the system.

This approach balances the accuracy of fine-grained retrieval with the broader context of larger document sections, while maintaining awareness of conversational history, clarifying ambiguous queries, and answering complex, multi-part questions through parallel agent execution. Its modular design allows each component—from document ingestion to retrieval and reasoning—to be independently customized or replaced without disrupting the overall system.

---

## PDF conversion to Markdown file for RAG system

Converting PDF documents into Markdown is often the most crucial step when building a high-quality RAG (Retrieval-Augmented Generation) system. Markdown offers an ideal middle ground: it retains the structural hierarchy of the original document—such as headings, lists, tables, code blocks, and formulas—while remaining lightweight and immediately usable by LLMs without requiring heavy post-processing.

**Why choose Markdown over plain text or JSON?**

Although plain text extraction is fast and JSON provides explicit structure, Markdown is particularly well-suited for RAG workflows because it:

- **Preserves document hierarchy**: Headings, subheadings, and lists remain intact, helping LLMs understand section boundaries, relationships, and overall flow.
- **Maintains semantic cues**: Formatting elements like bold text, italics, and code blocks provide additional context that improves comprehension and grounding.
- **Represents complex content naturally**: Tables, code snippets, mathematical expressions, and blockquotes are captured in a standardized and readable form.
- **Balances human and machine readability**: Unlike JSON’s verbose, schema-driven format or plain text’s lack of structure, Markdown is intuitive for both humans and language models.
- **Enables effective chunking**: Clear structural markers (headers, paragraphs) make it easier to split documents into meaningful chunks for retrieval.

By comparison, plain text strips away all formatting and hierarchy, making it difficult for retrieval systems to distinguish titles, metadata, and body content. JSON can encode structure, but it is often verbose, schema-dependent, and inefficient for large, text-heavy documents. Markdown naturally bridges this gap. That's why, this repository uses Markdown for RAG.

## How It Works

### Document Preparation: Hierarchical Indexing

Before queries can be answered effectively, documents are processed using a two-level hierarchical indexing strategy:

- **Parent Chunks**: Large sections based on Markdown headers (H1, H2, H3) to preserve overall context.
- **Child Chunks**: Smaller, fixed-size segments derived from parent chunks for precise retrieval.

This structure ensures that the system combines the **search precision of fine-grained chunks** with the **contextual depth of larger sections**, supporting both accurate and contextually rich answers.

---

### Question Processing: Four-Stage Intelligent Workflow
```
User Question → Conversation History Analysis → Question Clarification →
Agent Reasoning → Search relevant Child Chunks → Evaluate Relevance →
(If needed) → Retrieve Parent Chunks → Generate and Return Answer
```

#### Stage 1: Conversation History Understanding
- Extracts context from recent conversation history to maintain coherence.
- Ensures smooth dialogue continuity across multiple user queries.

#### Stage 2: Question Clarification

The system intelligently interprets the user’s input to improve retrieval and response quality:
1. **Resolves references** - Translates ambiguous references, e.g.,Converts "How do I update it?" → "How do I update python code?"
2. **Splits complex questions** - Breaks multi-part queries into focused sub-queries.
3. **Detects unclear queries** - Identifies vague, nonsensical, or inappropriate inputs.
4. **Requests clarification** - Engages human feedback when the system cannot confidently interpret the question.
5. **Rewrites for retrieval** - Rewrites queries using precise, keyword-rich language to improve search results.

#### Stage 3: Intelligent Retrieval

**Multi-Agent Map-Reduce Architecture:**

For complex or multi-part queries, the system automatically spawns parallel agent subgraphs using LangGraph’s `Send` API. Each agent handles a single sub-query independently through the full retrieval workflow:

1. Searches child chunks for precise results.
2. Evaluates whether the retrieved information is sufficient.
3. Retrieves parent chunks for additional context if needed.
4. Extracts and synthesizes answers.
5. Self-corrects and re-queries when results are incomplete.

All agent outputs are then aggregated into a single, coherent answer.

#### Stage 4: Answer Generation

- Combines information from retrieved chunks (or multiple agents) into a clear, accurate, and contextually relevant answer.
- Produces responses that are directly aligned with the user’s query while preserving conversational flow.

## Installation & Usage

Sample pdf files can be found here: [javascript](https://www.tutorialspoint.com/javascript/javascript_tutorial.pdf), [blockchain](https://blockchain-observatory.ec.europa.eu/document/download/1063effa-59cc-4df4-aeee-d2cf94f69178_en?filename=Blockchain_For_Beginners_A_EUBOF_Guide.pdf), [microservices](https://cdn.studio.f5.com/files/k6fem79d/production/5e4126e1cefa813ab67f9c0b6d73984c27ab1502.pdf), [fortinet](https://www.commoncriteriaportal.org/files/epfiles/Fortinet%20FortiGate_EAL4_ST_V1.5.pdf(320893)_TMP.pdf)  

### 1. Install Dependencies

**Configure LLM Provider (OLLAMA)**

Install Ollama and download the model:

```bash
# Install Ollama from https://ollama.com
ollama pull qwen3:4b-instruct-2507-q4_K_M
```

**Clone repo and install dependencies**

```bash
# Clone the repository
git clone <repo-url>
cd AGENTIC-VECTOR-RAG

# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.\.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python src/app.py
```

**Enjoy chatting** via local URL (`http://127.0.0.1:7860`)
