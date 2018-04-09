import discord


class OneGame():

    def __init__(self):
        self.members = []
        self.wolf = []
        self.wolf_num = 1
        self.minor_word = ""
        self.major_word = ""
        self.time_min = 3
        self.post = []
        self.channel = None


SomeGame = OneGame()
client = discord.Client()
inst = """\nメンバーを入力の入力の仕方(\":GameMember @membername\")\n
Wordのセットの仕方(\":GameWord 多数派 少数派\")\n
Wolfの人数を変える方法(\":GameWolfNum 2\")\n
Gameの時間を変える方法min(\":GameTime 5\")\n
投票は、DMに(\":GamePost @membername\")\n
"""


@client.event
async def on_message(message):
    # Gameを初期化し、メンバーの募集を始める
    if message.content.startswith(":GasmeReset"):
        SomeGame = OneGame()
        SomeGame.channel = message.channel
        await client.send_message(message.channel, )
    # メンバーの追加
    if message.content.startswith(":GameMember "):
        member = message.content.split(" ")
        SomeGame.members.append(member[1])
    # 単語の追加
    if message.content.startswith(":GameWord "):
        word = message.content.split(" ")
        SomeGame.major_word = word[1]
        SomeGame.minor_word = word[2]
    # wolfの数を変更
    if message.content.startswith(":GameWolfNum "):
        wolf_num = message.content.split(" ")
        SomeGame.wolf_num = int(wolf_num[1])
    # Game時間を変更
    if message.content.startswith(":GameTime "):
        time_min = message.content.split(" ")
        SomeGame.time_min = int(time_min[1])
    # wolfの数を変更
    if message.content.startswith(":GameStart"):
        # wolfを決める
        SomeGame.wolf = random.sample(SomeGame.members, SomeGame.wolf_num)
        # 全員にDMを送る
        for i in SomeGame.members:
            print(i)
        # 開始の合図
        m = "Game 開始です!!"
        await client.send_message(SomeGame.channel, m)
        # Timer開始
        for i in range(self.time_min):
            time.sleep(60)
            m = "後" + str(i) + "分です。"
            await client.send_message(SomeGame.channel, m)
        m = "Game 終了です!!"
        await client.send_message(SomeGame.channel, m)
    # 集計
    if message.content.startswith(":GamePost "):
        post = message.content.split(" ")
        SomeGame.post.append(post[1])
        if(len(SomeGame.members) == len(SomeGame.post)):
            m = "集計結果"
            await client.send_message(SomeGame.channel, m)
            for i in range(SomeGame.post):
                await client.send_message(SomeGame.channel, str(i) + "\n")
            m = "wolfは、"
            await client.send_message(SomeGame.channel, m)
            for i in range(SomeGame.wolf):
                await client.send_message(SomeGame.channel, str(i) + "\n")


client.run("token")
