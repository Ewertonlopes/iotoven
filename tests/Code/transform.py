import pandas as pd
import random

# Load the CSV data
df = pd.read_csv('Data/alpha.csv')

# Fixed potency value
p = 160  # Replace with your desired potency value

# Create a new DataFrame for the transformed data
new_df = pd.DataFrame(columns=['ti', 'tf', 'ai', 'af', 't', 'p'])

# Iterate through the rows of the original DataFrame
for i in range(5,len(df) - 60):
    # Extract values from the original DataFrame
    ti = df['temperature'].iloc[i]

    # Generate a random time duration between 1 and 10 seconds (adjust as needed)
    t = random.uniform(30, 60)

    # Calculate the index of the final temperature based on the time duration
    final_index = min(len(df) - 1, i + int(t))

    # Calculate the final temperature within the time frame
    tf = df['temperature'].iloc[final_index]

    # Calculate the initial and final angles
    ai = ti - (df['temperature'].iloc[i - 5:i].mean() if i >= 5 else 0)
    af = tf - (df['temperature'].iloc[final_index - 5:final_index].mean() if final_index >= 5 else 0)

    # Append the values to the new DataFrame
    new_df = new_df._append({
        'ti': ti,
        'tf': tf,
        'ai': ai,
        'af': af,
        't': t,
        'p': p
    }, ignore_index=True)

# Save the new DataFrame to a new CSV file
new_df.to_csv('new_data.csv', index=False)
