import pandas as pd
import numpy as np
import joblib 
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

# Load the saved model
loaded_model = tf.keras.models.load_model('modelbase')
scaler = StandardScaler()
scaler_path = 'modelbase/scaler.pkl'  # Adjust the path based on where you saved the scaler during training

# Load the scaler from the saved model directory
scaler = joblib.load(scaler_path)

new_data = pd.DataFrame({'ti': [80], 'tf': [80], 'ai': [0.2], 'af': [1.5], 't': [145]})

# Apply the same scaling to the new data
new_data_scaled = scaler.transform(new_data)

# Make predictions
predicted_p = loaded_model.predict(new_data_scaled)

print(f'Predicted P: {predicted_p}')