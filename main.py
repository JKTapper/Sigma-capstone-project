player_symbol = 'X'

class room():
    def __init__(self,size=1):
        #self.connections = connections
        self.orientation = 0
        self.size = size*2 + 1

    def __str__(self):
        empty_row = '|' + ' '*self.size + '|'
        top_and_bottom = ' ' + '-'*self.size + ' '
        rows = [top_and_bottom] + [empty_row]*self.size + [top_and_bottom]
        empty_room = '\n'.join(rows)
        player_location = player_coords[0] + (self.size+3)*player_coords[1] + self.size + 4
        room_string = empty_room[:player_location] + player_symbol + empty_room[player_location+1:]
        return room_string

player_coords = [1,1]
test_room = room(2)

def move_up(coords):
    if coords[1] == 0:
        return coords
    return [coords[0],coords[1]-1]

def move_down(coords):
    if coords[1] == size_of_current_room - 1:
        return coords
    return [coords[0],coords[1]+1]

def move_left(coords):
    if coords[0] == 0:
        return coords
    return [coords[0]-1,coords[1]]

def move_right(coords):
    if coords[0] == size_of_current_room - 1:
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
    size_of_current_room = test_room.size
    player_action_sequence = input()
    if player_action_sequence == 'exit':
        break
    for action_char in player_action_sequence:
        if action_char in 'wasd':
            player_coords = moves[action_char](player_coords)
        else:
            player_actions[action_char]()