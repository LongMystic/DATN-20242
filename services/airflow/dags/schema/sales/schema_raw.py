from schema.Table import Table

class Category(Table):
    """
    Class representing the category table in the sales schema.
    """
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = table_name
        self.iceberg_db = "sales_staging"
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
        self.SQL = "/sql/raw/extract_category.sql"
        

category = Category('category')
ALL_TABLES = [
    category
]