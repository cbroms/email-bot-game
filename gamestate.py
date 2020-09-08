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
E = Player("3", "I dunno my man", " SchoolofArt@cmu.edu")
F = Player("4", "world hello@", "mkguo@andrew.cmue.edu")

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
    # neighbourhood = graph[node]
    while queue:
        s = queue.pop(0)
        if s in graph.keys():
            for neighbour in graph[s]:
                # if neighbour not in visited:
                neighbour.parent = s
                visited.append(neighbour)
                queue.append(neighbour)
                print(neighbour.id)
            print("||\n")

def addPlayerIntoList(player):
    referredEmails = player.emails
    referredPlayers = []
    for i in range(len(referredEmails)):
        referredPlayers.append(Player("TEMP", "",referredEmails[i],None,player))
    players[player] = referredPlayers

def recieveEmail(response):
    #we need to find out who this is.
    #so far, we know they were referred to someone, who that is we don't know.
    #so based on what their email is and ID we can figure it out.
    for key in players:
        for player in players[key]:
            if player.id == response.id and player.email == response.email:
                print("do we get here")
                #we know who this is now!
                player.sentence = response.user_sentence
                player.emails = response.user_emails
                addPlayerIntoList(player)
                return

responder = Response(None)
responder.id = "4"
responder.email = "mkguo@andrew.cmue.edu"
responder.user_emails = ["koz@andrew.cmu.edu", "golan@flong.org", "abonilla@andrew.cmu.edu"]
responder.user_sentence = "Atleast it isn’t a pharmacy this time"

# Driver Code
#bfs(visited, players, A)
recieveEmail(responder)