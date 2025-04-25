def rotate_coords(coords, orientation):
    while orientation > 0:
        rotated_by_90_coords = [-coords[1],coords[0]]
        coords = rotated_by_90_coords
        orientation -= 1
    return coords

def translate_coords_into_index_in_room_string(coords,size,orientation):
    rotated_coords = rotate_coords(coords,orientation)
    adjusted_coords = [coord + (size//2) for coord in rotated_coords]
    location = adjusted_coords[0] + (size+3)*adjusted_coords[1] + size + 4
    return location

class object():
    def __init__(self,symbol,coords,room):
        self.symbol = symbol
        self.coords = coords
        self.room = room
        room.objects.add(self)
    
    def move_object(self,vector):
        rotated_vector = rotate_coords(vector,(4-self.room.orientation) % 4)
        new_coords = [sum(displacement) for displacement in zip(self.coords,rotated_vector)]
        size = self.room.size_category
        if new_coords[0] in range(-size,size+1) and new_coords[1] in range(-size,size+1):
            self.coords = new_coords
        else:
            self.check_if_object_is_in_doorway(new_coords)
    
    def check_if_object_is_in_doorway(self,new_coords):
        doorways = self.room.doorways
        for doorway_coords in doorways:
            if list(doorway_coords) == new_coords:
                self.move_object_through_connection(doorways[doorway_coords])
    
    def move_object_through_connection(self,connection):
        connection_ends = connection.connected_doorways
        self.room.objects.remove(self)
        for room in connection_ends:
            if room != self.room:
                self.room = room
                self.room.objects.add(self)
                self.coords = connection_ends[room]
                break
    
    def draw_object(self,room_string):
        location = translate_coords_into_index_in_room_string(self.coords,self.room.size,self.room.orientation)
        new_room_string = room_string[:location] + self.symbol + room_string[location+1:]
        return new_room_string
        

class room():
    def __init__(self,size=1):
        self.orientation = 0
        self.size = size*2 + 1
        self.size_category = size
        empty_row = '|' + ' '*self.size + '|'
        top_and_bottom = ' ' + '-'*self.size + ' '
        rows = [top_and_bottom] + [empty_row]*self.size + [top_and_bottom]
        self.empty_room_string = '\n'.join(rows)
        self.objects = set({})
        self.doorways = {}
        rooms.append(self)
        self.room_number = len(rooms)

    def __repr__(self):
        return 'room' + str(self.room_number)

    def __str__(self):
        room_string = self.empty_room_string
        for doorway in self.doorways:
            doorway_location = translate_coords_into_index_in_room_string(list(doorway),self.size,self.orientation)
            room_string = room_string[:doorway_location] + ' ' + room_string[doorway_location+1:]
        for object in self.objects:
            room_string = object.draw_object(room_string)
        return room_string
    
    def rotate_clockwise(self):
        self.orientation = (self.orientation + 1) % 4
    
    def rotate_anticlockwise(self):
        self.orientation = (self.orientation - 1) % 4
    
    def drop_breadcrumb(self):
        object('b',player.coords,self)
    
    def add_doorway(self,doorway_location,connection):
        self.doorways[doorway_location] = connection

class connection_between_rooms():

    def __init__(self,doorways):
        self.connected_doorways = doorways
        for doorway in doorways:
            doorway.add_doorway(doorways[doorway],self)

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

rooms = []
current_room = room(2)
test_connected_room = room(3)
connection_between_rooms({current_room:(3,0),test_connected_room:(-4,0)})
player = object('X',[0,0],current_room)

while True:
    current_room = player.room
    print(current_room)
    player_action_sequence = input()
    if player_action_sequence == 'exit':
        break
    for action_char in player_action_sequence:
        if action_char in 'wasd':
            player.move_object(vectors[action_char])
        else:
            player_actions[action_char](current_room)