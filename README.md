🛡️ Retail Watchdog: AI Supply Chain Copilot



![alt text](https://img.shields.io/badge/Cloud-Azure_OpenAI-0078D4?logo=microsoftazure)
![alt text](https://img.shields.io/badge/Language-Python_3.11-3776AB?logo=python)
![alt text](https://img.shields.io/badge/Orchestration-LangGraph_Stateful-FF6F00)
![alt text](https://img.shields.io/badge/Safety-Human_in_the_Loop-red)


Role: Internal Operational Copilot (B2E) Status: Production-Ready MVP (Dockerized)
1. The Business Challenge (El Desafío)
En el sector Retail, la resolución de incidencias logísticas sufre de dos cuellos de botella críticos:
* Fragmentación de Datos: Los agentes pierden ~15 min saltando entre el inventario (SQL) y normativas legales (PDF) para cada ticket.
* Riesgo Financiero: Automatizar reembolsos mediante IA sin supervisión genera un riesgo de alucinación inasumible en entornos corporativos.
2. The Solution (La Solución)
Retail Watchdog no es un chatbot de FAQs; es un Agente de Razonamiento con Estado diseñado como copiloto para equipos de soporte.
1. Auditoría en Tiempo Real: Cruza datos de stock (SQL) con cláusulas de compensación (RAG).
2. Seguridad Determinista (Dual-Gate): Implementa un freno a nivel de código. El agente no puede ejecutar un reembolso sin una validación humana explícita en el chat.
3. Trazabilidad Forense: Cada acción queda registrada en un log de auditoría inmutable para cumplimiento normativo (Compliance).
Impacto: Reducción del tiempo medio de resolución (AHT) de 15 min a <10 segundos.
3. Technical Architecture (High Level)
codeMermaid

```
graph TD
    User[👤 Operations Analyst] -->|Confirm/Action| UI[💻 Chainlit UI]
    UI -->|Thread_ID| Orchestrator[🧠 LangGraph Stateful Engine]
    
    subgraph "Azure AI Foundry"
        Orchestrator <-->|Reasoning| GPT[🤖 GPT-4o]
        RAGTool <-->|Embeddings| Emb[🔤 text-embedding-3]
    end
    
    subgraph "Safety Logic (Tools)"
        Orchestrator --> Router{Decision}
        Router -->|Read| SQLTool[📊 Inventory SQL]
        Router -->|Verify| RAGTool[📜 Policy RAG]
        Router -->|Write| RefundTool[🛡️ Safety-Gate Refund]
    end
    
    subgraph "Audit & Persistence"
        RefundTool -->|Log| Audit[(📝 Audit Trail)]
        SQLTool <--> DB[(🗄️ SQLite / Azure SQL)]
        RAGTool <--> Vector[(📚 ChromaDB)]
    end
```

Advanced Features implemented:
* Stateful Memory: Uso de MemorySaver en LangGraph para mantener el contexto multicanal sin re-enviar el historial (Token Efficiency).
* Boolean Safety Gate: La herramienta de escritura exige el parámetro human_confirmed=True, forzando el protocolo HITL (Human-in-the-loop).
* Clean Architecture: Desacoplamiento total entre la lógica del agente y la interfaz de usuario.
4. How to Run (Docker)
Prerequisites
* Docker Desktop.
* Azure OpenAI Endpoint & Key.
1. Build the Image
codeBash

```
docker build -t retail-watchdog:gold .
```

2. Run the Container
codeBash

```
docker run -p 8000:8000 --env-file .env retail-watchdog:gold
```

5. System Validation (Forensic Check)
Para validar que el sistema es transaccional y no solo genera texto, tras una ejecución de reembolso, puede auditarse la base de datos interna del contenedor:
codeBash

```
docker exec -it <CONTAINER_ID> sqlite3 data/inventory.db "SELECT * FROM refunds_log;"
```

Expected Result: Registro con order_id, reason y confirmed=1.
6. Enterprise Roadmap (Gap Analysis)
FeatureMVP (Current)Enterprise ProductionDatabaseSQLite (Local)Azure SQL Database (Serverless)Secrets.env / Environment VarsAzure Key VaultSearchChromaDB (Local)Azure AI Search (Semantic Ranker)ObservabilityConsole LogsAzure Application Insights

