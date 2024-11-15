# data_processing/preprocess.py
import numpy as np

def preprocess_data(data):
    # Standardization
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    standardized_data = (data - mean) / std
    return standardized_data

def main():
    # Sample data
    data = np.random.randn(100, 10)
    preprocessed_data = preprocess_data(data)
    print("Data preprocessed:", preprocessed_data[:5])  # Display first 5 rows

if __name__ == "__main__":
    main()
