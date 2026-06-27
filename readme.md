# AI Travel Planner (Multi-Agent System)

A cloud-deployed travel planning platform that uses **LLM-powered agents** to generate optimized travel plans (flights, hotels, and itinerary summaries) based on user input.

## How It Works
1. User submits a trip request from the **React frontend**.
2. The request hits a **FastAPI backend** that handles authentication and trip APIs.
3. An **LLM-based intent extractor** processes the request.
4. Multiple **AI agents** (planner, budget optimizer, summarizer) generate and refine the travel plan.
5. External travel data is fetched from **RapidAPI flights-sky** APIs.
6. Results are optimized and stored in **PostgreSQL**, with caching via **Redis**.
7. The final trip plan is returned to the frontend for display.

## Tech Stack
- **Frontend:** React (Create React App)
- **Backend:** FastAPI, Pydantic
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Caching:** Redis
- **LLM:** Hugging Face Inference API (Llama 3.1 8B)
- **External APIs:** RapidAPI flights-sky (flights & hotels)
- **Orchestration:** Multi-agent pipeline (intent → planner → optimizer → summarizer)
- **Containerization:** Docker & Docker Compose

## Cloud Deployment
- **Frontend:** Amazon S3 (static hosting)
- **Backend:** EC2 instance
- **Database:** Amazon RDS (PostgreSQL)
- **Containers:** Docker images stored in Amazon ECR
- **Caching:** Redis service

