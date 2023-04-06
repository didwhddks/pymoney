import sys
import os

def add(money, records):
    # transform the input string into list of tuples
    new_records = input("""Add some expense or income records with description and amount:
desc1 amt1, desc2 amt2, desc3 amt3, ...\n""").split(", ")
    new_records = [tuple(record.split()) for record in new_records]

    # check if the input string conforms to the specified format
    for record in new_records:
        if len(record) != 2:
            sys.stderr.write("The format of the records should be like this: breakfast -50, lunch -100, ...\nFail to add the records.\n")
            return money, records

    # try to add new records into the original records and calculate the balance
    try:
        records += [(desc, int(amt)) for desc, amt in new_records]
        money += sum(int(amt) for desc, amt in new_records)
    except ValueError:
        sys.stderr.write("Invalid value for money.\nFail to add the records.\n")
    finally:
        return money, records

def view(money, records):
    # print the records
    print("\nHere's your expense and income records: ")
    print("%s%-20s %s\n%s%s %s" %(" "*2, "Description", "Amount", " "*2, "="*20, "="*20))
    for i, (desc, amt) in enumerate(records):
        print("%d %-20s %s" %(i+1, desc, amt))
    print("%s%s %s" %(" "*2, "="*20, "="*20))
    print("Now you have %d dollars." %money)

def delete(money, records):
    # first show the current records to the user
    view(money, records)

    # receive the input record number and try to delete the record and calculate the balance
    try:
        deleted = int(input("\nWhich record do you want to delete (Please enter the corresponding record number)? "))
        money -= records[deleted-1][1]
        del records[deleted-1]
    except ValueError:
        sys.stderr.write("Invalid format. Fail to delete a record.\n")
    except IndexError:
        sys.stderr.write("There's no record with the record number %d. Fail to delete a record.\n" %deleted)
    finally:
        return money, records

def initialize():
    try:
        # try to open records.txt
        fh = open("records.txt", "r")
    except FileNotFoundError:
        # try to receive the initial amount of money and initialize the record list if the file is not found.
        try: 
            records = []
            money = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
            money = 0
    else:
        # the file is successfully opened. try to read the contents inside
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
            # the contents inside are invalid. remove the file and initialize again
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
    # write the records into the file records.txt
    with open("records.txt", "w") as file:
        file.write("%s\n" %str(initial_money))
        records = [[record[0], str(record[1])] for record in records]
        records = [" ".join(record) for record in records]
        for record in records:
            file.write("%s\n" %record)
        

initial_money, records = initialize()   # initialize the amount of money and the record list

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
