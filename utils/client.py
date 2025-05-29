# utils/nvidia_client.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")  
)

def query_nvidia(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1",
            messages=[
                {"role": "system", "content": "You are a helpful information extraction assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            top_p=0.9,
            max_tokens=1024,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
