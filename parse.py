def parseEmail(message):
    return Response(message)

def getSentence(message):
    for line in message:
        if not line.isspace() and not "@" in line:
            return line
    return ""

def getEmails(message):
    result = []
    for line in message:
        line.replace(","," ")
        wrds = line.split(" ")
        for wrd in wrds:
            if "@" in wrd:
                result.append(wrd)
    return result

class Response:
    def __init__(self, message):
        self.user_sentence = getSentence(message)
        self.user_emails = getEmails(message)