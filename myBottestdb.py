import mysql.connector
import pandas as pd
from pandas import ExcelWriter

datab= mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="telegrambot",
)
mycusor= datab.cursor()

if mycusor:
    print("connected")
else:
    print("failed connected")

# get file excel
def getExcel():
    file_import= "C:/MQM/TeleBot_git/TelegramBot/words.xlsx"
    data = pd.read_excel(file_import)
    val= data.values.tolist()
    return val

# insert excel data to db
def insertWords():
    sql=sql = "INSERT INTO words (ban_words, cor_words) VALUES (%s, %s)"
    data= getExcel()
    mycusor.executemany(sql,data)
    datab.commit()

insertWords()
# select ban words
def selectBanwords():
    sql= "SELECT ban_words FROM words"
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

    
# select correspond words
def selectCorwords():
    sql= "SELECT cor_words FROM words"
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res


def createTable(self, tblname):
    self.tblname= tblname
    sql= "CREATE TABLE {} ( name VARCHAR(255), phone VARCHAR(255))". format(tblname)
    mycusor.execute(sql)

# insert data to groupchat table
def insertData(chat_id, group_title, times):
    sql = "INSERT INTO groupchat (chat_id,group_title, times) VALUES (%s, %s, %s)"
    val= (chat_id, group_title, times)
    mycusor.execute(sql,val)
    datab.commit()

def selectData(chat_id):
    sql="SELECT * FROM groupchat WHERE chat_id={}".format(chat_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res
# print(selectData())

def deleteData():
    sql="DELETE  FROM groupchat WHERE times='1'"
    mycusor.execute(sql)
    datab.commit()
 # select groupchat_id   
def selectGCI():
    sql= "SELECT chat_id, COUNT(*) FROM groupchat GROUP BY chat_id "
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

#select number of message
def updateCntMes(chat_id):
    sql1= "Select times FROM groupchat where chat_id ={} ".format(chat_id)
    mycusor.execute(sql1)
    times= mycusor.fetchall()
    print(times)
    sql2= "UPDATE groupchat SET times={} WHERE chat_id={}".format(times[0][0]+1,chat_id)
    mycusor.execute(sql2)
    datab.commit()
   

# insert data to viomember table
def vioMember(chat_id,user_id, user_fullname):
    sql= "INSERT IGNORE INTO viomember (chat_id, user_id, user_fullname) VALUES (%s,%s, %s)"
    val= (chat_id, user_id, user_fullname)
    mycusor.execute(sql,val)
    datab.commit()

# get times of violations of each member
def viomember():
    sql= "SELECT user_id, user_fullname, chat_id, COUNT(*) FROM viomember GROUP BY user_id, chat_id "
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

# total violations of each group
def totalvio():
    sql= "SELECT chat_id, COUNT(*) FROM viomember GROUP BY chat_id "
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

def groupInfo():
    sql="SELECT DISTINCT group_title FROM groupchat WHERE NOT chat_id='-455427299'"
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

groupInfo= groupInfo()

def exportData():
    
    groupList=[]
    for i in groupInfo:
        groupList.append(i[0].replace("?",""))

    df= pd.DataFrame()
    df['Group_name']= groupList

    with ExcelWriter (r'C:/MQM/Group_title.xlsx') as writer:
        df.to_excel(writer, index= False)

exportData()

# print(selectData())
