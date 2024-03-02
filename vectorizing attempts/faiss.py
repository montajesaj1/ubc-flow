import json
import numpy as np
import faiss

# Read the JSON file
with open('UBCCourses.json', 'r') as f:
    data = json.load(f)

# Assuming each element in JSON represents a vector
vectors = []
for item in data:
    # Convert JSON data into vectors
    vector = np.array(item['CPSC'])  # Assuming 'vector' is the key for the vector data
    vectors.append(vector)

# Convert list of vectors into a numpy array
vectors = np.array(vectors).astype('float32')

# Initialize FAISS index
d = vectors.shape[1]  # Dimensionality of vectors
index = faiss.IndexFlatL2(d)  # Using L2 distance

# Add vectors to the index
index.add(vectors)

# Now you can perform similarity search or clustering using the index
