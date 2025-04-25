def rotate_coords(coords, orientation):
    while orientation > 0:
        rotated_by_90_coords = [-coords[1],coords[0]]
        coords = rotated_by_90_coords
        orientation -= 1
    return coords

class object():
    def __init__(self,symbol,coords,room):
        self.symbol = symbol
        self.coords = coords
        self.room = room
        room.objects.append(self)
    
    def move_object(self,vector):
        rotated_vector = rotate_coords(vector,(4-self.room.orientation) % 4)
        new_coords = [sum(displacement) for displacement in zip(self.coords,rotated_vector)]
        size = self.room.size_category
        if new_coords[0] in range(-size,size+1) and new_coords[1] in range(-size,size+1):
            self.coords = new_coords
    
    def draw_object(self,room_string):
        rotated_coords = rotate_coords(self.coords,self.room.orientation)
        adjusted_coords = [coord + self.room.size_category for coord in rotated_coords]
        location = adjusted_coords[0] + (self.room.size+3)*adjusted_coords[1] + self.room.size + 4
        new_room_string = room_string[:location] + self.symbol + room_string[location+1:]
        return new_room_string
        

class room():
    def __init__(self,size=1):
        #self.connections = connections
        self.orientation = 0
        self.size = size*2 + 1
        self.size_category = size
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
player = object('X',[0,0],current_room)

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