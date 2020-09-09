from __future__ import print_function
import pickle
import time 
import os.path
from email.mime.text import MIMEText
import base64
import re

from googleapiclient.discovery import build
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from parse import parseEmail
from gamestate import addPlayersIntoList, recieveEmail, Player

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']
service = None
maxIterations = 3
players = {}



#starting emails
#player 1 email automadlibs@gmail.com 
#starting sentences
# #max iterations

# def create_and_send_multiple_emails(service, message, emails):
#   for email in emails: 
#     create_and_send_email(service, message,email)

def initBot():
  iterations = 0
  email = "automadlibs@gmail.com"
  initalEmail = "mkomar@andrew.cmu.edu"

  threadId = create_and_send_email(service, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", initalEmail )
  thisBot = Player(threadId, email, initalEmail, None)
  players[thisBot] = [initalEmail]

def generateMessage(story):
  message = "You’ve been nominated." + \
            "\n Add a sentence in after the sentence below." + story[len(story)-1] + \
  "\nThank you\n\n iteration " + str(len(story)) + "out of " + str(maxIterations)

def sendMessage(story, emails):
  for email in emails:
      create_and_send_email(service, generateMessage(story,maxIterations), email)

def storyToString(story):
  # initialize an empty string
  string = ""
  # traverse in the string
  for sentence in story:
      string += sentence
  return string


"""
This will send everyone in the people array the story.
"""
def sendStoryToEveryone(story, people):
    message = ""
    message.join(story)
    for person in people:
        create_and_send_email(service, message, person.email)


# def receiveEmail(response, story):
#   """
#   :Arg response: a struct like-thing which contains data from the email.
#     contains user_sentence(string) and user_emails (array of strings)
#   :Arg story:(array of strings) so far. arr[currIteration] to access current sentence.
#     arr[currIteration] to access current sentence.
#   """
#   if len(story) < maxIterations:
#       story.append(response.user_setence)
#       players.append(response.user_emails)
#       sendMessage(story, response.user_emails)
#   else:
#       endGame(players,ThisBot)


def create_message(sender, to, subject, message_text):

  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {"raw": str( base64.b64encode(message.as_bytes()), "utf-8")}

def create_draft(service, user_id, message_body):
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()
    return draft
  except errors.HttpError as e:
    print( e )
    return None


# create an email and send it 
def create_and_send_email(service, message, recipient):
    email = create_message("automadlibs@gmail.com", recipient, "Test", message)
    draft = create_draft(service, "me", email)
    res = service.users().drafts().send(userId="me", body={"id": draft["id"]}).execute()
    return res["threadId"]



def sync_emails(service, history=None):

  if history is not None:
    print("checking for new messages... ", end="")
    res = service.users().history().list(userId="me", startHistoryId=history).execute()
    if "history" in res:
      for message in res["history"][0]["messages"]:
        print("\nnew message found, threadId: {}".format(message["threadId"]))
        # get the message content 
        res = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
        try:
          decodedBytes = base64.urlsafe_b64decode(res["payload"]["body"]["data"])
          content = str(decodedBytes, "utf-8")
          # parse the message, extracting the new sentence and word, in addition to new emails 
          parsed = parseEmail(content)
          print(parsed.user_emails, parsed.user_sentence)
          # construct and send the new messages 
          ids = []
          for email in parse.user_emails:
            threadId = create_and_send_email(service, "Hi there. This is a test.", email)
            print(threadId)
            ids.append(threadId)
          # update the game state with the response and new emails 
          receiveEmail(parsed, message["threadId"], ids, players)
        except:
          pass
          # print("not a new email")

    else:
      print("no new messages found")
    return res["historyId"]
  else:
    print("syncing inbox... ", end="")
    # get a list of the most recent messages in the inbox 
    res = service.users().messages().list(userId="me").execute()
    # get the most recent message's id 
    most_recent = res["messages"][0]["id"]
    # get the history timestamp of the most recent message 
    res = service.users().messages().get(userId="me", id=most_recent).execute()
    print("sync done")
    return res["historyId"]

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service 

    service = build('gmail', 'v1', credentials=creds)
    # now we can use the service to send, create, search through gmail 

    initBot()

    history = sync_emails(service)

    # check for new mail every 15 seconds 
    while True:
      # get any new replies and deal with them (parse, send to invited friends, etc)
      history = sync_emails(service, history)
      time.sleep(15)



    
if __name__ == '__main__':
    main()
