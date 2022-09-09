from functools import total_ordering
import pyodbc
from dto.Book import Book

def connectToDb():
    #TODO: store these in a property/env file somewhere
    server = '#'
    database = '#'
    username = '#'
    password = '#'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn.cursor()

def getAllBooks():
    bookList = []
    cursor = connectToDb()
    try:
        cursor.execute('SELECT * FROM dbo.Library')
        rows = cursor.fetchall() 
        for row in rows:
            bookList.append(list(row))
        cursor.close()
        return bookList
    except pyodbc.Error as err:
        print(err.args[1])
    finally:
        return bookList

def getSingleBook(id):
    bookList = []
    cursor = connectToDb()
    try:
        cursor.execute('SELECT * FROM dbo.Library WHERE Id = ?', id)
        row = cursor.fetchone() 
        bookList.append(list(row))
        cursor.close()
        return bookList
    except pyodbc.Error as err:
        print(err.args[1])
    finally:
        return bookList

def removeBook(id):
    cursor = connectToDb()
    success = True
    try:
        print('ID: ' + id)
        cursor.execute("DELETE FROM dbo.Library WHERE Id = ?", id)
        cursor.commit()
    except pyodbc.Error as err:
        print(err.args[1])
        success = False
        cursor.rollback()
    finally:
        cursor.close()
        return success

def addBook(data):
    cursor = connectToDb()
    success = True
    try:
        cursor.execute('INSERT INTO dbo.Library VALUES (?,?,?,?)', \
            [data.get('name'), data.get('author'), data.get('hasRead'), data.get('available')])
        cursor.commit()
    except pyodbc.Error as err:
        print(err.args[1])
        success = False
        cursor.rollback()
    finally: 
        cursor.close()
        return success

def updateBook(data, id):
    cursor = connectToDb()
    success = True
    try:
        cursor.execute('UPDATE dbo.Library SET Name=?,Author=?,has_read=?,available=? WHERE Id = ?',\
            [data.get('name'),data.get('author'),data.get('hasRead'),data.get('available'), id])
        cursor.commit()
    except pyodbc.Error as err:
        print(err.args[1])
        success = False
        cursor.rollback()
    finally:
        cursor.close()
        return success