from tensorflow.keras.models import load_model
import os
import pickle
import numpy as np

# Taking paths for all objects
curr_dir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(curr_dir, 'data/AE_model.h5')
mu_path = os.path.join(curr_dir, 'data/mu.pkl')

model = load_model(model_path, compile=False) # compile won't work as custom loss function was used for training

# Retreiving the mean value of all the ratings.
with open(mu_path, 'rb') as f:
    mu = pickle.load(f)

M = model.input_shape[1]

def predict(arr):
    return model.predict(arr-mu) + mu


if __name__ == "__main__":
    # Running a sample predict function
    sample = np.random.randint(low=0, high=6, size=(1, M))
    output = predict(sample) + mu
    print(output.min(), output.max(), output.mean())
