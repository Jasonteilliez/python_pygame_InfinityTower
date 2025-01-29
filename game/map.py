from settings import *
from random import randint, shuffle

class Map:
    WALL = '1'
    GROUND = '0'
    VOID = "-1"
    BOUNDARY = '1'
    PLAYER = 'P'

    def __init__(self):
        self.boundary = []
        self.floor = []
        self.entities = []
        self.all_room = []
        self.init_map()

    # create grid
    def add_grid(self):
        for line in range(MAP_HEIGTH):
            nv_line = []
            for col in range(MAP_WIDTH):
                nv_line.append(self.VOID)
            self.boundary.append(list(nv_line))
            self.floor.append(list(nv_line))
            self.entities.append(list(nv_line))

    # create room
    def create_room(self):
        return {
            "x" : randint(ROOM_SIZE_MIN,ROOM_SIZE_MAX),
            "y" : randint(ROOM_SIZE_MIN,ROOM_SIZE_MAX)
        }
    
    def position_room(self, room):
        return {
            "x" : randint(1, MAP_WIDTH -(room['x']+1)),
            "y" : randint(1, MAP_WIDTH -(room['y']+1))
        }
    
    def collision_room(self,room,room_pos):
        for j in range(room_pos['y'], room_pos['y']+room['y']):
            for i in range(room_pos['x'], room_pos['x']+room['x']):
                if self.floor[j][i] != "-1":
                    return False
        return True
    
    def place_room(self,room,room_pos):
        for j in range(room_pos['y'], room_pos['y']+room['y']):
            for i in range(room_pos['x'], room_pos['x']+room['x']):
                if i == room_pos['x'] or i == room_pos['x'] + room['x']-1 or \
                   j == room_pos['y'] or j == room_pos['y'] + room['y']-1 :
                    self.floor[j][i] = self.WALL
                    self.boundary[j][i] = self.BOUNDARY
                else :
                    self.floor[j][i] = self.GROUND
    
    def add_rooms(self):
        nb_rooms = randint(NB_ROOM_MIN,NB_ROOM_MAX)
        for room in range(nb_rooms):
            new_room = self.create_room()
            for _ in range(20):
                room_pos = self.position_room(new_room)
                if self.collision_room(new_room,room_pos):
                    self.place_room(new_room,room_pos)
                    self.all_room.append({'position':room_pos, 'size':new_room})
                    break

    # create path
    def create_liste_path(self):
        room_connexion = []
        path = []
        for i in range(len(self.all_room)):
            for j in range(randint(PATH_PER_ROOM_MIN, PATH_PER_ROOM_MAX)):
                room_connexion.append(i)
        shuffle(room_connexion)
        for (el) in range(len(room_connexion)-1):
            if room_connexion[el]!=room_connexion[el+1]:
                path.append([room_connexion[el],room_connexion[el+1]])
        return path
    
    def random_point_room(self,room):
        return {
            "x": randint(room['position']['x']+1, room['position']['x']+room['size']['x']-2),
            "y": randint(room['position']['y']+1, room['position']['y']+room['size']['y']-2)
        }
    
    def add_path_wall(self,pos):
        for j in range(-1,2):
            for i in range(-1,2):
                if self.floor[pos['y']+j][pos["x"]+i] == self.VOID:
                    self.floor[pos['y']+j][pos["x"]+i] = self.WALL
                    self.boundary[pos['y']+j][pos["x"]+i] = self.BOUNDARY
            
    def create_path_from_room_to_room(self, r1, r2):
        position1 = self.random_point_room(r1)
        position2 = self.random_point_room(r2)
        direction = randint(1,2)

        if direction == 1 :
            for i in range(min(position1['x'],position2['x']),max(position1['x'],position2['x'])+1):
                self.floor[position1['y']][i] = self.GROUND
                self.boundary[position1['y']][i] = self.VOID
                self.add_path_wall({"y":position1['y'],"x":i})
            for i in range(min(position1['y'],position2['y']),max(position1['y'],position2['y'])+1):
                self.floor[i][position2['x']] = self.GROUND
                self.boundary[i][position2['x']] = self.VOID
                self.add_path_wall({"y":i,"x":position2['x']})
        if direction == 2 : 
            for i in range(min(position1['x'],position2['x']),max(position1['x'],position2['x'])+1):
                self.floor[position2['y']][i] = self.GROUND
                self.boundary[position2['y']][i] = self.VOID
                self.add_path_wall({"y":position2['y'],"x":i})
            for i in range(min(position1['y'],position2['y']),max(position1['y'],position2['y'])+1):
                self.floor[i][position1['x']] = self.GROUND
                self.boundary[i][position1['x']] = self.VOID
                self.add_path_wall({"y":i,"x":position1['x']})

    def add_paths(self):
        list_path = self.create_liste_path()
        for path in list_path:
            self.create_path_from_room_to_room(self.all_room[path[0]],self.all_room[path[1]])

    # create entities
    def add_player(self, room):
        x = randint(room['position']['x']+1,room['position']['x']+room['size']['x']-2)
        y = randint(room['position']['y']+1,room['position']['y']+room['size']['y']-2)
        self.entities[y][x] = self.PLAYER

    def add_entities(self):
        self.add_player(self.all_room[0])


    def init_map(self):
        self.add_grid()
        self.add_rooms()
        self.add_paths()
        self.add_entities()
