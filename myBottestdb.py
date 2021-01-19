import mysql.connector
import pandas as pd
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
    file_import= "words.xlsx"
    data = pd.read_excel(file_import)
    val= data.values.tolist()
    return val

# insert excel data to db
def insertWords():
    sql=sql = "INSERT INTO words (ban_words, cor_words) VALUES (%s, %s)"
    data= getExcel()
    mycusor.executemany(sql,data)
    datab.commit()

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
def insertData(chat_id, user_id, user_fullname,message_id):
    sql = "INSERT INTO groupchat (chat_id, user_id, user_fullname, message_id) VALUES (%s, %s, %s, %s)"
    val= (chat_id, user_id,user_fullname,message_id )
    mycusor.execute(sql,val)
    datab.commit()

 # select group chat id   
def selectGCI():
    sql= "SELECT chat_id, COUNT(*) FROM groupchat GROUP BY chat_id "
    mycusor.execute(sql)
    res= mycusor.fetchall()
    return res

# insert data to viomember table
def vioMember(chat_id,user_id, user_fullname,times):
    sql= "INSERT IGNORE INTO viomember (chat_id, user_id, user_fullname, times) VALUES (%s,%s, %s, %s)"
    val= (chat_id, user_id, user_fullname, times)
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