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
def insertData(chat_id, group_title, totalMes):
    sql = "INSERT INTO groupchat (chat_id,group_title, totalMes) VALUES (%s, %s, %s)"
    val= (chat_id, group_title, totalMes)
    mycusor.execute(sql,val)
    datab.commit()

def selectData(chat_id):
    sql="SELECT * FROM groupchat WHERE chat_id={}".format(chat_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res
# print(selectData())

def deleteData():
    sql="DELETE  FROM groupchat WHERE totalMes='1'"
    mycusor.execute(sql)
    datab.commit()

 # select groupchat_id   
def selectTotalMes(chat_id):
    sql= "SELECT totalMes FROM groupchat WHERE chat_id = {} ".format(chat_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

def selectGCI():
    sql= "SELECT chat_id FROM groupchat"
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

#update number of message
def updateCntMes(chat_id):
    sql1= "SELECT totalMes FROM groupchat where chat_id ={} ".format(chat_id)
    mycusor.execute(sql1)
    totalMes= mycusor.fetchall()
    # print(times)
    sql2= "UPDATE groupchat SET totalMes={} WHERE chat_id={}".format(totalMes[0][0]+1,chat_id)
    mycusor.execute(sql2)
    datab.commit()
   
# get number of message:
def selectNumMes(chat_id):
    sql= "SELECT totalMes FROM groupchat where chat_id ={} ".format(chat_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

# insert data to viomember table
def insertVio(chat_id,user_id, user_fullname, timesVio):
    sql= "INSERT IGNORE INTO viomember (chat_id, user_id, user_fullname, timesVio) VALUES (%s,%s,%s, %s)"
    val= (chat_id, user_id, user_fullname, timesVio)
    mycusor.execute(sql,val)
    datab.commit()

#select violations chat_id
def selectvioGCI(chat_id, user_id):
    sql="SELECT chat_id, user_id  FROM viomember WHERE chat_id={} and user_id={}".format(chat_id, user_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

#update number of violation
def updateTimesVio(chat_id, user_id):
    sql1= "Select timesVio FROM viomember where chat_id ={} and user_id={} ".format(chat_id, user_id)
    mycusor.execute(sql1)
    times= mycusor.fetchall()
    sql2= "UPDATE viomember SET timesVio={} WHERE chat_id={} and user_id={}".format(times[0][0]+1,chat_id, user_id)
    mycusor.execute(sql2)
    datab.commit()

# get times of violations most 
def gettimesVio(chat_id):
    sql= "SELECT MAX(timesVio), user_fullname, user_id FROM viomember WHERE chat_id={} ".format(chat_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

    
#get member'info violated most
def getInfoVio(chat_id):
    sql= "SELECT user_id, timesVio FROM viomember WHERE chat_id={} ".format(chat_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

def delMem():
    sql="DELETE  FROM viomember WHERE timeVio >= '10'"
    mycusor.execute(sql)
    datab.commit()

# total violations of each group
def totalvio(chat_id):
    sql= "SELECT SUM(timesVio) FROM viomember WHERE chat_id={} ".format(chat_id)
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

#get title of group
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

# print(selectGCI())
