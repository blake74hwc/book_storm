from . import db


########################################
class BookStore(db.Model):
    __tablename__ = 'book_store'
    store_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(100), unique=True, nullable=False)
    cash_balance = db.Column(db.Numeric(10, 2))

    db_book_store_books = db.relationship('Books', backref='book_store')
    db_book_store_opening_hours = db.relationship(
        'OpeningHours', backref='book_store')


def __init__(self, store_name,  cash_balance):
    self.store_name = store_name
    self.cash_balance = cash_balance

########################################


class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Numeric(5, 2))

    store_id = db.Column(
        db.Integer, db.ForeignKey('book_store.store_id'), nullable=False)


def __init__(self, book_name,  price, store_id):
    self.book_name = book_name
    self.price = price
    self.store_id = store_id


class OpeningHours(db.Model):
    __tablename__ = 'opening_hours'
    store_id = db.Column(
        db.Integer, db.ForeignKey('book_store.store_id'), primary_key=True)
    week_day = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)


def __init__(self, store_id, week_day, start_time, end_time):
    self.store_id = store_id
    self.week_day = week_day
    self.start_time = start_time
    self.end_time = end_time
