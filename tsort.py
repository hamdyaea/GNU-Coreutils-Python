#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The tsort command from GNU coreutils in Python3.  
Example of use: cat file.txt | python3 tsort.py
'''

#!/usr/bin/env python3

import sys
from collections import defaultdict, deque

class TopologicalSorter:
    def __init__(self):
        # Graph representation using adjacency list
        self.graph = defaultdict(set)
        # Track in-degree for each node
        self.in_degree = defaultdict(int)
        # Set of all nodes
        self.nodes = set()

    def add_edge(self, u, v):
        """Add a directed edge from u to v"""
        if u not in self.graph[v]:
            self.graph[u].add(v)
            self.in_degree[v] += 1
            self.nodes.add(u)
            self.nodes.add(v)

    def sort(self):
        """Perform topological sorting"""
        # Queue of nodes with zero in-degree
        zero_in_degree = deque([node for node in self.nodes if self.in_degree[node] == 0])

        # Result list
        sorted_order = []

        while zero_in_degree:
            # Remove a node with zero in-degree
            current = zero_in_degree.popleft()
            sorted_order.append(current)

            # Reduce in-degree for adjacent nodes
            for neighbor in self.graph[current]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    zero_in_degree.append(neighbor)

        # Check for cycles
        if len(sorted_order) != len(self.nodes):
            raise ValueError("Graph contains a cycle")

        return sorted_order

def main():
    # Read input from stdin
    sorter = TopologicalSorter()

    try:
        for line in sys.stdin:
            # Split line into two nodes
            parts = line.strip().split()
            if len(parts) == 2:
                sorter.add_edge(parts[0], parts[1])
    except ValueError:
        print("Error: Invalid input format", file=sys.stderr)
        sys.exit(1)

    try:
        # Perform topological sort and print results
        result = sorter.sort()
        for item in result:
            print(item)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
