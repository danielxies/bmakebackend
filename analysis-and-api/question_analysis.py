from pydantic import BaseModel
from openai import OpenAI
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keys import Keys

client = OpenAI(api_key=Keys.OPENAI_API_KEY)

system_prompt = f"""Give the output in a  json format, 
No extra messages just purely the json output the json output needs to follow the format as follows: {format}. Nothing but the json file, only brackets, commas, and quotes are allowed and make sure that it is a valid json please.
Use this as reference:
1-2 (Poor): Candidate shows minimal understanding or competence. Responses are unclear, incorrect, or highly underdeveloped.
3-4 (Below Average): Some knowledge or skill is present but lacks depth, clarity, or correctness. Struggles significantly in application.
5-6 (Average): Candidate demonstrates a basic understanding and can perform adequately but may lack confidence, depth, or efficiency.
7-8 (Above Average): Strong competency with clear and mostly correct responses. Can handle moderate complexity with good reasoning.
9-10 (Excellent): Exceptional performance, demonstrating deep understanding, clear articulation, and high efficiency. Responses are insightful, precise, and well-structured.
"""

class QuestionResponse(BaseModel):
    score: float
    comment: str

class QuestionAnalysis:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
    
    def evaluate(self):
        response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": f"Analyze the following performance metrics for an employee evaluation:\n\n {system_prompt}"
            },
            {
                "role": "user",
                "content": f"Analyze the answer {self.answer} for the question {self.question}. Rate only the answer please"
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "question_evaluation",
                "schema": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "score": {"type": "number"},
                                "comment": {"type": "string"}
                            },
                            "required": ["score", "comment"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["data"],
                    "additionalProperties": False
                }
            }
        }
        )

        return response.choices[0].message.content

    def return_json(self):
        ret = json.loads(self.evaluate())
        ret["question"] = self.question
        ret["answer"] = self.answer
        return ret
    


if __name__ == "__main__":
    question = "What is the most important thing for a successful interview?"
    answer = "Knowledge of the job and the company"
    q = QuestionAnalysis(question, answer)
    print(q.return_json())
        
