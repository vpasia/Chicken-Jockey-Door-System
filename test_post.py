import requests
import os

# Define the URL of your Flask endpoint
url = 'http://localhost:5000/api/process_sound'

# Specify the path to the .wav file you want to upload
file_path = os.path.join(os.getcwd(), 'chicken-jockey-key2.wav')

# Open the file in binary mode and prepare the files dictionary
with open(file_path, 'rb') as f:
    files = {'chicken-jockey-key2.wav': f}
    # Send the POST request with the file
    response = requests.post(url, files=files)

# Print the response from the server
print(f'Status Code: {response.status_code}')
print(f'Response Body: {response.text}')