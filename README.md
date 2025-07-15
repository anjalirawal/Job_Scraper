# 💼 California Job Scraper

A Python-based web scraper to automatically extract job postings from company career pages located within a 150-mile radius of Los Angeles, CA. The scraper uses both BeautifulSoup (for static pages) and Selenium (for dynamic content), and filters results based on keywords and location-specific city names derived from geographic proximity.

---

## 📂 Project Structure

├── company_careers_los_angeles.csv # Input: List of companies and their careers page URLs
├── job_scraped_results.csv # Output: Final job listings scraped
├── selenium_job_scraper.py # Selenium-based scraper script
├── nearby_cities.py # Auto-generated list of cities within 150 miles of LA
├── uszips.csv # US ZIP code dataset for geolocation
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .gitignore # Files to ignore in Git