import numpy as np
import time
import heapq

'''
    This algorithm turned out to be much more convoluted than I expected it to be. Obviously there are
    much simpler solutions to this problem but they were not time efficient enough to pass all the tests.
    Because of this, I had to use multiple different ideas and algorithms to pass all the tests, such as,
    an implementation of the A* algorithm to do optimal pathfinding on the maze using a consistent heuristic
    and a priority queue. I also implemented the breadth-first search algorithm to identify minimal paths
    to the goal. Finally we use caching of intermediate solutions to avoid repeated computation of A*
    in a manner similar to dynamic programming.
'''

# Returns all the neighbouring walls (only cardinal directions) from a given point in the map. Will be used to identify possible walls to break.
def get_neighbouring_walls(center, map):

    center = center.strip('][').split(', ')
    neighs = []
    directions = []
    x = int(center[0])
    y = int(center[1])

    if x+1 < len(map) and map[x+1][y] == 1 and map[x+2][y] == 0:
        neighs.append([x+1,y])
        directions.append([1,0])

    if x-1 >= 0 and map[x-1][y] == 1 and map[x-2][y] == 0:
        neighs.append([x-1,y])
        directions.append([-1,0])

    if y+1 < len(map[0]) and map[x][y+1] == 1 and map[x][y+2] == 0:
        neighs.append([x,y+1])
        directions.append([0,1])

    if y-1 >= 0 and map[x][y-1] == 1 and map[x][y-2] == 0:
        neighs.append([x,y-1])
        directions.append([0,-1])

    return neighs, directions


def solution(map):

    # Runs the A* algorithm on the original maze and returns the distance traversed, the path used and the distances to the goal at any given point in the path.
    # If no solution is found it returns base_min_distance = 10000.
    base_min_distance, path, distances = astar([0,0], [len(map)-1,len(map[0])-1], map)

    # Theoretical smallest distance to goal.
    best_possible = get_heuristic_distance([0,0], [len(map)-1,len(map[0])-1]) + 1

    # If they are the same, return.
    if base_min_distance == best_possible:
        return base_min_distance

    # Initializing auxiliary variables
    min_distance = base_min_distance
    walls_to_break = []
    directions_to_break_from = []

    # Determine all the walls that can be broken to improve the solution.
    for element in distances:

        walls, directions = get_neighbouring_walls(element, map)

        for wall, direction in zip(walls, directions):
            if wall not in walls_to_break:

                walls_to_break.append(wall)
                directions_to_break_from.append(direction)

    '''
    If the A* did not find a solution we know that we must break a wall to escape since it is always solvable.
    In this context we can run a BFS starting from the goal to determine the minimal distance of every point to the goal.
    We can then start breaking walls and verifying if this creates an escape route. If it does, we compute the total
    distance and compare it to previous results, always keeping the best solution.
    '''
    if base_min_distance == 10000:
        optimal_distances_from_goal = bfs([len(map)-1,len(map[0])-1], map)

        for wall, direction in zip(walls_to_break, directions_to_break_from):

            origin = [a + b for a, b in zip([-x for x in direction], wall)]
            destination = [a + b for a, b in zip(direction, wall)]

            if str(destination) in optimal_distances_from_goal:

                total_distance = distances[str(origin)] + optimal_distances_from_goal[str(destination)] + 3
                if total_distance < min_distance:
                    min_distance = total_distance

                    if min_distance == best_possible:
                        return min_distance


    else:
        '''
        In this scenario, differently from the other case, the maze is solvable without breaking any walls,
        so we must find possible walls to break that will create shortcuts for the escape. This is complicated
        because a part of the initial solution may be dropped entirely in this context, which was not the case
        before. Because of this, these scenarios are much more computationally expensive then the ones before.
        '''

        distances_second_island = {}

        for wall, direction in zip(walls_to_break, directions_to_break_from):

            origin = [a + b for a, b in zip([-x for x in direction], wall)]
            destination = [a + b for a, b in zip(direction, wall)]

            # If this is a shortcut between two points in the original A* solution, just compute the shortcut efficiency
            # by subtracting the distances to the goal of both points
            if str(origin) in distances and  str(destination) in distances:

                shortcut_eff = max(distances[str(origin)], distances[str(destination)]) - min(distances[str(origin)], distances[str(destination)]) - 2
                if base_min_distance - shortcut_eff < min_distance:
                    min_distance = base_min_distance - shortcut_eff

            # If only the starting point of the "shortcut" is in the original A* solution...
            elif str(origin) in distances:

                # Ignore starting points that may not lead to improvements
                if distances[str(origin)] + get_heuristic_distance(destination, [len(map)-1,len(map[0])-1]) + 3 > min_distance:
                    continue

                # if the destination of the shortcut already has an optimal distance to the goal, compute the shortcut
                # efficiency in a similar way as described above
                if str(destination) in distances_second_island:

                    total_distance = distances[str(origin)] + distances_second_island[str(destination)] + 3

                    if total_distance < min_distance:
                        min_distance = total_distance

                        if min_distance == best_possible:
                            return min_distance

                    continue


                # If not compute the optimal distance from the destination to the shorcut to the goal using the A*
                new_distance, new_came_from, new_distances = astar(destination, [len(map)-1,len(map[0])-1], map)

                # If the A* cannot get to the goal, ignore this possible shortcut because we already broke one wall
                # and we cannot break another
                if str([len(map) - 1, len(map[0]) - 1]) not in new_distances:
                        continue

                # If the A* found a solution, record all the optimal distances to the goal that have been explored during the A*
                # so that we can use them later and save time
                else:
                    for place in new_distances:
                        if str(place) in distances_second_island:
                            continue
                        else:
                            distances_second_island[str(place)] = new_distances[str([len(map) - 1, len(map[0])-1])] - new_distances[str(place)]

                # Check if this shortcut presents an improvement on the best route so far.
                total_distance = new_distance + distances[str(origin)] + 2

                if total_distance < min_distance:
                    min_distance = total_distance

                    if min_distance == best_possible:
                        return min_distance

                    continue

            # If only the destination point of the "shortcut" is in the original A* solution... we will do something very
            # similar to the described above
            elif str(destination) in distances:

                # Ignore destinations that may not lead to improvements
                if distances[str(destination)] + get_heuristic_distance(origin, [len(map)-1,len(map[0])-1]) + 3 > min_distance:
                    continue

                # if the origin of the shortcut already has an optimal distance to the goal, compute the shortcut
                # efficiency in a similar way as described above
                if str(origin) in distances_second_island:

                    total_distance = distances[str(destination)] + distances_second_island[str(origin)] + 3

                    if total_distance < min_distance:
                        min_distance = total_distance

                        if min_distance == best_possible:
                            return min_distance

                    continue


                # If not compute the optimal distance from the destination to the shorcut to the goal using the A*
                new_distance, new_came_from, new_distances = astar(origin, [len(map)-1,len(map[0])-1], map)

                # If the A* cannot get to the goal, ignore this possible shortcut because we already broke one wall
                # and we cannot break another
                if str([len(map) - 1, len(map[0]) - 1]) not in new_distances:
                        continue

                # If the A* found a solution, record all the optimal distances to the goal that have been explored during the A*
                # so that we can use them later and save time
                else:
                    for place in new_distances:
                        if str(place) in distances_second_island:
                            continue
                            #if new_distances[destination < distance_second_island[str(distance)]:
                            #distance_second_island[str(distance)]
                        else:
                            distances_second_island[str(place)] = new_distances[str([len(map) - 1, len(map[0])-1])] - new_distances[str(place)]

                # Check if this shortcut presents an improvement on the best route so far.
                total_distance = new_distance + distances[str(destination)] + 2

                if total_distance < min_distance:
                    min_distance = total_distance

                    if min_distance == best_possible:
                        return min_distance

                    continue

    return min_distance

