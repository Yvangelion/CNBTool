from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# Define the search URL
search_url = "https://carsandbids.com/search?q=model+3&ss_id=75244366-d01f-48bb-9fbd-2b9110b84a7a"

# Open the search results page
driver.get(search_url)
time.sleep(5)

car_data = []

# Find all visible listings on the first page
listings = driver.find_elements(By.CSS_SELECTOR, "div.LazyLoad.is-visible")

for idx, listing in enumerate(listings[:5], start=1):  # Only do first 5
    try:
        print(f"\nProcessing listing #{idx}...")

        anchor = listing.find_element(By.TAG_NAME, "a")
        title = anchor.get_attribute("title")
        partial_link = anchor.get_attribute("href")
        full_link = "https://carsandbids.com" + partial_link if partial_link.startswith("/") else partial_link

        try:
            sold_price_elem = anchor.find_element(By.CLASS_NAME, "bid-value")
            sold_price = sold_price_elem.text
        except:
            sold_price = "N/A"

        # Go to the car's page
        driver.get(full_link)
        time.sleep(3)

        title_full = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div/div[1]/h1").text
        title_parts = title_full.split()
        year = title_parts[0]
        model = title_parts[1] + " " + title_parts[2]
        drive_type = title_parts[-1] if title_parts[-1] in ["AWD", "RWD"] else "Unknown"
        trim = " ".join(title_parts[3:-1]) if drive_type != "Unknown" else " ".join(title_parts[3:])

        sold_date = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[4]/div[1]/div/div/ul/li[2]/span/span").text
        bids = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[4]/div[1]/div/div/ul/li[3]/span[2]").text
        comments = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[4]/div[1]/div/div/ul/li[4]/span[2]").text

        car_data.append({
            "Title": title_full,
            "Year": year,
            "Model": model,
            "Trim": trim,
            "Drive Type": drive_type,
            "Sold Price": sold_price,
            "Sold Date": sold_date,
            "Bids": bids,
            "Comments": comments,
        })

        # Go back to the search results page
        driver.get(search_url)
        time.sleep(5)

        # Refresh the listings for the next iteration
        listings = driver.find_elements(By.CSS_SELECTOR, "div.LazyLoad.is-visible")

    except Exception as e:
        print(f"❌ Error on listing #{idx}: {e}")
        continue

# Write to JSON
with open("cars.json", "w", encoding="utf-8") as f:
    json.dump(car_data, f, indent=4, ensure_ascii=False)

print("\n✅ Scraped and saved 5 listings to cars.json")
driver.quit()
