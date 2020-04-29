from score import Game

new_game = Game()
win = False
while(not win):
    line,win = new_game.deals()
    