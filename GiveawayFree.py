import time
import requests
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

with open("Account.txt", "r") as keys:
    content = keys.read()
    start_index_email = content.find("Email :")
    start_index_Password = content.find("Password :")
    start_index_token = content.find("Token :")
    start_index_ID = content.find("ID :")

    
    if start_index_email and start_index_token:
        start_index_email += len("Email :")
        end_index_email = content.find("\n", start_index_email)
        
        start_index_Password += len("Password :")
        end_index_Password = content.find("\n", start_index_Password)

        start_index_token += len("Token :")
        end_index_token = content.find("\n", start_index_token)

        start_index_ID += len("ID :")
        end_index_ID = content.find("\n", start_index_ID)
        
        if end_index_email and end_index_token :
            email = content[start_index_email:end_index_email]
            password = content[start_index_Password:end_index_Password]
            TOKEN = content[start_index_token:end_index_token]
            id = int(content[start_index_ID:end_index_ID])
        else:
            print("E-posta veya token hatalı biçimde yazılmış.")
            quit
    else:
        print("E-posta veya token bulunamadı.")
        quit

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
time.sleep(9990)
submit_alien.click()

Bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@Bot.event
async def on_ready():
    global brain
    channel_id = id
    channel = Bot.get_channel(channel_id)
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
            if last_alian:
                for href in last_alian:
                    with open("giveaway.txt", "a") as file:
                        file.write(href + "\n")
                    driver.get(href)
                    try:
                        give = driver.find_element(By.ID, "giveaway-get-key")
                        give.click()
                        time.sleep(10)
                        comple = driver.find_element(
                            By.XPATH, "/html/body/div[6]/span/p[1]"
                        ).text
                        await channel.send(comple)
    
                    except:
                        refuse = driver.find_element("Couldn't claim giveaway:", href)
                        await channel.send(refuse)
            brain = current_href_set
        else:
            print("Siteye ulaşılamadı.")
Bot.run(TOKEN)
