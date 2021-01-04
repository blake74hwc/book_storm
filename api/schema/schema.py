from . import ma


class BookStoreSchema(ma.Schema):
    store_name = ma.Str(required=True, data_key='storeName')
    opening_hours = ma.Str(required=True, data_key='openingHours')
    cash_balance = ma.Float(required=True, data_key='cashBalance')


class BooksSchema(ma.Schema):
    book_name = ma.Str(required=True, data_key='bookName')
    store_name = ma.Str(required=True, data_key='storeName')
    price = ma.Float(required=True, data_key='price')


class OpeningHoursSchema(ma.Schema):
    week_day = ma.Integer(required=True, data_key='weekDay')
    start_time = ma.Time(required=True, data_key='startTime')
    end_time = ma.Time(required=True, data_key='endTime')
