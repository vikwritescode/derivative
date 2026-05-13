import sqlite3
import json
    
def main():
    # open database connection
    db = sqlite3.connect("src/debates.db")
    cursor = db.cursor()
    # get all users    
    cursor.execute("SELECT DISTINCT user_id FROM debates")
    users = cursor.fetchall()
    # extract user ids and write to whitelist.json
    user_ids = [user[0] for user in users]
    with open("whitelist.json", "w") as f:
        json.dump(user_ids, f)
    print(f"Whitelist generated with {len(user_ids)} user ids.")
        

if __name__ == "__main__":
    main()