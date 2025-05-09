#import keyboard
#
game_keys = {'w','a','s','d','q','e','b','x'}
#
#def get_user_input():
#    while True:
#        for key in game_keys:
#            if keyboard.is_pressed(key):
#                return key
#from labyrinth_generator import labyrinth 
import random

def rotate_coords(coords, orientation):
    while orientation > 0:
        rotated_by_90_coords = [-coords[1],coords[0]]
        coords = rotated_by_90_coords
        orientation -= 1
    return coords

def translate_coords_into_index_in_room_string(coords,size,orientation):
    rotated_coords = rotate_coords(coords,orientation)
    adjusted_coords = [coord + (size//2) for coord in rotated_coords]
    if any([coord not in range(-1,size+1) for coord in adjusted_coords]):
        raise Exception('OutOfBounds')
    location = adjusted_coords[0] + (size+3)*adjusted_coords[1] + size + 4
    return location

direction = {
    (True,True):0,
    (True,False):1,
    (False,True):3,
    (False,False):2
}

def check_direction(coords):
    x,y = coords
    object_direction = direction[(y>x,y>-x)]
    return object_direction

def empty_room(size):
        empty_row = '|' + ' '*size + '|'
        top_and_bottom = ' ' + '-'*size + ' '
        rows = [top_and_bottom] + [empty_row]*size + [top_and_bottom]
        return '\n'.join(rows)

def insert_into(string,index,symbol):
    new_string = string[:index] + symbol + string[index+1:]
    return new_string

class object():
    def __init__(self,symbol,coords,room):
        self.symbol = symbol
        self.coords = coords
        self.room = room
        room.objects.add(self)
        self.visited_rooms = {room}
    
    def move_object(self,vector):
        if automatically_drop_breadcrumbs:
            self.room.drop_breadcrumb()
        rotated_vector = rotate_coords(vector,(4-self.room.orientation) % 4)
        new_coords = [sum(displacement) for displacement in zip(self.coords,rotated_vector)]
        half_length = self.room.size // 2
        if new_coords[0] in range(-half_length,half_length+1) and new_coords[1] in range(-half_length,half_length+1):
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
                old_orientation = self.room.orientation
                self.visited_rooms.add(room)
                self.room = room
                self.room.objects.add(self)
                old_direction = check_direction(self.coords)
                self.coords = connection_ends[room]
                new_direction = (check_direction(self.coords) + 2)%4
                correction_rotation = old_direction - new_direction
                self.room.orientation = (correction_rotation + old_orientation)%4
                break
    
    def draw_object(self,room_string):
        #print(repr(self.room))
        location = translate_coords_into_index_in_room_string(self.coords,self.room.size,self.room.orientation)
        new_room_string = room_string[:location] + self.symbol + room_string[location+1:]
        return new_room_string
        

class room():
    def __init__(self,size=3):
        self.orientation = 0
        self.size = size
        empty_room_string = empty_room(self.size)
        self.empty_room_strings = {orientation:empty_room_string for orientation in range (0,4)}
        self.objects = set({})
        self.doorways = {}
        rooms.append(self)
        self.room_number = len(rooms)

    def __repr__(self):
        return 'room' + str(self.room_number)

    def __str__(self):
        room_string = self.empty_room_strings[self.orientation]
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
        mark(self,player.coords,'.')
    
    def add_doorway(self,doorway_location,connection):
        self.doorways[doorway_location] = connection

class connection_between_rooms():

    def __init__(self,doorways):
        self.connected_doorways = doorways
        for doorway in doorways:
            doorway.add_doorway(doorways[doorway],self)

class mark():
    
    def __init__(self,room,coords,symbol):
        room.empty_room_strings = {orientation:insert_into(room.empty_room_strings[orientation],translate_coords_into_index_in_room_string(coords,room.size,orientation),symbol) for orientation in range(0,4)}

class togglabe_setting():

    def __init__(self,initial_state):
        self.state = initial_state
    
    def __bool__(self):
        return self.state
    
    def toggle(self):
        self.state = not self.state

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

class labrinyth():

    def __init__(self,room_count = int(input('How many rooms do you want the labyrinth to have?'))):
        self.rooms = []
        self.available_doorway_locations = []
        self.current_number_of_rooms = 0
        self.add_room_to_labrinyth(15)
        while len(self.rooms) < room_count:
            new_room_size = random.randrange(5,11,2)
            new_room = self.add_room_to_labrinyth(new_room_size)
        for i in range(room_count//20):
            self.add_random_connection()

    def add_room_to_labrinyth(self,size):
        new_room = room(size)
        half_length = (size//2)+1
        self.rooms.append(new_room)
        new_room_doorway_locations = [
            (new_room,(0,half_length)),
            (new_room,(0,-half_length)),
            (new_room,(half_length,0)),
            (new_room,(-half_length,0)),
        ]
        if self.current_number_of_rooms > 0:
            entrance_to_new_room = new_room_doorway_locations.pop(random.randint(0,len(new_room_doorway_locations)-1))
            self.connect_room_to_labrinyth(entrance_to_new_room)
        self.available_doorway_locations += new_room_doorway_locations
        self.current_number_of_rooms += 1
    
    def connect_room_to_labrinyth(self,entrance_to_new_room):
        exit_to_rest_of_labyrinth = self.available_doorway_locations.pop(random.randint(0,len(self.available_doorway_locations)-1))
        connection_between_rooms({entrance_to_new_room[0]:entrance_to_new_room[1],exit_to_rest_of_labyrinth[0]:exit_to_rest_of_labyrinth[1]})
        #print(repr(entrance_to_new_room[0]) + ' >>> ' + repr(exit_to_rest_of_labyrinth[0]))
    
    def add_random_connection(self):
        while True:
            random_entrace,random_exit = random.choice(self.available_doorway_locations),random.choice(self.available_doorway_locations)
            if random_entrace[0] != random_exit[0]:
                connection_between_rooms({random_entrace[0]:random_entrace[1],random_exit[0]:random_exit[1]})
                #print(repr(random_entrace[0]) + ' ~ ' + repr(random_exit[0]))
                break


rooms = []
labrinyth1 = labrinyth()
current_room = labrinyth1.rooms[-1]
player = object('X',[0,0],current_room)
automatically_drop_breadcrumbs = togglabe_setting(True)

if __name__ == '__main__':
    while True:
        current_room = player.room
        print(current_room)
        player_action_sequence = input()
        if player_action_sequence == 'exit':
            break
        for action_char in player_action_sequence:
            if action_char in 'wasd':
                player.move_object(vectors[action_char])
            elif action_char in 'qe':
                player_actions[action_char](current_room)
            elif action_char == 'b':
                automatically_drop_breadcrumbs.toggle()
        print("You have explored " + str(len(player.visited_rooms)) + ' rooms.')