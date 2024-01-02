#%%
import requests
import json
import os

api_key = "QdPyWSeIGl5T2ZQn8QLrk51kOY6tr3VS7vgVzZZh"
headers = {'x-api-key': api_key}

#%%
r1 = requests.get('https://api.semanticscholar.org/datasets/v1/release').json()
print(r1[-3:])

#%%
r2 = requests.get('https://api.semanticscholar.org/datasets/v1/release/latest').json()
print(r2['release_id'])

#%%
print(json.dumps(r2['datasets'], indent=2))

#%%
url = 'https://api.semanticscholar.org/datasets/v1/release/latest/dataset/abstracts'
r3 = requests.get(url, headers=headers).json()
print(json.dumps(r3, indent=2))

#%%
url = 'https://api.semanticscholar.org/datasets/v1/release/latest/dataset/abstracts'
r3 = requests.get(url, headers=headers).json()
output_directory = 'downloaded_files'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for index, file_link in enumerate(r3['files'], 1):
    file_name = f"abstracts_file_{index}.gz"
    file_path = os.path.join(output_directory, file_name)
    print(f"Downloading {file_name}...")

    with requests.get(file_link, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Downloaded {file_name} to {file_path}")

#%%
url = 'https://api.semanticscholar.org/datasets/v1/release/latest/dataset/tldrs'
r3 = requests.get(url, headers=headers).json()
output_directory = 'downloaded_files'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for index, file_link in enumerate(r3['files'], 1):
    file_name = f"tldrs_file_{index}.gz"
    file_path = os.path.join(output_directory, file_name)
    print(f"Downloading {file_name}...")

    with requests.get(file_link, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Downloaded {file_name} to {file_path}")
# %%
url = 'https://api.semanticscholar.org/datasets/v1/release/latest/dataset/s2orc'
r3 = requests.get(url, headers=headers).json()
output_directory = 'downloaded_files'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for index, file_link in enumerate(r3['files'], 1):
    file_name = f"fulltext_file_{index}.gz"
    file_path = os.path.join(output_directory, file_name)
    print(f"Downloading {file_name}...")

    with requests.get(file_link, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Downloaded {file_name} to {file_path}")
