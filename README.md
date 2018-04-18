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
```
