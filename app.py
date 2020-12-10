import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/mvptodolist', methods=['GET', 'POST', 'PATCH', 'DELETE'])
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
            
          
    
                    
            