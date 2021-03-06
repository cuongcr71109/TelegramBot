import requests
import operator
import json

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        

    
    #functions get_updates
    def get_updates(self, offset=0, timeout=30):
        method_url = r'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method_url, params)
        data = json.loads(resp.text)
        if data['ok'] == True:
            result_json = data['result']
           
            return  result_json
        return data

    
    #function send messages    
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method_url = r'sendMessage'
        resp = requests.post(self.api_url + method_url, params)
        return resp
    
    #function delete message
    def del_message(self, chat_id, message_id):
        params = {'chat_id':chat_id ,'message_id': message_id}
        method_url = r'deleteMessage'
        resp= requests.get(self.api_url + method_url,params)
        return True

    #fucntion forward message
    def forward_message(self, chat_id, from_chat_id, message_id):
        params= {'chat_id':chat_id, 'from_chat_id':from_chat_id,'message_id': message_id}
        method_url=r'forwardMessage'
        resp= requests.post(self.api_url + method_url, params)
        return resp

    #function kick member
    def kick_member(self, chat_id, user_id):
        params= {'chat_id': chat_id, 'user_id': user_id}
        method_url = r'kickChatMember'
        resp= requests.post(self.api_url + method_url, params)
        return resp
    
    
           

token = '1699769501:AAHgmj5qvRfi_LsDf4Tk4B5quMiQd6_RD9g' #Token of your bot 
# username: @nguyenminhquanMQM_bot
#name : Nguyen Minh Quan

my_bot = BotHandler(token=token)