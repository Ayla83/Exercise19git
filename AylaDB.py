from sqlalchemy import create_engine
from sqlalchemy import text

whichuser = input("Please enter your user type: Staff/Council/Library_Member ")

engine = create_engine(f"mysql+pymysql://{whichuser}:password@localhost/group_d_library", echo=False, future=True)

# user can choose genre
genreword = input("What genre would you like? Choose from \n"
  "travel, romance, adventure, historical fiction, crime, cookery")
genrenumber = int
if genreword == "travel":
    genrenumber = 3
elif genreword == "romance":
    genrenumber = 4
elif genreword == "adventure":
    genrenumber = 8
elif genreword == "historical fiction":
    genrenumber = 10
elif genreword == "crime":
    genrenumber = 11
elif genreword == "cookery":
    genrenumber = 12

print(f"Books for genre {genreword} are: ")
with engine.connect() as conn:
    result = conn.execute(
        text("select book_title from books where genre = :param"),
        {"param": genrenumber}
    )
    for row in result:
        print(f"book_title: {row.book_title}")
    print("--------------------------")

# hip happening member to see latest releases
print("To filter books by release date: ")
start_date = input("Enter start date in the form YYYY-MM-DD: ")
end_date = input("Enter end date in the form YYYY-MM-DD: ")
with engine.connect() as conn:
    result = conn.execute(
        text("select book_title, author, release_date from books where release_date between :start and :end order by release_date desc"),
        {"start": start_date, "end": end_date})
    for row in result:
        print(f"{row.book_title} {row.author} {row.release_date}")
    print("--------------------------")

# tech enthusiast to borrow electronic books
booktype = input("Would you like to see paper or electronic books? ")
with engine.connect() as conn:
    result = conn.execute(
        text(f"select book_title, author, release_date from books where class = '{booktype}'"))
    print(f"{booktype} books: ")
    for row in result:
        print(f"{row.book_title} {row.author} {row.release_date}")
    print("--------------------------")

# local council to find out who is using the library
if whichuser == "Staff" or whichuser == "Council":
    print("To see members filtered by date of birth: ")
    start_date = input("Enter start date in the form YYYY-MM-DD: ")
    end_date = input("Enter end date in the form YYYY-MM-DD: ")
    with engine.connect() as conn:
        result = conn.execute(
            text('select * from personal_details where dob between :start and :end order by dob'),
            {"start": start_date, "end": end_date})
        for row in result:
            print(f"{row.dob} {row.user_cat} {row.gender}")
        print("--------------------------")

if whichuser == "Staff":
    # librarian to see who has overdue books
    print("Library members with overdue books are: ")
    with engine.connect() as conn:
        result = conn.execute(
            text('select first_name, last_name, return_date from library_members inner join loans on library_members.id= loans.person_id where loan_status = "not-returned" order by return_date'))
        for row in result:
            print(f"{row.first_name} {row.last_name} {row.return_date}")
        print("--------------------------")

    # new user to library
    print("Entering a new library member's details: ")
    userfirstname = input("Enter library member's first name: ")
    userlastname = input("Enter library member's last name: ")
    useraddress = int(input("Enter library member's address code: "))  # foreign keys - need to be created already
    userpersdet = int(input("Enter library member's personal details code: "))
    with engine.connect() as conn:
        conn.execute(
            text('insert into library_members (first_name, last_name, address, personal_details) values (:x, :y, :z, :p)'),
            {"x": userfirstname, "y": userlastname, "z": useraddress, "p": userpersdet})
        conn.commit()  # use this to make changes to the sql table
        print("--------------------------")
