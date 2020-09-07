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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']
service = None
maxIterations = 3
emails = []

def initBot():
  iterations = 0
  story = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit."]
  message = "You’ve been nominated." + \
            "\nAdd a sentence in after the sentence below." + "\n" + story[0] + \
            "\nThank you\n\n iteration " + str(iterations) + " out of " + str(maxIterations)
  initEmail = "mkomar@andrew.cmu.edu"
  create_and_send_email( service, message,initEmail)

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

def endGame(story):
    message = "Here's the story you've worked so hard to make\n\n" + storyToString(story)
    for email in emails:
        create_and_send_email(service, message, email)

# response is a struct(?) which contains user_sentence(string) and user_emails (array of strings)
#story (array of strings) containing the paragraph stuff so far. arr[currIteration] to access current sentence.
def receiveEmail(response, story):
  if len(story) < maxIterations:
      story.append(response.user_setence)
      emails.append(response.user_emails)
      sendMessage(story, response.user_emails)
  else:
      endGame(story)


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
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



def sync_emails(service, history=None):

  if history is not None:
    print("checking for new messages... ", end="")
    res = service.users().history().list(userId="me", startHistoryId=history).execute()
    if "history" in res:
      for message in res["history"][0]["messages"]:
        print("\nnew message found, threadId: {}".format(message["threadId"]))
        # get the message content 
        res = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
        decodedBytes = base64.urlsafe_b64decode(res["payload"]["body"]["data"])
        content = str(decodedBytes, "utf-8")
        # parse the message, extracting the new sentence and word, in addition to new emails 
        # parse_it()
        # construct and send the new messages 
        # create_and_send_email(service, "Hi there. This is a test.", "cbroms@andrew.cmu.edu")
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

    history = sync_emails(service)

    # check for new mail every 15 seconds 
    while True:
      history = sync_emails(service, history)
      time.sleep(15)
    
    # initBot()

    
if __name__ == '__main__':
    main()
