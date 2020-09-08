class Player:
    def __init__(self, id, sentence, emails):
        self.id = id
        self.sentence = sentence
        self.emails = emails


A = Player("0", "hello world!", ["wonderful!"])
B = Player("1", "as long as it's uncensored", ["wonderful!"])
C = Player("2", "Yeah well same with my parents", ["wonderful!"])
E = Player("3", "I dunno my man", ["wonderful!"])
F = Player("4", "world hello@", ["wonderful!"])

players = {
    A: [B, C, E, F],
    B: [C, E],
    F: [E],
    C: [],
}

visited = []  # List to keep track of visited nodes.
queue = []  # Initialize a queue

"""
This ain't doing exactly what we want it to do: 
It's giving us 1,2,3,4 and then 2,3, 3, then nothing but we their parents to appear in all of them
"""
def bfs(visited, graph, node):
    visited.append(node)
    queue.append(node)
    #neighbourhood = graph[node]
    while queue:
        s = queue.pop(0)
        if s in graph.keys():
            for neighbour in graph[s]:
                #if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
                print(neighbour.id)
            print("||\n")


# Driver Code
bfs(visited, players, A)
