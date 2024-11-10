import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
from keep_alive import keep_alive

# Botの初期設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ステータス表示（presence）
@tasks.loop(seconds=20)
async def presence_loop():
    game = discord.Game("/help - Bot Help")
    await bot.change_presence(activity=game)

# コマンドの同期が一度だけ行われるように制御するためのフラグ
synced = False

# Bot起動時の処理
@bot.event
async def on_ready():
    global synced
    if not synced:
        await bot.tree.sync()  # スラッシュコマンドの同期
        synced = True  # 同期済みフラグを設定
        print("スラッシュコマンドを同期しました。")
    print(f"Logged in as {bot.user.name}")
    presence_loop.start()

# /help コマンド：Botの使い方を表示
@bot.tree.command(
    name="help",
    description="利用可能なコマンド一覧を表示します"
)
async def bot_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ボットの使い方", color=discord.Colour.blurple()
    ).add_field(name="/say <メッセージ>", value="Botが指定したメッセージを送信") \
     .add_field(name="/random", value="ランダムに名前を変更します") \
     .add_field(name="/help", value="利用可能なコマンド一覧を表示します")
    
    await interaction.response.send_message(embed=embed)

# /say コマンド：指定されたメッセージをBotが発言
@bot.tree.command(
    name="say",
    description="指定されたメッセージをBotが発言します"
)
@app_commands.describe(message="Botが発言するメッセージ")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"{message}")

# /random コマンド：ユーザーの名前をランダムに変更
@bot.tree.command(
    name="random",
    description="ランダムにユーザーの名前を変更します"
)
async def random_name(interaction: discord.Interaction):
    random_names = ["受験面倒…", "鯖主とねんねこ万歳", "早く幻想郷行きたい…", "スーパーノヴァ", "ねんねこの技術力には脱帽だよ…"]
    new_name = random.choice(random_names)
    try:
        await interaction.user.edit(nick=new_name)
        await interaction.response.send_message(f"あなたの新しい名前は {new_name} です!")
    except discord.Forbidden:
        await interaction.response.send_message("名前を変更できませんでした。権限を確認してください。")

# Botを実行
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
