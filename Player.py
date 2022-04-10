class PlayerName():

    def get_Name(self):
        return self.Name

    def set_Name(self, Name):
        self.Name = Name

    def showPlayerName(self, player):
        print(player.Name)

    def savePlayer(self, player):
        with open('Players.txt', 'a') as f:
            f.writelines("Player Name: " + player.Name + "\n")


player = PlayerName()
print("Insert player Name:")
NameId = str(input())

while NameId == "":
    print("Please insert a player name...")
    NameId = str(input())
player.set_Name(NameId)
player.get_Name()
player.savePlayer(player)
