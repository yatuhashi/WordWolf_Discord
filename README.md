# WordWolf Discord Bot

Rewrite Dsicord Bot Token

```docker-compose.yml
    environment:
      - DISCORDTOKEN=xxxxx
```

Build
```
docker-compose up -d
```

Discord StartGameSetting
```
:GameNew
```

PlayCommand
```
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
```
