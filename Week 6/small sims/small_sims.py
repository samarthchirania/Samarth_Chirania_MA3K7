# Import necessary libraries
import random
from multiprocessing import Pool, cpu_count
from simulation_functions_n import simulate  # Import the simulate function

# The rest of your script remains the same...

import time
import csv
from collections import Counter



# Function to run simulations in parallel and measure time for each chunk
def run_simulation(n, chunk_size=1000):
    total_simulations = n * 10000
    pool_size = cpu_count()  # Number of CPU cores

    with Pool(pool_size) as pool:
        chunk_results = []
        for _ in range(total_simulations // chunk_size):
            start_time = time.time()
            results = pool.map(simulate, [n] * chunk_size)
            end_time = time.time()
            print(f"Chunk processed in {end_time - start_time:.2f} seconds.")
            chunk_results.extend(results)
    return chunk_results

# Function to write the final numbers and their frequencies to a CSV file
def write_results_to_csv(final_numbers, n):
    filename = f'simulation_results_{n}.csv'  # Dynamic filename based on the value of n
    frequencies = Counter(final_numbers)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Final Number', 'Frequency'])
        for number, freq in frequencies.items():
            writer.writerow([number, freq])
    print(f"Results have been written to {filename}")


# Main block to run the simulation
if __name__ == '__main__':
    while True:
        n_input = input("Enter the value of n (or type 'stop' to end): ").strip()
        if n_input.lower() == 'stop':
            print("Simulation stopped by user.")
            break

        try:
            n = int(n_input)
            final_numbers = run_simulation(n)
            write_results_to_csv(final_numbers, n)
        except ValueError:
            print("Please enter a valid integer or 'stop' to end.")

