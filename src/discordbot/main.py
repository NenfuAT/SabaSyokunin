import asyncio
import os
import socket

import discord
import requests
from discord import app_commands

# 環境変数からトークンとホスト名を取得
TOKEN = os.environ['DISCORDBOT_TOKEN']
PROXMOX_API_TOKEN_ID = os.environ['PROXMOX_API_TOKEN_ID']  
PROXMOX_API_TOKEN_SECRET = os.environ['PROXMOX_API_TOKEN_SECRET']
PROXMOX_HOST = os.environ['PROXMOX_HOST']  
PROXMOX_NODE = os.environ['PROXMOX_NODE'] 
MINECRAFT_LXC_VMID = os.environ['MINECRAFT_LXC_VMID']
MINECRAFT_LXC_HOST = os.environ['MINECRAFT_LXC_HOST']
MINECRAFT_LXC_PORT = int(os.environ['MINECRAFT_LXC_PORT'])

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
HEADERS = {
    'Authorization': f'PVEAPIToken={PROXMOX_API_TOKEN_ID}={PROXMOX_API_TOKEN_SECRET}',
}

def proxmox_start():
    url = f"{PROXMOX_HOST}/api2/json/nodes/{PROXMOX_NODE}/lxc/{MINECRAFT_LXC_VMID}/status/start"
    res = requests.post(url, headers=HEADERS, verify=False)
    return res

def proxmox_shutdown():
    url = f"{PROXMOX_HOST}/api2/json/nodes/{PROXMOX_NODE}/lxc/{MINECRAFT_LXC_VMID}/status/shutdown"
    res = requests.post(url, headers=HEADERS, verify=False)
    return res

def proxmox_status():
    url = f"{PROXMOX_HOST}/api2/json/nodes/{PROXMOX_NODE}/lxc/{MINECRAFT_LXC_VMID}/status/current"
    res = requests.get(url, headers=HEADERS, verify=False)
    return res

def is_minecraft_server_alive(host: str, port: int = 25565, timeout: float = 2.0) -> bool:
    """
    MinecraftサーバにTCP接続できるか試す。
    接続成功したらTrue、失敗したらFalse。

    Args:
        host (str): MinecraftサーバのIPまたはホスト名
        port (int): Minecraftサーバのポート番号（デフォルト25565）
        timeout (float): ソケットのタイムアウト秒数

    Returns:
        bool: 接続成功かどうか
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
# 起動時に動作する処理
@client.event
async def on_ready():
    print('ログインしました')
    new_activity = "テスト"
    await client.change_presence(activity=discord.Game(new_activity))
    await tree.sync()

# /minecraft コマンドグループの定義
minecraft_group = app_commands.Group(name="minecraft", description="Manage the Minecraft server")

# /minecraft start サブコマンドの定義
@minecraft_group.command(name="start", description="Minecraft鯖を起動します")
async def minecraft_start(interaction: discord.Interaction):
    await interaction.response.defer()
    res = proxmox_start()
    if res.status_code == 200 or res.status_code == 500 and "already running" in res.text:
        for _ in range(24):
            if is_minecraft_server_alive(MINECRAFT_LXC_HOST,MINECRAFT_LXC_PORT):
                await interaction.followup.send("Minecraft鯖が起動しました")
                return
            await asyncio.sleep(5)
        await interaction.followup.send("Minecraft鯖の起動を確認できませんでした")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {res.status_code}")


@minecraft_group.command(name="stop", description="Minecraft鯖を止めます")
async def minecraft_stop(interaction: discord.Interaction):
    await interaction.response.defer()
    res = proxmox_shutdown()
    if res.status_code == 200:
        await interaction.followup.send("Minecraft鯖に停止命令を出しましたまもなく終了します...")
    elif res.status_code == 500 and "not running" in res.text:
        await interaction.followup.send("Minecraft鯖は起動していません")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {res.status_code}")


# コマンドグループをCommandTreeに追加
tree.add_command(minecraft_group)

# /neko コマンドの定義
@tree.command(name='neko', description='猫が鳴きます')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('にゃーん')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
