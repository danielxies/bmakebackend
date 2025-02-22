import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'analysis-and-api'))
from analysis import evaluate_transcript
import json
import traceback

# Sample transcript with poor attitude and unprofessional responses
sample_transcript = """
Agent: Can you tell me about a challenging project you worked on recently?
User: Ugh, nothing really challenging. Most projects are pretty basic and boring. I just do what they tell me to do.

Agent: How do you handle conflicts with team members?
User: I don't really deal with conflicts. If someone's being difficult, I just ignore them or tell them to leave me alone. Not my problem.

Agent: What interests you about this position?
User: Honestly? Just the salary. I heard you guys pay well, and I need money. Don't really care about the actual work.

Agent: How do you stay updated with new technologies in your field?
User: I don't. Most new tech is just hype anyway. I stick to what I already know. Why learn new stuff when the old stuff works fine?

Agent: Can you describe your ideal work environment?
User: One where people leave me alone and don't micromanage me. I hate meetings and teamwork. Just let me do my thing and don't bother me.

Agent: How do you handle tight deadlines?
User: If it's too tight, I just tell them it's not possible. Not gonna stress myself out for someone else's poor planning. They can figure it out.

Agent: What's your approach to documentation and code reviews?
User: Documentation is a waste of time. If people can't understand my code, that's their problem. And code reviews just slow everything down.

Agent: Where do you see yourself in five years?
User: Haven't thought about it. Probably wherever pays the most. I'm not into all that career development stuff.
"""

def print_metric_evaluation(metric_name, metric_data):
    print(f"\n{metric_name.replace('_', ' ').title()}:")
    print(f"Score: {metric_data['score']}/10")
    print(f"Comment: {metric_data['comment']}")
    print(f"Confidence: {metric_data['confidence']:.2f}")

def test_evaluation():
    print("Testing transcript evaluation...")
    print("\nSample Transcript:")
    print(sample_transcript)
    print("\nEvaluating...")
    
    try:
        result = evaluate_transcript(sample_transcript)
        if not result:
            print("Evaluation failed - no result returned!")
            return
            
        print("\n=== Evaluation Results ===")
        
        # Print raw response for debugging
        print("\nRaw Response Structure:")
        print(json.dumps(result, indent=2))
        
        try:
            # Try to access the data structure
            data = result.get('data', {})
            if not data:
                print("\nERROR: No 'data' field in response!")
                print("Response keys available:", list(result.keys()))
                return
                
            # Print each metric's evaluation
            for metric_name, metric_data in data.items():
                if metric_name not in ['summary', 'overall_score']:
                    try:
                        print_metric_evaluation(metric_name, metric_data)
                    except Exception as metric_error:
                        print(f"\nError processing metric {metric_name}:")
                        print(f"Metric data: {metric_data}")
                        print(f"Error: {str(metric_error)}")
            
            print("\n=== Overall Results ===")
            print(f"Overall Score: {data.get('overall_score', 'N/A')}/10")
            print("\nSummary:")
            print(data.get('summary', 'No summary available'))
            
        except Exception as processing_error:
            print("\nError processing response structure:")
            print(f"Error: {str(processing_error)}")
            print("Response structure:")
            print(json.dumps(result, indent=2))
        
        # Save the full results to a file
        with open('evaluation_results.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("\nFull results saved to evaluation_results.json")
        
    except Exception as e:
        print("\nError during evaluation:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_evaluation() 