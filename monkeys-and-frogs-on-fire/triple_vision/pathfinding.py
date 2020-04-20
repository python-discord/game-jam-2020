from typing import List, Optional, Tuple

import arcade

from triple_vision import Settings as s
from triple_vision.utils import tile_to_pixels


class Node:

    def __init__(
        self,
        pos: Tuple[float, float],
        parent: Optional[Node] = None
    ) -> None:

        self.parent = parent
        self.pos = pos

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other: Node) -> bool:
        return self.pos == other.pos

    def __add__(self, other: Node) -> Node:
        return Node(
            (
                self.pos[0] + other.pos[0],
                self.pos[1] + other.pos[1]
            ),
            self
        )

    def __sub__(self, other: Node) -> Node:
        return Node(
            (
                self.pos[0] - other.pos[0],
                self.pos[1] - other.pos[1]
            ),
            self
        )


class PathFinder:

    def __init__(self, max_tries: int = 50) -> None:
        self.max_tries = max_tries

    def find(
        self,
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        collision_list: arcade.SpriteList
    ) -> List[Tuple[int, int]]:

        open_nodes = list()
        closed_nodes = list()

        start_node = Node(start_pos)
        end_node = Node(end_pos)

        open_nodes.append(start_node)

        for _ in range(self.max_tries):
            current_node = open_nodes[0]

            for node in open_nodes:
                if node.f < current_node.f:
                    current_node = node

            open_nodes.remove(current_node)
            closed_nodes.append(current_node)

            if current_node == end_node:
                path = list()

                current = current_node
                while current is not None:
                    path.append(current.pos)
                    current = current_node.parent

                return path[::-1]

            surroundings = [
                (-1, -1),
                (0, -1),
                (1, -1),
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0)
            ]

            children = [
                current + Node(pos) for pos in surroundings
                if not self._tile_is_blocked(*pos, collision_list)
            ]

            for child in children:

                for closed_node in closed_nodes:
                    if child == closed_node:
                        continue

                # http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html#the-a-star-algorithm
                child.g = current_node.g + 1

                n = child - end_node
                child.h = n.pos[0] ** 2 + n.pos[1] ** 2

                child.f = child.g + child.h

                for open_node in open_nodes:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_nodes.append(child)

    def _tile_is_blocked(self, x: float, y: float, sprite_list: arcade.SpriteList) -> bool:
        if x < 0 or x > s.MAP_SIZE[0] or y < 0 or y > s.MAP_SIZE[1]:
            return True

        blocking_sprites = arcade.get_sprites_at_exact_point(
            tile_to_pixels(x, y),
            sprite_list
        )
        if len(blocking_sprites) > 0:
            return True

        return False
