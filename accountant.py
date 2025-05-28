from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1CoZ72s9-uwX9RcEY81xSihEzUi4_PsjBzeImnrBvWmk'
SAMPLE_RANGE_NAME = 'Form Responses 1!A1:G'
EDIT_RANGE_NAME = 'Form Responses 1!A1:E'
adminID = '1651529355'  # Pallab Chat-ID

import time
import datetime
from tqdm.contrib.telegram import tqdm, trange
import telegram
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import threading
from subprocess import PIPE, Popen

msg = """
Hi! Pallab have set me up for updating you about your House renovation account.
                                                - gadhuBot

You can type the following commands to get the corresponding updates:
    /start -> shows this text
    /balance -> shows current balance
    /transactions N -> shows last N number of transactions
    /credit amount remark -> add credit, update everyone
    /debit amount remark -> add debit, update everyone
    /clear -> delete chat history
"""

def get_spreadsheet(creds):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    ##creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    ##if os.path.exists('token.json'):
    ##    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    ##if not creds or not creds.valid:
    ##    if creds and creds.expired and creds.refresh_token:
    ##        creds.refresh(Request())
    ##    else:
    ##        flow = InstalledAppFlow.from_client_secrets_file(
    ##            'credentials.json', SCOPES)
    ##        creds = flow.run_local_server(port=0)
    ##    # Save the credentials for the next run
    ##    with open('token.json', 'w') as token:
    ##        token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        return values
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[0]))
    except HttpError as err:
        print(err)

def put_spreadsheet(putLIST,creds):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    ##creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    ##if os.path.exists('token.json'):
    ##   creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    ##if not creds or not creds.valid:
    ##    if creds and creds.expired and creds.refresh_token:
    ##        creds.refresh(Request())
    ##    else:
    ##        flow = InstalledAppFlow.from_client_secrets_file(
    ##            'credentials.json', SCOPES)
    ##        creds = flow.run_local_server(port=0)
    ##    # Save the credentials for the next run
    ##    with open('token.json', 'w') as token:
    ##       token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        values = [putLIST]
        body = {'values': values}
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=EDIT_RANGE_NAME, valueInputOption='USER_ENTERED', body=body).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        return values
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[0]))
    except HttpError as err:
        print(err)

