from database.mongodb import users_collection

print("Users in database:\n")

for user in users_collection.find():
    print(user)