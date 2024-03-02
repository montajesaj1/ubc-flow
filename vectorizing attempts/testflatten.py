import json
import numpy as np

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def json_to_vectors(json_data):
    flattened_data = [flatten_dict(obj) for obj in json_data]
    
    # Example: One-hot encoding for simplicity
    unique_keys = set(key for obj in flattened_data for key in obj.keys())
    vectorized_data = []
    for obj in flattened_data:
        vector = [1 if key in obj else 0 for key in unique_keys]
        vectorized_data.append(vector)
    
    return np.array(vectorized_data)

# Example JSON data
json_data = [
    {
        'id': 1,
        'name': 'John',
        'address': {
            'city': 'New York',
            'zip': 10001
        }
    },
    {
        'id': 2,
        'name': 'Alice',
        'address': {
            'city': 'Los Angeles',
            'zip': 90001
        }
    }
]

vectors = json_to_vectors(json_data)
print(vectors)
