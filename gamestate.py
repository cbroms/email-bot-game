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



recieveEmail(responder)
EndGame(visited, players, A)

