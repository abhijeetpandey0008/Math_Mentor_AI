import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer


MEMORY_FILE = "memory/memory_store.json"

model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------
# LOAD MEMORY
# -------------------------
def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


# -------------------------
# SAVE MEMORY ENTRY
# -------------------------
def save_memory(entry):

    memory = load_memory()

    # generate embedding
    entry["embedding"] = model.encode(entry["question"]).tolist()

    # avoid duplicate questions
    for item in memory:
        if item["question"].lower() == entry["question"].lower():
            return

    memory.append(entry)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


# -------------------------
# SEMANTIC SEARCH
# -------------------------
def retrieve_similar(question, threshold=0.75):

    memory = load_memory()

    if len(memory) == 0:
        return None

    query_embedding = model.encode(question)

    best_match = None
    best_score = 0

    for item in memory:

        # skip old entries without embeddings
        if "embedding" not in item:
            continue

        emb = np.array(item["embedding"])

        score = np.dot(query_embedding, emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(emb)
        )

        if score > best_score:
            best_score = score
            best_match = item

    if best_score > threshold:

        # if corrected solution exists, return it
        if "corrected_solution" in best_match:
            best_match["solution"] = best_match["corrected_solution"]

        return best_match

    return None


# -------------------------
# UPDATE FEEDBACK (HITL)
# -------------------------
def update_feedback(question, corrected_solution):

    memory = load_memory()

    for item in memory:

        if item["question"].lower() == question.lower():

            item["feedback"] = "incorrect"
            item["corrected_solution"] = corrected_solution

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)