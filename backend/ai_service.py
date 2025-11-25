import google.generativeai as genai
import os
import json
from schemas import SubTaskCreate
from typing import AsyncGenerator

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_subtasks_stream(goal_description: str) -> AsyncGenerator[SubTaskCreate, None]:
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""Break down this goal into exactly 5 actionable subtasks: "{goal_description}"

For each subtask, provide:
1. A clear, actionable description
2. A complexity score from 1-10

Output each subtask as a JSON object on a new line:
{{"description": "step description", "complexity_score": 5}}

Generate all 5 subtasks now."""
    
    try:
        response = model.generate_content(prompt, stream=True)
        
        buffer = ""
        subtask_count = 0
        
        for chunk in response:
            try:
                if chunk.text:
                    buffer += chunk.text
                    
                    while '\n' in buffer and subtask_count < 5:
                        line_end = buffer.index('\n')
                        line = buffer[:line_end].strip()
                        buffer = buffer[line_end + 1:]
                        
                        if not line or line.startswith('```'):
                            continue
                        
                        line = line.replace('```json', '').replace('```', '').strip()
                        
                        if line.startswith('{') and line.endswith('}'):
                            try:
                                data = json.loads(line)
                                if 'description' in data and 'complexity_score' in data:
                                    subtask_count += 1
                                    yield SubTaskCreate(
                                        description=data["description"],
                                        complexity_score=int(data["complexity_score"])
                                    )
                            except (json.JSONDecodeError, KeyError, ValueError):
                                continue
            except Exception as e:
                print(f"Chunk error: {e}")
                continue
        
        if buffer.strip() and subtask_count < 5:
            lines = buffer.strip().split('\n')
            for line in lines:
                if subtask_count >= 5:
                    break
                    
                line = line.strip().replace('```json', '').replace('```', '').strip()
                if line.startswith('{') and line.endswith('}'):
                    try:
                        data = json.loads(line)
                        if 'description' in data and 'complexity_score' in data:
                            subtask_count += 1
                            yield SubTaskCreate(
                                description=data["description"],
                                complexity_score=int(data["complexity_score"])
                            )
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
                        
    except Exception as e:
        print(f"Error generating subtasks: {e}")
        raise e

async def generate_subtasks(goal_description: str) -> list[SubTaskCreate]:
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""Break down this goal into exactly 5 actionable subtasks: "{goal_description}"

Return as a JSON array:
[
  {{"description": "step 1", "complexity_score": 5}},
  {{"description": "step 2", "complexity_score": 7}}
]

Complexity scores: 1 (easiest) to 10 (hardest)."""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
            
        data = json.loads(text)
        
        subtasks = []
        for item in data[:5]:
            subtasks.append(SubTaskCreate(
                description=item["description"],
                complexity_score=item["complexity_score"]
            ))
            
        return subtasks
    except Exception as e:
        print(f"Error generating subtasks: {e}")
        raise e
