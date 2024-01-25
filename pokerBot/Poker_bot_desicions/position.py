#This program will take the amount of players and give the positioning based on three ranks
#1. Early Position
#2. Middle Positon
#3. Late Position

position = {}
def current_position(player_positions):
    #If the table size is 2 there are only two positions, EP and LP
    #The List is going ot be ordered from left to right,
    # left being first to act right being second

    #This method gives a player a position based on where they are in the list
    positions = {}
    if len(player_positions) == 2:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'LP'
    elif len(player_positions) == 3:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'MP'
        positions[player_positions[2]] = 'LP'
    elif len(player_positions) == 4:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'MP'
        positions[player_positions[2]] = 'MP'
        positions[player_positions[3]] = 'LP'
    elif len(player_positions) == 5:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'EP'
        positions[player_positions[2]] = 'MP'
        positions[player_positions[3]] = 'LP'
        positions[player_positions[4]] = 'LP'
    elif len(player_positions) == 6:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'EP'
        positions[player_positions[2]] = 'MP'
        positions[player_positions[3]] = 'MP'
        positions[player_positions[4]] = 'LP'
        positions[player_positions[5]] = 'LP'
    elif len(player_positions) == 7:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'EP'
        positions[player_positions[2]] = 'MP'
        positions[player_positions[3]] = 'MP'
        positions[player_positions[4]] = 'MP'
        positions[player_positions[5]] = 'LP'
        positions[player_positions[6]] = 'LP'
    elif len(player_positions) == 8:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'EP'
        positions[player_positions[2]] = 'EP'
        positions[player_positions[3]] = 'MP'
        positions[player_positions[4]] = 'MP'
        positions[player_positions[5]] = 'MP'
        positions[player_positions[6]] = 'LP'
        positions[player_positions[7]] = 'LP'
    elif len(player_positions) == 9:
        positions[player_positions[0]] = 'EP'
        positions[player_positions[1]] = 'EP'
        positions[player_positions[2]] = 'EP'
        positions[player_positions[3]] = 'MP'
        positions[player_positions[4]] = 'MP'
        positions[player_positions[5]] = 'MP'
        positions[player_positions[6]] = 'LP'
        positions[player_positions[7]] = 'LP'
        positions[player_positions[8]] = 'LP'
    return positions
#FIXME need sasha to parse data
#position  = current_position(player_positions)