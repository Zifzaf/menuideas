import requests
from bs4 import BeautifulSoup
import sqlite3


def create_database():
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS menus (menu TEXT NOT NULL PRIMARY KEY)"""
    )
    conn.commit()
    conn.close()


def insert_menu(menu_item):
    conn = sqlite3.connect("menu.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO menus (menu) VALUES (?)", (menu_item,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicate entries
    conn.close()


def fetch_menu(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        p_tags_inside_a_tags = soup.select("a p")

        menu_data = set()

        for p_tag in p_tags_inside_a_tags:
            dish = p_tag.get_text(strip=True)
            menu_data.add(dish)

        return list(menu_data)

    return None


if __name__ == "__main__":
    create_database()

    with open("urls.txt", "r") as file:
        urls = file.read().splitlines()

    for url in urls:
        menu = fetch_menu(url)
        if menu:
            for dish in menu:
                insert_menu(dish)
        else:
            print(f"Failed to fetch menu from {url}")
