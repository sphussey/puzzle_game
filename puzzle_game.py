import turtle
import random
import time
##############################################
#               Program Info                 #
##############################################
'''

filename = puzzle_game.py
Title: Ms. Pickles the Pug's Shuffle Puzzle Game
Creater: Shane Hussey
Course: CS5001 Fall 2021 Evening
File path : this file should exist in /slider_puzzle_project_fall2021_assets


Explanation:
Turtle was used as a graphical user interface to create a shuffle puzzle board game.

This program consists of a game class which is created with the following
usage in main:

game = Puzzle('filename.puz')

Creating the instance of the class will create the main game-board including the following
components:
- game background
- game buttons
- show the leaderboard on the screen if it exists
- extract data from puzzle file provided
- register images and create puzzle pieces on the screen


the game will automatically start and be fully functional upon instance creation and requires
no other input from the user

To dos:
- update splash screens for load, quit, win and lose
- 

The play method of the class manages the program response to clicking on the screen and
is the main driver of all functionality contained within the program including:


'''


##############################################
#           File Requirements                #
##############################################
'''
Puzzle Files  must be in Same Directory if no path is defined

this file (puzzle_game.py) needs to be in the folder
/slider_puzzle_project_fall_2021

error.txt file is required in same directory

'''


QUITBUTTON = './Resources/quitbutton.gif'
LOADBUTTON = './Resources/loadbutton.gif'
RESETBUTTON = './Resources/resetbutton.gif'
splash_pic = './Resources/splash_screen.gif'


##############################################
#           Create Instances                 #
##############################################

screen = turtle.Screen()
screen.setup(width=1200, height=800)
player_count = turtle.Turtle()
player_count.hideturtle()
background = turtle.Turtle()
background.hideturtle()
leader_board = turtle.Turtle()
leader_board.hideturtle()
turtle = turtle.Turtle()


