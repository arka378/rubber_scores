import os

class Team:

    def __init__(self,teamname):

        self.name = teamname
        self.status = '' #declarer/defender
        self.trump = '' #S/H/D/C/NT
        self.level = 0 #1-7

        self.contract = 0 #6 + self.level
        self.tricks = 0 #1-13

        self.vulnerable = 0 #1/0
        self.double = 0 #1/0
        self.redouble = 0 #1/0

        self.below_the_line = 0
        self.above_the_line = 0

        self.total = 0
        self.score = 0
        self.hons = 0
        self.aces = 0

        
class Game:

    def __init__(self):

        team1 = str(input('Enter name of Team 1: '))
        team2 = str(input('Enter name of Team 2: '))
        self.trump = ''
        self.suits = ['NT','S','H','D','C']
        self.factors = [30,30,30,20,20]
        self.suit_factor = dict(zip(self.suits,self.factors))

        self.teams = [Team(team1),Team(team2)]
        self.write_teams()

    def deals(self):
        self.bidding()
        self.scoring()
        for team in self.teams:
            print(team.name,int(team.above_the_line),int(team.below_the_line))
        line,win = self.win_game()
        return line,win


    def bidding(self):

        legal = False
        while(not legal):
            print('-'*50)
            declarer = str(input('Declaring team name: '))
            if declarer not in [team.name for team in self.teams]:
                print('Invalid team name! Enter again.')
            else:
                legal = True
                for team in self.teams:
                    if team.name == declarer:
                        print('ENTER DETAILS FOR DECLARING TEAM '+ team.name + ': \n')
                        team.status = 'declarer'

                        check = False
                        while not check:
                            team.trump = str(input('Enter trump suit (NT/S/H/D/C): '))
                            if team.trump not in self.suits:
                                print('Invalid suit!')
                            else:
                                check = True
                                self.trump = team.trump

                        check = False
                        while not check:
                            team.level = int(input('Enter call level: '))
                            if team.level < 1 or team.level > 7:
                                print('Invalid call level!')
                            else:
                                check = True
                                team.contract = 6 + team.level
                        

                        check = False
                        while not check:
                            team.double = int(input('Double? (1/0): '))
                            if team.double not in [0,1]:
                                print('Please enter 0 if not doubled or 1 if doubled!')
                            else:
                                check = True

                        check = False
                        while not check:
                            if team.double == 1: 
                                team.redouble = int(input('Redouble? (1/0): '))
                            if team.redouble not in [0,1]:
                                print('Please enter 0 if not redoubled or 1 if redoubled!')
                            else:
                                check = True
                                if team.redouble == 1: team.double = 0

                    else:
                        team.status = 'defender'


        

    def scoring(self):

        for team in self.teams:
            if team.status == 'declarer':

                check = False
                while not check:
                    team.tricks = int(input('Enter number of tricks: '))
                    if team.tricks < 0 or team.tricks > 13:
                        print('Invalid number of tricks!')
                    else:
                        check = True

                #Contract points
                if team.tricks >= team.contract:
                    team.below_the_line += team.level*self.suit_factor[team.trump]*2**(team.double)*4**(team.redouble) 
                    if team.trump == 'NT':
                        team.below_the_line += 10*2**(team.double)*4**(team.redouble)

                #Slam bonus 
                if team.tricks == 12 and team.contract == 12:
                    team.above_the_line += 500*(3/2)**team.vulnerable

                if team.tricks == 13 and team.contract == 13:
                    team.above_the_line += 1000*(3/2)**team.vulnerable

                #Overtrick bonus
                if team.tricks > team.contract:
                    overtrick = team.tricks - team.contract
                    #print('Over?: ',overtrick)
                    team.above_the_line += ((100*2**team.vulnerable)*team.double + (200*2**team.vulnerable)*team.redouble + (1-team.double)*(1-team.redouble)*self.suit_factor[team.trump])*overtrick

                #Insult bonus
                team.above_the_line += 100*team.redouble + 50*team.double

                #Undertrick penalty
                if team.tricks < team.contract:
                    for dteam in self.teams:
                        if dteam.status == 'defender':

                            undertrick = team.contract - team.tricks
                            #print('Undertricks: ',undertrick)
                            #print(team.vulnerable,dteam.vulnerable)
                            for i in range(1,undertrick+1):
                                if i==1:
                                    #print('penalty for 1: ',100*2**team.double*4**team.redouble*team.vulnerable + (1-team.vulnerable)*50*2**team.double*4**team.redouble)#(50*2**team.vulnerable)*(2**(team.double+2*team.redouble))
                                    dteam.above_the_line += 100*2**team.double*4**team.redouble*team.vulnerable + (1-team.vulnerable)*50*2**team.double*4**team.redouble#(50*2**team.vulnerable)*(2**(team.double+2*team.redouble)) 
                                elif i>1 and i<4:
                                    #print('penalty for 2 and 3: ',(100+ 50*team.double + 50*team.redouble)*2**team.double*4**team.redouble*team.vulnerable + (1-team.vulnerable)*(50+ 50*team.double + 50*team.redouble)*2**team.double*4**team.redouble)#(100+50*team.vulnerable)*(2**(team.double+2*team.redouble))
                                    dteam.above_the_line += (100+ 50*team.double + 50*team.redouble)*2**team.double*4**team.redouble*team.vulnerable + (1-team.vulnerable)*(50+ 50*team.double + 50*team.redouble)*2**team.double*4**team.redouble#(100+50*team.vulnerable)*(2**(team.double+2*team.redouble))
                                else:
                                    dteam.above_the_line += (100+ 50*team.double + 50*team.redouble)*2**team.double*4**team.redouble*team.vulnerable + (1-team.vulnerable)*(100+ 50*team.double + 50*team.redouble)*2**team.double*4**team.redouble#(150+50*team.vulnerable)*(2**(team.double+2*team.redouble))

                #Honors bonus
                if self.trump != 'NT':
                    team.hons = int(input('Number of trump honours: '))
                    if team.hons == 4:
                        team.above_the_line += 100
                    elif team.hons == 5:
                        team.above_the_line += 150
                else:
                    team.aces = int(input('Number of aces: '))
                    if team.aces == 4:
                        team.above_the_line += 150

        self.write_scores()


    def win_game(self):
        line_status,win_status = False,False
        for team in self.teams:
            if team.status == 'declarer':
                if team.below_the_line >= 100:
                    print(team.name,' won this game! They are now vulnerable. Scores are being reset.')
                    line_status = True
                    team.vulnerable = 1
                    team.total += team.below_the_line + team.above_the_line
                    team.below_the_line = 0
                    team.above_the_line = 0
                    team.score += 1
                    for dteam in self.teams:
                        if dteam.status == 'defender':
                            dteam.total += dteam.below_the_line + dteam.above_the_line
                            dteam.below_the_line = 0
                            dteam.above_the_line = 0
                    self.write_endgame()
                    win_status = self.win_rubber()
                    if not win_status:
                        self.write_newgame()
                else:
                    line_status = False

                return line_status,win_status


    def win_rubber(self):
        decided = False
        teamscore,teamvul = [],[]
        for team in self.teams:
            teamscore.append(team.score)
            teamvul.append(team.vulnerable)
        
        #Rubber bonus
        if teamscore[0] == 2:
            self.teams[0].above_the_line += 500*(7/5)**teamvul[1]
        elif teamscore[1] == 2:
            self.teams[1].above_the_line += 500*(7/5)**teamvul[0]


        if 2 in teamscore:
            teamtotal = []
            names = []
            for team in self.teams:
                team.total += team.above_the_line
                teamtotal.append(team.total)
                names.append(team.name)
                print(names[-1],int(teamtotal[-1]))

            self.write_totals()

            winner = self.teams[teamtotal.index(max(teamtotal))].name
            loser = self.teams[teamtotal.index(min(teamtotal))].name
            
            print('Winner of the Rubber is :',winner)
            decided = True

        return decided

        
    def write_teams(self):

        if os.path.exists('./scorecard'): os.remove('scorecard')
        with open('scorecard','w') as fid:
            print('~'*50,file=fid)
            print(self.teams[0].name,'\t\t',self.teams[1].name,file=fid)
            print('~'*50,file=fid)
            print('\n',file=fid)
            print('-'*50,file=fid)
            print('\n',file=fid)

    def write_scores(self):

        with open('scorecard','r') as fid:
            lines = fid.readlines()

        for i,line in enumerate(lines):
            if '-'*50 in line:
                j = i

        above = j-1
        below = j+1
        lines[above] = str(int(self.teams[0].above_the_line)) + '\t\t' + str(int(self.teams[1].above_the_line)) + '\n'
        lines[below] = str(int(self.teams[0].below_the_line)) + '\t\t' + str(int(self.teams[1].below_the_line)) + '\n'

        with open('scorecard','w') as fid:
            fid.writelines(lines)

    def write_endgame(self):

        with open('scorecard','a') as fid:
            print('x'*50,file=fid)

    def write_newgame(self):

        with open('scorecard','a') as fid:
            print('\n',file=fid)
            print('-'*50,file=fid)
            print('\n',file=fid)

    def write_totals(self):

        with open('scorecard','a') as fid:
            print(str(int(self.teams[0].total)) + '\t\t' + str(int(self.teams[1].total)),file=fid)
            print('x'*50,file=fid)
