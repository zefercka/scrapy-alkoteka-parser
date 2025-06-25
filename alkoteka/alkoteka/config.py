import os
from dotenv import load_dotenv


class Settings:
    """Application configuration settings"""
    
    def __init__(self):
        load_dotenv()
        
        self.start_urls = []
        with open("urls.txt", "r") as file:
            for line in file:
                self.start_urls.append(line.strip())
        
        self.proxies = []
        with open("proxies.txt", "r") as file:
            for line in file:
                self.proxies.append(line.strip())
        
        self.city_uuid = os.getenv("CITY_UUID")


settings = Settings()