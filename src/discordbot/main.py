import os

import discord
import requests
from discord import app_commands

# 環境変数からトークンとホスト名を取得
TOKEN = os.environ['DISCORDBOT_TOKEN']
MINECRAFT_CONTAINER_HOST = os.environ['MINECRAFT_CONTAINER_HOST']
MINECRAFT_API_PORT = os.environ['MINECRAFT_API_PORT']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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
@minecraft_group.command(name="start", description="Start the Minecraft server")
async def minecraft_start(interaction: discord.Interaction):
    # 応答を遅延させる
    await interaction.response.defer()
    
    response = requests.get(f'http://{MINECRAFT_CONTAINER_HOST}:{MINECRAFT_API_PORT}/api/start')
    
    if response.status_code == 200:
        await interaction.followup.send("Minecraft鯖を起動しました")
    elif response.status_code == 409:
        await interaction.followup.send("Minecraft鯖は既に起動しています")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {response.status_code}")

# /minecraft stop サブコマンドの定義
@minecraft_group.command(name="stop", description="Stop the Minecraft server")
async def minecraft_stop(interaction: discord.Interaction):
    # 応答を遅延させる
    await interaction.response.defer()
    
    response = requests.get(f'http://{MINECRAFT_CONTAINER_HOST}:{MINECRAFT_API_PORT}/api/stop')
    
    if response.status_code == 200:
        await interaction.followup.send("Minecraft鯖を停止しました")
    elif response.status_code == 409:
        await interaction.followup.send("Minecraft鯖は起動していません")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {response.status_code}")

# コマンドグループをCommandTreeに追加
tree.add_command(minecraft_group)

# /neko コマンドの定義
@tree.command(name='neko', description='猫が鳴きます')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('にゃーん')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
