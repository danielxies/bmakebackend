import requests
from pydantic import BaseModel
import json
from openai import OpenAI
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keys import Keys
from question_analysis import QuestionAnalysis


format = """
    "Category": {
        "Rating": float,
        "Comment": str
    },
"""

system_prompt = f"""Give the output in a  json format, 
No extra messages just purely the json output the json output needs to follow the format as follows: {format}. Nothing but the json file, only brackets, commas, and quotes are allowed and make sure that it is a valid json please.
Use this as reference:
1-2 (Poor): Candidate shows minimal understanding or competence. Responses are unclear, incorrect, or highly underdeveloped.
3-4 (Below Average): Some knowledge or skill is present but lacks depth, clarity, or correctness. Struggles significantly in application.
5-6 (Average): Candidate demonstrates a basic understanding and can perform adequately but may lack confidence, depth, or efficiency.
7-8 (Above Average): Strong competency with clear and mostly correct responses. Can handle moderate complexity with good reasoning.
9-10 (Excellent): Exceptional performance, demonstrating deep understanding, clear articulation, and high efficiency. Responses are insightful, precise, and well-structured.
"""

metrics = """
Rate each answer on a scale of 1 to 10, where 1 is the lowest score and 10 is the highest, based on the following criteria:

Technical Knowledge & Domain Expertise
"How well does the candidate demonstrate knowledge relevant to their field?"

Problem-Solving & Analytical Thinking
"How effectively does the candidate break down problems and apply logical reasoning to reach a solution?"

Communication & Clarity
"How clearly and concisely does the candidate explain their thoughts, processes, and technical concepts?"

Adaptability & Learning Ability
"How well does the candidate handle unfamiliar topics or adjust their approach based on new information?"

Collaboration & Teamwork
"How effectively does the candidate discuss working in teams, resolving conflicts, and contributing to group projects?"

Innovation & Creativity
"How well does the candidate demonstrate original thinking, propose new ideas, or improve existing solutions?"

Attention to Detail & Accuracy
"How precise is the candidate in their explanations, calculations, or technical responses?"

Time Management & Organization
"How well does the candidate discuss handling deadlines, managing tasks, and prioritizing work?"

Ethical & Professional Judgment
"Does the candidate demonstrate an understanding of ethical considerations and professional responsibility in STEM fields?"
"""

class QuantitativeAnswer(BaseModel):
    technical_knowledge: float
    technical_knowledge_comment: str
    problem_solving: float
    problem_solving_comment: str
    communication: float
    communication_comment: str
    adaptability: float
    adaptability_comment: str
    collaboration: float
    collaboration_comment: str
    innovation: float
    innovation_comment: str
    attention_to_detail: float
    attention_to_detail_comment: str
    time_management: float
    time_management_comment: str
    ethical_judgment: float
    ethical_judgment_comment: str
    summary: str


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

client = OpenAI(api_key=Keys.OPENAI_API_KEY)
import json

def create_evaluation_schema():
    """Creates the schema for the interview evaluation structured output"""
    return {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "technical_knowledge": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "problem_solving": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "communication": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "adaptability": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "collaboration": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "innovation": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "attention_to_detail": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "time_management": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "ethical_judgment": {
                        "type": "object",
                        "properties": {
                            "score": {"type": "number"},
                            "comment": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["score", "comment", "confidence"]
                    },
                    "summary": {"type": "string"},
                    "overall_score": {"type": "number"}
                },
                "required": [
                    "technical_knowledge", "problem_solving", "communication",
                    "adaptability", "collaboration", "innovation",
                    "attention_to_detail", "time_management",
                    "ethical_judgment", "summary", "overall_score"
                ],
                "additionalProperties": False
            }
        },
        "required": ["data"],
        "additionalProperties": False
    }

def evaluate_transcript(text):
    """Evaluates the interview transcript using GPT-4-Turbo with structured output"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert interview evaluator. Analyze the following interview transcript and provide detailed scores and feedback.
                    Use the following scoring reference:
                    1-2 (Poor): Candidate shows minimal understanding or competence
                    3-4 (Below Average): Some knowledge but lacks depth or clarity
                    5-6 (Average): Basic understanding and adequate performance
                    7-8 (Above Average): Strong competency with clear responses
                    9-10 (Excellent): Exceptional performance with deep understanding
                    
                    For each metric, provide:
                    - A score from 1-10
                    - A specific comment explaining the score
                    - A confidence score (0-1) indicating how confident you are in this assessment
                    """
                },
                {
                    "role": "user",
                    "content": f"Analyze this interview transcript:\n\n{text}"
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "interview_evaluation",
                    "schema": create_evaluation_schema()
                }
            }
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error in evaluation: {str(e)}")
        return None


# For individual questions - segment each question and rates it
def evaluate_individual_question(text):
    data = {}
    lines = text.strip().split('\n')
    qa_pairs = []
    current_question = None
    
    for line in lines:
        if line.startswith("Agent:"):
            current_question = line.replace("Agent:", "").strip()
        elif line.startswith("User:") and current_question is not None:
            answer = line.replace("User:", "").strip()
            qa_pairs.append((current_question, answer))
            current_question = None  # Reset for the next question
    
    for i in range(len(qa_pairs)):
        question = QuestionAnalysis(qa_pairs[i][0], qa_pairs[i][1])
        data[f"question{i}"] = question.return_json()
    
    return json.dumps(data, indent=4)
    

