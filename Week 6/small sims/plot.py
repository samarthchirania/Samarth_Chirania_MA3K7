import pandas as pd
import matplotlib.pyplot as plt

l = [3]

for i in range(len(l)):
    n = l[i]
    k = l[i] * 10000

    # Read the CSV file into a DataFrame
    df = pd.read_csv(f'simulation_results_{n}.csv')

    # Extract the first and second columns
    x = df.iloc[:, 0]  # Assuming the first column is X-axis values
    y = df.iloc[:, 1]  # Assuming the second column is Y-axis values

    # Plot the data
    plt.bar(x, y)

    # Add labels and title
    plt.xlabel('Numbers')
    plt.ylabel('Frequencies')
    plt.title(f'Plot of frequencies of a game of size {n} after {k} simulations')

    # Save the plot
    plt.savefig(f'plot_{n}.png')

    # Show the plot
    plt.show()
