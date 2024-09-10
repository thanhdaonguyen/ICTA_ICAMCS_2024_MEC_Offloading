
def Dijkstra(graph, start, end):
    
    # Create a dictionary to store the shortest distance from the start node to each node
    distance = {node: float('inf') for node in graph}
    distance[start] = 0
    
    # Create a set to keep track of visited nodes
    visited = set()
    
    # Create a priority queue to store nodes with their corresponding distances
    queue = [(start, 0)]
    
    while queue:
        # Get the node with the minimum distance from the queue
        current_node, current_distance = min(queue, key=lambda x: x[1])
        queue.remove((current_node, current_distance))
        
        # Check if the current node has been visited
        if current_node in visited:
            continue
        
        # Add the current node to the visited set
        visited.add(current_node)
        
        # Check if we have reached the end node
        if current_node == end:
            break
        
        # Explore the neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            # Calculate the new distance to the neighbor node
            new_distance = current_distance + weight
            
            # Update the distance if the new distance is smaller
            if new_distance < distance[neighbor]:
                distance[neighbor] = new_distance
                # Add the neighbor node to the queue
                queue.append((neighbor, new_distance))
    
    # Return the shortest distance from the start node to the end node
    return distance[end]
    
if __name__ == '__main__':

    # Define the graph as an adjacency list
    graph = {
        1: {2: 1, 3: 4},
        2: {1: 1, 3: 2, 4: 5},
        3: {1: 4, 2: 2, 4: 1},
        4: {2: 5, 3: 1}
    }
    
    # Find the shortest path from node 1 to node 4
    shortest_distance = Dijkstra(graph, 1, 4)
    print(f"The shortest distance from node 1 to node 4 is: {shortest_distance}")