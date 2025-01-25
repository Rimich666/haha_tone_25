from repository import base, YdbBase


def exec_file(fn):
    base.check_IAM()
    with open(fn, 'r') as f:
        query = f.read()
    base.pool.execute_with_retries(query)


def create_tables():
    base.check_IAM()
    base.exec_file(YdbBase.create)


def drop_tables():
    base.check_IAM()
    base.exec_file(YdbBase.drop)


def clear_tables():
    base.check_IAM()
    base.exec_file(YdbBase.clear)


def insert_color(values):
    base.check_IAM()
    return base.session.transaction().execute(
        f"REPLACE INTO colors (name, hex) "
        f"VALUES {values};"
    )
