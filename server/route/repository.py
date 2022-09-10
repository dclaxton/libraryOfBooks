from functools import total_ordering
import pyodbc
from flask import jsonify
from dto.Book import Book
import config.conf as conf
import json

def connectToDb():
    #TODO: store these in a property/env file somewhere
    server = conf.DB_ADDR
    database = conf.DB_NAME
    username = conf.DB_USER
    password = conf.DB_PASS
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn.cursor()

def getAllBooks():
    bookList = []
    cursor = connectToDb()
    try:
        cursor.execute('SELECT * FROM dbo.Library')
        rows = cursor.fetchall() 
        for row in rows:
            #print(json.dumps(Book(row.Id,row.Name,row.Author,row.has_read,row.Available), default=lambda o: o.encode()))
            bookList.append(Book(row.Id,row.Name,row.Author,row.has_read,row.Available))
        cursor.close()
        return bookList
    except pyodbc.Error as err:
        print(err.args[1])
    finally:
        return bookList

def getSingleBook(id):
    cursor = connectToDb()
    try:
        cursor.execute('SELECT * FROM dbo.Library WHERE Id = ?', id)
        row = cursor.fetchone()
        cursor.close()
        return Book(row[0], row[1], row[2], row[3], row[4]) if row is not None else None
    except pyodbc.Error as err:
        print(err.args[1])

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