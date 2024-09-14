import requests
import zipfile
import io

def download_repo(repo_url, name):
    # Adjust URL for downloading zip file
    repo_zip_url = repo_url + "/archive/refs/heads/main.zip"
    response = requests.get(repo_zip_url)
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall("./repo/" + name)
