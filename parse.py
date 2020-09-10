def parseEmail(message):
    return Response(message)

def getSentence(message):
    messageAr = message.split("\n")

    # find the line that contains automadlibs@gmail.com, indicating we've reached the section
    # with the old email copied 

    for i in range(len(messageAr)):
        if i < len(messageAr) - 1 and "automadlibs@gmail.com" in messageAr[i]:
            del messageAr[i:]
    
    message = " ".join(messageAr)
    messageAr = message.split(" ")
    res = ""
    for word in messageAr:
        if not "@" in word:
            res += " " + word.strip()
    res = res.strip()
    return res

def getEmails(message):
    messageAr = message.split("\n")
    result = []
    for line in messageAr:
        line.replace(","," ")
        wrds = line.split(" ")
        for wrd in wrds:
            if "@" in wrd and "automadlibs" not in wrd and "mailto" not in wrd and "<" not in wrd:
                result.append(wrd)
    return result

class Response:
    def __init__(self, message):
        self.user_sentence = getSentence(message)
        self.user_emails = getEmails(message)
