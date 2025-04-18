

class Table:
    """
    Class representing a table in a database.
    """
    def __init__(self, name: str):
        self.name = name
        self.iceberg_db = None
        self.COLUMNS = []
        self.SQL = ""