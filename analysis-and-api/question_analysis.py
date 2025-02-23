from pydantic import BaseModel
from openai import OpenAI
import os
import json
import sys
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

system_prompt = f"""Give the output in a json format, 
No extra messages just purely the json output the json output needs to follow the format as follows: {format}. Nothing but the json file, only brackets, commas, and quotes are allowed and make sure that it is a valid json please.
Use this as reference for scoring on a scale of 1-10:
1-3 (Poor): Only for responses that show harmful intent, extremely unprofessional behavior, or dangerous suggestions
4-5 (Below Average): For responses that are clearly off-topic or show significant misunderstanding
6-7 (Average): For basic, acceptable responses that address the question
8-9 (Above Average): For good, detailed responses that show understanding
10 (Excellent): For exceptional, insightful responses

Be lenient in scoring. Unless the response shows harmful intent or is completely irrelevant, score it at least a 6.
For responses over 1 minute in length, automatically give a high score (8-10) to reward engagement."""

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
        
