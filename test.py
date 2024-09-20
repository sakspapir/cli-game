class Item:
    def __init__(self, name, description, aliases=None):
        self.name = name
        self.description = description
        self.aliases = aliases if aliases else []

    def __str__(self):
        return f"{self.name}: {self.description}"

    def add_alias(self, alias):
        if alias not in self.aliases:
            self.aliases.append(alias)


class Object:
    def __init__(self, name, description, aliases=None):
        self.name = name
        self.description = description
        self.aliases = aliases if aliases else []

    def __str__(self):
        return f"{self.name}: {self.description}"

    def add_alias(self, alias):
        if alias not in self.aliases:
            self.aliases.append(alias)


class Human:
    def __init__(self, name, description, aliases=None):
        self.name = name
        self.description = description
        self.aliases = aliases if aliases else []

    def __str__(self):
        return f"{self.name}: {self.description}"

    def add_alias(self, alias):
        if alias not in self.aliases:
            self.aliases.append(alias)


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.objects = []
        self.humans = []

    def add_item(self, item):
        self.items.append(item)

    def add_object(self, obj):
        self.objects.append(obj)

    def add_human(self, human):
        self.humans.append(human)

    def look(self):
        print(self.description)
        for item in self.items:
            print(item)
        for obj in self.objects:
            print(obj)
        for human in self.humans:
            print(human)

    def look_at(self, name):
        for item in self.items:
            if name == item.name or name in item.aliases:
                print(item)
                return
        for obj in self.objects:
            if name == obj.name or name in obj.aliases:
                print(obj)
                return
        for human in self.humans:
            if name == human.name or name in human.aliases:
                print(human)
                return
        print(f"There is no {name} here.")


def show_instructions():
    print("")
    print("Welcome to the Adventure Game!")
    print("Commands: go [direction], get [item], look, look at [name]")


def show_status():
    print("---------------------------")
    print(f"You are in the {current_room.name}")
    print(f"Inventory: {[item.name for item in inventory]}")
    current_room.look()
    print("---------------------------")


# Define the rooms and items
hall = Room("Hall", "The hall is spacious and well-lit.")
kitchen = Room("Kitchen", "The kitchen is clean and modern.")
dining_room = Room("Dining Room", "The dining room has a large table and chairs.")
garden = Room("Garden", "The garden is full of beautiful flowers.")

key = Item("Key", "A small rusty key.", aliases=["rusty key", "old key", "key"])
monster = Item("Monster", "A scary monster!", aliases=["beast", "creature"])
potion = Item("Potion", "A magical healing potion.", aliases=["elixir", "medicine", "potion"])

stove = Object("Stove", "A modern electric stove.", aliases=["oven", "cooker"])
door = Object("Door", "A wooden door with a brass handle.", aliases=["entrance", "exit", "door"])

alice = Human("Alice", "A friendly neighbor.", aliases=["neighbor", "friend"])

# Add items, objects, and humans to rooms
hall.add_item(key)
hall.add_object(door)
kitchen.add_item(monster)
kitchen.add_object(stove)
dining_room.add_item(potion)
garden.add_human(alice)

# Define room connections
rooms = {
    'Hall': hall,
    'Kitchen': kitchen,
    'Dining Room': dining_room,
    'Garden': garden
}

hall.connections = {'south': kitchen, 'east': dining_room}
kitchen.connections = {'north': hall}
dining_room.connections = {'west': hall, 'south': garden}
garden.connections = {'north': dining_room}

# Start the player in the Hall
current_room = hall
inventory = []

show_instructions()

# Main game loop
while True:
    show_status()
    
    # Get the player's next move
    move = input("> ").lower().split()
    
    # If they type 'go' first
    if move[0] == 'go':
        if move[1] in current_room.connections:
            current_room = current_room.connections[move[1]]
        else:
            print("You can't go that way!")
    
    # If they type 'get' first
    elif move[0] == 'get':
        for item in current_room.items:
            if move[1] == item.name or move[1] in item.aliases:
                inventory.append(item)
                print(f"{item.name} got!")
                current_room.items.remove(item)
                break
        else:
            print(f"Can't get {move[1]}!")
    
    # If they type 'look'
    elif move[0] == 'look':
        if len(move) == 1:
            current_room.look()
        elif len(move) > 1 and move[1] == 'at':
            current_room.look_at(' '.join(move[2:]))
    
    # Check if the player has encountered the monster
    if any(item.name == 'Monster' for item in current_room.items):
        print("A monster has got you... GAME OVER!")
        break
    
    # Check if the player has won
    if current_room == garden and any(item.name == 'Key' for item in inventory) and any(item.name == 'Potion' for item in inventory):
        print("You escaped the house... YOU WIN!")
        break
