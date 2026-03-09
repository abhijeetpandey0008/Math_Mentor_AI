import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)


def generate_response(prompt):

    response = client.chat_completion(
        model="Qwen/Qwen3-Coder-Next",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.2
    )

    return response.choices[0].message.content