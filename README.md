# 🏘️ Village Development Planner AI

> **Microsoft Reactor — Agents League: Reasoning Agents Battle**  
> Built by Bhanu Pratap | Azure AI Foundry + Python + Streamlit

---

## 🚀 What is this?

An AI-powered multi-agent system that helps governments and organizations make data-driven decisions for Indian village development. Each sector has a dedicated AI agent powered by **Azure AI Foundry (gpt-oss-120b)** that reasons through village data and provides actionable recommendations.

## 🤖 AI Agents

| Agent | Domain | Role |
|---|---|---|
| 💧 Water Agent | Water & Sanitation | Analyzes water availability, quality, infrastructure |
| 🌾 Agriculture Agent | Farming | Crop yield, irrigation, market linkage |
| ❤️ Healthcare Agent | Health | PHC access, mortality rates, schemes |
| 🎓 Education Agent | Learning | Literacy, dropout, infrastructure |
| 💼 Employment Agent | Livelihood | Unemployment, skill gaps, SHGs |
| 🏗️ Infrastructure Agent | Roads & Power | Connectivity, electricity, drainage |
| 🌳 Environment Agent | Ecology | Deforestation, waste, renewable energy |

## 🛠️ Tech Stack

- **Azure AI Foundry** — gpt-oss-120b reasoning model
- **azure-ai-inference SDK** — proper Foundry integration
- **Python + Streamlit** — web app framework
- **Plotly** — interactive charts
- **python-dotenv** — environment management

## ⚡ Quick Start

```bash
# 1. Clone and enter directory
cd village-planner-agent

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
copy .env.example .env
# Edit .env and add your Azure AI Foundry credentials

# 5. Run the app
streamlit run app.py
```

## 🔑 Environment Variables

```
AZURE_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/v1
AZURE_API_KEY=your_key_here
AZURE_DEPLOYMENT=gpt-oss-120b
```

## ✨ Features

- 📊 Real-time village development dashboard
- 🤖 7 specialized AI reasoning agents
- 💰 Smart budget allocation with charts
- 🗺️ 3-phase development roadmap
- 📋 Government scheme intelligence
- 🔬 What-If scenario simulation
- 📈 Agent-wise scoring and recommendations

## 🏆 Hackathon Track

**Agents League — Reasoning Agents Battle @ Microsoft Reactor**

This project demonstrates multi-agent reasoning where each agent independently analyzes a domain, scores it, and the orchestrator synthesizes a holistic village development plan — embodying the core principles of reasoning agent architecture.
