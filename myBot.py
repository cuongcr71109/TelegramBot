import requests
from datetime import datetime, timedelta
import time
import operator
import json
import collections
import mysql.connector
import myBottestdb
from myBottestdb import *
from BotHandler import*




def main():
    new_offset = 0
    print('hi, now launching...')
    now= datetime.now()
    now= now.strftime("%H:%M:%S")
    print(now)

      

    while True:
        all_updates = my_bot.get_updates(new_offset)
    
           
        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                
                
                first_update_id = current_update['update_id']

                if 'channel_post' in current_update:
                    message_id = current_update['channel_post']['message_id']
                    first_chat_id= current_update['channel_post']['chat']['id']
                    first_chat_text= current_update['channel_post']['text']
                    user_id= current_update['channel_post']['sender_chat']['id']
            
                else :
                    first_chat_id = current_update['message']['chat']['id']   
                    message_id = current_update['message']['message_id']
                    user_id = current_update['message']['from']['id']
                    group_title= current_update['message']['chat']['title']
                    group_type=  current_update['message']['chat']['type']
                
                    
                    if 'text' not in current_update['message'] :
                        first_chat_text = 'New member'
                    else:                    
                        first_chat_text = current_update['message']['text']
                    
                    if 'last_name' in current_update['message']:   
                        first_last_name= current_update['message']['chat']['last_name']
                        
                                                    
                    elif 'first_name'  in current_update['message']:
                        first_chat_name = current_update['message']['chat']['first_name']
                    
                    elif 'message' in current_update['message']:
                        message_id = current_update['message']['message_id']
                                    
                    elif 'new_chat_member' in current_update['message']:
                        first_chat_name = current_update['message']['new_chat_member']['first_name']
                        first_last_name = " "
                        user_fullname = first_chat_name
                        
                    elif 'from' in current_update['message']:
                        first_chat_name = current_update['message']['from']['first_name']
                        if 'last_name' not in current_update['message']['from']:
                            first_last_name = " "
                        else:
                            first_last_name = current_update['message']['from']['last_name']
                        
                    elif 'left_chat_member' in current_update['message']:
                        
                        first_chat_name= current_update['message']['left_chat_member']['first_name']
                        first_last_name= " "
                        user_fullname = first_chat_name
                        
                    user_fullname= first_chat_name +" " + first_last_name

                    if first_chat_text:
                        my_bot.send_message(first_chat_id," ")
                        new_offset = first_update_id +1
                    

                    my_bot.join_group('https://t.me/joinchat/RcGGtdG60NynCrJK') 
                    # send_message
                    corWords= selectCorwords() #corresponse words
                    for i in corWords:
                        if first_chat_text == i[0]:
                            my_bot.send_message(first_chat_id, "Nice to meet you, " + first_chat_name)
                            new_offset = first_update_id +1
                            break

                    # delete_message
                    banWords= selectBanwords() #banned words
                    for i in banWords:
                        if first_chat_text == i[0]: 
                            my_bot.del_message(first_chat_id, message_id)
                            new_offset = first_update_id +1
                            vioMember(first_chat_id, user_id, user_fullname)
                            break

                    
                    # kick_member
                    vioList= viomember() #violation information
                    # print('vioList',vioList)
                    for i in vioList:    
                        if first_chat_id == int(i[2]): 
                            if i[3] >=10:                                 
                                my_bot.kick_member(i[2], i[0])                    
                    

                    
                    insertData(first_chat_id, user_id, user_fullname, group_title, group_type)
                    groupList= selectGCI()
                    # print('group',groupList) 
                    
                    
                    for i in groupList:
                        # count total messages
                        if first_chat_id == int(i[0]):
                            if first_chat_text == "/count": 
                                my_bot.send_message(first_chat_id, "Total messages are: " +str(i[1]) )
                        # forward_message
                        if i[0] != '-455427299':
                            my_bot.forward_message(i[0],'-455427299', message_id)

                    
                    #statistics
                    totalvioList= totalvio()
                   
                    for i in totalvioList:
                        if first_chat_id == int(i[0]):
                            if first_chat_text == "/count":
                                if str(i[1]) ==" None":
                                    my_bot.send_message(first_chat_id, "Total violations are: 0" )
                                    my_bot.send_message(first_chat_id, "Total deleted messages are: 0" )
                                else: 
                                    my_bot.send_message(first_chat_id, "Total violations are: " +str(i[1]) )
                                    my_bot.send_message(first_chat_id, "Total deleted messages are: " +str(i[1]) )

                    


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        