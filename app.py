import mariadb
from flask import Flask, request, Response
import json
import dbcreds
import hashlib
import secrets
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/mvptodolist', methods=['GET', 'POST', 'DELETE'])
def Tasks_endpoint():
    if request.method == 'GET':
        conn = None
        cursor = None
        Tasks = None
        try:
           conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
           cursor = conn.cursor()
           cursor.execute("SELECT * FROM task_table")
           Tasks = cursor.fetchall()
           
        except Exception as error:
            print("Error: ")
            print(error)
        finally:
            if(cursor !=None):
             cursor.close()
            if(conn !=None):
             conn.rollback()
             conn.close()
            if(Tasks !=None):
             return Response(json.dumps(Tasks, default=str), mimetype="application/json", status=200)
            else: 
             return Response("Something went wrong!", mimetype="text/html", status=500)
     
    elif request.method =='POST':
        conn = None
        cursor = None
        createdAt = request.json.get("createdAt")
        task = request.json.get("task")
        username = request.json.get("username")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO task_table(createdAt, task, username) VALUES(?, ?, ?)", [createdAt, task, username])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Error: ")
            print(error)
        finally:
            if(cursor !=None):
             cursor.close()
            if(conn !=None):
             conn.rollback()
             conn.close()
            if(rows == 1):
                return Response("Task inserted", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong", mimetype="text/html", status=500)
    
    
    elif request.method == "DELETE":
        conn = None
        cursor = None 
        task_id =request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port,              database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM task_table WHERE id=?", [task_id])
            conn.commit() 
            rows = cursor.rowcount    
        except Exception as error:
            print("Something went wrong (This is LAZY)")  
            print(error)  
        finally: 
            if cursor != None:
                cursor.close() 
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Delete Success", mimetype="text/html", status=204)
            else:
                return Response("Delete Failed", mimetype="text/html", status=500)   

##############################################user login###########################################  
@app.route('/api/login', methods=['POST', 'DELETE'])
def user_session_endpoint():
    
    if request.method == 'POST':
        conn = None
        cursor = None
        email = request.json.get("email")
        password = request.json.get("password")
 
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute ("SELECT * FROM user_table WHERE email = ? AND password = ? ", [email, password])
            user = cursor.fetchall()
            loginToken = secrets.token_urlsafe(20)
            print(user)
            if len (user) == 1:
                cursor.execute ("INSERT INTO user_session (user_id, loginToken) VALUES (?,?)", [user[0][0], loginToken]) 
                conn.commit()
                rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                user={
                    "id": user[0][0],
                    "email": email,
                    "username": user[0][2],
                    "loginToken": loginToken
                }
           
                return Response(json.dumps(user,default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
            
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_session WHERE loginToken = ?", [loginToken])
            conn.commit() 
            rows = cursor.rowcount    
        except Exception as error:
            print("Something went wrong (This is LAZY)")  
            print(error)  
        finally: 
            if cursor != None:
                cursor.close() 
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Logout Success", mimetype="text/html", status=204)
            else:
                return Response("Logout Failed", mimetype="text/html", status=500)
            
##############################################signup#########################################################
@app.route('/api/signup', methods=['POST'])
def user_signup_endpoint():
    
    if request.method == 'POST':
        conn = None
        cursor = None
        email = request.json.get("email")
        password = request.json.get("password")
        username = request.json.get("username")
        rows = None
        
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_table (email, password, username) VALUES (?,?,?)", [ email, password, username])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY): ")
            print(error)
            
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                user={
               
                    "email": email,
                  
                    "username": username,
                  
                }
                return Response(json.dumps(user,default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
                                               
            
          
    
                    
            