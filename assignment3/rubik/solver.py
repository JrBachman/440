from typing import List
from typing import Optional

from sqlalchemy import false

import rubik


def shortest_path(
        start: rubik.Position,
        end: rubik.Position,
) -> Optional[List[rubik.Permutation]]:     

        """
        Using 2-way BFS, finds the shortest path from start to end.
        Returns a list of Permutations representing that shortest path.
        If there is no path to be found, return None instead of a list.

        You can use the rubik.quarter_twists move 6-tuple.
        Each move can be applied using rubik.perm_apply.
        """


        #Invariant documentation:
        #The problem is started with a dictionary of start and end parents as well as an empty set to be filled with the current tier.
        #used sets for the ease of use of set comparistons.
        #With each iteration the problem advances a tier from the start and checks the current end tier if a perm exists in it. it then advances
        #the end tier one and proceeds with the same check.
        #The problem gets smaller as the operations go as we proceed one step closer to the solution if it exists.
        #The problem terminates when the next posistion of a move is found in the set of the opposite side. Or when the loop reaches its limit and a path is not found
        #Once the match is found the program adds the start path to a list and the inverse of the end path to a list and returns the combined lists.


        moves = rubik.quarter_twists

        parentStart = {}
        parentEnd = {} 
        parentStart[start] = None
        parentEnd[end] = None

        start_current_tier = set()
        end_current_tier = set()
        start_current_tier.add(start)
        end_current_tier.add(end)
        #check if no moves are required
        if end in parentStart:
                return path(parentStart, parentEnd, end)

        for i in range(7):
                start_next_tier = set()
                for position in start_current_tier:
                        #apply all possible moves to all positions of the current tier
                        for move in moves:
                                next_position = rubik.perm_apply(move, position)
                                #makes sure move does not undo the last move of the position
                                if next_position not in parentStart:
                                        parentStart[next_position] = (position, move)
                                        start_next_tier.add(next_position)
                                        #if a match is found call list maker and terminate
                                        if next_position in parentEnd:
                                                return path(parentStart,parentEnd,next_position)
                #sets new tier made to be current working tier
                start_current_tier = start_next_tier
                end_next_tier = set()
                #same as above but for end tiers
                for position in end_current_tier:
                        for move in moves:
                                next_position = rubik.perm_apply(move, position)
                                if next_position not in parentEnd:
                                        parentEnd[next_position] = (position, move)
                                        end_next_tier.add(next_position)
                                        if next_position in parentStart:
                                                return path(parentStart,parentEnd,next_position)

                end_current_tier = end_next_tier
        #if this point is reached no path exists. I hope.
        return None

def path(parentStart, parentEnd, position):
        #makes empty list to fill in start half of path
        start_path = []
        current_position = position

        while parentStart[current_position] != None:
                (current_position, move) = parentStart[current_position]
                start_path.insert(0, move)

        end_path = []
        current_position = position

        while parentEnd[current_position] != None:
                (current_position, move) = parentEnd[current_position]
                end_path.append(rubik.perm_inverse(move))
        
        return start_path + end_path 

