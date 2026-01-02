# Gen AI Examples & Demos

A comprehensive collection of Generative AI examples, demos, and tutorials covering various aspects of modern AI development including LLMs, prompt engineering, RAG systems, agents, and more.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Examples](#examples)
  - [Hello World](#hello-world)
  - [Tokenization](#tokenization)
  - [Prompt Engineering](#prompt-engineering)
  - [RAG Systems](#rag-systems)
  - [LangGraph](#langgraph)
  - [Agents](#agents)
  - [Voice Agent](#voice-agent)
  - [Other Examples](#other-examples)
- [Environment Variables](#environment-variables)
- [Technologies Used](#technologies-used)

## Overview

This repository contains practical examples and implementations of various Generative AI concepts, from basic "Hello World" applications to advanced AI agents with memory and tool-calling capabilities.

## Prerequisites

- Python 3.8+
- Node.js (for todo_app)
- Docker & Docker Compose (for database services)
- OpenAI API Key
- Google Gemini API Key (for some examples)
- Neo4j Database (for memory agent)
- Qdrant Vector Database (for RAG examples)
- Redis (for queue system)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gen-ai
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with required API keys (see [Environment Variables](#environment-variables))

4. Start required services using Docker Compose:
```bash
# For RAG examples
cd rag && docker-compose up -d

# For Memory Agent
cd mem_agent && docker-compose up -d

# For LangGraph with checkpoints
cd langgraph && docker-compose up -d
```

## Project Structure

```
gen-ai/
├── 01_tokenization/        # Tokenization examples using tiktoken
├── hello_world/            # Basic OpenAI & Gemini integration examples
├── hf_basic/              # HuggingFace basics
├── image/                 # Image processing with AI
├── langgraph/             # LangGraph examples with state management
├── mem_agent/             # Memory-enabled agent using Mem0
├── ollama-fastapi/        # FastAPI server with Ollama integration
├── prompts/               # Prompt engineering techniques
│   ├── zero.py           # Zero-shot prompting
│   ├── few.py            # Few-shot prompting
│   ├── cot.py            # Chain of Thought prompting
│   └── persona.py        # Persona-based prompting
├── rag/                   # RAG implementation with Qdrant
├── rag_queue/             # RAG with Redis Queue for async processing
├── todo_app/              # Simple HTML/JS todo application
├── voice_agent/           # Voice-enabled AI agent
└── weather_agent/         # Weather agent with tool calling
```

## Examples

### Hello World

Basic examples demonstrating OpenAI and Google Gemini integration.

**Location:** `hello_world/`

```bash
cd hello_world
python main.py
```

Features:
- Basic OpenAI API integration
- Gemini API integration
- Simple chat completion examples

### Tokenization

Learn how tokenization works in LLMs using tiktoken.

**Location:** `01_tokenization/`

```bash
cd 01_tokenization
python main.py
```

Features:
- Token encoding/decoding
- Understanding token counts
- Token visualization

### Prompt Engineering

Explore different prompt engineering techniques.

**Location:** `prompts/`

#### Zero-Shot Prompting
```bash
cd prompts
python zero.py
```
Direct instruction without examples.

#### Few-Shot Prompting
```bash
python few.py
```
Learning from provided examples.

#### Chain of Thought (CoT)
```bash
python cot.py
```
Step-by-step reasoning with tool calling capabilities.

#### Persona-Based Prompting
```bash
python persona.py
```
Role-playing and persona-specific responses.

### RAG Systems

#### Basic RAG

**Location:** `rag/`

Retrieval-Augmented Generation using Qdrant vector database.

```bash
# Start Qdrant
cd rag
docker-compose up -d

# Index documents
python index.py

# Start chatting
python chat.py
```

Features:
- Document ingestion from PDF
- Vector embeddings with OpenAI
- Similarity search with Qdrant
- Context-aware responses

#### RAG with Queue System

**Location:** `rag_queue/`

Scalable RAG system with async processing using Redis Queue.

```bash
# Start Redis
cd rag_queue
docker-compose up -d

# Start worker
python -m queues.worker

# Start server
uvicorn server:app --reload

# Use the API
curl -X POST "http://localhost:8000/chat?query=your_question"
```

Features:
- Asynchronous query processing
- Job queue management
- Status tracking
- FastAPI integration

### LangGraph

**Location:** `langgraph/`

State management and graph-based workflows for LLM applications.

#### Basic LangGraph
```bash
cd langgraph
python chat.py
```

#### LangGraph with Checkpoints
```bash
# Start MongoDB
docker-compose up -d

python chat_checkpoint.py
```

Features:
- State management
- Multi-node workflows
- Conversation checkpointing
- MongoDB persistence

### Agents

#### Weather Agent

**Location:** `weather_agent/`

AI agent with tool-calling capabilities and Chain of Thought reasoning.

```bash
cd weather_agent
python agent.py
```

Features:
- Chain of Thought prompting
- Multiple tool support (weather API, system commands)
- Step-by-step reasoning
- Structured output parsing

Tools available:
- `get_weather(city)`: Fetch weather information
- `run_command(cmd)`: Execute system commands

#### Memory Agent

**Location:** `mem_agent/`

Conversational agent with persistent memory using Mem0.

```bash
# Start Neo4j and Qdrant
cd mem_agent
docker-compose up -d

python memory.py
```

Features:
- Persistent conversation memory
- Neo4j graph store for relationships
- Qdrant vector store for semantic search
- User-specific memory isolation
- Context-aware responses

### Voice Agent

**Location:** `voice_agent/`

Voice-enabled AI agent with Speech-to-Text and Text-to-Speech capabilities.

```bash
cd voice_agent
python main.py
```

Features:
- Real-time speech recognition
- Google Speech-to-Text
- OpenAI Text-to-Speech
- Voice-optimized responses
- Ambient noise adjustment

### Other Examples

#### Ollama FastAPI Server
**Location:** `ollama-fastapi/`

FastAPI server for Ollama integration.

```bash
cd ollama-fastapi
uvicorn server:app --reload
```

#### HuggingFace Basics
**Location:** `hf_basic/`

Basic HuggingFace transformers examples.

```bash
cd hf_basic
python main.py
```

#### Image Processing
**Location:** `image/`

AI-powered image processing examples.

```bash
cd image
python main.py
```

#### Todo App
**Location:** `todo_app/`

Simple frontend todo application.

```bash
cd todo_app
# Open index.html in your browser
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key

# Neo4j (for memory agent)
NEO_CONNECTION_URI=bolt://localhost:7687
NEO_USER_NAME=neo4j
NEO_PASSWORD=your_neo4j_password

# Qdrant (usually runs locally)
QDRANT_URL=http://localhost:6333

# Redis (for queue system)
REDIS_URL=redis://localhost:6379
```

## Technologies Used

### AI/ML Frameworks
- **OpenAI API** - GPT models and embeddings
- **Google Gemini** - Alternative LLM provider
- **LangChain** - LLM application framework
- **LangGraph** - State management for LLM apps
- **Mem0** - Memory layer for AI agents
- **Ollama** - Local LLM deployment

### Vector Databases
- **Qdrant** - Vector similarity search
- **Neo4j** - Graph database for relationships

### Other Technologies
- **FastAPI** - Modern web framework
- **Redis Queue (RQ)** - Job queue system
- **PyPDF** - PDF processing
- **SpeechRecognition** - Speech-to-text
- **PyAudio** - Audio processing
- **tiktoken** - Tokenization
- **Transformers** - HuggingFace models
- **Pydantic** - Data validation

## Key Concepts Demonstrated

### Prompt Engineering
- Zero-shot prompting
- Few-shot prompting
- Chain of Thought (CoT)
- Persona-based prompting

### RAG (Retrieval-Augmented Generation)
- Document indexing
- Vector embeddings
- Similarity search
- Context injection

### AI Agents
- Tool calling
- Memory systems
- Multi-step reasoning
- State management

### Production Patterns
- Async processing with queues
- API design with FastAPI
- Checkpoint/persistence
- Error handling and retries

## Contributing

Feel free to contribute by:
1. Adding new examples
2. Improving existing code
3. Fixing bugs
4. Enhancing documentation

## License

This project is for educational purposes.

## Resources

- [OpenAI Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Mem0 Documentation](https://docs.mem0.ai/)

---

**Note:** This is a learning repository. Make sure to follow best practices and security guidelines when using API keys and deploying to production.