# A* algorithm returns optimal paths from a given starting position to a goal. Also returns the minimal distance
# to the goal for every point in the path found.
def astar(start, goal, map):

    directions = [[1,0], [0,1], [0,-1], [-1,0]]
    frontier = PriorityQueue()

    maximum_heuristic = get_heuristic_distance(start, goal)

    frontier.push(start, maximum_heuristic)

    min_distance = {}
    min_distance[str(start)] = 0

    min_heuristic = {}
    min_heuristic[str(start)] = get_heuristic_distance(start, goal)

    came_from = {}

    while not frontier.isEmpty():

        current = frontier.pop()

        if current == goal:
            return min_distance[str(current)] + 1, came_from, min_distance

        else:
            for direction in directions:

                neighbour = [a + b for a, b in zip(current, direction)]

                if all(val >= 0 for val in neighbour) and neighbour[0] <= goal[0] and neighbour[1] <= goal[1] and map[neighbour[0]][neighbour[1]] == 0:
                    tscore = min_distance[str(current)] + 1

                    if str(neighbour) not in min_distance or tscore < min_distance[str(neighbour)]:

                        neigh_heuristic_dist = get_heuristic_distance(neighbour, goal)

                        min_distance[str(neighbour)] = tscore
                        min_heuristic[str(neighbour)] = tscore + neigh_heuristic_dist
                        came_from[str(neighbour)] = current

                        frontier.update(neighbour, tscore + neigh_heuristic_dist + neigh_heuristic_dist/maximum_heuristic)

    return 10000, came_from, min_distance

# Breadth-first search that in used to find all the optimal distances from a point to every point that is connected to it
# (without breaking any walls). Returns all the points and distances
def bfs(start, map):

    directions = [[1,0], [0,1], [0,-1], [-1,0]]
    visited = []
    frontier = []
    distances = {}

    frontier.append(start)
    distances[str(start)] = 0

    while len(frontier) > 0:

        current = frontier.pop(0)
        visited.append(current)

        for direction in directions:

            neighbour = [a + b for a, b in zip(current, direction)]

            if all(val >= 0 for val in neighbour) and neighbour[0] < len(map) and neighbour[1] < len(map[0]) and map[neighbour[0]][neighbour[1]] == 0:
                if neighbour not in frontier and neighbour not in visited:
                    distances[str(neighbour)] = distances[str(current)] + 1
                    frontier.append(neighbour)

    return distances

# Implementation of the priority queue used in the A* algorithm
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


# Function to determine the manhattan distance between two points.
def get_heuristic_distance(position, goal):

    distance = 0
    distance += abs(position[0] - goal[0])
    distance += abs(position[1] - goal[1])

    return distance

#floor = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
floor = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]

a = solution(floor)
print(a)
