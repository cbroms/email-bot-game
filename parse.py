def parseEmail(message):
    return Response(message)

def getSentence(message):
    messageAr = message.split("\n")
    for line in messageAr:
        if not line.isspace() and not "@" in line:
            return line
    return ""

def getEmails(message):
    messageAr = message.split("\n")
    result = []
    for line in messageAr:
        line.replace(","," ")
        wrds = line.split(" ")
        for wrd in wrds:
            if "@" in wrd:
                result.append(wrd)
    return result

class Response:
    def init(self, message):
        self.user_sentence = getSentence(message)
        self.user_emails = getEmails(message)