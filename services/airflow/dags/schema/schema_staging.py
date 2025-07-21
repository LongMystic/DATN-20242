from schema.Table import Table

class Category(Table):
    """
    Class representing the category table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "INT", "comment": "ID"},
            {"name": "category_id", "type": "INT", "comment": "Category ID"},
            {"name": "category_name", "type": "STRING", "comment": "Category Name"},
            {"name": "level", "type": "INT", "comment": "Category Name"},
            {"name": "parent_category", "type": "STRING", "comment": "Category Name"},
            {"name": "parent_id", "type": "INT", "comment": "Category Name"},
            {"name": "industry_id", "type": "INT", "comment": "Category Name"},
            {"name": "is_selected", "type": "INT", "comment": "Category Name"}
        ]
        self.SQL = "sql/staging/transform_category.sql"


class HolidaysEvents(Table):
    """
    Class representing the holidays_events table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "INT", "comment": ""},
            {"name": "date", "type": "TIMESTAMP", "comment": ""},
            {"name": "type", "type": "STRING", "comment": ""},
            {"name": "locale", "type": "STRING", "comment": ""},
            {"name": "locale_name", "type": "STRING", "comment": ""},
            {"name": "description", "type": "STRING", "comment": ""},
            {"name": "transferred", "type": "BOOLEAN", "comment": ""}
        ]
        self.SQL = "sql/staging/transform_holidays_events.sql"


class Items(Table):
    """
    Class representing the items table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "INT", "comment": ""},
            {"name": "item_nbr", "type": "INT", "comment": ""},
            {"name": "family", "type": "STRING", "comment": ""},
            {"name": "class", "type": "INT", "comment": ""},
            {"name": "perishable", "type": "INT", "comment": ""}
        ]
        self.SQL = "sql/staging/transform_items.sql"


class Oil(Table):
    """
    Class representing the oil table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "INT", "comment": ""},
            {"name": "date", "type": "TIMESTAMP", "comment": ""},
            {"name": "dcoilwtico", "type": "DOUBLE", "comment": ""}
        ]
        self.SQL = "sql/staging/transform_oil.sql"


class Stores(Table):
    """
    Class representing the stores table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "INT", "comment": ""},
            {"name": "store_nbr", "type": "INT", "comment": ""},
            {"name": "city", "type": "STRING", "comment": ""},
            {"name": "state", "type": "STRING", "comment": ""},
            {"name": "type", "type": "STRING", "comment": ""},
            {"name": "cluster", "type": "INT", "comment": ""}
        ]
        self.SQL = "sql/staging/transform_stores.sql"


class Transactions(Table):
    """
    Class representing the transactions table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "INT", "comment": ""},
            {"name": "store_nbr", "type": "INT", "comment": ""},
            {"name": "date", "type": "TIMESTAMP", "comment": ""},
            {"name": "transactions", "type": "INT", "comment": ""}
        ]
        self.SQL = "sql/staging/transform_transactions.sql"


class Sales(Table):
    """
    Class representing the sales table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "BIGINT", "comment": ""},
            {"name": "date", "type": "TIMESTAMP", "comment": ""},
            {"name": "store_nbr", "type": "INT", "comment": ""},
            {"name": "item_nbr", "type": "INT", "comment": ""},
            {"name": "unit_sales", "type": "DOUBLE", "comment": ""},
            {"name": "onpromotion", "type": "INT", "comment": ""}
        ]
        self.SQL = "sql/staging/transform_sales.sql"


class SalesLimit(Table):
    """
    Class representing the sales table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "id", "type": "BIGINT", "comment": ""},
            {"name": "date", "type": "TIMESTAMP", "comment": ""},
            {"name": "store_nbr", "type": "INT", "comment": ""},
            {"name": "item_nbr", "type": "INT", "comment": ""},
            {"name": "unit_sales", "type": "DOUBLE", "comment": ""},
            {"name": "onpromotion", "type": "INT", "comment": ""}
        ]
        self.SQL = "sql/staging/transform_sales_limit.sql"

# Instantiate staging table classes
category_dim = Category('category_dim')
holidays_events_dim = HolidaysEvents('holidays_events_dim')
items_dim = Items('items_dim')
oil_fact = Oil('oil_fact')
stores_dim = Stores('stores_dim')
transactions_fact = Transactions('transactions_fact')
sales_fact = Sales('sales_fact')
sales_limit_fact = SalesLimit('sales_limit_fact')

ALL_TABLES = [
    # category_dim,
    holidays_events_dim,
    items_dim,
    oil_fact,
    stores_dim,
    transactions_fact,
    sales_fact,
    # sales_limit_fact
]
