import random
import asyncio
import os
from discord.ext.commands import Bot


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
        self.members.remove(mem)
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

    def ResetPost(self):
        self.post = {}
        for i in self.members:
            self.post[i] = 0

    def Channel(self, ch):
        self.channel = ch

    def Server(self, sv):
        self.server = sv


SomeGame = OneGame()
client = Bot(command_prefix=':')
inst = """\n
**********************************************
Gameの初期化        :GameNew
Memberの入力        :GameAddMember やつはし
Memberの削除        :GameDelMember やつはし
Memberの初期化      :GameResetMember
Memberの確認        :GameMember
Wordの入力          :GameWord 多数派 少数派
Wolfの人数変更      :GameWolfNum 2
Gameの時間変更(min) :GameTime 5
投票は、DMに        :GamePost やつはし
Game開始            :GameStart
GameHelp            :GameHelp
**********************************************
"""


@client.command(pass_context=True)
async def GameHelp(context):
    await client.send_message(context.message.channel, inst)


@client.command(pass_context=True)
async def GameNew(context):
    # Gameを初期化し、メンバーの募集を始める
    global SomeGame
    SomeGame = OneGame()
    SomeGame.Channel(context.message.channel)
    m1 = "Gameデータをリセットしました\n" + inst + "\n" + "#######現在サーバーにいるメンバーは以下の人です#######"
    member_list = ""
    for i in context.message.server.members:
        if str(i.status) == "online":
            member_list = member_list + "・" + str(i.name)
    m2 = "############################################\n上記の人をゲームに参加させてください  :GameAddMember やつはし"
    await client.send_message(SomeGame.channel, m1 + "\n" + member_list + "\n" + m2)


@client.command(pass_context=True)
async def GameAddMember(context, member):
    # メンバーの追加
    global SomeGame
    for i in context.message.server.members:
        if member == i.name:
            SomeGame.AddMember(str(member))
            await client.send_message(i, "WordWolfGameに参加しました。投票はここでしてください  :GamePost やつはし")


@client.command()
async def GameMember():
    # メンバーの確認
    global SomeGame
    for i in SomeGame.members:
        await client.send_message(SomeGame.channel, i)


@client.command()
async def GameDelMember(member):
    # メンバーの削除
    global SomeGame
    SomeGame.DelMember(str(member))


@client.command()
async def GameResetMember():
    # メンバーのリセット
    global SomeGame
    SomeGame.ResetMember()


@client.command()
async def GameWord(word1, word2):
    # 単語の追加
    global SomeGame
    SomeGame.Word(word2, word1)


@client.command()
async def GameWolfNum(num):
    # wolfの数を変更
    global SomeGame
    SomeGame.WolfNum(int(num))


@client.command()
async def GameTime(m):
    # Game時間を変更
    global SomeGame
    SomeGame.Time(int(m))


@client.command(pass_context=True)
async def GameStart(context):
    global SomeGame
    # wolfを決める
    SomeGame.Wolf()
    SomeGame.ResetPost()
    # 全員にDMを送る
    for i in context.message.server.members:
        for j in SomeGame.members:
            if i.name == j:
                if j in SomeGame.wolf:
                    await client.send_message(i, SomeGame.minor_word)
                    continue
                await client.send_message(i, SomeGame.major_word)
    # 開始の合図
    m = "WordWolfGame 開始です!!"
    await client.send_message(SomeGame.channel, m)
    # Timer開始
    for i in range(SomeGame.time_min - 1):
        m = "後" + str(SomeGame.time_min - i) + "分です"
        await client.send_message(SomeGame.channel, m)
        await asyncio.sleep(60.0)
    await asyncio.sleep(30.0)
    m = "残り30秒です\n"
    await client.send_message(SomeGame.channel, m)
    await asyncio.sleep(30.0)
    m = "Game 終了です!!\n 投稿してください。DMに  :GamePost やつはし"
    await client.send_message(SomeGame.channel, m)


@client.command()
async def GamePost(post):
    # 集計
    global SomeGame
    SomeGame.Post(str(post))
    if len(SomeGame.members) == sum(SomeGame.post.values()):
        m = "集計結果\n"
        for k, v in SomeGame.post.items():
            m = m + str(k) + ":" + str(v) + "\n"
        m = m + "\nwolfは、"
        for i in SomeGame.wolf:
            m = m + str(i) + ", "
        m = m[:-2] + "\nwordは、多数派: " + SomeGame.major_word + " 少数派: " + SomeGame.minor_word
        await client.send_message(SomeGame.channel, m)


print("起動")
client.run(os.environ["DISCORDTOKEN"])
