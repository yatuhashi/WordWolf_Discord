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
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
reset game                 :GameNew
input member               :GameAddMember MemberName
delete member              :GameDelMember MemberName
reset member               :GameResetMember
member list                :GameMember
input word                 :GameWord MajorWord MinorWord
change the number of wolf  :GameWolfNum 2
change the game time(min)  :GameTime 5
post in DM                 :GamePost MemberName
game start                 :GameStart
Help                       :GameHelp
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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
    m1 = "Reset the game data.\n" + inst + "\n" + "##########current members in this server.#############"
    member_list = ""
    for i in context.message.server.members:
        if str(i.status) == "online":
            member_list = member_list + "・" + str(i.name)
    m2 = "############################################\njoin the game  :GameAddMember MemberName"
    await client.send_message(SomeGame.channel, m1 + "\n" + member_list + "\n" + m2)


@client.command(pass_context=True)
async def GameAddMember(context, member):
    # メンバーの追加
    global SomeGame
    for i in context.message.server.members:
        if member == i.name:
            SomeGame.AddMember(str(member))
            await client.send_message(i, "You joined in the WordWolfGame. You will post in this channel when game over  :GamePost MemberName")


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
    try:
        SomeGame.DelMember(str(member))
    except:
        await client.send_message(SomeGame.channel, "Error")


@client.command()
async def GameResetMember():
    # メンバーのリセット
    global SomeGame
    SomeGame.ResetMember()


@client.command()
async def GameWord(word1, word2):
    # 単語の追加
    global SomeGame
    try:
        SomeGame.Word(word2, word1)
    except:
        await client.send_message(SomeGame.channel, "Error")


@client.command()
async def GameWolfNum(num):
    # wolfの数を変更
    global SomeGame
    try:
        SomeGame.WolfNum(int(num))
    except:
        await client.send_message(SomeGame.channel, "Error")


@client.command()
async def GameTime(m):
    # Game時間を変更
    global SomeGame
    try:
        SomeGame.Time(int(m))
    except:
        await client.send_message(SomeGame.channel, "Error")


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
    m = "WordWolfGame Start!!"
    await client.send_message(SomeGame.channel, m)
    # Timer開始
    for i in range(SomeGame.time_min - 1):
        m = "You have " + str(SomeGame.time_min - i) + "minutes remaining"
        await client.send_message(SomeGame.channel, m)
        await asyncio.sleep(60.0)
    await asyncio.sleep(30.0)
    m = "You have only 30 seconds.\n"
    await client.send_message(SomeGame.channel, m)
    await asyncio.sleep(30.0)
    m = "The game is over!!\nPlease vote in DM. :GamePost MemberName"
    await client.send_message(SomeGame.channel, m)


@client.command(pass_context=True)
async def GamePost(context, post):
    # 集計
    global SomeGame
    if post in SomeGame.members:
        SomeGame.Post(str(post))
    else:
        await client.send_message(context.message.channel, "Error")
    if len(SomeGame.members) == sum(SomeGame.post.values()):
        m = "Result\n"
        for k, v in SomeGame.post.items():
            m = m + str(k) + ":" + str(v) + "\n"
        m = m + "\nWolf is "
        for i in SomeGame.wolf:
            m = m + str(i) + ", "
        m = m[:-2] + "\nWord is major: " + SomeGame.major_word + ",  minor: " + SomeGame.minor_word
        await client.send_message(SomeGame.channel, m)


client.run(os.environ["DISCORDTOKEN"])
