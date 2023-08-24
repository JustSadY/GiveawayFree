import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

email = "Mail@example.com"
password = "Password"

site_alian_url = "https://na.alienwarearena.com/ucf/Giveaway"
login_alian_url = "https://na.alienwarearena.com/login"

with open("giveaway.txt", "r") as dosya:
    giveaway = dosya.read().split("\n")

brain = set()

driver = webdriver.Edge()

driver.get(login_alian_url)
email_alien = driver.find_element(By.NAME, "_username")
password_alien = driver.find_element(By.NAME, "_password")
submit_alien = driver.find_element(By.NAME, "_login")

email_alien.send_keys(email)
password_alien.send_keys(password)
time.sleep(10)
submit_alien.click()

while True:
    response = requests.get(site_alian_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        current_href_set = set(
            [
                link.get("href")
                for link in soup.find_all("a", href=True)
                if link.get("href").startswith("/ucf/show")
            ]
        )

        new_hrefs = current_href_set - brain
        prefix = "https://na.alienwarearena.com"
        last_alian = [
            prefix + item for item in new_hrefs if prefix + item not in giveaway
        ]
        driver.get(site_alian_url)
        time.sleep(10)
        try:
            give = driver.find_element(By.ID, "giveaway-get-key")
            give.click()
        except:
            print("Couldn't claim giveaway:", href)

        if last_alian:
            for href in last_alian:
                with open("giveaway.txt", "a") as file:
                    file.write(href + "\n")
                time.sleep(10)
                driver.get(href)
                try:
                    give = driver.find_element(By.ID, "giveaway-get-key")
                    give.click()
                    print("Giveaway claimed:", href)
                except:
                    print("Couldn't claim giveaway:", href)
        brain = current_href_set
    else:
        print("Siteye ulaşılamadı.")
    time.sleep(3600)