class Termibot:
    def __init__(self):
        self.TOKEN = '1711613332:AAHzf0GMQPjnBINOfIhfbK9dmIUo7mHiThw'
        self.BOT = telegram.Bot(token=self.TOKEN)
        self.smsID = []
        self.dict = {}
        self.creds = None
        self.flow = None

    def cmdTRIGGER(self):
        self.updater = Updater(self.TOKEN, use_context=True)
        dp = self.updater.dispatcher
        try:
            dp.add_handler(MessageHandler(Filters.all, self.strSMS))
        except:
            pass
        self.updater.start_polling()
        self.updater.idle()

    def strSMS(self, update, context):
        txt = update.message.text
        USERid = update.message.chat.id
        if USERid not in self.dict:
            self.dict[USERid]=len(self.dict)
            print(update.message.message_id)
            self.smsID.append([update.message.message_id])
        else:
            self.smsID[self.dict[USERid]].append(update.message.message_id)
        cmd = txt.split(' ')[0]
        args = txt.split(' ')[1:]
        print(cmd,args)
        if cmd == '/start':
            self.start(userid=USERid)
        elif cmd == '/authenticate':
            self.authenticate(userid=USERid)
        elif cmd == '/token':
            code = args[0]
            self.savetoken(userid=USERid,CODE=code)
        elif cmd == '/balance':
            try:
                self.balance(userid=USERid)
            except:
                self.authenticate(userid=USERid)
        elif cmd == '/transactions':
            try:
                if len(args)==0:
                    self.transactions(userid=USERid)
                else:
                    self.transactions(userid=USERid,args=args[0])
            except:
                self.authenticate(userid=USERid)
        elif cmd == '/credit':
            try:
                amnt=float(args[0])
                rmrk=' '.join(args[1:])
            except:
                amnt=float(args[-1])
                rmrk=' '.join(args[:-1])
            try:
                self.credit(amount=amnt,remark=rmrk)
            except:
                self.authenticate(userid=USERid)
        elif cmd == '/debit':
            try:
                amnt=float(args[0])
                rmrk=' '.join(args[1:])
            except:
                amnt=float(args[-1])
                rmrk=' '.join(args[:-1])
            try:
                self.debit(amount=amnt,remark=rmrk)
            except:
                self.authenticate(userid=USERid)
        elif cmd == '/clear':
            self.cls(userid=USERid)
        elif cmd == '/exit':
            if str(USERid)==adminID:
                self.EXIT(userid=USERid)
            else:
                TXT = 'command not found !'
                self.sendUPDATE(CHATID=USERid,txt=TXT)
        elif cmd[0] == '/':
            TXT = 'command not found !'
            self.sendUPDATE(CHATID=USERid,txt=TXT)
        else:
            TXT = "Sorry I can only read '/commands', not 'texts'."
            self.sendUPDATE(CHATID=USERid,txt=TXT)

    def start(self,userid):
        self.sendUPDATE(CHATID=userid,txt=msg)

    def authenticate(self,userid):
        creds = None
        if os.path.exists('token.json'):
            try:
                print('inside try')
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                self.creds = creds
            except:
                print('removing token')
                creds = None
                os.remove('token.json')
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    os.remove('token.json')
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
                auth_url, _ = self.flow.authorization_url(prompt='consent')
                TXT="Please go to this URL: {}".format(auth_url)
                self.sendUPDATE(CHATID=userid,txt=TXT)

    def savetoken(self,userid,CODE):
        # Save the credentials for the next run
        token = self.flow.fetch_token(code=CODE)
        creds = self.flow.credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        self.authenticate(userid)

    def balance(self,userid='all'):
        values=get_spreadsheet(creds=self.creds)
        bal=values[1][6]
        TXT="current balance: %.2f/-"%(float(bal))
        if userid!='all':
            self.sendUPDATE(CHATID=userid,txt=TXT)
        else:
            self.sendUPDATE2all(txt=TXT)

    def transactions(self,userid,args=1):
        values=get_spreadsheet(creds=self.creds)
        total_transactions=len(values)
        num=min(int(args),total_transactions-1)
        for i in range(total_transactions-num,total_transactions):
            val=values[i]
            TXT=self.maketext(val)
            self.sendUPDATE(CHATID=userid,txt=TXT)

    def credit(self,amount,remark):
        timestamp = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        values=[timestamp, '', '', amount, remark]
        put_spreadsheet(values,creds=self.creds)
        TXT = "A new transaction is done!\n\ntime: %s\ncredit: %s/-\nremarks: %s"%(timestamp,amount,remark)
        self.sendUPDATE2all(txt=TXT)
        self.balance(userid='all')

    def debit(self,amount,remark):
        timestamp = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        values=[timestamp, amount, remark, '', '']
        put_spreadsheet(values,creds=self.creds)
        TXT = "A new transaction is done!\n\ntime: %s\ndebit: %s/-\nremarks: %s"%(timestamp,amount,remark)
        self.sendUPDATE2all(txt=TXT)
        self.balance(userid='all')

    def maketext(self,vals):
        if len(vals)==3:
            text="time: %s\ndebit: %s/-\nremarks: %s"%(vals[0],vals[1],vals[2])
        else:
            if vals[1]=='' or vals[2]=='':
                text="time: %s\ncredit: %s/-\nremarks: %s"%(vals[0],vals[3],vals[4])
            else:
                text="time: %s\ndebit: %s/-\nremarks: %s\ncredit: %s/-\nremarks: %s"%(vals[0],vals[1],vals[2],vals[3],vals[4])
        return text

    def EXIT(self,userid):
        txt = "Thanks! I am signing off."
        self.sendUPDATE(userid,txt)
        time.sleep(2)
        self.cls(userid=userid)
        threading.Thread(target=self.shutdown).start()

    def shutdown(self):
        self.updater.stop()
        self.updater.is_idle = False

    def cls(self,userid):
        smsID = self.smsID[self.dict[userid]]
        for i in smsID:
            self.BOT.delete_message(chat_id=userid, message_id=i)
        self.smsID[self.dict[userid]] = []

    def sendUPDATE2all(self,txt):
        USERs = list(self.dict.keys())
        for CHATID in USERs:
            self.sendUPDATE(CHATID,txt)

    def sendUPDATE(self,CHATID,txt):
        self.BOT.sendChatAction(chat_id=CHATID, action="typing")
        msg = self.BOT.sendMessage(chat_id=CHATID, text=txt)
        self.smsID[self.dict[CHATID]].append(msg.message_id)

def main():
    k=Termibot()
    k.cmdTRIGGER()

if __name__ == "__main__":
    main()
