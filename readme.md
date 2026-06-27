# ✈️ BonVoyage – AI Travel Assistant

BonVoyage is a cloud-native **AI-powered travel planning platform** that leverages a **multi-agent LLM architecture** to generate personalized travel itineraries, optimize budgets, and recommend flights and hotels based on natural language user requests. The system combines large language models, real-time travel APIs, and scalable cloud infrastructure to deliver an end-to-end intelligent travel planning experience.

---

## 🚀 Features

* 🤖 Multi-agent AI workflow for itinerary planning and optimization
* 🧠 Natural language trip planning using **Llama 3.1 (8B)**
* ✈️ Real-time flight and hotel recommendations via **RapidAPI**
* 💰 Budget-aware travel optimization
* 📋 AI-generated itinerary summaries
* 🔐 Secure authentication and session management
* ⚡ Redis-based caching for improved response times
* ☁️ Fully deployed on AWS using containerized services

---

## 🏗️ System Architecture

```
                 User
                  │
                  ▼
         React Frontend (S3)
                  │
                  ▼
        FastAPI Backend (EC2)
                  │
                  ▼
        Intent Extraction Agent
                  │
                  ▼
        ┌──────────────────────┐
        │ Multi-Agent Pipeline │
        ├──────────────────────┤
        │ Planner Agent        │
        │ Budget Agent         │
        │ Summary Agent        │
        └──────────────────────┘
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
RapidAPI Flights/Hotels     PostgreSQL (RDS)
                              │
                              ▼
                          Redis Cache
                              │
                              ▼
                  Personalized Travel Plan
```

---

## ⚙️ Workflow

1. Users describe their travel requirements through the React web application.
2. The FastAPI backend authenticates requests and forwards them to the AI orchestration layer.
3. An **Intent Extraction Agent** identifies travel preferences, destinations, dates, and budget constraints.
4. Specialized AI agents collaboratively:

   * Generate travel itineraries
   * Optimize travel budgets
   * Recommend flights and hotels
   * Produce concise itinerary summaries
5. Flight and accommodation information is retrieved in real time using RapidAPI.
6. Generated travel plans are stored in PostgreSQL while Redis caches frequently accessed data.
7. The optimized itinerary is returned to the frontend for an interactive user experience.

---

## 🛠️ Technology Stack

### Frontend

* React
* JavaScript
* HTML/CSS

### Backend

* FastAPI
* Python
* Pydantic
* SQLAlchemy

### Artificial Intelligence

* Hugging Face Inference API
* Llama 3.1 (8B)
* Multi-Agent LLM Orchestration
* Prompt Engineering

### Data Layer

* PostgreSQL
* Redis

### External APIs

* RapidAPI Flights-Sky
* Hotel Search APIs

### Cloud & DevOps

* Amazon EC2
* Amazon S3
* Amazon RDS
* Amazon ECR
* Docker
* Docker Compose

---

## ☁️ Deployment

| Component          | Service                 |
| ------------------ | ----------------------- |
| Frontend           | Amazon S3               |
| Backend API        | Amazon EC2              |
| Database           | Amazon RDS (PostgreSQL) |
| Container Registry | Amazon ECR              |
| Cache              | Redis                   |
| Deployment         | Docker & Docker Compose |

---

## 🎯 Highlights

* Designed an end-to-end **multi-agent AI travel assistant** capable of reasoning over user preferences and generating personalized itineraries.
* Integrated **LLM-powered planning** with real-time flight and hotel data retrieval.
* Built a scalable full-stack architecture using **FastAPI, React, PostgreSQL, Redis, and AWS**.
* Containerized the application using Docker for portable and reproducible deployments.
* Optimized system responsiveness through Redis caching and cloud-native deployment on AWS.