##############################################
#                   Classes                  #
##############################################

    
class Puzzle:
    '''
    this class is used to run a sliding puzzle game. this includes
    a startup and slash screen, creating all componants of the screen
    as well as interaction with 
    
    '''
    
    
    def __init__(self, puzz_file: str):
        '''
        Function - creates a class object
        
        Input - puzz file name as a string

        returns -
        self.turn = 0
        self.STARTINGX and self.STARTINGY for board creation
        self.image_positions = list in order of 
        '''
        self.startup_sequence()
        self.gameboard_background()
        self.draw_buttons()
        # save puzz file as make puzz file lowercase
        self.puzz_file = puzz_file.lower()
        # set turn number to 0 
        self.turn = 0
        # self.validate_puzz_file()
        # extract info from puzzle file
        self.extract_puzz_file()
        # register images from puzzle files as shapes
        self.add_images()
        self.STARTINGX = -420 + (self.tile_size / 2)
        self.STARTINGY = 320 - (self.tile_size / 2)
        self.create_tile_positions()

        turtle.setpos(self.STARTINGX, self.STARTINGY)
        #define playerboard
        self.board = []
        for i in range(0, len(self.image_list), self.tile_rows): 
            self.board.append(self.image_list[i:i + self.tile_rows])
        self.draw_squares()
        self.draw_thumbnail()
        self.display_leaderboard()
        self.scramble_board()
        screen.onscreenclick(self.play)
        screen.mainloop()
        

    def startup_sequence(self):
        '''
        startup sequence for game including splashscreen, prompt for
        player name, and number of moves between 5 and 200
        '''
        # Splash screen
        screen.title("CS5001 Sliding Puzzle Game")
        screen.bgpic(splash_pic)
        screen.ontimer(screen.clearscreen,3000)
        # ask for player name
        player = screen.textinput("CS5001 Puzzle Slide", "Your Name:")
        #check for valid player (not null) and eventually log error
        while player == "":
            self.write_to_errorlog("User entered invalid player name")
            player = screen.textinput("Error", "Please enter a player name!")
        self.player_name = player
        # ask for number of moves between 5 and 200
        move_num = screen.textinput("5001 Puzzle Slide - Moves", "Enter the number of moves (chances) you want (5-200):")
        # validate number of moves between 5 and 200
        while move_num == "" or (float(move_num) % 1) != 0 or int(move_num) > 200 or int(move_num) < 5:
            self.write_to_errorlog("User entered invalid number of moves")
            move_num = screen.textinput("5001 Puzzle Slide - Moves", "Enter the number of moves (chances) you want (5-200):")
        self.turn_limit = int(move_num)
        
    def gameboard_background(self):
        '''
        function creates the squares on the screen which is used
        as the background for the game
        '''
        # game board
        background.pen(pensize=10,pencolor="black",speed=10)
        background.penup()
        background.setpos(150,350)
        background.pendown()
        gamespace_pos = [(-550,350),(-550,-150),(150,-150),(150,350)]
        for x in gamespace_pos:
            background.setpos(x)
        # operations dashboard
        background.penup()
        background.setpos(550,-200)
        background.pendown()
        opspace_pos = [(-550,-200),(-550,-350),(550,-350),(550,-200)]
        for x in opspace_pos:
            background.setpos(x)
        # leader board
        background.penup()
        background.pen(pensize=6,pencolor="blue",speed=10)
        background.setpos(550,350)
        background.pendown()
        leaderspace_pos = [(200,350),(200,-150),(550,-150),(550,350)]
        for x in leaderspace_pos:
            background.setpos(x)

        background.penup()
        background.setpos(250,300)
        background.write("Leaders: ", True, align="center",font=('Arial', 18, 'normal'))

    def draw_buttons(self):
        '''
        function creates the squares on the screen which is used
        as the buttons for the game
        '''
        turtle.setpos(450,-275)
        screen.addshape(QUITBUTTON)
        turtle.showturtle()
        turtle.shape(QUITBUTTON)
        turtle.stamp()
        turtle.hideturtle()

        turtle.setpos(350,-275)
        screen.addshape(LOADBUTTON)
        turtle.showturtle()
        turtle.shape(LOADBUTTON)
        turtle.stamp()
        turtle.hideturtle()

        turtle.setpos(250,-275)
        screen.addshape(RESETBUTTON)
        turtle.showturtle()
        turtle.shape(RESETBUTTON)
        turtle.stamp()
        turtle.hideturtle()  

    # extract data from puzzle file into dictionary
        
    def extract_puzz_file(self):
        '''
        Function - this file extracts info from the puzzle file input
        
        inputs-
        self.puzz_file = sting input of file name and path
        
        returns =
        self.puzz_data_dict = dictionary of strings order of files in
        the correct position ex. {'1': 'image_name', etc.}
        self.tile_size = size of tile side in pixels from puzz
        self.puzzle_name = name of puzzle from puzz_file
        self.tile_number = total number of tiles in the puzzle
        self.tile_rows = total number of tile rows/columns in puzzle
        self.thumbnail = string of thumbnail picture with path
        self.image_list = images in order of display on the screen in 1st order list

        
        '''
        # try to open the puzzle file in the current directory and extract needed information
        try:
            with open(self.puzz_file, 'r') as puzzle:
                lines = puzzle.readlines()
                puzz_data_dict = {}
                for line in lines:
                    key = line.split('\n')[0].split()[0].split(':')[0]
                    value = line.split('\n')[0].split()[1]
                    puzz_data_dict[key] = value
                self.puzz_data_dict = puzz_data_dict
            # extract from dictionary of data
            self.tile_size = int(self.puzz_data_dict['size'])
            self.puzzle_name = self.puzz_data_dict['name']
            self.tile_number = int(self.puzz_data_dict['number'])
            self.tile_rows = int(self.tile_number ** 0.5)
            self.thumbnail = self.puzz_data_dict['thumbnail']
            image_list = []
            for x in range(1, (self.tile_number + 1)):
                image_list.append(self.puzz_data_dict.get(str(x)))
            self.image_truth_set = image_list
            self.image_list = image_list
            self.blank_peice = self.image_list[-1]
        # if something goes wrong, write and error to the error.txt and ask user for new puzzfile
        # brings user back to start screen if error
        except:
            print(f"Cound not load information from {self.puzz_file}")
            self.write_to_errorlog(f"extract_puzz_file: Cound not load information from {self.puzz_file}")

        
    def add_images(self):
        '''
        function - adds images from puzzle file to screen shapes
        inputs -
        self.tile_number for looping through for index
        self.image_list = single order list 
        returns - nothing
        just adds image.gif s as screen shapes
        
        '''
        # register images as shapes
        for image in range(self.tile_number):
            screen.addshape(self.image_list[image])
            
    def create_tile_positions(self):
        '''
        function = creates the coordinate positions used to
        build build the gamboard 
        '''
        # set list of coordinates for squares
        self.position_list = []
        for row in range(self.tile_rows):
            for column in range(self.tile_rows):
                self.position_list.append((
                self.STARTINGX + (self.tile_size * column),
                self.STARTINGY - (self.tile_size * row)))

    def draw_squares(self):
        '''
        function = draws squares on the gameboard with the
        registered shapes from the puzzle file
        '''
        turtle.penup()
        for x in range(self.tile_number):
            turtle.setpos(self.position_list[x])
            turtle.shape(self.image_list[x])
            turtle.stamp()
            
        turtle.hideturtle()
        

    def draw_thumbnail(self):
        '''
        function = draws thumbnail of image on top right corner of screen
        
        '''
        turtle.setpos(450,325)
        screen.addshape(self.thumbnail)
        turtle.showturtle()
        turtle.shape(self.thumbnail)
        turtle.stamp()
        turtle.hideturtle()

    def play(self, x, y):
        '''
        function =
        1.) takes onscreen click and saves clicked column and row
        (0 to 3 starting from top left corner)
        2.) self.find_clicked_peice() to define self.clicked_peice
        (ex. self.clicked_peice = '/path/to/file'
        3.)self.find_blank() to define
        - self.blank_peice (ex. '/path/to/file')
        - self.blank_row (ex. 0-3)
        - self.blank_column (ex. 0-3)
        3.) if self.is_adjacent() is true 
        
        inputs =
        x = x coordinate which is clicked (from onscreenclick())
        y = y coordinate which is clicked (from onscreenclick())
        self.tile_size = size of each image in pixels

        outputs =
        self.clicked_row =
        self.clicked_column = 
        
        '''
        print(x,y)
        # manage puzzleboard gameplay
        if (-545 <= x <= 145) and (-145 <= y <= 345):
            self.clicked_column =  int((x + 420) // self.tile_size)
            self.clicked_row = int(-1 * (((y - 320) // self.tile_size) + 1))
            # find clicked peice image (may not need here)
            self.find_clicked_peice()
            # determine blank column 
            self.find_blank()
            
            if self.is_adjacent() == True:
                self.swap_tiles()
                self.turn += 1
                player_count.penup()
                player_count.setpos(-250,-300)
                player_count.clear()
                player_count.write("Player Moves: "+ str(self.turn), True, align="center",font=('Arial', 18, 'normal'))
        # reset screen if click on reset button
        if (209 <= x <= 291) and (-316 <= y <= -235):
            self.reset_board()
            self.draw_squares()
        # load new puzzle if click on load button
        if (308 <= x <= 390) and (-315 <= y <= -235):
            puzz_file = screen.textinput("CS5001 Puzzle Slide", "Enter the name of a valid .puz file:")
            screen.clearscreen()
            self.__init__(puzz_file)
        if (410 <= x <= 490) and (-300 <= y <= -250):
            print("you quit")
            screen.clearscreen()
            screen.bye()
        # determin if you won or lost the game
        self.win_or_lose()


        
    def win_or_lose(self):
        '''
        for each turn this checks the number of turns you have taken
        and if the puzzle order you have is right
        '''
        # did you win?
        #check if you have not exceeded turn limit
        turn_lose_status = self.turn >= self.turn_limit
        
        truth_list = []
        for x in range(1, (self.tile_number + 1)):
            truth_list.append(self.puzz_data_dict.get(str(x)))
        if turn_lose_status == True:
            print("you lose. Game will close now.")
            screen.ontimer(screen.bye,5000)
        if turn_lose_status == False and self.image_list == truth_list:
            self.wirte_to_leaderboard()
            print("you won!!!")
            screen.clearscreen()
            self.__init__(self.puzz_file)
            
    def reset_board(self):
        '''
        function resets board so that tiles match the thumbnail,
        to be used during gameplay and does not change player moves
        inputs = none
        returns = none
        '''
        #create image list again based off original puzzle data
        image_list = []
        for x in range(1, (self.tile_number + 1)):
            image_list.append(self.puzz_data_dict.get(str(x)))
        self.image_list = image_list
        self.board = []
        for i in range(0, len(self.image_list), self.tile_rows): 
            self.board.append(self.image_list[i:i + self.tile_rows])
        self.draw_squares()
        
    
    def track_tile(self, tile):
        """Returns the position of an element in a 2D list."""
        # loop through board to find the row and column numbers for a tile
        for x, y in enumerate(self.board):
            if tile in y:
                return x, y
            else:
                pass
    

    def find_clicked_peice(self):
        '''
        function = finds clicked peice image name
        '''
        # define the clicked peice image name and save it as the new self.clicked_peice
        if (0 <= self.clicked_row < self.tile_rows and
            0 <= self.clicked_column < self.tile_rows):
            self.clicked_peice = self.board[self.clicked_row][self.clicked_column]

        
            

    def is_adjacent(self):
        '''
        function checks if the square you clicked on is next to the
        blank square and returns true or false depending on answer
        '''
        # return true if the clicked peice is next to the blank peice
        if (abs(self.blank_column - self.clicked_column) == 1 and
            abs(self.blank_row - self.clicked_row) == 0):
            return True
        if (abs(self.blank_row - self.clicked_row) == 1 and
            abs(self.blank_column - self.clicked_column) == 0):
            return True
        # return False if the clicked peice isn't next to the blank peice
        return False

    def find_blank(self):
        '''
        find the blank square row and column (index in board)
        '''
        # find the row and column of the blank peice (0,0) being the top left
        # peice and (3,3) being the bottom right in the board
        for row in self.board:
            if self.blank_peice in row:
                self.blank_row = int(self.board.index(row))
                self.blank_column = int(row.index(self.blank_peice))
                

    def swap_tiles(self):
        '''
        function to swap tiles if the clicked tile is next to the blank tile
        '''
        # find the row and column of clicked peice
        self.track_tile(self.clicked_peice)
        # check if the clicked peice is next to the blank peice
        if self.is_adjacent() == True:
            # if so swap the two peices
            temp = self.blank_peice
            self.board[self.blank_row][self.blank_column] = self.clicked_peice
            self.board[self.clicked_row][self.clicked_column] = temp
        # create a new image list off of the swapped peices in the board
        self.image_list = []
        for nest in self.board:
            for element in nest:
                self.image_list.append(element)
                
        screen.tracer(0)
        # redraw squares
        self.draw_squares()


    def scramble_board(self):

        '''
        board_size = range(self.tile_number)
        temp = self.image_list
        self.image_list = []
        for x in board_size:
            self.image_list.append(temp[random.choice(board_size)])
        '''
        # randomly shuffle image list
        random.shuffle(self.image_list)
        # create a new board based off shuffled image list
        self.board = []
        for i in range(0, len(self.image_list), self.tile_rows): 
            self.board.append(self.image_list[i:i + self.tile_rows])
        # redraw squares
        self.draw_squares()

    def wirte_to_leaderboard(self):
        # try to open leaderboard, read its contents, store that info, and write over it with new info included
        try:
            with open("leaderboard.txt","r") as leaderboard:
                self.leaderboard_contents = leaderboard.read()
            with open("leaderboard.txt","w") as leaderboard:
                message = self.player_name + ',' + str(self.turn) + ';' + self.leaderboard_contents
                leaderboard.write(message)
        # if no leaderboard exists, write to error log and create leaderboard.txt file and write to it
        except:
            self.write_to_errorlog("wirte_to_leaderboard: no leaderboard.txt file in current directory")
            with open("leaderboard.txt","w") as leaderboard:
                message = self.player_name + ',' + str(self.turn) + ';'  
                leaderboard.write(message)
        
    def sort_leaderboard(self,leader_list):
        '''
        function - takes the unsorted leaderboard and sorts the list
        and returns the sorted list
        '''
        for game in range(0,len(leader_list)):
            for info in range(0,(len(leader_list)-game-1)):
                if (leader_list[info][1] > leader_list[info+1][1]):
                    temp = leader_list[info]
                    leader_list[info] = leader_list[info + 1]
                    leader_list[info + 1] = temp
        return leader_list

    def read_leaderboard(self):
        '''
        read information from leaderboard.txt
        '''
        # open leaderboard.txt file and 
        with open('leaderboard.txt', 'r') as leaderboard:
            # get string of all contents (should only be one line)
            leaders = leaderboard.read()
            # remove last ';' from string so it doesnt fuck up splitting into a list
            leaders = leaders.removesuffix(';')
            #create empty list to append 
            player_info = []
            for x in leaders.split(";"):
                player_info.append(x.split(","))
            print(player_info)
            for x in range(len(player_info)):
                player_info[x][1] = int(player_info[x][1])
            return player_info
            
    def display_leaderboard(self):
        '''
        function - manage leaderboard display
        uses read_leaderboard and sort_leaderboard and display it on the screen
        '''
        leaderboard_display_list = self.sort_leaderboard(self.read_leaderboard())
        # take top 5 players with lowest turns taken
        self.top5 = leaderboard_display_list[0:5]
        #create message to be printed on screen
        leader_string = ''
        for nest in self.top5:
            player = nest[0]
            score = nest[1]
            rank = self.top5.index(nest) + 1
            leader_string += f'{rank}: Player: {player} Score: {score}\n\n'
        # print leader string message to screen
        leader_board.penup()
        leader_board.setpos(350,0)
        leader_board.write(leader_string, True, align="center",
                           font=('Arial', 18, 'normal'))

    def write_to_errorlog(self, message):
        '''
        function takes in error messages from program and writes them
        out to error.txt
        '''
        # try to open error.txt and append error message with datetime
        try:
            with open("error.txt","a") as errorlog:
                errormessage = str(time.localtime()) + ' | ' + message + '\n'
                errorlog.write(errormessage)
        # if error.txt doesnt exist, open an error.txt, write that there was no file and
        # then recursively call error writer to put in original error message
        except:
            with open("error.txt","w") as errorlog:
                errormessage = str(time.localtime()) + ' | ' + "missing error.txt" + '\n'
                errorlog.write(errormessage)
            self.write_to_errorlog(message)

##############################################
#                   main                     #
##############################################

def main():
    game = Puzzle('mario.puz')
    
 
    
if __name__ == "__main__":
    main()


