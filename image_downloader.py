# image_downloader
import os
import requests

class ImageDownloader:
    @staticmethod
    def download_image(url, file_path):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded image: {file_path}")
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")