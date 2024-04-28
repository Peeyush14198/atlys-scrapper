<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dental Product Scraper</title>
</head>
<body>
  <h1>Dental Product Scraper</h1>

  <h2>Overview</h2>
  <p>The Dental Product Scraper is a web scraping tool built with FastAPI that extracts product data from the Dental Stall website and stores it in MongoDB. If MongoDB is not available, the data is stored in a local JSON file. The scraper follows object-oriented principles and includes retry mechanisms for robustness.</p>

  <h2>Setup</h2>
  <ol>
    <li>Clone the repository:
      <pre><code>git clone https://github.com/yourusername/dental-product-scraper.git
cd dental-product-scraper</code></pre>
    </li>
    <li>Install dependencies:
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>Run the application:
      <pre><code>uvicorn main:app --reload --port 8001</code></pre>
    </li>
  </ol>

  <h2>Project Structure</h2>
  <pre><code>dental-product-scraper/
│
├── main.py              # FastAPI application
├── mongodb_handler.py   # MongoDB data handler class
├── scraper.py           # Scraper class for extracting product data
├── config.py            # Configuration file for MongoDB URL and other settings
└── requirements.txt     # Python dependencies
</code></pre>

  <h2>Authentication</h2>
  <p>The application uses simple API key authentication. To access the scraping endpoint, include the <code>X-API-Key</code> header with your API key. For example:</p>
  <pre><code>curl --location 'http://127.0.0.1:8001/scrape/?page=5' \
--header 'X-API-Key: bfmjSplZ3f'</code></pre>

  <h2>Data Storage</h2>
  <ul>
    <li>If MongoDB is available, scraped data is stored in MongoDB using bulk write operations with upsert functionality. If a product with the same name already exists, its data is updated; otherwise, a new document is inserted.</li>
    <li>If MongoDB is not available or if there is an error connecting to MongoDB, the data is stored locally in a JSON file named <code>scraped_data.json</code>.</li>
  </ul>

  <h2>Upsert Process</h2>
  <p>The upsert process in MongoDB involves updating existing documents if they match certain criteria and inserting new documents if no match is found. In this project, the scraper performs an upsert operation for each product. If a product with the same name already exists in the database, its data is updated with the new scraped data; otherwise, a new document is inserted.</p>
</body>
</html>
