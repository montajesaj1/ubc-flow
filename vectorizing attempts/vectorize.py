from sklearn.feature_extraction import DictVectorizer
import json

with open('UBCCourses.json', 'r') as file:
    json_data = json.load(file)

for key, value in json_data.items():
    if isinstance(value, dict):
        json_data[key] = json.dumps(value)
vectorizer = DictVectorizer()

X = vectorizer.fit_transform(json_data)

print(X)

print(X.shape)  # This will print the dimensions of the feature matrix
print(X.toarray())  # This will print the feature matrix as a dense array
print(X.shape)  # This will print the dimensions of the feature matrix
print(X.toarray())  # This will print the feature matrix as a dense array

