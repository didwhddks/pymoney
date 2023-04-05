import sys
import os

def add(money, records):
    new_records = input("""Add some expense or income records with description and amount:
desc1 amt1, desc2 amt2, desc3 amt3, ...\n""").split(", ")
    new_records = [tuple(record.split()) for record in new_records]
    try:
        for record in new_records:
            if len(record) != 2:
                raise
    except:
        sys.stderr.write("The format of a record should be like this: breakfast -50.\nFail to add a record.\n")
    else:
        try:
            records += [(desc, int(amt)) for desc, amt in new_records]
            money += sum(int(amt) for desc, amt in new_records)
        except ValueError:
            sys.stderr.write("Invalid value for money.\nFail to add a record.\n")
    finally:
        return money, records

def view(money, records):
    print("Here's your expense and income records: ")
    print("  %-20s %s\n  %s %s" %("Description", "Amount", "="*20, "="*20))
    for i, (desc, amt) in enumerate(records):
        print("%d %-20s %s" %(i+1, desc, amt))
    print("  %s %s" %("="*20, "="*20))
    print("Now you have %d dollars." %money)

def delete(money, records):
    view(money, records)
    try:
        deleted = int(input("\nWhich record do you want to delete (Please enter the corresponding record number)? "))-1
        del records[deleted]
    except ValueError:
        sys.stderr.write("Invalid format. Fail to delete a record.\n")
    return money, records

def initialize():
    try:
        fh = open("records.txt", "r")
    except FileNotFoundError:
        try: 
            records = []
            money = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
            money = 0
    else:
        try:
            money = int(fh.readline())
            records = []
            for record in fh.readlines():
                record = record.split()
                if len(record) != 2:
                    raise
                record = (record[0], int(record[1]))
                records.append(record)
        except:
            sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
            fh.close()
            os.remove("records.txt")
            money, records = initialize()
        else:
            print("Welcome back!")
            fh.close()
    finally:
        return money, records

def save(initial_money, records):
    with open("records.txt", "w") as file:
        file.write("%s\n" %str(initial_money))
        records = [[record[0], str(record[1])] for record in records]
        records = [" ".join(record) for record in records]
        for record in records:
            file.writelines("%s\n" %record)
        

initial_money, records = initialize()

while True:
    command = input("\nWhat do you want to do (add / view / delete / exit)? ")
    if command == "add":
        initial_money, records = add(initial_money, records)
    elif command == "view":
        view(initial_money, records)
    elif command == "delete":
        initial_money, records = delete(initial_money, records)
    elif command == "exit":
        save(initial_money, records)
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")
