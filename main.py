# main.py
from fastapi import FastAPI, HTTPException, Query, Depends # type: ignore
from fastapi.security import APIKeyHeader # type: ignore
from app.service.scrapper import Scraper
from app.db.mongodb_handler import MongoDBHandler
from app.service.notification import Notification
import json

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")



async def authenticate(api_key: str = Depends(api_key_header)):
    config = load_config("config/config.json")
    if api_key != config.get("api_key"):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

@app.get("/scrape/", dependencies=[Depends(authenticate)])
async def scrape_dental_stall(
    page: int = Query(None, description="Page number to scrape"),
    proxy: str = None
):
    # Base URL of the website to scrape
    base_url = "https://dentalstall.com/shop/page/"

    # Initialize objects
    scraper = Scraper(base_url)
    
    config = load_config("config/config.json")
    notification = Notification()

    # Scrape data
    scraped_data = scraper.scrape(page, proxy)
    print(scraped_data)

    # Store scraped data in MongoDB
    if scraped_data:
         if config.get("mongo_uri"):
             mongo_handler = MongoDBHandler(config.get("mongo_uri"))
             mongo_handler.store_data(scraped_data)
         else:
            with open("scraped_data.json", "w") as json_file:
                json.dump(scraped_data, json_file, indent=4)

    # Send notification
    notification.send_notification(f"Scraping completed. Total products scraped: {len(scraped_data)}")

    return {"message": "Scraping completed"}

def load_config(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="127.0.0.1", port=8001)
