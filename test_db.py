# from database.base import engine
# try:
#     conn = engine.connect()
#     print("database connected")
#     conn.close()
# except Exception as e:
#     print("failed",e)

from database.supabase_client import supabase

# Upload a test file
with open("test.txt", "w") as f:
    f.write("Hello Supabase")

with open("test.txt", "rb") as f:
    supabase.storage.from_("scans").upload("test/test.txt", f.read())

print("Uploaded ✅")

# List files
files = supabase.storage.from_("scans").list("test")
print(files)