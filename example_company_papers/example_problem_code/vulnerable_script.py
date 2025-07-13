import re

def register_user(email, password):
    if re.match(r".+@.+\..+", email):
        save_to_db(email, password)  # ⚠️ Plaintext password saved!
    else:
        print("Invalid email")

def save_to_db(email, password):
    with open("users.txt", "a") as f:
        f.write(f"{email}: {password}\n")
