import asyncio
import json
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

# --- 設定ファイルの読み込み ---
def load_config():
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            # DiscordサーバーID(k)をintに変換して保持
            return {int(k): v for k, v in raw_data.items()}
    except FileNotFoundError:
        print("Error: config.json が見つかりません。")
        return {}

SERVER_CONFIG = load_config()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
HEADERS = {
    'Authorization': f'PVEAPIToken={PROXMOX_API_TOKEN_ID}={PROXMOX_API_TOKEN_SECRET}',
}

def proxmox_start(vmid):
    url = f"{PROXMOX_HOST}/api2/json/nodes/{PROXMOX_NODE}/lxc/{vmid}/status/start"
    return requests.post(url, headers=HEADERS, verify=False)

def proxmox_shutdown(vmid):
    url = f"{PROXMOX_HOST}/api2/json/nodes/{PROXMOX_NODE}/lxc/{vmid}/status/shutdown"
    return requests.post(url, headers=HEADERS, verify=False)

def proxmox_status(vmid):
    url = f"{PROXMOX_HOST}/api2/json/nodes/{PROXMOX_NODE}/lxc/{vmid}/status/current"
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
    conf = SERVER_CONFIG.get(interaction.guild_id)
    if not conf:
        await interaction.response.send_message("このサーバーの設定が config.json にありません。", ephemeral=True)
        return
    await interaction.response.defer()
    res = proxmox_start(conf['VMID'])
    if res.status_code == 200 or res.status_code == 500 and "already running" in res.text:
        for _ in range(24):
            if is_minecraft_server_alive(conf['HOST'], conf['PORT']):
                await interaction.followup.send("Minecraft鯖が起動しました")
                return
            await asyncio.sleep(5)
        await interaction.followup.send("Minecraft鯖の起動を確認できませんでした")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {res.status_code}")


@minecraft_group.command(name="stop", description="Minecraft鯖を止めます")
async def minecraft_stop(interaction: discord.Interaction):
    conf = SERVER_CONFIG.get(interaction.guild_id)
    if not conf:
        await interaction.response.send_message("このサーバーの設定がありません。", ephemeral=True)
        return
    await interaction.response.defer()
    res = proxmox_shutdown(conf['VMID'])
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
