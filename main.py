player_symbol = 'X'

class room():
    def __init__(self,connections):
        self.connections = connections
        self.orientation = 0

    def __str__(self):
        empty_room = " --- \n|   |\n|   |\n|   |\n ---"
        player_location = player_coords[0] + 6*player_coords[1] + 7
        room_string = empty_room[:player_location] + player_symbol + empty_room[player_location+1:]
        return room_string

player_coords = [1,1]
test_room = room([])

def move_up(coords):
    if coords[1] == 0:
        return coords
    return [coords[0],coords[1]-1]

def move_down(coords):
    if coords[1] == 2:
        return coords
    return [coords[0],coords[1]+1]

def move_left(coords):
    if coords[0] == 0:
        return coords
    return [coords[0]-1,coords[1]]

def move_right(coords):
    if coords[0] == 2:
        return coords
    return [coords[0]+1,coords[1]]

moves = {
    'w':move_up,
    'a':move_left,
    's':move_down,
    'd':move_right
}

player_actions = {}

while True:
    print(test_room)
    player_action_sequence = input()
    if player_action_sequence == 'exit':
        break
    for action_char in player_action_sequence:
        if action_char in 'wasd':
            player_coords = moves[action_char](player_coords)
        else:
            player_actions[action_char]()