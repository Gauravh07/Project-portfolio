import discord
import aiohttp
import base64
import time
# === CONFIG ===
TOKEN = 'your token here'  # Replace with your bot token
AVATAR_PATH = 'avatar.jpg'     # Ensure this file is in the same folder
CHANNEL_ID = 1368696857798246431  # Replace with your channel ID

class AvatarUpdater(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"[+] Logged in as {self.user}")

        # Step 1: Change avatar
        try:
            with open(AVATAR_PATH, 'rb') as f:
                b64_avatar = base64.b64encode(f.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"[-] File '{AVATAR_PATH}' not found.")
            await self.close()
            return

        payload = {'avatar': f'data:image/jpeg;base64,{b64_avatar}'}
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bot {TOKEN}'}
            async with session.patch('https://discord.com/api/v10/users/@me', json=payload, headers=headers) as resp:
                if resp.status == 200:
                    print("[+] Avatar changed successfully.")
                else:
                    print(f"[-] Failed to change avatar. Status: {resp.status}")
                    await self.close()
                    return

        # Step 2: Print CDN avatar URL
        avatar_url = self.user.display_avatar.url
        print(f"[CDN Avatar URL] {avatar_url}")

        # Step 3: Send message in specified channel
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            try:
                await channel.send("👋 Hello! I’ve just changed my avatar. Take a look!")
                print("[+] Message sent to channel.")
            except Exception as e:
                print(f"[-] Failed to send message: {e}")
        else:
            print("[-] Channel not found. Check if bot has access.")

        # Step 4: Done
        await self.close()

# === RUN ===


# === RUN ===
if __name__ == '__main__':
    start_time = time.time()
    client = AvatarUpdater()
    client.run(TOKEN)
    end_time = time.time()
    print(f"[+] Total runtime: {end_time - start_time:.2f} seconds")
