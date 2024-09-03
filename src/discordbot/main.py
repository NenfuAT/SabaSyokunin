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
@minecraft_group.command(name="start", description="Minecraft鯖を起動します")
async def minecraft_start(interaction: discord.Interaction):
    await interaction.response.defer()
    response = requests.get(f'http://{MINECRAFT_CONTAINER_HOST}:{MINECRAFT_API_PORT}/api/start')
    
    if response.status_code == 200:
        await interaction.followup.send("Minecraft鯖を起動しました")
    elif response.status_code == 409:
        await interaction.followup.send("Minecraft鯖は既に起動しています")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {response.status_code}")

# /minecraft stop サブコマンドの定義
@minecraft_group.command(name="stop", description="Minecraft鯖を止めます")
async def minecraft_stop(interaction: discord.Interaction):
    await interaction.response.defer()
    response = requests.get(f'http://{MINECRAFT_CONTAINER_HOST}:{MINECRAFT_API_PORT}/api/stop')
    
    if response.status_code == 200:
        await interaction.followup.send("Minecraft鯖を停止しました")
    elif response.status_code == 409:
        await interaction.followup.send("Minecraft鯖は起動していません")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {response.status_code}")

# /minecraft backup サブコマンドの定義
@minecraft_group.command(name="backup", description="Minecraft鯖をバックアップします")
async def minecraft_backup(interaction: discord.Interaction):
    await interaction.response.defer()
    response = requests.get(f'http://{MINECRAFT_CONTAINER_HOST}:{MINECRAFT_API_PORT}/api/backup')
    
    if response.status_code == 200:
        await interaction.followup.send("Minecraft鯖をバックアップしました")
    elif response.status_code == 409:
        await interaction.followup.send("Minecraft鯖が起動中です停止してから実行してください")
    else:
        await interaction.followup.send(f"エラー: ステータスコード {response.status_code}")

class DeleteModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="本当に消しますか? 消す場合「delete」と入力してください")
        self.add_item(discord.ui.TextInput(label="確認コード", placeholder=""))

    async def on_submit(self, interaction: discord.Interaction):
        input_text = self.children[0].value
        if input_text == "delete":
            await interaction.response.defer()
            response = requests.get(f'http://{MINECRAFT_CONTAINER_HOST}:{MINECRAFT_API_PORT}/api/delete')
            
            if response.status_code == 200:
                await interaction.followup.send("Minecraft鯖を削除しました")
            elif response.status_code == 409:
                await interaction.followup.send("Minecraft鯖が起動中です停止してから実行してください")
            else:
                await interaction.followup.send(f"エラー: ステータスコード {response.status_code}")
        else:
            await interaction.response.send_message("無効な文字列です")

@minecraft_group.command(name="delete", description="Minecraft鯖を削除します")
async def minecraft_delete(interaction: discord.Interaction):
    modal = DeleteModal()
    await interaction.response.send_modal(modal)

# コマンドグループをCommandTreeに追加
tree.add_command(minecraft_group)

# /neko コマンドの定義
@tree.command(name='neko', description='猫が鳴きます')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('にゃーん')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
