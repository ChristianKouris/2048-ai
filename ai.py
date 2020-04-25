from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modifying this __init__ function
    def __init__(self, state, current_depth, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.depth = current_depth
        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        if len(self.children):
            return 0
        else: 
            return 1

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modifying this __init__ function
    def __init__(self, root_state, depth): 
        self.root = Node(root_state, 0, MAX_PLAYER)
        self.depth = depth
        self.simulator = Game()
        self.simulator.board_size = len(root_state[0])

    # recursive function to build a game tree
    def build_tree(self, node=None):
        if node == None:
            node = self.root

        if node.depth == self.depth: 
            return 

        if node.player_type == MAX_PLAYER:
            for direction in MOVES:
                is_moved = self.simulator.move(direction)
                if( not is_moved ):
                    continue
                child = Node( self.simulator.get_state(), node.depth+1, CHANCE_PLAYER )
                self.build_tree( child )
                node.children.append( (direction, child) )
                self.simulator.reset(*(node.state))

        elif node.player_type == CHANCE_PLAYER:
            for tile in self.simulator.get_open_tiles():
                self.simulator.tile_matrix[tile[0]][tile[1]] = 2
                child = Node( self.simulator.get_state(), node.depth+1, MAX_PLAYER )
                self.build_tree( child )
                self.simulator.tile_matrix[tile[0]][tile[1]] = 0
                node.children.append( (None, child) )

    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):

        if node == None:
            node = self.root

        if node.is_terminal():
            return (None, node.state[1])

        elif node.player_type == MAX_PLAYER:
            value = -1
            direction = None
            for child in node.children:
                (c_dir, c_val) = self.expectimax(child[1])
                if c_val > value:
                    value = c_val
                    direction = child[0]
            return (direction, value)

        elif node.player_type == CHANCE_PLAYER:
            value = 0
            for child in node.children:
                value += self.expectimax(child[1])[1]
            value /= len(node.children)
            return (None, value)

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        return random.randint(0, 3)
