import pandas as pd
import numpy as np

# Number of data points
n = 100000

# Generate timestamps in milliseconds
timestamps = np.arange(0, n*100, 100)  # Every 100 ms

# Generate speed (km/h), average around 40 with some noise
speed = np.random.normal(loc=40, scale=10, size=n)
speed = np.clip(speed, 0, 80)  # Speed limits

# Calculate cumulative distance (km)
distance = np.cumsum(speed * (100 / 3600000))  # Speed converted to distance over 100 ms intervals

# Initialize SOC (state of charge) at 100%
soc = np.zeros(n)
soc[0] = 100

# Driving modes: 0-Normal, 1-Sports, 2-Economy
modes = np.random.choice([0, 1, 2], size=n, p=[0.5, 0.3, 0.2])

def soc_decrement(mode):
    # SOC depletion per 100 ms segment for modes (% decrement)
    if mode == 0:  # Normal
        return np.random.uniform(0.001, 0.002)
    elif mode == 1:  # Sports (higher consumption)
        return np.random.uniform(0.002, 0.004)
    else:  # Economy (lower consumption)
        return np.random.uniform(0.0005, 0.001)

# Calculate SOC decrement over time
for i in range(1, n):
    soc[i] = max(soc[i-1] - soc_decrement(modes[i]), 0)

# Map mode numbers to labels
mode_labels = np.array(['Normal', 'Sports', 'Economy'])

# Create DataFrame
df = pd.DataFrame({
    'timestamp_ms': timestamps,
    'distance_km': distance,
    'soc_percent': soc,
    'mode': mode_labels[modes]
})

# Save to CSV
df.to_csv('ev_mode_usage_dataset.csv', index=False)
