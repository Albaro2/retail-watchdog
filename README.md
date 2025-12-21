# 🛒 Retail Watchdog: AI Supply Chain Optimizer

![Azure](https://img.shields.io/badge/Cloud-Azure_OpenAI-0078D4?logo=microsoftazure)
![Python](https://img.shields.io/badge/Language-Python_3.11-3776AB?logo=python)
![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?logo=docker)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph_ReAct-FF6F00)

> **Status:** MVP / Proof of Concept (Ready for Container Apps)

## 1. The Business Challenge (El Desafío)
In modern Retail, the disconnection between **Inventory Systems** (SQL) and **Corporate Policies** (Unstructured PDFs) creates friction in customer support.
*   **The Problem:** Support agents take an average of **15 minutes** to cross-reference stock data with refund policies to make a decision.
*   **The Impact:** High operational costs and low NPS (Net Promoter Score) due to delays.

## 2. The Solution (La Solución)
**Retail Watchdog** is an Autonomous AI Agent (Agentic Workflow) that orchestrates complex decision-making without human intervention.
It is not a chatbot; it is a **reasoning engine** that:
1.  **Verifies** real-time stock status via SQL connections.
2.  **Retrieves** the specific applicable return policy via Vector Search (RAG).
3.  **Executes** the compliant business decision (Refund vs. Coupon).

**Result:** Resolution time reduced from 15 min to **<10 seconds**.

---

## 3. Technical Architecture (High Level)

This solution implements the **ReAct Pattern** (Reason + Act) on Azure.

```mermaid
graph TD
    User[👤 Business User] -->|Chat Interface| UI[💻 Chainlit UI]
    UI -->|Stream| Orchestrator[🧠 LangGraph Orchestrator]
    
    subgraph "Azure AI Foundry"
        Orchestrator <-->|Reasoning| GPT[🤖 GPT-4o]
        RAGTool <-->|Embeddings| Emb[🔤 text-embedding-3]
    end
    
    subgraph "Agent Logic (Nodes)"
        Orchestrator -->|Decide| Router{Decision}
        Router -->|Need Data?| SQLTool[🛠️ SQL Inventory Tool]
        Router -->|Need Rules?| RAGTool[🛠️ Policy RAG Tool]
    end
    
    subgraph "Data Persistence"
        SQLTool <-->|Query| DB[(🗄️ SQLite / Azure SQL)]
        RAGTool <-->|Search| Vector[(📚 ChromaDB / AI Search)]
    end
