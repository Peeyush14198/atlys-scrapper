# scraper.py
from bs4 import BeautifulSoup # type: ignore
import json
import requests # type: ignore
import re
import time

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.max_retries = 3

    def scrape(self, page=None, proxy=None):
        scraped_data = []

        # Construct URL based on page number
        if page:
            url = f"{self.base_url}{page}/"
        else:
            url = self.base_url

        for attempt in range(1, self.max_retries + 1):
            try:
                print("Attempting to retrieve data from", attempt)
                response = requests.get(url, proxies={"https": proxy} if proxy else None)
              
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    script_tags = soup.find_all("script", type="text/javascript")

                    # Find the script tag containing the product data
                    target_script = None
                    for script in script_tags:
                        if "window.ga4w" in script.text:
                            target_script = script
                            break

                    if target_script:
                        # Extract JSON data
                        json_data = target_script.string.split("window.ga4w = ")[1].split("document")[0].strip().rstrip(";")
                        data = json.loads(fix_json(json_data))

                        # Extract products
                        products = data.get("data", {}).get("products", [])
                        for product in products:
                            product_name = product.get("name", "")
                            product_id  =  product.get("id", "")
                            product_price = product.get("prices", {}).get("price", "")
                            img_tag = soup.find("img", alt=re.compile(re.escape(product_name), re.IGNORECASE))
                            product_image = img_tag.get("data-lazy-src", "") if img_tag else ""

                            scraped_data.append({
                                "title": product_name,
                                "price": product_price,
                                "image": product_image,
                                "id" : product_id
                            })
                    else:
                        print("Script tag containing product data not found")
                    break  # Break out of the retry loop if successful
                else:
                    print(f"Failed to fetch page: {url}. Retrying...")
            except Exception as e:
                print(f"Error occurred: {str(e)}. Retrying...")

            # Sleep for a short duration before retrying
            time.sleep(1)

        return scraped_data

def fix_json(json_data):
    """
    Function to fix JSON data by adding double quotes around property names and values.
    """
    json_data = json_data.replace("{ ", '{"')
    json_data = json_data.replace(": ", '": ')
    json_data = json_data.replace("}, ", '}, "')
    return json_data
