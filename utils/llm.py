# import os
# from dotenv import load_dotenv
# from huggingface_hub import InferenceClient

# load_dotenv()

# client = InferenceClient(
#     token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
# )


# def generate_response(prompt):

#     response = client.text_generation(
#         model="meta-llama/Llama-3-8B-Instruct",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=512,
#         temperature=0.2
#     )
#     return response.choices[0].message.content

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

def generate_response(prompt):

    response = client.text_generation(
        prompt=prompt,
        max_new_tokens=512,
        temperature=0.2
    )

    return response


