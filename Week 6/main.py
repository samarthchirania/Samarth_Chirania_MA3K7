from simulations import simulate_draw
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time
from collections import defaultdict
import csv
from collections import Counter
import signal


def simulate_chunk(pool, chunk_size):
    # Simulate a chunk of simulations and measure the time taken
    start_time = time.time()
    final_numbers = pool.map(simulate_draw, [None] * chunk_size)
    end_time = time.time()
    duration = end_time - start_time  # Calculate the duration for this chunk
    return final_numbers, duration

stop_requested = False

def signal_handler(signal, frame):
    global stop_requested
    stop_requested = True
    print("Stop requested. Finishing up...")

signal.signal(signal.SIGINT, signal_handler)


def run_simulation_until_all_even_numbers(pool, pool_size=None, chunk_size=10000, update_interval=20000):
    global stop_requested
    all_numbers = []  # List to accumulate all generated numbers across batches
    generated_even_numbers = set()  # Set to keep track of unique even numbers generated
    target_even_numbers = set(range(0, 2023, 2))  # All even numbers from 0 to 2022
    total_simulations = 0  # Total number of simulations that have finished

    while not stop_requested and not target_even_numbers.issubset(generated_even_numbers):
        # Simulate a batch and accumulate the results
        chunk_final_numbers, duration = simulate_chunk(pool, chunk_size)
        all_numbers.extend(chunk_final_numbers)  # Accumulate all numbers
        total_simulations += chunk_size  # Update the total simulations count

        # Update the set of generated even numbers
        generated_even_numbers.update(n for n in chunk_final_numbers if n % 2 == 0)

        print(f"Batch of {chunk_size} simulations completed in {duration:.2f} seconds. Total simulations: {total_simulations}")
        print(f"Unique even numbers generated so far: {len(generated_even_numbers)}")

        # Periodic update or graceful exit
        if len(all_numbers) >= update_interval or stop_requested or target_even_numbers.issubset(generated_even_numbers):
            # Calculate frequencies using Counter on the accumulated list
            frequencies = Counter(all_numbers)

            # Write to CSV, ensuring data is sorted by number
            with open('big_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Final Number', 'Frequency'])
                for number, frequency in sorted(frequencies.items()):
                    writer.writerow([number, frequency])
            print(f"CSV updated with {len(frequencies)} unique numbers and their frequencies after {total_simulations} total simulations.")

            if target_even_numbers.issubset(generated_even_numbers):
                print(f"All even numbers up to 2022 have been generated after {total_simulations} total simulations.")
                break

            if stop_requested:
                print(f"Exiting simulation after {total_simulations} total simulations...")
                break

    return all_numbers



def plot_frequencies(final_numbers_list):
    frequencies = defaultdict(int)
    for final_number in final_numbers_list:
        frequencies[final_number] += 1

    sorted_freq = sorted(frequencies.items())
    numbers, frequencies = zip(*sorted_freq)

    plt.figure(figsize=(10, 6))
    plt.bar(numbers, frequencies, color='skyblue')
    plt.xlabel('Final Number')
    plt.ylabel('Frequency')
    plt.title(f'Frequency of Final Numbers Over {len(final_numbers_list)} Simulations')
    plt.show()


if __name__ == '__main__':
    with Pool() as pool:
        final_numbers_list = run_simulation_until_all_even_numbers(pool)

        # Plotting frequencies
        plot_frequencies(final_numbers_list)
        print(f"Total unique numbers generated: {len(final_numbers_list)}")

        # Final CSV update with sorted data
        frequencies = Counter(final_numbers_list)
        with open('big_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Final Number', 'Frequency'])
            for number, frequency in sorted(frequencies.items()):
                writer.writerow([number, frequency])
        print("Final frequency results have been written to big_data.csv")
