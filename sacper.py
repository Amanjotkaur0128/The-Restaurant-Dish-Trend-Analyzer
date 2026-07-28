import requests
from bs4 import BeautifulSoup
import re 
import pandas as pd
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab') 
from collections import Counter
import seaborn as sns

from nltk.corpus import stopwords # Keep this
from nltk.tokenize import word_tokenize # Keep this

pd.set_option('display.float_format', lambda x: '%.2f' % x)


def clean_price(price_str):
    """
    Cleans a price string (e.g., '$ 1,000') into a float (e.g., 1000.00).
    Returns None if price_str is invalid or cannot be converted to a reasonable price.
    """
    if price_str is None:
        return None

    # Remove currency symbols, commas, and any leading/trailing whitespace
    cleaned_price = re.sub(r'[^\d.]', '', price_str).strip()

    # If after cleaning, the string is empty or just a dot, return None
    if not cleaned_price or cleaned_price == '.':
        return None

    try:
        price_float = float(cleaned_price)
        # Add a sanity check for extremely high or low prices.
        # Assuming prices are generally between GYD 100 and GYD 100,000
        # You can adjust these bounds if necessary based on real menu prices.
        if 100 <= price_float <= 100000:
            return price_float
        else:
            print(f"Warning: Price '{price_str}' (cleaned to {price_float}) is outside expected range. Returning None.")
            return None # Price is outside expected range
    except ValueError:
        print(f"Warning: Could not convert price string '{cleaned_price}' (from '{price_str}') to float. Returning None.")
        return None

