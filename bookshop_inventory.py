import sqlite3

#=== Create or open database ===#
# Create a file with SQLite3
try:
    db = sqlite3.connect('ebookstore')
except Exception as e:
    print("Error - could not connect to database")
    print(e)
    exit()

try:
    # Create a table
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ebookstore (
        id INTEGER PRIMARY KEY NOT NULL,
        title TEXT,
        author TEXT,
        qty, INTEGER )
    ''')
    db.commit()

# Populate table with initial values
    books_ = [
        (3001, "A Tale of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
        (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
        (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
        (3005, "Alice in Wonderland", "Lewis Carroll", 12)
    ]

    cursor.executemany('''INSERT OR IGNORE INTO ebookstore(id, title, author, qty)
                        VALUES(?, ?, ?, ?)''', books_)
    db.commit()

except Exception as e:
    print(e)
    db.close()
    exit()

#=== Define Functions ===#
# Function to print error and retry if user input is not an integer
def check_int(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to create a list of ID numbers in database
def list_ids():
    cursor.execute('''SELECT id FROM ebookstore''')
    # Add id numbers to list
    id_list = []
    for row in cursor:
        id_list.append(row[0])
    return id_list

# Function to ask user if they want to try again if they enter an invalid book ID
def check_id(in_list):
    while True:
        # User enters book ID
        id_num = check_int("ID Number: ") # User input must be able to be cast to integer

        # Check that ID number is unique
        id_list = list_ids()

        # If ID is in list of IDs ask if user wants to try again
        if id_num in id_list:
            exists = "already exists"
        else:
            exists = "does not exist"

        # If function requires the ID to exist when it does not, or if it requires ID to not exist when it does
        if in_list != exists:
            # User chooses whether to try again or return to main menu
            choose = check_int(f"\nID number {exists}. Would you like to try again?\n"
                               "1. Yes\n"
                               "2. No\n"
                               "Enter selection number: ") # User input must be able to be cast to integer

            # If user chooses to try again, ask for ID number
            if choose == 1:
                print("")

            # If user chooses not to try again, exit
            elif choose == 2:
                break

            # If user enters an invalid number, ask them to try again
            else:
                print("Invalid selection. Please try again.")

        # If the ID number existence matches what is required, return to main function
        else:
            break

    return id_num

# Function to insert data into table
def add_book():
    # Ask user for ID number and check if it is unique
    in_list = "does not exist" # Unique ID is required
    id_num = check_id(in_list)
    id_list = list_ids()

    # If the ID number does not exist, user enters book title, author and quantity
    if id_num not in id_list:
        book_title = input("Enter book title: ")
        book_author = input("Enter book author: ")
        quantity = check_int("Enter number of copies: ") # User input must be able to be cast to integer

        # Insert book information into database
        try:
            cursor.execute('''INSERT INTO ebookstore (id, title, author, qty)
                           VALUES(?, ?, ?, ?)''', (id_num, book_title, book_author, quantity))
            db.commit()
            print("Book added\n")

        except Exception as e:
            print(e)

    # Go back to main menu if user entered an existing ID number and chose not to try again
    else:
        print("")

# Function to display a specific book by ID number
def search_book_id(id_num):
    try:
        # Select the row with the corresponding ID number to user's entry
        cursor.execute('''SELECT id, title, author, qty FROM ebookstore WHERE id=?''', (id_num,))
        book = cursor.fetchone()
        print(f"\n| ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Quantity: {book[3]} |\n")
    except Exception as e:
        print(e)

# Function to update book information
def update_book():
    # Ask user for ID number and check if it is unique
    in_list = "already exists"  # Existing ID is required
    print("Enter the ID number of the book you want to update below")
    id_num = check_id(in_list)
    id_list = list_ids()

    # If ID number exists, search and update book
    if id_num in id_list:
        # Display the selected book to the user
        search_book_id(id_num)

        # User chooses what to update
        selection = ""
        while selection != 0:
            selection = check_int("What would you like to update?\n"
                                  "1. Title\n"
                                  "2. Author\n"
                                  "3. Quantity\n"
                                  "0. Exit\n"
                                  "Enter option number: ") # User input must be able to be cast to integer
            print("")

            try:
                # Update title
                if selection == 1:
                    # User enters new book title
                    new_title = input("Enter new book title: ")
                    # Update row value
                    cursor.execute('''UPDATE ebookstore SET title=? WHERE id=?''', (new_title, id_num))
                    db.commit()
                    print("Book updated\nYou can choose to update another detail or return to the main menu\n")

                # Update author
                elif selection == 2:
                    # User enters new author
                    new_author = input("Enter new author name: ")
                    # Update row value
                    cursor.execute('''UPDATE ebookstore SET author=? WHERE id=?''', (new_author, id_num))
                    db.commit()
                    print("Book updated\nYou can choose to update another detail or return to the main menu\n")

                # Update Quantity
                elif selection == 3:
                    # User enters new quantity
                    new_quantity = check_int("Enter new book quantity: ")
                    # Update row value
                    cursor.execute('''UPDATE ebookstore SET qty=? WHERE id=?''', (new_quantity, id_num))
                    db.commit()
                    print("Book updated\nYou can choose to update another detail or return to the main menu\n")

                # Exit
                elif selection == 0:
                    pass

                # Error message if user enters a number other than the available options
                else:
                    print("Invalid selection. Please try again.\n")

            except Exception as e:
                print(e)

    # Go back to main menu if user entered a non-existent ID number and chose not to try again
    else:
        print("")

# Function to delete book from database
def delete_book():
    # Ask user for ID number and check if it is unique
    in_list = "already exists"  # Existing ID is required
    print("Enter the ID number of the book you want to delete below")
    id_num = check_id(in_list)
    id_list = list_ids()

    # If ID number exists, ask if user wants to continue and delete book
    if id_num in id_list:
        # Display selected book to user
        search_book_id(id_num)

        # Ask user if they want to delete the book
        print("Are you sure you want to delete this book?\n"
                               "1. Yes\n"
                               "2. No\n")

        while True:
            # User confirms that they want to delete the book
            choose = check_int("Enter option number: ")  # User input must be able to be cast to integer

            # Delete book
            if choose == 1:
                try:
                    cursor.execute('''DELETE FROM ebookstore WHERE id=?''', (id_num,))
                    db.commit()
                    print("Book deleted\n")
                except Exception as e:
                    print(e)
                break

            # Go back to main menu
            elif choose == 2:
                print("")
                break

            # Error message if user enters a number other than the available options
            else:
                print("Invalid selection. Please try again.")

    # Go back to main menu if user entered a non-existent ID number and chose not to try again
    else:
        print("")

# Function to search for a book by user input ID number
def user_search():
    # Ask user for ID number and check if it is unique
    in_list = "already exists"  # Existing ID is required
    print("Enter the ID number of the book you want to search below")
    id_num = check_id(in_list)
    id_list = list_ids()

    # Display book information
    if id_num in id_list:
        search_book_id(id_num)

    # Go back to main menu if user enters a non-existent ID and does not want to try again
    else:
        print("")

#=== Menu ===#
menu = ""

while menu != 0:
    menu = check_int("What would you like to do?\n"
                     "1. Enter book\n"
                     "2. Update book\n"
                     "3. Delete book\n"
                     "4. Search books\n"
                     "0. Exit\n"
                     "Enter option number here: ")
    print("")

    # Enter book
    if menu == 1:
        add_book()

    # Update book
    elif menu == 2:
        update_book()

    # Delete book
    elif menu == 3:
        delete_book()

    # Search books
    elif menu == 4:
        user_search()

    # Exit
    elif menu == 0:
        db.close()
        print("Goodbye")

    # Error message if user enters a number other than the available options
    else:
        print("Invalid menu selection. Please try again.\n")
