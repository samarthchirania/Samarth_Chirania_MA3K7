# simulations.py
import random

def simulate_draw(dummy):
    papers = list(range(1, 2025))  # Using a list for compatibility with random.sample
    while len(papers) > 1:
        a, b = random.sample(papers, 2)
        papers.remove(a)
        papers.remove(b)
        papers.append(abs(a - b))  # Keep the operation simple; allow 0 as a result
    return papers[0] if papers else 0  # Return the final number or 0 if the list is empty

# Moved simulate_chunk to this module
def simulate_chunk(chunk_size):
    return [simulate_draw(None) for _ in range(chunk_size)]