def scrape_giraffe_cafe(url):
    """
    Scrapes menu items from the Giraffe Cafe website.
    """
    print(f"Attempting to scrape: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return [] 

    soup = BeautifulSoup(response.content, 'html.parser')

    menu_items_data = []

    
    menu_items = soup.find_all('div', class_='menu-item')

    if not menu_items:
        print("No menu items found with class 'menu-item'. Check selectors.")

    for item in menu_items:
        name = None
        price = None
        description = None

        name_tag = item.find('h3', class_='menu-title')
        if name_tag:
            name = name_tag.get_text(strip=True)

        price_tags = item.find_all('div', class_='menu-price')
        for p_tag in price_tags:
            price_text = p_tag.get_text(strip=True)
            if price_text.startswith('$'): 
                price = price_text
                break 

       
        description_tag = item.find('div', class_='menu-subtitle')
        if description_tag:
            description = description_tag.get_text(strip=True)

        if name and price: # Only add if we successfully found at least name and price
            menu_items_data.append({
                'restaurant': 'Giraffe Cafe',
                'dish_name': name,
                'price': clean_price(price),
                'description': description if description else '', # Ensure description is always a string
                'cuisine_type': 'Cafe' # Manually assign for now
            })

    return menu_items_data

def scrape_pf_changs(url):
    """
    Scrapes menu items from the P.F. Chang's website.
    """
    print(f"Attempting to scrape: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return [] # Return an empty list if there's an error

    soup = BeautifulSoup(response.content, 'html.parser')

    menu_items_data = []

   
    menu_items = soup.find_all('div', class_='w-layout-cell')

    if not menu_items:
        print("No menu items found with class 'w-layout-cell'. Check selectors.")

    for item_cell in menu_items:
        name = None
        description = None
        price = None

    
        name_tag = item_cell.find('h3', class_='heading')
        if name_tag:
            name = name_tag.get_text(strip=True)

        
        description_tag = item_cell.find('p', class_='paragraph-3')
        if description_tag:
            description = description_tag.get_text(strip=True)

        
       
        price_tag = item_cell.find('p', class_='product-price')
        if price_tag:
            price_tag = item_cell.find('p', class_='product-price')
        if price_tag:
            # TEMPORARY DEBUG PRINT: See the raw tag content
            print(f"DEBUG: P.F. Chang's raw price tag: {price_tag}")
            price = price_tag.get_text(strip=True)
            # TEMPORARY DEBUG PRINT: See the string price before cleaning
            print(f"DEBUG: P.F. Chang's string price: '{price}'")
            price = price_tag.get_text(strip=True)

        # Only add if we found a name and price
        if name and price:
            menu_items_data.append({
                'restaurant': "P.F. Chang's",
                'dish_name': name,
                'price': clean_price(price),
                'description': description if description else '',
                'cuisine_type': 'Asian-American' # Manually assign for now
            })
    return menu_items_data

def scrape_nikkei_guyana(url):
    """
    Scrapes menu items from the Nikkei Guyana website.
    """
    print(f"Attempting to scrape: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return [] # Return an empty list if there's an error

    soup = BeautifulSoup(response.content, 'html.parser')

    menu_items_data = []


    menu_items = soup.find_all('div', class_='pt-food-menu-item')

    if not menu_items:
        print("No menu items found with class 'pt-food-menu-item'. Check selectors.")

    for item in menu_items:
        name = None
        price = None
        description = None

        
        name_span = item.find('h6', class_='pt-food-menu-title')
        if name_span:
         
            name_wrap_span = name_span.find('span', class_='title-wrap')
            if name_wrap_span:
                name = name_wrap_span.get_text(strip=True)
            else: # Fallback if title-wrap isn't always present
                name = name_span.get_text(strip=True)

        price_tag = item.find('span', class_='pt-food-menu-price')
        if price_tag:
            price = price_tag.get_text(strip=True)

   
        description_tag = item.find('p', class_='pt-food-menu-details')
        if description_tag:
            description = description_tag.get_text(strip=True)

        if name and price: # Only add if we successfully found at least name and price
            menu_items_data.append({
                'restaurant': 'Nikkei Guyana',
                'dish_name': name,
                'price': clean_price(price),
                'description': description if description else '',
                'cuisine_type': 'Nikkei (Peruvian-Japanese)' # Manually assign for now
            })

    return menu_items_data

if __name__ == "__main__":
    all_scraped_data = []
    output_csv_path = 'scraped_menu_data.csv'

    # Set Pandas display option for better readability of floats
    pd.set_option('display.float_format', lambda x: '%.2f' % x) # Added this line for clean output

    perform_scraping = True # Keep this True to re-scrape with the improved clean_price

    if perform_scraping:
        # Scrape Giraffe Cafe
        giraffe_url = "https://www.giraffecafegy.com/menu"
        giraffe_data = scrape_giraffe_cafe(giraffe_url)
        if giraffe_data:
            print(f"\nSuccessfully scraped {len(giraffe_data)} items from Giraffe Cafe.")
            all_scraped_data.extend(giraffe_data)
        else:
            print("Failed to scrape any menu items from Giraffe Cafe.")

        print("-" * 50)

        # Scrape P.F. Chang's
        pf_changs_url = "https://www.pfchangs.gy/our-menu"
        pf_changs_data = scrape_pf_changs(pf_changs_url)
        if pf_changs_data:
            print(f"\nSuccessfully scraped {len(pf_changs_data)} items from P.F. Chang's.")
            all_scraped_data.extend(pf_changs_data)
        else:
            print("Failed to scrape any menu items from P.F. Chang's.")

        print("-" * 50)

        # Scrape Nikkei Guyana
        nikkei_url = "https://nikkeiguyana.com/food-menu/"
        nikkei_data = scrape_nikkei_guyana(nikkei_url)
        if nikkei_data:
            print(f"\nSuccessfully scraped {len(nikkei_data)} items from Nikkei Guyana.")
            all_scraped_data.extend(nikkei_data)
        else:
            print("Failed to scrape any menu items from Nikkei Guyana.")

        print("\n" + "=" * 50)
        print(f"Total items scraped across all restaurants: {len(all_scraped_data)}")
        print("=" * 50)

        # Create DataFrame and Save to CSV
        if all_scraped_data:
            df = pd.DataFrame(all_scraped_data)
            df.to_csv(output_csv_path, index=False, encoding='utf-8')
            print(f"\nSuccessfully saved scraped data to {output_csv_path}")
        else:
            print("No data to process or save.")
            exit()

    else: # If perform_scraping is False, load from CSV (for quicker iteration on analysis)
        try:
            df = pd.read_csv(output_csv_path)
            print(f"\nSuccessfully loaded data from {output_csv_path} for analysis.")
            print(f"Total items loaded: {len(df)}")
            # Re-apply clean_price to the loaded data to ensure consistency if any manual changes were made to CSV
            df['price'] = df['price'].apply(clean_price)
            # Drop rows where price became None after cleaning
            df.dropna(subset=['price'], inplace=True)
            print(f"Total items after cleaning price column: {len(df)}")

        except FileNotFoundError:
            print(f"Error: {output_csv_path} not found. Please run with perform_scraping=True first.")
            exit()

        # --- Data Analysis and Visualization ---
    print("\n--- Starting Data Analysis ---")

    # Basic Statistics
    print("\nOverall Price Statistics:")
    print(df['price'].describe())

    print("\nAverage Price per Restaurant:")
    print(df.groupby('restaurant')['price'].mean().sort_values(ascending=False))

    print("\nNumber of Dishes per Restaurant:")
    print(df['restaurant'].value_counts())

    # --- Basic Visualization (Bar Chart of Average Prices) ---
    plt.figure(figsize=(10, 6))
    # Inside your plotting code for the Average Dish Price chart:
    sns.barplot(x='restaurant', y='price', data=df, estimator=lambda x: x.mean(), color='pink')
    plt.title('Average Dish Price per Restaurant')
    plt.xlabel('Restaurant')
    plt.ylabel('Average Price (GYD)')
    # Fix for tilted X-axis labels
    plt.xticks(rotation=0, ha='center') # Set rotation to 0 for horizontal labels
    plt.tight_layout()
    plt.savefig('average_price_per_restaurant.png')
    plt.show()

    print(f"\nGenerated 'average_price_per_restaurant.png'")

    # --- Another Basic Visualization (Dish Count per Restaurant) ---
    plt.figure(figsize=(10, 6))
    sns.countplot(x='restaurant', data=df, palette='pastel')
    plt.title('Number of Dishes per Restaurant')
    plt.xlabel('Restaurant')
    plt.ylabel('Number of Dishes')
    # Fix for tilted X-axis labels
    plt.xticks(rotation=0, ha='center') # Set rotation to 0 for horizontal labels
    plt.tight_layout()
    plt.savefig('dish_count_per_restaurant.png')
    plt.show()

    print(f"\nGenerated 'dish_count_per_restaurant.png'")  

    print("\n--- Generating Price Distribution Histograms ---")
    # Create a figure with subplots for each restaurant's price histogram
    restaurants = df['restaurant'].unique()
    n_restaurants = len(restaurants)

    # Determine grid size for subplots
    cols = 2
    rows = (n_restaurants + cols - 1) // cols # Calculate rows needed

    plt.figure(figsize=(cols * 6, rows * 4)) # Adjust figure size dynamically

    for i, restaurant in enumerate(restaurants):
        plt.subplot(rows, cols, i + 1) # Create subplot
        # Filter data for the current restaurant
        restaurant_data = df[df['restaurant'] == restaurant]['price'].dropna() # Drop NaNs for histogram

        # Plot histogram
        sns.histplot(restaurant_data, kde=True, bins=10,palette='flare') # kde=True adds a density curve
        plt.title(f'Price Distribution: {restaurant}')
        plt.xlabel('Price (GYD)')
        plt.ylabel('Number of Dishes')
        plt.tight_layout()

    plt.suptitle('Price Distribution by Restaurant (Histograms)', y=1.02) # Overall title
    plt.savefig('price_distribution_histograms.png')
    plt.show()
    print(f"\nGenerated 'price_distribution_histograms.png'")

    # --- New Analysis: Price Distribution (Box Plots) ---
    print("\n--- Generating Price Distribution Box Plots ---")
    plt.figure(figsize=(12, 7)) # Single figure for all box plots
    sns.boxplot(x='restaurant', y='price', data=df, palette='pastel')
    plt.title('Price Distribution by Restaurant (Box Plots)')
    plt.xlabel('Restaurant')
    plt.ylabel('Price (GYD)')
    plt.xticks(rotation=0, ha='center') # Ensure labels are horizontal
    plt.tight_layout()
    plt.savefig('price_distribution_boxplots.png')
    plt.show()
    print(f"\nGenerated 'price_distribution_boxplots.png'")  

    # --- New Analysis: Common Keywords/Ingredients PER RESTAURANT ---
    print("\n--- Analyzing Common Keywords/Ingredients PER RESTAURANT ---")

    # Get unique restaurant names
    restaurants = df['restaurant'].unique()
    top_n_keywords = 15 # You can adjust this number for how many top keywords per chart

    # Get English stopwords
    stop_words = set(stopwords.words('english'))

    for restaurant in restaurants:
        print(f"\nProcessing keywords for: {restaurant}")

        # Filter data for the current restaurant
        restaurant_data = df[df['restaurant'] == restaurant].copy()
        
        # Combine dish names and descriptions into a single text series
        restaurant_data['combined_text'] = restaurant_data['dish_name'].fillna('') + ' ' + restaurant_data['description'].fillna('')

        all_words_restaurant = []
        for text in restaurant_data['combined_text']:
            # Tokenize text (split into words) and convert to lowercase
            tokens = word_tokenize(text.lower())
            # Filter out non-alphabetic words, stopwords, and short words (e.g., length < 2)
            filtered_words = [
                word for word in tokens
                if word.isalpha() and word not in stop_words and len(word) > 2
            ]
            all_words_restaurant.extend(filtered_words)

        # Count word frequencies for the current restaurant
        word_counts_restaurant = Counter(all_words_restaurant)

        # Get the top N most common words for this restaurant
        common_words_restaurant = word_counts_restaurant.most_common(top_n_keywords)

        if common_words_restaurant: # Only plot if there are words found
            common_words_df_restaurant = pd.DataFrame(common_words_restaurant, columns=['Word', 'Frequency'])

            print(f"Top {top_n_keywords} Keywords for {restaurant}:")
            print(common_words_df_restaurant)

            # Visualize Top Keywords for the current restaurant
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Frequency', y='Word', data=common_words_df_restaurant.sort_values(by='Frequency', ascending=True), palette='viridis')
            plt.title(f'Top {top_n_keywords} Common Keywords: {restaurant}')
            plt.xlabel('Frequency')
            plt.ylabel('Keyword')
            plt.tight_layout()

            # Generate a clean filename for each restaurant (e.g., "top_keywords_Giraffe_Cafe.png")
            filename = f"top_keywords_{restaurant.replace(' ', '_').replace('.', '')}.png"
            plt.savefig(filename)
            plt.show()
            print(f"\nGenerated '{filename}'")
        else:
            print(f"No significant keywords found for {restaurant}.")    
print("raw data")
print(df.to_string()) 


