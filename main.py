def rotate_coords(coords, orientation, size):
    while orientation > 0:
        rotated_by_90_coords = [size-coords[1]-1,coords[0]]
        coords = rotated_by_90_coords
        orientation -= 1
    return coords

def rotate_vector(vector,orientation):
    while orientation > 0:
        rotated_by_90_vector = [-vector[1],vector[0]]
        vector = rotated_by_90_vector
        orientation -= 1
    return vector

class object():
    def __init__(self,symbol,coords,room):
        self.symbol = symbol
        self.coords = coords
        self.room = room
        room.objects.append(self)
    
    def move_object(self,vector):
        print(vector)
        rotated_vector = rotate_vector(vector,(4-self.room.orientation) % 4)
        print(rotated_vector)
        new_coords = [sum(displacement) for displacement in zip(self.coords,rotated_vector)]
        if new_coords[0] in range(self.room.size) and new_coords[1] in range(self.room.size):
            self.coords = new_coords
    
    def draw_object(self,room_string):
        rotated_coords = rotate_coords(self.coords,self.room.orientation,self.room.size)
        location = rotated_coords[0] + (self.room.size+3)*rotated_coords[1] + self.room.size + 4
        new_room_string = room_string[:location] + self.symbol + room_string[location+1:]
        return new_room_string
        

class room():
    def __init__(self,size=1):
        #self.connections = connections
        self.orientation = 0
        self.size = size*2 + 1
        empty_row = '|' + ' '*self.size + '|'
        top_and_bottom = ' ' + '-'*self.size + ' '
        rows = [top_and_bottom] + [empty_row]*self.size + [top_and_bottom]
        self.empty_room_string = '\n'.join(rows)
        self.objects = []

    def __str__(self):
        room_string = self.empty_room_string
        for object in self.objects:
            room_string = object.draw_object(room_string)
        return room_string
    
    def rotate_clockwise(self):
        self.orientation = (self.orientation + 1) % 4
    
    def rotate_anticlockwise(self):
        self.orientation = (self.orientation - 1) % 4
    
    def drop_breadcrumb(self):
        object('b',player.coords,self)


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

vectors = {
    'w':[0,-1],
    'a':[-1,0],
    's':[0,1],
    'd':[1,0]
}

player_actions = {
    'q':room.rotate_anticlockwise,
    'e':room.rotate_clockwise,
    'b':room.drop_breadcrumb
}

current_room = room(2)
player = object('X',[1,1],current_room)

while True:
    print(current_room)
    size_of_current_room = current_room.size
    player_action_sequence = input()
    if player_action_sequence == 'exit':
        break
    for action_char in player_action_sequence:
        if action_char in 'wasd':
            player.move_object(vectors[action_char])
        else:
            player_actions[action_char](current_room)