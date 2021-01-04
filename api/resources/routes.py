from .bookStore import BookStoreOpenApi, BookStoreOpenHoursApi


def initialize_routes(api):
    api.add_resource(BookStoreOpenApi, '/bookStore/open')
    api.add_resource(BookStoreOpenHoursApi, '/bookStore/openHours')
