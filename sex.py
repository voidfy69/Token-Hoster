import discord
import asyncio
import requests
import threading
import sys
import os
import random
from aiohttp import ClientSession
from typing import Optional
from colorama import Fore
import time

class TaskPool:
    def __init__(self, limit):
        self.sem = asyncio.Semaphore(limit)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def put(self, coro):
        async with self.sem:
            await coro

class TokenHandler:
    def __init__(self, tokens, proxies, proxyless):
        self.tokens = tokens
        self.proxies = proxies
        self.proxyless = proxyless

    async def start(self):
        channel = ""  # Replace with your channel ID
        async with TaskPool(5_000) as pool:
            tasks = [self.typingSpammer(token, channel) for token in self.tokens]
            await asyncio.gather(*tasks)  # Gather all tasks

    async def typingSpammer(self, token, chId):
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        tk = token
        try:
            tk = token[:25] + "*" * 34
        except:
            tk = "*" * len(token)

        randomProxy = ''
        if not self.proxyless:
            randomProxy = self.proxies[random.randint(0, len(self.proxies) - 1)]

        while True:
            async with ClientSession(headers=headers) as session:
                async with session.post(f"https://discord.com/api/v9/channels/{chId}/typing", proxy=randomProxy) as r:
                    if r.status == 204:
                        print(
                            '\n                                       '
                            + Fore.BLUE + '[' + Fore.CYAN + '/' +
                            Fore.BLUE + '] ' + Fore.CYAN +
                            f'{tk} successfully started typing!\n' +
                            Fore.RESET)
                    elif r.status == 400:
                        print(
                            '\n                                       '
                            + Fore.BLUE + '[' + Fore.CYAN + '/' +
                            Fore.BLUE + '] ' + Fore.CYAN +
                            f'{tk} couldn\'t start typing!\n' +
                            Fore.RESET)
                    else:
                        text = await r.text()
                        if "You need to verify your account" in text:
                            print(
                                '\n                                       '
                                + Fore.BLUE + '[' + Fore.CYAN + '/' +
                                Fore.BLUE + '] ' + Fore.CYAN +
                                f'{tk} is unverified and removed from list!\n'
                                + Fore.RESET)
                            if token in self.tokens:
                                self.tokens.remove(token)
                        elif "Unauthorized" in text:
                            print(
                                '\n                                       '
                                + Fore.BLUE + '[' + Fore.CYAN + '/' +
                                Fore.BLUE + '] ' + Fore.CYAN +
                                f'{tk} is invalid and removed from list!\n'
                                + Fore.RESET)
                            if token in self.tokens:
                                self.tokens.remove(token)
                        else:
                            print(
                                '\n                                       '
                                + Fore.BLUE + '[' + Fore.CYAN + '/' +
                                Fore.BLUE + '] ' + Fore.CYAN +
                                f'{tk} failed to start typing!\n' +
                                Fore.RESET)
            await asyncio.sleep(10)  # Wait before restarting the typing

def Clear():
    if sys.platform in ["linux", "linux2"]:
        os.system("clear")
    else:
        os.system("cls")

Clear()

def setTitle(title: Optional[any] = None):
    if sys.platform.startswith('win'):
        os.system(f"title {title}")

setTitle("Multiple Token Hoster - [Void]")

session = requests.Session()
tokens = []
with open("tokens.txt", "r") as f:
    tokens_ = f.read().split("\n")

if len(tokens_) == 0:
    print("Void | There Are No Tokens, Please Add Some Tokens To Host In tokens.txt File.")
    exit()

def Check_Token(Token):
    response = requests.get(f"https://discord.com/api/v9/users/@me", headers={"Authorization": Token})
    if response.status_code in [204, 200, 201]:
        print(f"Void | {Token} Is Valid.")
        tokens.append(Token)
    if "need to verify" in response.text:
        print(f"Void | {Token} Is On Verification.")
    elif response.status_code in [404, 401, 400]:
        print(f"Void | {Token} Invalid Token Or Rate Limited.")

for tk in tokens_:
    Check_Token(tk)

if len(tokens) == 0:
    print("Void | All Tokens Were Invalid, Try Again Later With Working Tokens.")
    exit()

time.sleep(2)
Clear()
menu = f"""{Fore.RED}[-]{Fore.RESET} Created by Void\n"""
print(menu)

st = "Idle"
akks = []
stl = st.lower()
if stl == "dnd":
    status = discord.Status.dnd
elif stl == "idle":
    status = discord.Status.idle
elif stl == "online":
    status = discord.Status.online

ty = "Streaming"
name = "Void On Top"
tyy = ty.lower()
if tyy == "streaming":
    acttt = discord.Streaming(name=name, url="https:/twitch/Void")
elif tyy == "playing":
    acttt = discord.Game(name=name)
elif tyy == "listening":
    acttt = discord.Activity(type=discord.ActivityType.listening, name=name)
elif tyy == "watching":
    acttt = discord.Activity(type=discord.ActivityType.watching, name=name)

async def hosting(token, status, activity):
    client = discord.Client(status=status, activity=activity)

    @client.event
    async def on_ready():
        print(f"Void | Connected: {client.user}")
        vc = client.get_channel(123)  # Replace with your voice channel ID
        if vc is not None:
            try:
                await vc.connect()
            except Exception as e:
                print(f"Error connecting to voice channel: {e}")

    await client.start(token, bot=False)

loop = asyncio.get_event_loop()
for tk in tokens:
    loop.create_task(hosting(tk, status, acttt))
    akks.append(tk)
    print(f"Void | {tk} Is Hosted.\n")

threading.Thread(target=loop.run_forever).start()

token_handler = TokenHandler(tokens, proxies=[], proxyless=True)
loop.create_task(token_handler.start())

while True:
    pass
