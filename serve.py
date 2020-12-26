import bjoern
from app import app
host ='0.0.0.0'
port = 5001
print("Bjoern up and running")
bjoern.run(app, host, port)