from __future__ import annotations

from typing import Optional, Tuple, Iterator

import arcade

from triple_vision import Settings as s
from triple_vision.utils import tile_to_pixels


class Node:
    __slots__ = ('parent', 'pos', 'f', 'g', 'h')

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

    def __key(self):
        return self.pos[0], self.pos[1]

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other: Node) -> bool:
        return self.__key() == other.__key()

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

    def __init__(self, max_tries: int = 300) -> None:
        self.max_tries = max_tries

    def find(
        self,
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        collision_list: arcade.SpriteList,
        map_list: arcade.SpriteList
    ) -> Iterator[Tuple[int, int]]:

        if self._tile_is_blocked(*end_pos, collision_list):
            return

        if not self._tile_is_blocked(*end_pos, map_list):
            return

        open_nodes = set()
        closed_nodes = set()

        start_node = Node(start_pos)
        end_node = Node(end_pos)

        open_nodes.add(start_node)

        surroundings = (
            Node((0, -1)),
            Node((1, 0)),
            Node((0, 1)),
            Node((-1, 0))
        )

        for _ in range(self.max_tries):
            if not open_nodes:
                return

            current_node = min(open_nodes, key=lambda node: node.f)

            open_nodes.remove(current_node)
            closed_nodes.add(current_node)

            if current_node == end_node:
                path = []

                current = current_node
                while current is not None:
                    path.append(current.pos)
                    current = current.parent

                return reversed(path)

            children = (
                current_node + pos_node for pos_node in surroundings
                if not PathFinder._tile_is_blocked(*(current_node + pos_node).pos, collision_list)
            )

            for child in children:

                if child in closed_nodes:
                    continue

                # http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html#the-a-star-algorithm
                child.g = current_node.g + 1

                n = child - end_node
                child.h = n.pos[0] ** 2 + n.pos[1] ** 2

                child.f = child.g + child.h

                if child in open_nodes:
                    if any(child.g > open_node.g for open_node in open_nodes):
                        continue

                open_nodes.add(child)

    @staticmethod
    def _tile_is_blocked(x: int, y: int, sprite_list: arcade.SpriteList) -> bool:
        if x < 0 or x > s.MAP_SIZE[0] or y < 0 or y > s.MAP_SIZE[1]:
            return True

        blocking_sprites = arcade.get_sprites_at_exact_point(
            tile_to_pixels(x, y),
            sprite_list
        )

        return len(blocking_sprites) > 0
