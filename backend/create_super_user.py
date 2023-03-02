#!/usr/bin/env python

import env
import psycopg2
import secrets
import hashlib
import getpass


USER = env.DB_USER
PASSWORD = env.DB_PASSWORD
DB_NAME = env.DB_NAME

con = psycopg2.connect(
    database=DB_NAME, user=USER, password=PASSWORD, host="localhost", port=5432
)


def create_user(connection, name: str, email: str, password: str) -> None:
    cur = connection.cursor()
    cur.execute(
        "insert into super_users values(%s, %s, %s)",
        (
            name,
            email,
            hash_password(password),
        ),
    )
    connection.commit()


def user_exists(connection, name: str) -> bool:
    cur = connection.cursor()
    cur.execute("select name from super_users where name = %s", (name,))
    if len(cur.fetchall()) > 0:
        return True
    return False


def email_exists(connection, email: str) -> bool:
    cur = connection.cursor()
    cur.execute("select email from super_users where email = %s", (email,))
    if len(cur.fetchall()) > 0:
        return True
    return False


def get_salt():
    return secrets.token_hex(8)


def hash_password(plain_text_password):
    salt = get_salt()
    password = (plain_text_password + salt).encode("utf-8")
    hashed_password = hashlib.sha512(password).hexdigest()
    return f"{salt}${hashed_password}"


def main():
    print("Enter your credentials to create user")
    name = str(input("Enter Username:"))
    email = str(input("Enter Email:"))
    password = str(getpass.getpass("Enter Password:"))
    re_password = str(getpass.getpass("Re-enter password"))
    if password != re_password:
        print("Passwords do not mach")
        return
    if user_exists(con, name):
        print("User already exists")
        return
    if email_exists(con, email):
        print("Email is already used")
        return
    if len(name) < 5:
        print("Name must be at least 5 chars")
    if len(password) < 8:
        print("Password must be at least 8 chars")
        return
    create_user(con, name, email, password)


if __name__ == "__main__":
    main()
