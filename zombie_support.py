"""
Support code for ZombieGame.
"""

import random
from typing import List, Tuple, Dict

# characters that can represent entities in a grid
PLAYER = "P"
HOSPITAL = "H"
BORDER = "#"

ZOMBIE = "Z"
TRACKING_ZOMBIE = "T"
ZOMBIES = (ZOMBIE, TRACKING_ZOMBIE)

GARLIC = "G"
CROSSBOW = "C"
PICKUP_ITEMS = (GARLIC, CROSSBOW)
# lifetime of pickup items
LIFETIMES = {GARLIC: 10, CROSSBOW: 5}

# actions a player can make
UP = "W"
LEFT = "A"
DOWN = "S"
RIGHT = "D"
DIRECTIONS = (UP, LEFT, DOWN, RIGHT)
FIRE = "F"

# direction offsets, see random_directions docstring for more details
OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# user interaction constants
ACTION_PROMPT = "Enter your next action: "
WIN_MESSAGE = "You win!"
LOSE_MESSAGE = "You lose!"

HOLDING_MESSAGE = "The player is currently holding:"
FIRE_PROMPT = "Direction to fire: "
NO_ZOMBIE_MESSAGE = "No zombie in that direction!"
INVALID_FIRING_MESSAGE = "Invalid firing direction entered!"
NO_WEAPON_MESSAGE = "You are not holding anything to fire!"


def random_directions() -> List[Tuple[int, int]]:
    """
    Return a randomly sorted list of directions.

    The list will always contain (0, 1), (0, -1), (1, 0), (-1, 0)
    but the order will be random.

    Each direction is represented by an offset that is the change
    in (x, y) coordinates that results from moving in the direction.
    """
    return random.sample(OFFSETS, k=4)

class Position:
    """
    The position class represents a location in a 2D grid.

    A position is made up of an x coordinate and a y coordinate.
    The x and y coordinates are assumed to be non-negative whole numbers which
    represent a square in a 2D grid.

    Examples:
        >>> position = Position(2, 4)
        >>> position
        Position(2, 4)
        >>> position.get_x()
        2
        >>> position.get_y()
        4
    """

    def __init__(self, x: int, y: int):
        """
        The position class is constructed from the x and y coordinate which the
        position represents.

        Parameters:
            x: The x coordinate of the position
            y: The y coordinate of the position
        """
        self._x = x
        self._y = y

    def get_x(self) -> int:
        """Returns the x coordinate of the position."""
        return self._x

    def get_y(self) -> int:
        """Returns the y coordinate of the position."""
        return self._y

    def distance(self, position: "Position") -> int:
        """
        Returns the manhattan distance between this point and another point.

        The manhattan distance for two points (x_1, y_1) and (x_2, y_2)
        is calculated with the formula

        |x_1 - x_2| + |y_1 - y_2|

        where |x| is the absolute value of x.

        Parameters:
            position: Another position to calculate the distance from
                      the current position.
        """
        dx = abs(self.get_x() - position.get_x())
        dy = abs(self.get_y() - position.get_y())
        return dx + dy

    def in_range(self, position: "Position", range: int) -> bool:
        """
        Returns true if the given position is in range of the current position.

        The distance between the two positions are calculated by the manhattan
        distance. See the Position.distance method for details.

        Parameters:
            position: Another position to check if it is within range
                      of this current position.
            range: The maximum distance for another position to be considered
                   within range of this position.

        Precondition:
            range >= 0
        """
        distance = self.distance(position)
        return distance < range

    def add(self, position: "Position") -> "Position":
        """
        Add a given position to this position and return a new instance of
        Position that represents the cumulative location.

        This method shouldn't modify the current position.

        Examples:
            >>> start = Position(1, 2)
            >>> offset = Position(2, 1)
            >>> end = start.add(offset)
            >>> end
            Position(3, 3)

        Parameters:
            position: Another position to add with this position.

        Returns:
            A new position representing the current position plus
            the given position.
        """
        return Position(self._x + position.get_x(), self._y + position.get_y())

    def __eq__(self, other: object) -> bool:
        """
        Return whether the given other object is equal to this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are equal, return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        # an __eq__ method needs to support any object for example
        # so it can handle `Position(1, 2) == 2`
        # https://www.pythontutorial.net/python-oop/python-__eq__/
        if not isinstance(other, Position):
            return False
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __hash__(self) -> int:
        """
        Calculate and return a hash code value for this position instance.

        This allows Position instances to be used as keys in dictionaries.

        A hash should be based on the unique data of a class, in the case
        of the position class, the unique data is the x and y values.
        Therefore, we can calculate an appropriate hash by hashing a tuple of
        the x and y values.
        
        Reference: https://stackoverflow.com/questions/17585730/what-does-hash-do-in-python
        """
        return hash((self.get_x(), self.get_y()))

    def __repr__(self) -> str:
        """
        Return the representation of a position instance.

        The format should be 'Position({x}, {y})' where {x} and {y} are replaced
        with the x and y value for the position.

        Examples:
            >>> repr(Position(12, 21))
            'Position(12, 21)'
            >>> Position(12, 21).__repr__()
            'Position(12, 21)'
        """
        return f"Position({self.get_x()}, {self.get_y()})"

    def __str__(self) -> str:
        """
        Return a string of this position instance.

        The format should be 'Position({x}, {y})' where {x} and {y} are replaced
        with the x and y value for the position.
        """
        return self.__repr__()


class GameInterface:
    """
    The GameInterface class is an abstract class that handles the communication
    between the interface used to play the game and the game itself.

    For this assignment, we will only have one interface to play the game,
    the text interface.
    """

    def draw(self, game) -> None:
        """
        Draw the state of a game to the respective interface.

        The abstract GameInterface class should raise a NotImplementedError for
        this method.

        Parameters:
            map (Game): An instance of the game class that is to be displayed
                        to the user by printing the grid.
        """
        raise NotImplementedError

    def play(self, game) -> None:
        """
        The play method takes a game instance and orchestrates the running of
        the game, including the interaction between the player and the game.

        The abstract GameInterface class should raise a NotImplementedError for
        this method.

        Parameters:
            game (Game): An instance of the Game class to play.
        """
        raise NotImplementedError

EntityLocations = Dict[Tuple[int, int], str]
"""
EntityLocations stores locations of entities in the game map.

The key is a tuple, as (x, y) coordinates,
which represents the location of the entity.
The value is a string representing the entity.
"""


def load_map(filename: str) -> Tuple[EntityLocations, int]:
    """
    Open and read a map file, converting it into a tuple.

    The first element of the returned tuple contains a dictionary which maps
    (x, y) coordinates to a string representing an entity in the map.

    The second element of the returned tuple is the size of the map.

    Parameters:
        filename: Path where the map file should be found.

    Returns:
        A tuple containing the serialized map and the size of the map.
    """
    with open(filename) as map_file:
        contents = map_file.readlines()

    result = {}
    for y, line in enumerate(contents):
        for x, char in enumerate(line.strip("\n")):
            if char != " ":
                result[(x, y)] = char

    return result, len(contents)


if __name__ == "__main__":
    print("This file is not intended to be run on its own. Run a2.py instead.")
