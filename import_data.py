import sys
import os
import getopt
import types
import json
import calendar
import datetime
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from database.models import BookStore, Books, OpeningHours

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_NAME')
)

db = SQLAlchemy(app)


def help():
    print("""
        Usage : python import_data.py [OPTIONS] FILE_PATH
        Options:
        -b, --book_store    import book_store_data
        -u, --user          import user_data
        """)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hb:u:", ["book_store=", "user="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-b", "--book_store"):
            readInsertBookStore(arg)
        elif opt in ("-u", "--user"):
            readInsertBookStore(arg)


wdn = dict(zip(calendar.day_abbr, range(7)))


def getWeekNum(d):
    d = d[:3]
    n = wdn.get(d)
    return n


def parseTime(h, m=0, p=''):
    h = int(h)
    m = int(m)
    timestr = '{:d}:{:02d}'.format(h, m)+p
    return datetime.datetime.strptime(timestr, "%I:%M%p").time()


def resolveOpHours(opHours):
    opHours = opHours.strip()
    opHoursArr = opHours.split()
    days = opHoursArr[:len(opHoursArr)-5]
    hours = ' '.join(opHoursArr[len(opHoursArr)-5:]).strip()
    dayList = []
    if len(days) > 1:
        days = ''.join(days).split(',')
        for d in days:
            if '-' in d:
                start, end = d.split('-')
                start = getWeekNum(start)
                end = getWeekNum(end)
                for i in range(start, end+1):
                    dayList.append(i)
                    pass
            else:
                n = getWeekNum(d)
                dayList.append(n)
            pass
    else:
        days = ''.join(days)
        n = getWeekNum(days)
        dayList.append(n)
    startTime, endTime = hours.split('-')
    sTime, sP = startTime.split()
    eTime, eP = endTime.split()
    sh, *sm = sTime.split(':')
    if not sm:
        sm = 0
    else:
        sm = sm[0]
    eh, *em = eTime.split(':')
    if not em:
        em = 0
    else:
        em = em[0]
    startTime = parseTime(sh, sm, sP)
    endTime = parseTime(eh, em, eP)

    return dayList, startTime, endTime


def readInsertBookStore(p):
    fileHandle = open(p, encoding='utf-8')
    jsonStr = fileHandle.read()
    fileHandle.close()
    bookStoreDict = json.loads(jsonStr)
    try:
        for store in bookStoreDict:
            storeName = store.get('storeName')
            cashBalance = store.get('cashBalance')
            openingHours = store.get('openingHours')
            books = store.get('books')

            bookStore = BookStore(store_name=storeName,
                                  cash_balance=cashBalance)
            db.session.add(bookStore)
            db.session.flush()
            storeId = bookStore.store_id

            for opHours in openingHours.split('/'):
                dayList, startTime, endTime = resolveOpHours(opHours)
                for week_day in dayList:
                    opHoursModel = OpeningHours(
                        store_id=storeId, week_day=week_day, start_time=startTime, end_time=endTime)
                db.session.add(opHoursModel)

            for b in books:
                bookName = b.get('bookName')
                price = b.get('price')
                book = Books(book_name=bookName, price=price, store_id=storeId)
                db.session.add(book)
                pass

            pass
    except:
        db.session.rollback()
    else:
        db.session.commit()
        pass


def readInsertUser(p):
    fileHandle = open(p, encoding='utf-8')
    print(fileHandle.read())
    fileHandle.close()


if __name__ == "__main__":
    main(sys.argv[1:])
