import requests
import time
import json


# For recursive scraping of all the property links
page = 1
end_page = 30

html_lines = []
search_string = "url"


def scrape_listing_links(search_string: str, start_page: int):
    url = f"https://www.houseful.ca/toronto-on/p-{start_page}/@43.653226,-79.3831843/"  # This is the main page list collection
    response = requests.get(url)

    result = []

    if response.status_code == 200:
        html_lines = response.text.splitlines()
    else:
        print(f"Request failed with status code {response.status_code}")

    for line in html_lines:
        if search_string in line and line != '"url": "https://www.houseful.ca/"':
            split_line = line.split(": ").pop()
            split_line = split_line.strip('",\\')  # Remove the double quotes and comma
            print(split_line)
            result.append(split_line)

    return result


def save_file(fileName: str, data):
    with open(fileName, "w") as f:
        json.dump(data, f)


result = []
scrape_listing_links(search_string, page)

while page != 3:
    print(f"Scraping page {page}")
    links = scrape_listing_links(
        search_string, page
    )  # Get the links from the current page
    result.extend(links)  # Use extend() instead of append()
    page += 1
    print("Done scraping, waiting 5 seconds...")
    time.sleep(5)

print(f"Output: {result}")
result = list(set(result))  # Removes duplicates

save_file("houseful_links.json", result)
