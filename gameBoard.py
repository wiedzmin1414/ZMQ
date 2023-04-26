import random


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def is_neighbor(self, other):
        x_diff = abs(self.x - other.x)
        y_diff = abs(self.y - other.y)
        return x_diff <= 1 and y_diff <= 1

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def return_neighboring_positions(self):
        return [Position(self.x+1, self.y), Position(self.x-1, self.y),
                Position(self.x, self.y+1), Position(self.x, self.y-1),
                Position(self.x+1, self.y+1), Position(self.x+1, self.y-1),
                Position(self.x-1, self.y+1), Position(self.x-1, self.y-1)]

    def move(self, direction):
        direction = direction.lower()
        if direction == 'w':
            self.move_up()
        if direction == 's':
            self.move_down()
        if direction == 'a':
            self.move_left()
        if direction == 'd':
            self.move_right()


class GameBoard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.clients_positions = {}
        self.requests = {}
        self.not_available_positions_to_spawn = []
        self.max_players = (x//3) * (y//3)
        self.number_of_players = 0

    def is_position_in_board(self, position):
        return 0 <= position.x < self.x and 0 <= position.y < self.y

    def get_players_positions(self):
        return self.clients_positions.values()

    def get_client_position(self, client_name):
        return self.clients_positions[client_name]

    def get_available_position_to_spawn_player(self):
        x = random.randint(0, self.x-1)
        y = random.randint(0, self.y-1)
        position = Position(x, y)
        if position not in self.not_available_positions_to_spawn:
            self.not_available_positions_to_spawn.append(position)
            self.not_available_positions_to_spawn += position.return_neighboring_positions()
            return position

    def add_client(self, client_id):
        if self.number_of_players <= self.max_players:
            position = self.get_available_position_to_spawn_player()
            self.clients_positions[client_id] = position
            self.max_players += 1
            return True
        else:
            return False


