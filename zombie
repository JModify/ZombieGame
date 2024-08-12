"""
A text-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

from typing import Tuple, Optional, Dict, List
from collections import defaultdict

from zombie_support import *


# Implement your classes here.
class Entity:
    """
    The Entity class represents any object that appears on the grid.
    """

    def step(self, position: Position, game: "Game") -> None:
        """
        The step function is called for every entity on the game grid.
        If an entity needs to perform an action when the player moves,
        this function will handle that.

        Parameters:
            position (Position): The current position of the entity.
            game (Game): The instance of the game.
        """
        pass

    def display(self) -> str:
        """
        The display function for any entity returns the
        entity's token. This function must be present in every
        entity class.

        Returns:
            (str): The token of the entity
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Returns the string representation of any given entity.

        Examples:
            >>> repr(Player())
            'Player()'
        """
        return self.__class__.__name__ + '()'

class Grid:
    """
    The grid class handles all mapping in the game. Aditionally,
    all added entities are stored inside the class.

    The size of the game grid must be provided during
    initialization.

    Examples:
        >>> grid = Grid(5)
    """
    
    def __init__(self, size: int):
        """
        The grid class is constructed using the size of the
        game grid. The mapping dictionary is also declared
        in this constructor.

        Parameters:
            size (int): The size of the game grid.
        """
        self._size = size
        self._mapping = {}

    def get_size(self) -> int:
        """
        Used to get the size of the grid object. Used
        in outside objects to avoid reference of private
        variable.

        Returns:
            (int): Size of game grid.
        """
        return self._size

    def in_bounds(self, position: Position) -> bool:
        """
        Checks if the specified position is inside the
        game grid.

        Parameters:
            position (Position): The position to check.

        Returns:
            (bool): True if position is inside grid, false
                    if it is not.
        """
        x = position.get_x()
        y = position.get_y()
        
        if (x >= 0) and (x < self._size):
            if (y >= 0) and (y < self._size):
                return True
        return False

    
    def add_entity(self, position: Position, entity: Entity) -> None:
        """
        Adds the specified entity to the specified position.

        Parameters:
            position (Position): The position of which to add the entity.
            entity (Entity): The entity to add to the grid.
        """
        if self.in_bounds(position):
            self._mapping.update({position:entity})
        else:
            return None

     
    def remove_entity(self, position: Position) -> None:
        """
        Removes any entity at the specified position.

        Parameters:
            position (Position): The position of which to remove an entity.
        """
        try:
            self._mapping.pop(position)
        except KeyError:
            return None
    
    def get_entity(self, position: Position) -> Optional[Entity]:
        """
        Get the entity from mapping at the specified position.

        Parameters:
            position (Position): The position to retrieve entity.

        Returns:
            Optional[Entity]: The entity at the given position. Returns
                              none if there is no entity at this position.
        """
        if self.in_bounds(position):
            try:
                entity = self._mapping[position]
                return entity
            except KeyError:
                return None
        else:
            return None

    def move_entity(self, start: Position, end: Position) -> None:
        """
        Moves any entity at the start position to the end position.
        If there is no entity at this position, nothing will be moved.

        Parameters:
            start (Position): The position of the entity to move
            end (Position): The position which the entity must be moved too.
        """
        entity = self.get_entity(start)
        
        if entity is not None:
            if self.in_bounds(end) and self.in_bounds(start):
                self._mapping.pop(start)
                self._mapping.update({end:entity})

    def get_entities(self) -> List[Entity]:
        """
        Creates a list of all entities on the board.

        Returns:
            List[Entity]: A list of all entities in the grid.
        """
        mapping = self.get_mapping()

        entities = []
        for value in mapping.values():
            entities.append(value)
            
        return entities

    def find_player(self) -> Optional[Position]:
        """
        Retrieves the position of the player on the board.

        Returns:
            Optional[Position]: The position of the player. Returns
                                none if the player cannot be found.
        """
        position = None
        for key, value in self._mapping.items():
            if value.display() == PLAYER:
                position = key
        return position
    
    def serialize(self) -> Dict[Tuple[int, int], str]:
        """
        Converts the board mapping to a condensed format.

        Returns:
            Dict[Tuple[int, int], str]: A dictionary of the mapping with
                                        keys as tuples and the values as
                                        the display string of the entity.
        """
        serialized = {}

        for key, value in self.get_mapping().items():
            x = key.get_x()
            y = key.get_y()
            serialized.update({(x, y):value.display()})

        return serialized

    def get_mapping(self) -> Dict[Position, Entity]:
        """
        Retrieves the mapping of the grid. Used in outside classes
        to avoid reference of private variables.
        """
        return self._mapping

class Player(Entity):
    """
    The player class is a subclass of entity and represents the
    player in the game. There will only ever be one player in the
    game at any given time.

    The objective of this entity is to reach the hospital entity.
    """

    def display(self) -> str:
        """
        Retrieves the entity token for the player

        Returns:
            (str): The token of player as a string "P".
        """
        return PLAYER

class Hospital(Entity):
    """
    The hospital class is a subclass of entity and represents the
    hospital in the game. There will only ever be one hospital in the
    game at any given time.

    The player must reach this entity to win the game.
    """

    def display(self) -> str:
        """
        Retrieves the entity token for the hospital.

        Returns:
            (str): The token of hospital as a string "H".
        """
        return HOSPITAL

class VulnerablePlayer(Player):
    """
    The vulnerable player entity handles infection in the game.
    Once a vulnerable player has been infected, the game is lost.
    """

    def __init__(self):
        """
        The vulnerable player constructor stores the infection
        state of the player.
        """
        self._infected = False

    def infect(self) -> None:
        """
        Sets the infection state of the player to true.
        Once this method has been called, the game is lost.
        """
        self._infected = True

    def is_infected(self) -> bool:
        """
        Checks whether the player is infected.

        Returns:
            (bool): True if the player if infected, false if
                    they have not been infected.
        """
        return self._infected

class Zombie(Entity):
    """
    The zombie entity randomly moves through the board.
    If a vulnerable player and zombie move to the same block
    then the zombie infects the player.

    Zombies cannot move onto any entities, though if a player
    and zombie move to the same block, then infection occurs.
    """

    def step(self, position: Position, game: "Game") -> None:
        """
        The step function is called after a player makes any move.

        Parameters:
            position (Position): The current position of the zombie
            game (Game): The instance of the game
        """
        directions = random_directions()
        grid = game.get_grid()

        # Loops through all possible directions in randomized order.
        for direction in directions:
            x = direction[0]
            y = direction[1]
            offset = Position(x, y)
            new_position = position.add(offset)

            
            if grid.in_bounds(new_position):
                player_position = grid.find_player()

                # Check if the new position will
                # move the zombie onto an entity
                if grid.get_entity(new_position) is not None:

                    # Check if the new position contains the player and
                    # infect. Else, do nothing and continue to next
                    # possible direction.
                    if new_position == player_position:
                        game.get_player().infect()
                        break
                else:
                    grid.move_entity(position, new_position)
                    break
                    

    def display(self) -> str:
        """
        Retrieve the entity tokens of the zombie.

        Returns:
            (str): The token of zombie as a string "Z"
        """
        return ZOMBIE

class TrackingZombie(Zombie):
    """
    Tracking zombie entity that follows the player through
    the grid. If contact is made, the player's infection
    state becomes true and the game is lost.
    """
    
    def step(self, position: Position, game: "Game") -> None:
        """
        Step event called when a player makes a move.

        Parameters:
            position (Position): The current position of the
                                 tracking zombie.
        """
        directions = random_directions()
        grid = game.get_grid()

        # Retrieves all distances for the possible next positions
        distances = []
        for direction in directions:
            x = direction[0]
            y = direction[1]
            offset = Position(x, y)
            
            new_position = position.add(offset)
            player_position = grid.find_player()
            
            distance = new_position.distance(player_position)
            distances.append((new_position, distance))

        # Sort into ordered list of tuples -> [(Position, distance)]
        sorted_list = sorted(distances, key=lambda tup: tup[1])

    def display(self) -> str:
        """
        Retrievesthe character used to represent tracking zombie.

        Returns:
            (str): Entity token of the tracking zombie "T".
        """
        return TRACKING_ZOMBIE

class Pickup(Entity):
    """
    Abstract class representing any entities which can be
    picked up. Entities which are picked up are added to the
    player's inventory.
    """
    
    def __init__(self):
        """
        Constructur initializing the lifetime of a pickup
        entity.
        """
        self._lifetime = self.get_durability()

    def get_durability(self) -> int:
        """
        Abstract method representing the maximum 
        durability of an item. Raises a NotImplementedError
        if the method is not implemented.

        Returns:
            (int): The maximum steps a player can
                   take before the item is destroyed.
        """
        raise NotImplementedError

    def get_lifetime(self) -> int:
        """
        The lifetime value of a given entity. Decreases
        every time the player makes a move.

        Returns:
            (int): Number of steps left a player can take before
                   item is removed from player inventory.
        """
        return self._lifetime

    def hold(self) -> None:
        """
        Decreases the durability of the item after every
        step. Called on step event.
        """
        self._lifetime -= 1

    def __repr__(self) -> str:
        """
        Represents a pickup entity and it's lifetime.

        Returns:
            (str): The name of a pickup entity with it's
                   life time in brackets.

        Examples:
            >>> repr(Garlic())
                'Garlic(10)'
        """
        return self.__class__.__name__ + \
               "(" + str(self.get_lifetime()) + ")"

class Garlic(Pickup):
    """
    The garlic item allows the player to avoid infection from
    zombies when the item is held.
    """
    
    def get_durability(self) -> int:
        """
        Retrieves the maximum durability of the garlic item.

        Returns:
            (int): A constant value of 10.
            
        """
        return LIFETIMES[GARLIC]

    def display(self) -> str:
        """
        Retrieves the entity token for garlic.

        Returns:
           (str): The entity token for garlic "G".
        """
        return GARLIC

class Crossbow(Pickup):
    """
    When held, the crossbow item allows the player to remove
    a single zombie entity from the grid in the given direction.
    """
    def get_durability(self) -> int:
        """
        Retrieves the maximum durability of the crossbow item.

        Returns:
            (int): A constant value of 5.
        """
        return LIFETIMES[CROSSBOW]

    def display(self) -> str:
        """
        Retrieves the entity token for the crossbow.

        Returns:
            (str): The entity token as a string for the
                   crossbow "C".
        """
        return CROSSBOW

class Inventory:
    """
    The inventory class is where all pickup entities are stored
    in the game. It is also run on the step event to update
    lifetimes.
    """

    def __init__(self):
        """
        The inventory class constructor initializes the inventory
        list where pickup entities are stored.
        """                
        self._inventory = []

    def step(self) -> None:
        """
        The step method is to decrease the lifetime of a pickup
        entity on the step event. It is also responsible for
        removing the item from the user's inventory once
        it is depleted.
        """
        for item in self._inventory:
            item.hold()
            if item.get_lifetime() == 0:
                self.remove_item(item)

    def get_items(self) -> List[Pickup]:
        """
        Retrieves a list of all the items a player
        has in their inventory.

        Returns:
            List[Pickup]: List of pickup items being
                          held.
        """
        return self._inventory

    def add_item(self, item: Pickup) -> None:
        """
        Add a pickup entity to the player inventory.

        Parameters:
            item (Pickup): The instance of an item
                           to add to the inventory.
        """
        self.get_items().append(item)

    def remove_item(self, item: Pickup) -> None:
        """
        Remove a pickup entity from the players inventory.
        Called when an item is depleted.

        Parameters:
            item (Pickup): The instance of an item to remove
                           from the inventory list.
        """
        self.get_items().remove(item)

    def contains(self, pickup_id: str) -> bool:
        """
        Checks if the player has a specific item type.

        Parameters:
            pickup_id (str): The entity token of the pickup item.

        Returns:
            (bool): True if the player has the item, false if
                    they do not.
        """
        for item in self._inventory:
            if item.display() == pickup_id:
                return True
        return False

class HoldingPlayer(VulnerablePlayer):
    """
    The HoldingPlayer class represents a player which has an
    inventory and so can hold pickup items.
    """
    
    def __init__(self):
        """
        The HoldingPlayer class constructor creates a new
        instance of Inventory and also stores a new infection
        state for a given player.
        """
        self._infected = False
        self._inventory = Inventory()
    
    def get_inventory(self) -> Inventory:
        """
        Retrieves the players inventory instance.

        Returns:
            (Inventory): The saved instance of inventory.
        """
        return self._inventory

    def infect(self) -> None:
        """
        Overrides the superclass method for player infection.
        This function prevents zombie infection if the player
        is holding garlic in their infentory.
        """
        if not self.get_inventory().contains(GARLIC):
            self._infected = True

    def step(self, position: Position, game: "Game") -> None:
        """
        Calls the step method of the inventory class.

        Parameters:
            position (Position): The current position of this entity
            game (Game): The game being played in it's current state.
        """
        self._inventory.step()
            

class MapLoader():
    """
    Creates a new grid instance based on the specified map file.
    Also creates the main grid instance for the game that stores
    map file entities.
    """

    def load(self, filename: str) -> Grid:
        """
        Creates a grid instance using the map file path. Also maps
        all entities onto the grid using map loader.

        Parameters:
            filename (str): The file path as a string.

        Returns:
            (Grid): A new instance of grid with mapped entities.
        """
        loaded_map = load_map(filename)
        entity_locs = loaded_map[0]
        
        map_loader = AdvancedMapLoader()
        
        size = loaded_map[1]
        grid = Grid(size)

        for key, value in entity_locs.items():
            
            x = key[0]
            y = key[1]
            entity = map_loader.create_entity(value)
            grid.add_entity(Position(x, y), entity)
        
        return grid

    def create_entity(self, token: str) -> Entity:
        """
        Abstract method used in subclasses to create new instance
        of entities based on the provided token.

        Parameters:
            token (str): The token of the entity to create.
            
        Returns:
            (Entity): The entity instance using token.
        """
        raise NotImplementedError

class BasicMapLoader(MapLoader):
    """
    The basic map loader is used to create Player and Hospital
    entities.
    """

    def create_entity(self, token: str) -> Entity:
        """
        Function used to create a new instance of entities based on
        the provided token. Raises a value error if the token is invalid.

        Parameters:
            token (str): The token of the entity to create.
            
        Returns:
            (Entity): The entity instance from token.
        """
                
        if token == PLAYER:
            return Player()
        elif token == HOSPITAL:
            return Hospital()
        else:
            raise ValueError("ValueError - Entity not found")

class IntermediateMapLoader(BasicMapLoader):
    """
    The intermediate map loader is used to create Player, Hospital
    and Zombie instances.
    """
    
    def create_entity(self, token: str) -> Entity:
        """
        Function used to create a new instance of entities based on the
        provided token. Raises a value error if the token is invalid.

        Parameters:
            token (str): The token of the entity to create.
            
        Returns:
            (Entity): The entity instance from token.
        """
                
        if token == PLAYER:
            return VulnerablePlayer()
        elif token == HOSPITAL:
            return Hospital()
        elif token == ZOMBIE:
            return Zombie()
        else:
            raise ValueError("ValueError - Entity not found")

class AdvancedMapLoader(IntermediateMapLoader):
    """
    The intermediate map loader is used to create Player, Hospital,
    Zombie, Tracking Zombie, Garlic and Crossbow instances.
    """
    
    def create_entity(self, token: str) -> Entity:
        """
        Function used to create a new instanceof entities based on the
        provided token. Raises a value error if the token is invalid.

        Parameters:
            token (str): The token of the entity to create.
            
        Returns:
            (Entity): The entity instance from token.
        """
                
        if token == PLAYER:
            return HoldingPlayer()
        elif token == HOSPITAL:
            return Hospital()
        elif token == ZOMBIE:
            return Zombie()
        elif token == TRACKING_ZOMBIE:
            return TrackingZombie()
        elif token == CROSSBOW:
            return Crossbow()
        elif token == GARLIC:
            return Garlic()
        else:
            raise ValueError("ValueError - Entity not found")
    
class Game:
    """
    The game class handles all logic needed for actions the
    player performs in the grid.

    The class has direct access to an instance of grid and
    handles logic after a step has been taken by the player.
    """

    def __init__(self, grid: Grid):
        """
        The game class is constructed using the grid. The
        constructor also stores steps taken by the player
        in the game.

        Parameters:
            grid (Grid): An instance of the game grid.
        """
        self._grid = grid
        self._steps = 0

    def get_grid(self) -> Grid:
        """
        Retrieves an instance of the game grid.

        Returns:
            (Grid): The grid of the game.
        """
        return self._grid

    def get_player(self) -> Optional[Player]:
        """
        Retrives the instance of player within the game.
        Uses the game grid to first find the player position,
        then uses this position to get the entity instance.

        Returns:
            Optional[Player]: The player instance of it exists
                              on the board, None if it does not.
        """
        player_position = self._grid.find_player()
        
        if player_position is not None:
            player = self._grid.get_entity(player_position)
            return player
        else:
            return None
    
    def step(self) -> None:
        """
        Runs the step event for all entities on the board.
        Additionally, this method adds to the step count
        (stored inside this class) every time it is called.
        """
        mapping = self._grid.get_mapping().copy()

        for position, entity in mapping.items():
            entity.step(position, self)

        self._steps += 1

    def get_steps(self) -> int:
        """
        Retrieves the number of steps the player has taken
        in the game.

        Returns:
            (int): The step count as an int.
        """
        return self._steps

    def move_player(self, offset: Position) -> None:
        """
        Moves the player based on the offset as a position.

        Parameters:
            offset (Position): The offset to move the player as
                               a position instance.
        """
        player_pos = self.get_grid().find_player()
        new_pos = player_pos.add(offset)
        
        self.get_grid().move_entity(player_pos, new_pos)

    def direction_to_offset(self, direction: str) -> Optional[Position]:
        """
        Calculates the offset as a position based on the given direction.

        Parameters:
            direction (str): The direction used to calculate
                             the positon offset.

        Returns:
            Optional[Position]: The offset as a position. Returns None
                                if the given direction is not found.
        """
        if direction == UP:
            return Position(0, -1)
        elif direction == DOWN:
            return Position(0, 1)
        elif direction == LEFT:
            return Position(-1, 0)
        elif direction == RIGHT:
            return Position(1, 0)
        else:
            return None

    def has_won(self) -> bool:
        """
        Checks if the player has won based on the existence
        of the hospital in the game grid.

        Returns:
            (bool): True if the game has been won, false if
                    it has not.
        """
        mapping = self.get_grid().get_mapping()

        # Search through the mapping for the hospital entity. If the
        # hospital is still in mapping, the game has not been won.
        has_hospital = False
        for value in mapping.values():
            if value.display() == HOSPITAL:
                has_hospital = True

        return not has_hospital

    def has_lost(self) -> bool:
        """
        Checks if the game has been lost. The game instance as a
        a super class does will always return this function as
        false because there is no way to lose the game.

        Returns:
            (bool): Always returns false
        """
        return False

class IntermediateGame(Game):
    """
    Handles the game at an intermediate level and is used
    to check when a player has been infected.
    """

    def has_lost(self) -> bool:
        """
        Checks whether the game has been lost based on
        the infection state of the player.

        Returns:
            (bool): True if the player is infected, false if
                    they are not.
        """
        if super().get_player().is_infected():
            return True

class AdvancedGame(IntermediateGame):
    """
    The advanced game allows the player to collect pickup
    entities from the map.
    """
    
    def move_player(self, offset: Position) -> None:
        """
        Handles player movement so that the player is now able
        to collect pickup entities.

        Parameters:
            offset (Position): The offset of which the player will
                               move.
        """
        grid = super().get_grid()
        position = grid.find_player()
        end_position = position.add(offset)

        # Check that offset position is within game board.
        if grid.in_bounds(end_position):
            
            entity = grid.get_entity(end_position)

            # Checks if the entity at the next position
            # is a pickup entity, and if so create a new
            # instance of it.
            if entity is not None:
                
                grid_mapping = grid.serialize
                player = super().get_player()
                entity_id = entity.display()

                if entity_id in PICKUP_ITEMS:
##                    if entity_id == GARLIC:
                    player.get_inventory().add_item(entity)
##                    elif entity_id == CROSSBOW:
##                        player.get_inventory().add_item(entity)

            # Superclass method called to move entity.
            super().move_player(offset)
                
        
    
class TextInterface(GameInterface):
    """
    Handles the user interface as a text representation
    for the game.

    The text interface also handles
    """

    def __init__(self, size: int):
        """
        The TextInterface class is constructed using the size of
        the game board.

        Parameters:
            size (int): The size of the grid.
        """
        self._size = size

    def draw(self, game: Game) -> None:
        """
        Draws the game board from a game instance.
        Game board is printed row by row.

        Parameters:
            game (Game): The instance of the game to draw.
        """
        border = BORDER + (BORDER * self._size) + BORDER
        grid = game.get_grid()
        
        print(border)
        # Builds each row one at a time. Checks each column of
        # row to see if an entity needs to be printed.
        for row in range(self._size):
            row_builder = BORDER
            
            for column in range(self._size):
                entity = grid.get_entity(Position(column, row))
                if entity is not None:
                    row_builder += entity.display()
                else:
                    row_builder += ' '
            row_builder += BORDER
            print(row_builder)
        print(border)

    def play(self, game: Game) -> None:
        """
        Main loop for the game. Checks if the game is over based
        on whether the player has won or lost.

        Parameters:
            game (Game): The instance of the game to play.
        """
        game_over = False
        while not game_over:
            if not game.has_lost():
                if not game.has_won():
                    self.draw(game)
                    action = input(ACTION_PROMPT)
                    self.handle_action(game, action)
                else:
                    print(WIN_MESSAGE)
                    game_over = True
            else:
                print(LOSE_MESSAGE)
                game_over = True
            

    def handle_action(self, game: Game, action: str) -> None:
        """
        Handles all actions of the player in the game. Also calls
        the step function after every action. If the action is not
        a direction, the method will only call the step function.
        """
        if action in DIRECTIONS:
            offset = game.direction_to_offset(action)
            game.move_player(offset)
        game.step()

class AdvancedTextInterface(TextInterface):
    """
    AdvancedTextInterface class handles item holding and adds
    messages to the grid. The class is an extension of the text
    interface and calls super functions.
    """

    def draw(self, game: Game) -> None:
        """
        Draws an extension to the game board of which displays
        the items a player is holding as well as their
        remaining durability.

        Parameters:
            game (Game): The game instance in its current state.
        """
        super().draw(game)
        
        player = game.get_player()
        inventory = player.get_inventory()
        items = inventory.get_items()
        
        if len(items) > 0:
            print(HOLDING_MESSAGE)
            for item in inventory.get_items():
                print(repr(item))
        

    def handle_action(self, game: Game, action: str) -> None:
        """
        Handles crossbow fire and any messages associated with
        it. After the action is complete, the super method is called
        so that the step event occurs.

        Parameters:
            game (Game): The game being played
            action (str): The action which a player enters.
        """

        if action == FIRE:
            player = game.get_player()
            inventory = player.get_inventory()
            grid = game.get_grid()
            player_pos = game.get_grid().find_player()

            if inventory.contains(CROSSBOW):
                direction = input(FIRE_PROMPT)

                current_row = player_pos.get_y()
                current_column = player_pos.get_x()

                
                zombie_shot = False

                # Loop cycles through very row and column to locate
                # all zombie entities on the map. If the fire direction
                # entered is in the grid line of a zombie, the first
                # zombie closest to the player is removed.
                
                for row in range(self._size):
                    for column in range(self._size):
                        position = Position(column, row)
                        entity = grid.get_entity(Position(column, row))

                        # Checks if the entity is an instance of the
                        # zombie superclass. This allows for removal of
                        # tracking zombies.
                        if isinstance(entity, Zombie):
                            if not zombie_shot:
                                position = Position(column, row)
                                if direction == UP:
                                    if column == current_column:
                                        if row < current_row:
                                            grid.remove_entity(position)
                                            zombie_shot = True
                                            break
                                elif direction == DOWN:
                                    if column == current_column:
                                        if row > current_row:
                                            grid.remove_entity(position)
                                            zombie_shot = True
                                            break
                                elif direction == LEFT:
                                    if row == current_row:
                                        if column < current_column:
                                            grid.remove_entity(position)
                                            zombie_shot = True                                            
                                            break
                                elif direction == RIGHT:
                                    if row == current_row:
                                        if column > current_column:
                                            grid.remove_entity(position)
                                            zombie_shot = True                                            
                                            break
                                else:
                                    print(INVALID_FIRING_MESSAGE)
                                    
                                    # Boolean set to true to avoid
                                    # unneccessary messages. Zombie is NOT
                                    # shot.
                                    zombie_shot = True
                                    break
                                    
                # If the loop ends and a zombie has not
                # been removed from the grid, fail message
                # is sent
                if not zombie_shot:
                    print(NO_ZOMBIE_MESSAGE)
            else:
                print(NO_WEAPON_MESSAGE)

        # Superclass called to handle movement inputs and call
        # step event.
        super().handle_action(game, action)
            

def main():
    """Entry point to gameplay."""

    map_name = input("Map: ")
    grid = AdvancedMapLoader().load(map_name)
    game = AdvancedGame(grid)

    interface = AdvancedTextInterface(grid.get_size())
    interface.play(game)
    
if __name__ == "__main__":
    main()
