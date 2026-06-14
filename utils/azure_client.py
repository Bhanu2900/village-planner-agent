import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AZURE_API_KEY", "")
DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT", "gpt-oss-120b")
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://village-planner-ai-agen-resource.openai.azure.com/openai/v1")

def get_ai_response(village_name: str, data: dict, agent: str = None, scenario: str = None) -> str:
    """Call Azure AI Foundry via the azure-ai-inference SDK."""
    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.ai.inference.models import SystemMessage, UserMessage
        from azure.core.credentials import AzureKeyCredential

        # For gpt-oss-120b the endpoint must point to the deployment directly
        endpoint = f"https://village-planner-ai-agen-resource.services.ai.azure.com/models"

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(API_KEY),
        )

        agents_summary = "\n".join([
            f"- {name}: score {info['score']}/100, issues: {', '.join(info['issues'])}"
            for name, info in data["agents"].items()
        ])

        system_prompt = """You are an expert AI Village Development Planning Agent working within Microsoft Azure AI Foundry.
Your role is to analyze Indian village data and provide actionable, data-driven development recommendations.
You think step by step, consider dependencies between sectors, and prioritize high-impact interventions.
Always respond in a structured, practical manner relevant to Indian rural development context."""

        if scenario:
            user_prompt = f"""Village: {village_name}
Current development score: {data['metrics']['dev_score']}/100
Budget: ₹{data['metrics']['budget']}

Agent scores:
{agents_summary}

Scenario to simulate: {scenario}

Analyze this scenario step by step:
1. Immediate impacts
2. Secondary effects
3. Budget implications
4. Risk factors
5. Final recommendation"""

        elif agent:
            info = data["agents"].get(agent, {})
            user_prompt = f"""Village: {village_name}
Agent: {agent} Development Agent
Current score: {info.get('score', 'N/A')}/100
Key issues: {', '.join(info.get('issues', []))}

Provide a detailed {agent} sector analysis:
1. Root cause analysis of low score
2. Top 3 priority interventions
3. Specific government schemes to apply for
4. 6-month action plan
5. Expected score improvement"""

        else:
            user_prompt = f"""Village: {village_name}
Population: {data['metrics']['population']}
Development Score: {data['metrics']['dev_score']}/100
Budget: ₹{data['metrics']['budget']}

Agent scores:
{agents_summary}

Priorities: {', '.join([p['name'] for p in data['priorities']])}

As a reasoning agent, analyze this village and provide:
1. Critical assessment of current situation
2. Top 5 immediate actions needed
3. Budget reallocation suggestions
4. 3-year development strategy
5. Key risks and mitigation plan"""

        response = client.complete(
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt)
            ],
            model=DEPLOYMENT,
            max_tokens=800,
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Azure AI Foundry connection error: {str(e)}\n\nPlease check your .env file credentials."
