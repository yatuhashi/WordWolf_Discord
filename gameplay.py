import discord
import random
import asyncio


class OneGame():

    def __init__(self):
        self.members = []
        self.wolf = []
        self.wolf_num = 1
        self.minor_word = ""
        self.major_word = ""
        self.time_min = 3
        self.post = {}
        self.channel = None

    def AddMember(self, mem):
        self.members.append(mem)
        self.post[mem] = 0

    def DelMember(self, mem):
        del self.members[mem]
        del self.post[mem]

    def ResetMember(self):
        self.members = []
        self.post = {}

    def Word(self, mi, ma):
        self.minor_word = mi
        self.major_word = ma

    def Time(self, mi):
        self.time_min = mi

    def WolfNum(self, num):
        self.wolf_num = num

    def Wolf(self):
        self.wolf = random.sample(self.members, self.wolf_num)

    def Post(self, mem):
        self.post[mem] = self.post[mem] + 1

    def Channel(self, ch):
        self.channel = ch


SomeGame = OneGame()
client = discord.Client()
inst = """\nMemberの入力(\":GameAddMember やつはし\")\n
Memberの削除(\":GameDelMember やつはし\")\n
Memberのリセット(\":GameResetMember\")\n
Wordのセット(\":GameWord 多数派 少数派\")\n
Wolfの人数を変える(\":GameWolfNum 2\")\n
Gameの時間を変えるmin(\":GameTime 5\")\n
投票は、DMに(\":GamePost @membername\")\n
Game開始(:GameStart)\n
"""


@client.event
async def on_message(message):
    global SomeGame
    # Gameを初期化し、メンバーの募集を始める
    if message.content.startswith(":GameReset"):
        SomeGame = OneGame()
        SomeGame.Channel(message.channel)
        await client.send_message(message.channel, "Gameデータをリセットしました。\n")
        await client.send_message(message.channel, inst)
        await client.send_message(message.channel, "現在いるメンバーは、")
        for i in message.server.members:
            await client.send_message(message.channel, i.name + "\n")
    # メンバーの追加
    if message.content.startswith(":GameAddMember "):
        member = message.content.split(" ")
        SomeGame.AddMember(member[1])
        for i in message.server.members:
            if member[1] == i.name:
                await client.send_message(i, "Gameに参加しました。投票はここでしてください。")
    # メンバーの確認
    if message.content.startswith(":GameMember"):
        for i in SomeGame.members:
            await client.send_message(SomeGame.channel, i)
    # メンバーの削除
    if message.content.startswith(":GameDelMember "):
        member = message.content.split(" ")
        SomeGame.DelMember(member[1])
    # メンバーのリセット
    if message.content.startswith(":GameResetMember"):
        SomeGame.ResetMember()
    # 単語の追加
    if message.content.startswith(":GameWord "):
        word = message.content.split(" ")
        SomeGame.Word(word[2], word[1])
    # wolfの数を変更
    if message.content.startswith(":GameWolfNum "):
        wolf_num = message.content.split(" ")
        SomeGame.WolfNum(int(wolf_num[1]))
    # Game時間を変更
    if message.content.startswith(":GameTime "):
        time_min = message.content.split(" ")
        SomeGame.Time(int(time_min[1]))
    # wolfの数を変更
    if message.content.startswith(":GameStart"):
        # wolfを決める
        SomeGame.Wolf()
        # 全員にDMを送る
        for i in message.server.members:
            for j in SomeGame.members:
                if i.name == j:
                    if j in SomeGame.wolf:
                        await client.send_message(i, SomeGame.minor_word)
                        continue
                    await client.send_message(i, SomeGame.major_word)
        # 開始の合図
        m = "Game 開始です!!"
        await client.send_message(SomeGame.channel, m)
        # Timer開始
        for i in range(SomeGame.time_min):
            m = "後" + str(SomeGame.time_min - i) + "分です。"
            await client.send_message(SomeGame.channel, m)
            await asyncio.sleep(60.0)
        m = "Game 終了です!!\n 投稿してください。DMに(:GamePost やつはし)"
        await client.send_message(SomeGame.channel, m)
    # 集計
    if message.content.startswith(":GamePost "):
        post = message.content.split(" ")
        SomeGame.Post(post[1])
        if len(SomeGame.members) == sum(SomeGame.post.values()):
            m = "集計結果"
            await client.send_message(SomeGame.channel, m)
            for k, v in SomeGame.post.items():
                await client.send_message(SomeGame.channel, str(k) + ":" + str(v) + "\n")
            m = "wolfは、"
            await client.send_message(SomeGame.channel, m)
            for i in SomeGame.wolf:
                await client.send_message(SomeGame.channel, str(i) + "\n")
            m = "wordは、"
            await client.send_message(SomeGame.channel, m)
            await client.send_message(SomeGame.channel, "多数派: " + SomeGame.major_word + "\n")
            await client.send_message(SomeGame.channel, "少数派: " + SomeGame.minor_word + "\n")


client.run("")
