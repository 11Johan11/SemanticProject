import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json
import time

if __name__ == "__main__":
    results = []

    # Load movie data
    with open("search_movie_dump.json", "r", encoding="utf-8") as f:
        searchable_movies = json.load(f)

    total = len(searchable_movies)
    
    # Chrome options to block images and styles
    chrome_options = uc.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2,  # Block images
        "profile.managed_default_content_settings.stylesheets": 2  # Block stylesheets
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Initialize the browser with options
    driver = uc.Chrome(options=chrome_options, headless=False)
    
    c = 0
    for entry in searchable_movies:
        imdb = entry["imdb"]["value"]
        # Open the IMDb page
        driver.get(f'https://www.imdb.com/title/{imdb}/?ref_=nm_flmg_knf_c_1')

        # Wait for the page to load completely
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to load

        try:
            # Locate the rating element using its data-testid attribute
            rating_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="hero-rating-bar__aggregate-rating__score"] > span.sc-d541859f-1')
            
            # Extract the text content (the rating value)
            rating = rating_element.text
            print(f"Rating: {rating}")
        except Exception as e:
            print(f"An error occurred: {e}")
            rating = "N/A"  # Default value if scraping fails
        finally:
            # Append results
            results.append({"imdb": imdb, "rating": rating})
            c += 1
            print(f"Remaining: {total - c}")

    # Save results to a JSON file
    with open("movie_ratings.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    # Close the browser
    driver.quit()
