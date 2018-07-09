class User(object):

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        print(f"{self.name}'s email address has been changed from {self.email} to {address}.")
        self.email = address

    def __repr__(self):
        num_books = str(len(self.books))
        return f'''User: {self.name}, email: {self.email}, books read: {num_books}'''

    def __eq__(self, other_user):
        return (self.name == other_user.name and self.email == other_user.email)

    def read_book(self,book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        total = 0
        num = 0
        for book in self.books:
            if self.books[book] is not None:
                num += 1
                total += self.books[book]
        if num > 0:
            return total/num
        else:
            return "No ratings"

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __repr__(self):
        return f'''{self.title}; ISBN: {self.isbn}'''

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        print(f'''{self.title}'s ISBN has been changed from {self.isbn} to {new_isbn}.''')
        self.isbn = new_isbn

    def add_rating(self, rating):
        if rating is not None and rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            return '''Invalid Rating.'''

    def get_average_rating(self):
        total = 0
        if(len(self.ratings) > 0):
            total = 0
            for rating in self.ratings:
                total += rating
            return total / len(self.ratings)
        else:
            return "No Ratings"


    def __eq__(self,other_book):
        return (self.title == other_book.title and self.isbn == other_book.isbn)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return f'''{self.title} by {self.author}'''

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return f'''{self.title}, a {self.level} manual on {self.subject}'''

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return f'''
        This TomeRater has {len(self.users)} users, 
        who have read a total of {len(self.books)} books.
        '''

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating = None):
        if self.isbn_is_unique(book):
            if self.users.get(email) is None:
                print(f'''No user with email {email}''')
            else:
                self.users[email].read_book(book, rating)
                book.add_rating(rating)
                if book not in self.books:
                    self.books[book] = 1
                else:
                    self.books[book] += 1
        else:
            print(f'''
                >>>>>OOPS!
                Tried to add {book} but
                ISBN {book.get_isbn()} has already been assigned.
              ''')

    def isbn_is_unique(self, b):
        unique = True
        for book in self.books:
            if book.get_title() != b.get_title() and book.get_isbn() == b.get_isbn():
                unique = False
                break
        return unique

    def add_user(self, name, email, books = None):
        #note: this didn't work with the populate file, specfically this line:
        #
        #Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])
        #
        #But it worked when I broke that line into 2 lines, like this:
        #
        #user_books = [book1, novel1, nonfiction1]
        #Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books)

        if self.checkEmailAddress(email):
            if email in self.users:
                print(f'''
                >>>>>OOPS!
                {self.users[email]} already exists.
                Maybe you want to use:
                add_books_to_user()''')
            else:
                self.users[email] = User(name, email)
                if books is not None:
                    for book in books:
                        self.add_book_to_user(book, email)
        else:
            print(f'''
                >>>>>OOPS!  User not added!
                {email} is an invalid email address.''')

    def checkEmailAddress(self, email):
        ending = email[-4:]
        return (".edu" in ending) or (".org" in ending) or (".com" in ending)

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users:
            print(user)

    def get_most_read_book(self):
        max = 0
        most_read = ""
        for book in self.books:
            if self.books[book] > max:
                most_read = book.title
                max = self.books[book]
        return most_read

    def highest_rated_book(self):
        book_rating = 0
        for book in self.books:
            r = book.get_average_rating()
            if r > book_rating:
                book_rating = r
                best = book
        return best

    def most_positive_user(self):
        user_rating = 0
        for user in self.users:
            this_user = self.users[user]
            r = this_user.get_average_rating()
            if r > user_rating:
                user_rating = r
                pos = this_user
        return pos