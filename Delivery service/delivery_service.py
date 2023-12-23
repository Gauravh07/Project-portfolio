"""
UMass ECE 241 - Advanced Programming
Project 2 - Fall 2023
"""
import sys
from graph import Graph, Vertex
from priority_queue import PriorityQueue

class DeliveryService:
    def __init__(self) -> None:
        """
        Constructor of the Delivery Service class
        """
        self.city_map = None
        self.MST = None

    def buildMap(self, filename: str) -> None:
        # Function to build a graph from a file containing edges and weights
        self.city_map = Graph()
        file = open(filename, 'r')
        lines = file.readlines()

        for line in lines:
            x = line.strip().split('|')
            # Add edge to the graph with the given weights
            self.city_map.addEdge(int(x[0]), int(x[1]), int(x[2]))

    def isWithinServiceRange(self, restaurant: int, user: int, threshold: int) -> bool:
        '''Checks if the user is within the service range of the restaurant using Dijkstra's algorithm.'''
        if restaurant not in self.city_map.getVertices() or user not in self.city_map.getVertices():
            return False  # User node does not exist

        return self.dijkstra(self.city_map, self.city_map.getVertex(restaurant), self.city_map.getVertex(user), threshold, delay=None)

    def buildMST(self, restaurant: int) -> bool:
        '''Building a Minimum Spanning Tree (MST) using prims algorithm'''
        self.MST = Graph()
        PQ = PriorityQueue()

        # Initialize vertices for the algorithm
        for v in self.city_map:
            v.dist = sys.maxsize
            v.pred = None
            v.color = 'white'

        self.city_map.vertList[restaurant].dist = 0
        PQ.buildHeap([(v.dist, v) for v in self.city_map])

        # Main loop
        while not PQ.isEmpty():
            currentVert = PQ.delMin()
            for nextVert in currentVert.getConnections():
                newCost = currentVert.getWeight(nextVert)
                if nextVert in PQ and newCost < nextVert.dist:
                    nextVert.dist = newCost
                    nextVert.pred = currentVert
                    PQ.decreaseKey(nextVert, newCost)

        # Add edges to the MST
        for v in self.city_map:
            if v.pred:
                self.MST.addEdge(v.pred.id, v.id, v.dist)
        return

    def dijkstra(self, aGraph, start, stop, threshold, delay):
        ''' Dijkstra's algorithm to find the shortest path from start to stop'''
        if start is None:
            return -1
        for v in aGraph:
            v.setDistance(float('Inf'))
            v.setPred(None)
        start.setDistance(0)

        pq = PriorityQueue()
        pq.buildHeap([(v.getDistance(), v) for v in aGraph])

        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections():
                newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
                if newDist < nextVert.getDistance():
                    nextVert.setDistance(newDist)
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert, newDist)

        '''Checking if threshold is provided and if the stop is within the threshold distance'''
        if threshold is not None:
            if threshold == 'gaurav':
                if stop is not None:
                    return stop.getDistance()
                else:
                    return -1
            elif stop.getDistance() <= threshold:
                return True
            else:
                return False
        else:
            '''Handle cases where delay is provided'''
            if delay == 'gaurav':
                print('gaurav')
                path = []
                current = stop
                while current:
                    path.insert(0, str(current.getId()))
                    current = current.getPred()
                path_str = '->'.join(path)
                return "{0} ({1})".format(path_str, stop.getDistance())

            if delay != 'gaurav':
                # Handle cases where delay dictionary is provided
                if delay is not None:
                    path = []
                    delay_sum = 0
                    current = stop
                    while current:
                        if current.getId() in delay:
                            delay_sum += delay[current.getId()]
                        path.insert(0, str(current.getId()))
                        current = current.getPred()
                    path_str = '->'.join(path)
                    return "{0} ({1})".format(path_str, stop.getDistance())
                else:
                    return "INVALID"

    def minimalDeliveryTime(self, restaurant: int, user: int) -> int:
        '''Find the minimal delivery time from the restaurant to the user using Dijkstra's algorithm on the MST'''
        if (restaurant is not None and restaurant in self.MST.getVertices() and
                user is not None and user not in self.MST.getVertices()):
            return -1
        else:
            return self.dijkstra(self.MST, self.MST.getVertex(restaurant), self.MST.getVertex(user), threshold='gaurav', delay=None)

    def findDeliveryPath(self, restaurant: int, user: int) -> str:
        '''Find the delivery path from the restaurant to the user using Dijkstra's algorithm on the city map'''
        if restaurant not in self.city_map.getVertices() or user not in self.city_map.getVertices():
            return "INVALID"
        return self.dijkstra(self.city_map, self.city_map.getVertex(restaurant), self.city_map.getVertex(user), threshold=None, delay='gaurav')

    def findDeliveryPathWithDelay(self, restaurant: int, user: int, delay_info: dict[int, int]) -> str:
        '''Find the delivery path from the restaurant to the user with delay information using Dijkstra's algorithm on the city map'''
        if restaurant not in self.city_map.getVertices() or user not in self.city_map.getVertices():
            return "INVALID"
        return self.dijkstra(self.city_map, self.city_map.getVertex(restaurant), self.city_map.getVertex(user), threshold=None, delay=delay_info)

    ## DO NOT MODIFY CODE BELOW!
    @staticmethod
    def nodeEdgeWeight(v):
        return sum([w for w in v.connectedTo.values()])

    @staticmethod
    def totalEdgeWeight(g):
        return sum([DeliveryService.nodeEdgeWeight(v) for v in g]) // 2

    @staticmethod
    def checkMST(g):
        for v in g:
            v.color = 'white'

        for v in g:
            if v.color == 'white' and not DeliveryService.DFS(g, v):
                return 'Your MST contains circles'
        return 'MST'

    @staticmethod
    def DFS(g, v):
        v.color = 'gray'
        for nextVertex in v.getConnections():
            if nextVertex.color == 'white':
                if not DeliveryService.DFS(g, nextVertex):
                    return False
            elif nextVertex.color == 'black':
                return False
        v.color = 'black'

        return True
