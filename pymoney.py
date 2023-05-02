import sys
import os

class Record:
    """Represent a record"""
    def __init__(self, category, description, amount):
        self._category, self._description, self._amount = category, description, amount

    @property
    def category(self):
        """
        Get the value of the attribute self._category.

        Arguments:
        self._category -- category of the record

        Returns:
        self._category
        """

        return self._category
    @property
    def description(self):
        """
        Get the value of the attribute self._description.

        Arguments:
        self._description -- description of the record

        Returns:
        self._description
        """

        return self._description
    @property
    def amount(self):
        """
        Get the value of the attribute self._amount.

        Arguments:
        self._amount -- amount of the record

        Returns:
        self._amount
        """

        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self, categories):
        try:
            fh = open("records.txt", "r")
            self._initial_money = int(fh.readline())
            self._records = []
            for record in fh.readlines():
                record = record.split()
                if len(record) != 3 or categories.is_category_valid(record[0]) == False:
                    raise
                record = Record(record[0], record[1], int(record[2]))
                self._records.append(record)
        except FileNotFoundError:
            # try to receive the initial amount of money and initialize the record list if the file is not found.
            try: 
                self._records = []
                self._initial_money = int(input("How much money do you have? "))
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                self._initial_money = 0
        except:
            sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
            fh.close()
            os.remove("records.txt")
            try: 
                self._records = []
                self._initial_money = int(input("How much money do you have? "))
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                self._initial_money = 0
        else:
            print("Welcome back!")
            fh.close()
    
    def add(self, record, categories):
        """
        Add the input records from the user into current record list and calculate the balance.

        Arguments:
        record -- input records from the user
        categories -- predefined category
        self._records -- current record list
        self._initial_money -- current balance

        Returns:
        None
        """

        record = [r.split() for r in record.split(", ")]
        # check if the input string conforms to the specified format
        for r in record:
            if len(r) != 3:
                sys.stderr.write("The format of the records should be like this: meal breakfast -50, income lottery 100, ...\nFail to add the records.\n")
                return
            if categories.is_category_valid(r[0]) == False:
                sys.stderr.write("Some of the specified categories are not in the category list.\nYou can check the category list by command \"view categories\".\nFail to add the records.\n")
                return
        # try to add new records into the original records and calculate the balance
        try:
            record = [Record(r[0], r[1], int(r[2])) for r in record]
            self._records += record
            self._initial_money += sum([r.amount for r in record])
        except ValueError:
            sys.stderr.write("Invalid value for money.\nFail to add the records.\n")

    def view(self):
        """
        Show the balance and all of the records in the record list with their categories,
        descriptions and amounts.

        Arguments:
        self._records -- current record list
        self._initial_money -- current balance

        Returns:
        None
        """

        # print the records
        print("\nHere's your expense and income records: ")
        print("%3s %-15s %-20s %s" %("", "Category", "Description", "Amount"))
        print("%3s %s %s %s" %("", "="*15, "="*20, "="*10))
        for idx, record in enumerate(self._records):
            print("%3d %-15s %-20s %s" %(idx+1, record.category, record.description, record.amount))
        print("%3s %s %s %s" %("", "="*15, "="*20, "="*10))
        print("%3s Now you have %d dollars." %("", self._initial_money))

    def delete(self, delete_record):
        """
        Delete the specified record from the record list and recalculate the balance.

        Arguments:
        delete_record -- record number of the deleted record
        self._records -- current record list
        self._initial_money -- current balance

        Returns:
        None
        """

        try:
            delete_record = int(delete_record)
            self._initial_money -= self._records[delete_record-1].amount
            del self._records[delete_record-1]
        except ValueError:
            sys.stderr.write("Invalid format. Fail to delete a record.\n")
        except IndexError:
            sys.stderr.write("There's no record with the record number %d. Fail to delete a record.\n" %delete_record)

    def find(self, category, target_categories):
        filter_records = list(filter(lambda record: record.category in target_categories, self._records))
        total = sum([record.amount for record in filter_records])
        print("\nHere's your expense and income records under category \"%s\": " %category)
        print("%3s %-15s %-20s %s" %("", "Category", "Description", "Amount"))
        print("%3s %s %s %s" %("", "="*15, "="*20, "="*10))
        for idx, record in enumerate(filter_records):
            print("%3d %-15s %-20s %s" %(idx+1, record.category, record.description, record.amount))
        print("%3s %s %s %s" %("", "="*15, "="*20, "="*10))
        print("%3s The total amount above is %d." %("", total))

    def save(self):
        # write the records into the file records.txt
        with open("records.txt", "w") as fh:
            fh.write("%s\n" %str(self._initial_money))
            save_records = [[record.category, record.description, str(record.amount)] for record in self._records]
            save_records = [" ".join(record)+"\n" for record in save_records]
            fh.writelines(save_records)


class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

    def view(self):
        def recursive_view(categories, level=0):
            if type(categories) == list:
                for subcategory in categories:
                    recursive_view(subcategory, level+1)
            else:
                print("%s- %s" %(" "*4*(level-1), categories))

        recursive_view(self._categories)

    def is_category_valid(self, category):
        def recursive_check(category, categories):
            if type(categories) == list:
                for subcategory in categories:
                    if recursive_check(category, subcategory):
                        return True
                return False
            else:
                return category == categories

        return recursive_check(category, self._categories)

    def find_subcategories(self, category):
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for idx, subcategory in enumerate(categories):
                    yield from find_subcategories_gen(category, subcategory, found)

                    if subcategory == category and idx+1 < len(categories) and type(categories[idx+1]) == list:
                        yield from find_subcategories_gen(category, categories[idx+1], True)
            else:
                if category == categories or found == True:
                    yield categories

        return [i for i in find_subcategories_gen(category, self._categories)]



categories = Categories()
records = Records(categories)

while True:
    command = input("""\nWhat do you want to do (add / view / delete / view categories / find / 
exit)? """)
    if command == "add":
        record = input("Add some expense or income records with category, description and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n")
        records.add(record, categories)
    elif command == "view":
        records.view()
    elif command == "delete":
        records.view()
        delete_record = input("\nWhich record do you want to delete (Please enter the corresponding record number)? ")
        records.delete(delete_record)
    elif command == "view categories":
        categories.view()
    elif command == "find":
        category = input("Which category do you want to find? ")
        target_categories = categories.find_subcategories(category)
        records.find(category, target_categories)
    elif command == "exit":
        records.save()
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")
