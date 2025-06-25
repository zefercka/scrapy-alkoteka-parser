import os

from dotenv import load_dotenv


class Settings:
    """Application configuration settings"""
    
    def __init__(self):
        load_dotenv()
        
        self.start_urls = []
        if os.path.exists("urls.txt"):
            with open("urls.txt", "r") as file:
                for line in file:
                    self.start_urls.append(line.strip())
        
        self.proxies = []
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as file:
                for line in file:
                    self.proxies.append(line.strip())
        
        self.city_uuid = os.getenv("CITY_UUID")


settings = Settings()