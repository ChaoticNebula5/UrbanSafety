"""
AI Classification Agent using LangChain + Ollama
"""
try:
    from langchain_ollama import OllamaLLM
except ImportError:
    from langchain_community.llms import Ollama as OllamaLLM

from langchain.prompts import PromptTemplate
from config import settings
import json
import re


class IncidentClassifier:
 
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0.3 
        )
        
        self.prompt = PromptTemplate(
            input_variables=["title", "description"],
            template="""You are an urban safety analyst. Classify this incident report into the correct category.

Incident Title: {title}
Description: {description}

CATEGORY DEFINITIONS (choose EXACTLY ONE):
1. "theft" - Any stealing, robbery, burglary, shoplifting, pickpocketing, armed robbery, jewelry store robbery, bike theft, car theft
2. "assault" - Physical violence, fighting, stabbing, shooting, weapons, battery, attack with knives/guns/weapons
3. "vandalism" - Property damage, graffiti, broken windows, destruction of property
4. "traffic" - Car accidents, collisions, vehicle crashes, traffic violations, road incidents
5. "suspicious_activity" - Loitering, stalking, following people, suspicious behavior
6. "other" - Medical emergencies, fires, natural disasters, lost items (ONLY if none of above fit)

EXAMPLES:
- "Armed robbery at gunpoint" → theft
- "Person stabbed in fight" → assault  
- "Bike stolen from parking" → theft
- "Group fighting with knives" → assault
- "Car accident on highway" → traffic
- "Person unconscious after fall" → other (medical)

SEVERITY LEVELS:
- critical: Armed robbery, weapons involved, life-threatening, immediate danger
- high: Violence, theft, serious injury, urgent response needed
- medium: Property damage, suspicious activity, minor injuries
- low: Minor issues, no immediate threat

OUTPUT FORMAT (respond with ONLY this JSON, no other text):
{{
  "category": "theft|assault|vandalism|traffic|suspicious_activity|other",
  "severity": "low|medium|high|critical",
  "summary": "Brief description in 10-15 words"
}}"""
        )
        
        self.chain = self.prompt | self.llm
    
    def classify(self, title: str, description: str) -> dict:
        try:
            response = self.chain.invoke({
                "title": title,
                "description": description
            })
            
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
            
            valid_categories = ["theft", "assault", "vandalism", "traffic", "suspicious_activity", "other"]
            valid_severities = ["low", "medium", "high", "critical"]
            
            if result["category"] not in valid_categories:
                result["category"] = "other"
            if result["severity"] not in valid_severities:
                result["severity"] = "medium"
            
            return {
                "category": result["category"],
                "severity": result["severity"],
                "ai_summary": result["summary"]
            }
            
        except Exception as e:
            print(f"AI classification error: {e}")
            return {
                "category": "other",
                "severity": "medium",
                "ai_summary": f"{title} - Pending manual review"
            }
    
    def classify_batch(self, incidents: list[dict]) -> list[dict]:
        return [self.classify(inc["title"], inc["description"]) for inc in incidents]


ai_classifier = IncidentClassifier()
