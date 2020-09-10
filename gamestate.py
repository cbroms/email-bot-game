class Player:
    def __init__(self, id, sentence, email, emails = None, parent=None):
        self.id = id
        self.sentence = sentence
        self.email = email
        self.emails = emails
        self.child = None
        self.parent = parent
        #parent.child = self

class Response:
    def __init__(self, message):
        self.user_sentence = ""
        self.user_emails = ["mkomar@andrew.cmu.edu", "cbroms@andrew.cmu.edu"]
        self.id = ""
        self.email = ""

A = Player("0", "hello world!", "cassonde@andrew.cmu.edu")
B = Player("1", "as long as it's uncensored", "kjgreen@andrew.cmu.edu")
C = Player("2", "Yeah well same with my parents", "calight@andrew.cmu.edu")
E = Player("4", "I dunno my man", "mkguo@andrew.cmue.edu")
F = Player("3", "world hello@", "SchoolofArt@cmu.edu")

players = {
    A: [B, C, E, F],
    B: [C, E],
    F: [E],
    E: [],
}




"""
This will send everyone in the people array the story.
"""
# def sendStoryToEveryone(story, people):
#     message = ""
#     message.join(story)
#     for person in people:
#         create_and_send_email(service, message, person.email)

"""
Performs a BFS search algorithm to give what to who
"""
def EndGame(graph, node):
    visited = []  # List to keep track of visited nodes.
    queue = []  # Initialize a queue
    visited.append(node)
    queue.append(node)
    # neighbourhood = graph[node]
    while queue:
        s = queue.pop(0)
        if s in graph.keys():
            story = []
            neighbours = []
            story.append(node.sentence)
            for neighbour in graph[s]:
                # if neighbour not in visited:
                neighbour.parent = s
                visited.append(neighbour)
                queue.append(neighbour)
                story.append(neighbour.sentence)
                neighbours.append(neighbour)
            sendStoryToEveryone(story,neighbours)

#Init all these emails as players with their generated IDs
def addPlayersIntoList(emails, ids,gamePlayers, player):
    referredPlayers = []
    for i in range(len(emails)):
        referredPlayers.append(Player(ids[i], "" ,emails[i],None,player))
    gamePlayers[player] = referredPlayers

#When we have a response from a given email
def recieveEmail(response, ident, ids, gamePlayers):
    #we need to find out who this is
    for key in gamePlayers:
        if str(key.id) == str(ident):
            #we know who this is now!
            referredPlayers = []
            for i in range(len(key.emails)):
                responder = Player(ids[i], response.user_sentence, key.emails[i],response.user_emails,key)
                addPlayersIntoList(responder.emails,ids,gamePlayers,responder)
                referredPlayers.append(responder)
            gamePlayers[key] = referredPlayers
            return key
    return key