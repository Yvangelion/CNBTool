from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

# Setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://carsandbids.com/search?q=model+3")
time.sleep(3)

# Scroll and load enough listings
SCROLL_PAUSE_TIME = 2
MAX_LISTINGS = 30
previous_len = 0

while True:
    listings = driver.find_elements(By.XPATH, "/html/body/div/div[2]/div[2]/div/div[2]/ul[1]/li")
    
    if len(listings) >= MAX_LISTINGS:
        break

    if len(listings) > 0:
        driver.execute_script("arguments[0].scrollIntoView();", listings[-1])
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    if len(listings) == previous_len:
        print("No more listings loaded.")
        break

    previous_len = len(listings)

# Collect links
car_links = []
for listing in listings[:MAX_LISTINGS]:
    try:
        anchor = listing.find_element(By.TAG_NAME, "a")
        href = anchor.get_attribute("href")
        if href:
            car_links.append(href)
    except:
        continue

car_data = []

# Visit each car page
for idx, link in enumerate(car_links, start=1):
    try:
        print(f"\nProcessing listing #{idx}: {link}")
        driver.get(link)
        time.sleep(3)

        title_full = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div/div[1]/h1").text
        title_parts = title_full.split()
        year = title_parts[0]
        model = title_parts[1] + " " + title_parts[2]
        drive_type = title_parts[-1] if title_parts[-1] in ["AWD", "RWD"] else "Unknown"
        trim = " ".join(title_parts[3:-1]) if drive_type != "Unknown" else " ".join(title_parts[3:])

        try:
            sold_price_elem = driver.find_element(By.CLASS_NAME, "bid-value")
            sold_price = sold_price_elem.text
        except:
            sold_price = "N/A"

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
            "Link": link
        })

    except Exception as e:
        print(f"❌ Error on listing #{idx}: {e}")
        continue

# Save to JSON
with open("cars.json", "w", encoding="utf-8") as f:
    json.dump(car_data, f, indent=4, ensure_ascii=False)

print(f"\n✅ Scraped and saved {len(car_data)} listings to cars.json")
driver.quit()
