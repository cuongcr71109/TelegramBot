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
                
                
                first_update_id = int (current_update['update_id'])
                # print(type(first_update_id))
                # print(type(first_update_id))
                if 'channel_post' in current_update:
                    message_id = current_update['channel_post']['message_id']
                    first_chat_id= current_update['channel_post']['chat']['id']
                    first_chat_text= current_update['channel_post']['text']
                    user_id= current_update['channel_post']['sender_chat']['id']
                    group_title= current_update['channel_post']['chat']['title']
                    
                    if first_chat_text:
                        my_bot.send_message(first_chat_id," ")
                        new_offset = first_update_id +1
            
                else :
                    first_chat_id = current_update['message']['chat']['id']   
                    message_id = current_update['message']['message_id']
                    user_id = current_update['message']['from']['id']
                    group_title= current_update['message']['chat']['title']
                    
                
                    
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
                            violation= selectvioGCI(first_chat_id, user_id)
                            my_bot.del_message(first_chat_id, message_id)
                            new_offset = first_update_id +1
                            if len(violation) >0 :
                                updateTimesVio(first_chat_id, user_id)
                            else:
                                insertVio(first_chat_id, user_id, user_fullname,1)
                            break

                    
                    # kick_member
                    vioList= getInfoVio(first_chat_id) #violation information
                    for i in vioList:  
                        if i[1] >=10:                              
                            my_bot.kick_member(first_chat_id, i[0])
                            delMem()  

                  
                    # insert data to groupchat table
                    groupData=selectData(first_chat_id)
                    if len(groupData) >0 :
                        updateCntMes(first_chat_id)         
                    else :
                        insertData(first_chat_id, group_title,1)

                    # count total messages
                    totalMes= selectNumMes(first_chat_id)[0][0]
                    print(totalMes)   
                    if first_chat_text == "/count": 
                        my_bot.send_message(first_chat_id, "Total messages are: " + str(totalMes))
                
                    # forward_message
                    chatForward= selectGCI()
                    for i in chatForward:
                        if i[0] != '-455427299':
                            my_bot.forward_message(i[0],'-455427299', message_id)

                    #statistic    
                    # get num of violations
                    totalvioList= totalvio(first_chat_id)
                    total= totalvioList[0][0]
        
                    if first_chat_text == "/count":
                        if str(total) ==" None":
                            my_bot.send_message(first_chat_id, "Total violations are: 0" )
                            my_bot.send_message(first_chat_id, "Total deleted messages are: 0" )
                        else: 
                            my_bot.send_message(first_chat_id, "Total violations are: " +str(total))
                            my_bot.send_message(first_chat_id, "Total deleted messages are: " + str(total))

                    # get info of member violated most
                    vioperson=gettimesVio(first_chat_id)
                    if len(vioperson)>0:
                        if first_chat_text == "/count":
                            my_bot.send_message(first_chat_id, "Member violated most is: " + vioperson[0][1])
                        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        