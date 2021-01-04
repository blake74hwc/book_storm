from flask import Response, request
from flask_restful import Resource
from datetime import datetime, timedelta
from database.models import BookStore, OpeningHours
from api.schema.schema import BookStoreSchema, OpeningHoursSchema
from database import db


class BookStoreOpenApi(Resource):
    # def post(self):
    #     db.drop_all()
    #     db.create_all()
    #     return 'init success!', 200

    def get(self):
        dt = request.args.get('dt')
        weekDay = request.args.get('weekDay')
        time = request.args.get('time')

        if dt and weekDay and time:
            return {
                'message': 'Bad Request'
            }, 400
        if bool(weekDay) != bool(time):
            return {
                'message': 'Bad Request'
            }, 400

        week_day = None
        opTime = None
        if dt:
            dt = datetime.strptime(dt, '%Y-%m-%d %H:%M')
            week_day = dt.weekday()
            opTime = dt.time()
        if weekDay and time:
            week_day = weekDay
            opTime = time

        query = OpeningHours.query.filter_by(
            week_day=week_day).filter(OpeningHours.start_time <= opTime, OpeningHours.end_time >= opTime)
        qb = []
        for q in query:
            qb.append(q.book_store)
            pass
        book_stores_schema = BookStoreSchema(many=True)
        bookStoreList = book_stores_schema.dump(qb)

        return {'data': bookStoreList}, 200


class BookStoreOpenHoursApi(Resource):
    def get(self):
        more = request.args.get('more')
        less = request.args.get('less')
        ohList = OpeningHours.query.all()
        for oh in ohList:
            openingHoursSchema = OpeningHoursSchema()
            oh = openingHoursSchema.dump(oh)
            sHour, sMin, *_ = oh.get('startTime').split(':')
            eHour, eMin, *_ = oh.get('endTime').split(':')
            startTime = timedelta(hours=int(sHour), minutes=int(sMin))
            endTime = timedelta(hours=int(eHour), minutes=int(eMin))
            time = endTime - startTime
            hours = time.seconds / 3600
            print('sTime ='+str(startTime), 'eTime=' +
                  str(endTime), 'time='+str(time),hours)
        return {'data': ohList}, 200
