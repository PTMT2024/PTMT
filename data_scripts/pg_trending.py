import pandas as pd
import matplotlib.pyplot as plt

workload_dir = '/home/sherry/projects/sk_prokect/mldpp/run_scripts/log/tune_v2_ipc/autonuma/10s/BFS/202406181056_34G'

labels = ['numa_pages_migrated', 'pgdemote_kswapd', 'numa_hint_faults']

df = pd.DataFrame()

for label in labels:
    print(f'Processing {label}')
    with open(f'{workload_dir}/{label}.txt', 'r') as f:
        lines = f.readlines()
        y_values = [int(line.split()[1]) for line in lines]

    # Subtract the first number from all numbers
    first_value = y_values[0]
    y_values = [y - first_value for y in y_values]

    # Add the data to the DataFrame
    df[label] = y_values

# Create a list of seconds for the x-axis
df['Time (seconds)'] = list(range(1, len(df) + 1))

# Reorder the DataFrame columns
df = df[['Time (seconds)'] + labels]

# Plot the data
for label in labels:
    plt.plot(df['Time (seconds)'], df[label], label=label)

plt.xlabel('Time (seconds)')
plt.ylabel('Count')
plt.title('Metrics over time')
plt.legend()
plt.savefig(f'{workload_dir}/metrics.png')