from schema.Table import Table

class ItemReport(Table):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "date", "type": "DATE", "comment": "Date"},
            {"name": "item_nbr", "type": "INT", "comment": "Item Number"},
            {"name": "family", "type": "STRING", "comment": "Family"},
            {"name": "class", "type": "STRING", "comment": "Class"},
            {"name": "perishable", "type": "INT", "comment": "Perishable"},
            {"name": "city", "type": "STRING", "comment": "City"},
            {"name": "state", "type": "STRING", "comment": "State"},
            {"name": "unit_sales", "type": "INT", "comment": "Unit Sales"}
        ]
        self.SQL = "sql/business/load_agg_item_report.sql"

class StoreReport(Table):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "date", "type": "DATE", "comment": "Date"},
            {"name": "store_nbr", "type": "INT", "comment": "Store Number"},
            {"name": "city", "type": "STRING", "comment": "City"},
            {"name": "state", "type": "STRING", "comment": "State"},
            {"name": "store_type", "type": "STRING", "comment": "Store Type"},
            {"name": "store_cluster", "type": "STRING", "comment": "Store Cluster"},
            {"name": "total_sales", "type": "INT", "comment": "Total Sales"},
            {"name": "promotional_sales", "type": "INT", "comment": "Promotional Sales"},
            {"name": "regular_sales", "type": "INT", "comment": "Regular Sales"}
        ]
        self.SQL = "sql/business/load_agg_store_report.sql"

class ProductReport(Table):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_business"
        self.COLUMNS = [
            {"name": "date", "type": "DATE", "comment": "Date"},
            {"name": "item_nbr", "type": "INT", "comment": "Item Number"},
            {"name": "product_family", "type": "STRING", "comment": "Product Family"},
            {"name": "product_class", "type": "STRING", "comment": "Product Class"},
            {"name": "perishable", "type": "INT", "comment": "Perishable"},
            {"name": "total_sales", "type": "INT", "comment": "Total Sales"}
        ]
        self.SQL = "sql/business/load_agg_product_report.sql"

item_report = ItemReport("item_report")
store_report = StoreReport("store_report")
product_report = ProductReport("product_report")
ALL_TABLES = [
    # item_report,
    store_report, 
    product_report
]
