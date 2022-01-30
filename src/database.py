from collections import defaultdict


class Database:
    instance = None

    def __init__(self):
        if not Database.instance:
            Database.instance = self
        else:
            raise Exception("Database already created")
        self.db = defaultdict(list)

    def add_email(self, email_to, content):
        self.db[email_to].insert(0, content)
        while len(self.db[email_to]) > 10:
            del self.db[email_to][10]

    def get_email(self, email_to):
        return self.db[email_to]


Database()
