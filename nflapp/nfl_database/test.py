from nfl_database.scrapeESPN import getRoster, Player

def test_print(text):
    print (text)

link = "http://www.espn.com/nfl/player/_/id/3052117"

player = Player(link)

print(player.link)
print(player.position)
print(player.physical)