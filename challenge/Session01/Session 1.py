from flask import request
import sqlite3

    # Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/searchProduct', methods=['GET'])
def search_products():
    query = request.args.get('query')
    # Validate query string from request
    if validate_query(query) == False:
        return
    # Use parameterized query to avoid injection
    sql = "SELECT * FROM products WHERE name LIKE %s"
    try:
        conn = get_db_connection()
        results = conn.execute(sql, ('%' + query + '%')).fetchall()
        conn.close()
        return results
    except Exception as e:
        print("search_products() :An error occurred: {e}")
    finally:
        conn.close()

def validate_query(query):
    # Script pattern validate
    script_pattern = re.compile(r'<script.*?>.*?</script>', re.IGNORECASE)
    # Special character validate
    special_characters_pattern = re.compile(r'[^a-zA-Z0-9 ]')

    if script_pattern.search(query) or special_characters_pattern.search(query):
        return False
        
    return True

@app.route('/addProduct', methods=['POST'])
def add_product():
    product = request.get_json()
    
    # Validate product fields
    if validate_query(product.name) == False or validate_query(product.price) == False or validate_query(product.quantity) == False:
        return
    try:
        conn = get_db_connection()
        cursor = conn.getcursor()

    # Insert the product into the database
    # Use parameterized query to avoid injection
        cursor.execute('''
            INSERT INTO products (name, price, quantity)
            VALUES (?, ?, ?)
        ''', (product.name, product.price, product.quantity))

        conn.commit()
        conn.close()
    except Exception as e:
        print("add_product(): An error occurred: {e}")
    finally:
        conn.close()

@app.route('/editProduct', methods=['PUT'])
def edit_product():
    product = request.get_json()
    
    # Validate product fields
    if validate_query(product.id) == False or validate_query(product.name) == False or validate_query(product.price) == False or validate_query(product.quantity) == False:
        return
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

    # Update the product
    # Use parameterized query to avoid injection
        cursor.execute('''
        UPDATE products
        SET name = ?, price = ?, quantity = ?
        WHERE id = ?
    ''', (product.name, product.price, product.quantity, product.id))

        conn.commit()
        conn.close()
    except Exception as e:
        print("edit_product(): An error occurred: {e}")
    finally:
        conn.close()

def create_table():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

    # Create products table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
            ''')

            conn.commit()
            conn.close()
        except Exception as e:
            print("create_table(): An error occurred: {e}")
        finally:
            conn.close()    

@app.route('/')
def home():
    create_table()
    return "Welcome to the Product Management App!"


     
class Product:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name        # Product name
        self.price = price      # Product price
        self.quantity = quantity # Available quantity
    