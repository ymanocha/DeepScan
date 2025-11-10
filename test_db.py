from database.base import engine
try:
    conn = engine.connect()
    print("database connected")
    conn.close()
except Exception as e:
    print("failed",e)