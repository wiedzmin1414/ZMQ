import random
import collections


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Position(self.x, self.y)

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
        if direction in 'wu':
            self.move_up()
        if direction in 's':
            self.move_down()
        if direction in 'al':
            self.move_left()
        if direction in 'dr':
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

    def log(self, message):
        print(message)

    def is_position_in_board(self, position):
        return 0 <= position.x < self.x and 0 <= position.y < self.y

    def get_players_positions(self):
        return self.clients_positions.values()

    def get_client_position(self, client_name):
        return self.clients_positions[client_name]

    def get_available_position_to_spawn_player(self):
        while True:
            x = random.randint(0, self.x-1)
            y = random.randint(0, self.y-1)
            position = Position(x, y)
            if position not in self.not_available_positions_to_spawn:
                self.not_available_positions_to_spawn.append(position)
                self.not_available_positions_to_spawn += position.return_neighboring_positions()
                return position

    def add_client(self, client_id):
        if self.number_of_players < self.max_players:
            position = self.get_available_position_to_spawn_player()
            self.clients_positions[client_id] = position
            self.number_of_players += 1
        else:
            self.log(f"There is already maximum number of clients connected: {self.number_of_players}")
            return False

    def process_request(self, requests):
        new_clients_positions = self.clients_positions.copy()

        output = {}
        for client, request in requests.items():
            old_position = self.clients_positions[client]
            new_position = old_position.copy()
            new_position.move(request)
            if self.is_position_in_board(new_position):
                new_clients_positions[client] = new_position
            else:
                output[client] = 'nok'
        occupied_positions = new_clients_positions.values()
        counts_position = collections.Counter(occupied_positions).items()
        collisions = [position for position, count in counts_position if count > 1]
        for client, new_candidate_position in new_clients_positions.items():
            if new_candidate_position not in collisions:
                if client not in output:
                    self.clients_positions[client] = new_candidate_position
                    output[client] = 'ok'
            else:
                output[client] = 'nok'
        for client, request in requests.items():
            if request == 'p':
                output[client] = self.get_positions(client)
        return output

    def get_positions(self, client):
        client_position = self.get_client_position(client)
        other_positions = self.clients_positions.copy()
        del other_positions[client]
        return [client_position] + list(other_positions.values())
