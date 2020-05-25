from . import memory_store

DB_TYPE_DEBUG = 1
DB_TYPE_TEST = 2
DB_TYPE_PROD = 3

_db_type = DB_TYPE_PROD


def get_debug():
    return memory_store.get()


def get_test():
    return memory_store.get()


def get_production():
    return memory_store.get_prod()


def release_debug():
    return memory_store.release()


def release_test():
    return memory_store.release()


def release_production():
    return memory_store.release()


def get():
    if _db_type == DB_TYPE_PROD:
        return get_production()
    if _db_type == DB_TYPE_DEBUG:
        return get_debug()
    if _db_type == DB_TYPE_TEST:
        return get_test()


def release():
    if _db_type == DB_TYPE_PROD:
        release_production()
    elif _db_type == DB_TYPE_DEBUG:
        release_debug()
    elif _db_type == DB_TYPE_TEST:
        release_test()


def set_type(db_type):
    global _db_type
    release()
    _db_type = db_type
