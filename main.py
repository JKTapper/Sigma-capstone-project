player_coords = [1,1]
player_symbol = 'X'

class room():
    def __init__(self,connections):
        self.connections = connections
        self.orientation = 0

    def __str__(self):
        empty_room = """
         --- 
        |   |
        |   |
        |   |
         ---
        """
        player_location = player_coords[0] + 5*player_coords[1] + 6
        room_string = empty_room[:player_location] + player_symbol + empty_room[player_location:]
        return room_string
    
test_room = room([])
print(test_room)