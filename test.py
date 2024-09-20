def show_instructions():
    print("Welcome to the Adventure Game!")
    print("Commands: go [direction], get [item]")

def show_status():
    print("---------------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")
    if "item" in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']}")
    print("---------------------------")

# Define the rooms and items
rooms = {
    'Hall': {'south': 'Kitchen', 'east': 'Dining Room', 'item': 'key'},
    'Kitchen': {'north': 'Hall', 'item': 'monster'},
    'Dining Room': {'west': 'Hall', 'south': 'Garden', 'item': 'potion'},
    'Garden': {'north': 'Dining Room'}
}

# Start the player in the Hall
current_room = 'Hall'
inventory = []

show_instructions()

# Main game loop
while True:
    show_status()
    
    # Get the player's next move
    move = input("> ").lower().split()
    
    # If they type 'go' first
    if move[0] == 'go':
        if move[1] in rooms[current_room]:
            current_room = rooms[current_room][move[1]]
        else:
            print("You can't go that way!")
    
    # If they type 'get' first
    if move[0] == 'get':
        if 'item' in rooms[current_room] and move[1] == rooms[current_room]['item']:
            inventory.append(move[1])
            print(f"{move[1]} got!")
            del rooms[current_room]['item']
        else:
            print(f"Can't get {move[1]}!")
    
    # Check if the player has encountered the monster
    if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
        print("A monster has got you... GAME OVER!")
        break
    
    # Check if the player has won
    if current_room == 'Garden' and 'key' in inventory and 'potion' in inventory:
        print("You escaped the house... YOU WIN!")
        break

