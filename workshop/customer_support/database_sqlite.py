from typing import List, Dict
import sqlite3

class SQLiteDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('customer_support.db')
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.insert_initial_data()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT,
                username TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                customer_id TEXT,
                product TEXT,
                quantity INTEGER,
                price REAL,
                status TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        self.connection.commit()

    def insert_initial_data(self):
        customers = [
            {"id": "1213210", "name": "John Doe", "email": "john@gmail.com", "phone": "123-456-7890", "username": "johndoe"},
            {"id": "2837622", "name": "Priya Patel", "email": "priya@candy.com", "phone": "987-654-3210", "username": "priya123"},
            {"id": "3924156", "name": "Liam Nguyen", "email": "lnguyen@yahoo.com", "phone": "555-123-4567", "username": "liamn"},
            {"id": "4782901", "name": "Aaliyah Davis", "email": "aaliyahd@hotmail.com", "phone": "111-222-3333", "username": "adavis"},
            {"id": "5190753", "name": "Hiroshi Nakamura", "email": "hiroshi@gmail.com", "phone": "444-555-6666", "username": "hiroshin"},
            {"id": "6824095", "name": "Fatima Ahmed", "email": "fatimaa@outlook.com", "phone": "777-888-9999", "username": "fatimaahmed"},
            {"id": "7135680", "name": "Alejandro Rodriguez", "email": "arodriguez@protonmail.com", "phone": "222-333-4444", "username": "alexr"},
            {"id": "8259147", "name": "Megan Anderson", "email": "megana@gmail.com", "phone": "666-777-8888", "username": "manderson"},
            {"id": "9603481", "name": "Kwame Osei", "email": "kwameo@yahoo.com", "phone": "999-000-1111", "username": "kwameo"},
            {"id": "1057426", "name": "Mei Lin", "email": "meilin@gmail.com", "phone": "333-444-5555", "username": "mlin"}
        ]

        orders = [
            {"id": "24601", "customer_id": "1213210", "product": "Wireless Headphones", "quantity": 1, "price": 79.99, "status": "Shipped"},
            {"id": "13579", "customer_id": "1213210", "product": "Smartphone Case", "quantity": 2, "price": 19.99, "status": "Processing"},
            {"id": "97531", "customer_id": "2837622", "product": "Bluetooth Speaker", "quantity": 1, "price": "49.99", "status": "Shipped"}, 
            {"id": "86420", "customer_id": "3924156", "product": "Fitness Tracker", "quantity": 1, "price": 129.99, "status": "Delivered"},
            {"id": "54321", "customer_id": "4782901", "product": "Laptop Sleeve", "quantity": 3, "price": 24.99, "status": "Shipped"},
            {"id": "19283", "customer_id": "5190753", "product": "Wireless Mouse", "quantity": 1, "price": 34.99, "status": "Processing"},
            {"id": "74651", "customer_id": "6824095", "product": "Gaming Keyboard", "quantity": 1, "price": 89.99, "status": "Delivered"},
            {"id": "30298", "customer_id": "7135680", "product": "Portable Charger", "quantity": 2, "price": 29.99, "status": "Shipped"},
            {"id": "47652", "customer_id": "8259147", "product": "Smartwatch", "quantity": 1, "price": 199.99, "status": "Processing"},
            {"id": "61984", "customer_id": "9603481", "product": "Noise-Cancelling Headphones", "quantity": 1, "price": 149.99, "status": "Shipped"},
            {"id": "58243", "customer_id": "1057426", "product": "Wireless Earbuds", "quantity": 2, "price": 99.99, "status": "Delivered"},
            {"id": "90357", "customer_id": "1213210", "product": "Smartphone Case", "quantity": 1, "price": 19.99, "status": "Shipped"},
            {"id": "28164", "customer_id": "2837622", "product": "Wireless Headphones", "quantity": 2, "price": 79.99, "status": "Processing"}
        ]
        self.cursor.executemany('''
            INSERT OR IGNORE INTO customers (id, name, email, phone, username)
            VALUES (:id, :name, :email, :phone, :username)
        ''', customers)
        self.cursor.executemany('''
            INSERT OR IGNORE INTO orders (id, customer_id, product, quantity, price, status)
            VALUES (:id, :customer_id, :product, :quantity, :price, :status)
        ''', orders)
        self.connection.commit()

    def get_customer(self, key:str, value:str) -> Dict[str, str]:
        if key in {"email", "phone", "username"}:
            self.cursor.execute(f'SELECT * FROM customers WHERE {key} = ?', (value,))
            customer = self.cursor.fetchone()
            if customer:
                return {
                    "id": customer[0],
                    "name": customer[1],
                    "email": customer[2],
                    "phone": customer[3],
                    "username": customer[4]
                }
            else:   
                return f"Couldn't find a customer with {key} of {value}"
        else:
            raise ValueError(f"Invalid key: {key}")
        return None

    def get_order_by_id(self, order_id: str) -> Dict[str, str]:
        self.cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = self.cursor.fetchone()
        if order:
            return {
                "id": order[0],
                "customer_id": order[1],
                "product": order[2],
                "quantity": order[3],
                "price": order[4],
                "status": order[5]
            }
        return None
    
    def get_customer_orders(self, customer_id: str) -> List[Dict[str, str]]:
        self.cursor.execute('SELECT * FROM orders WHERE customer_id = ?', (customer_id,))
        orders = self.cursor.fetchall()
        return [
            {
                "id": order[0],
                "customer_id": order[1],
                "product": order[2],
                "quantity": order[3],
                "price": order[4],
                "status": order[5]
            } for order in orders
        ]

    def cancel_order(self, order_id: str) -> str:
        order = self.get_order_by_id(order_id)
        if order:
            if order["status"] == "Processing":
                order["status"] = "Cancelled"
                self.cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (order["status"], order_id))
                self.connection.commit()
                return "Cancelled the order"
            else:
                return "Order has already shipped.  Can't cancel it."
        return "Can't find that order!"
    
if __name__ == "__main__":
    db = SQLiteDatabase()
    print("Database initialized and initial data inserted.")