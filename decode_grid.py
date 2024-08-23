import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load URL")
    return response.text

def parse_html_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    if not tables:
        raise Exception("No tables found in the document")
    
    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 3:  # Ensure we have x, character, y
                try:
                    x = int(cols[0].text.strip())
                    character = cols[1].text.strip()
                    y = int(cols[2].text.strip())
                    data.append([x, character, y])
                except ValueError:
                    continue  # Skip rows that cannot be converted to integers
    return data

def print_grid_from_data(data):
    df = pd.DataFrame(data, columns=['x', 'character', 'y'])
    max_x = df['x'].max()
    max_y = df['y'].max()

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for _, row in df.iterrows():
        grid[row['y']][row['x']] = row['character']

    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
    html_content = fetch_data_from_url(url)
    data = parse_html_table(html_content)
    print_grid_from_data(data)
