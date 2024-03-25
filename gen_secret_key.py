import os

def generate_secret_key():
    return os.urandom(24).hex()

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Your secret key is:", secret_key)
