import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from urllib.parse import urljoin
from nearby_cities import CALIFORNIA_CITIES

# Keywords to match job titles
KEYWORDS = ['data', 'analyst', 'market', 'business', 'growth', 'product', 'report', 'strategy', 'operations', 'new graduate', 'graduate', 'project', 'associate', 'intern', 'junior', 'entry level','Account Manager', 'Account Executive', 'Customer Success', 'Support', 'Marketing','Consultant', 'Developer', 'Specialist', 'coordinator']


# File paths
INPUT_FILE = 'company_careers_los_angeles.csv'
OUTPUT_FILE = 'jobs_scraped_la_results.csv'

# Set up headless Chrome
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

# Extract jobs from dynamic career pages
def extract_jobs_with_selenium(driver, url):
    job_posts = []
    try:
        driver.set_page_load_timeout(20)
        driver.get(url)
        time.sleep(5)  # Wait for dynamic content to load

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            try:
                text = link.text.strip()
                href = link.get_attribute("href")
                if text and href and any(k in text.lower() for k in KEYWORDS):
                    job_posts.append({
                        'Job Title': text,
                        'Job Link': urljoin(url, href),
                        'Date Posted': None  # Optional: Add logic to extract date if needed
                    })
            except Exception:
                continue

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error loading {url}: {e}")
    return job_posts

def is_city_mentioned(title):
    title_lower = title.lower()
    return any(city in title_lower for city in CALIFORNIA_CITIES)

def main():
    df = pd.read_csv(INPUT_FILE)
    results = []
    driver = init_driver()

    for index, row in df.iterrows():
        company_name = str(row.iloc[0]).strip()
        url = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else None

        if not url or url.lower() == 'nan' or not url.startswith('http'):
            print(f" Skipping {company_name}: No valid URL")
            continue

        print(f" Scraping: {company_name} | {url}")
        try:
            jobs = extract_jobs_with_selenium(driver, url)
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue
        if not jobs:
            print(f"No jobs found for {company_name} at {url}")
            continue

        for job in jobs:
            title = job['Job Title']
            if not is_city_mentioned(title):
                print(f"Skipping {title}: Not in California cities")
                continue

            results.append({
                'Company Name': company_name,
                'Job Title': title,
                'Date Posted': job['Date Posted'],
                'Job Link': job['Job Link']
            })

    driver.quit()
    output_df = pd.DataFrame(results)
    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\\n Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()