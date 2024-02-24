from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = "SELECT product_id, name, price_per_unit FROM products;"
    cursor.execute(query)
    products = cursor.fetchall()
    return products

def get_all_uoms(connection):
    cursor = connection.cursor()
    query = "SELECT uom_id, uom_name FROM uom;"
    cursor.execute(query)
    uoms = cursor.fetchall()
    return uoms

#ADD PRODUCT
def add_product(connection):
    product_name = input("Enter product name: ")
    price_per_unit = input("Enter price per unit: ")

    if not product_name or not price_per_unit:
        print("Error: Please fill in all fields")
        return

    uoms = get_all_uoms(connection)
    print("Available Unit of Measures:")
    for uom_id, uom_name in uoms:
        print(f"{uom_id}:{uom_name}")
    uom_selection  = input("Select your unit of measure: ")

    try:
        uom_selection = int(uom_id)
        if uom_selection not in [uom[0] for uom in uoms]: #looping through the uom ids and chekcing if user selction is in there
            raise ValueError("Invalid UOM ID")     
    except ValueError("Invalid Selection, please try again"):

        product = {
            'product_name': product_name,
            'uom_id': uom_selection,
            'price_per_unit': price_per_unit
        }

        try:
            last_row_id = insert_new_product(connection, product)
            print("Product added successfully with ID:", last_row_id)
        except Exception as e:
            print(f"Failed to add product: {str(e)}")
    product = {
        'product_name': product_name,
        'uom_id': uom_id,
        'price_per_unit': price_per_unit
    }

    try:
        last_row_id = insert_new_product(connection, product)
        print("Product added successfully with ID:", last_row_id)
    except Exception as e:
        print(f"Failed to add product: {str(e)}")


#DELETE PRODUCT
def delete_product(connection):
    products = get_all_products(connection)

    if not products:
        print("No products found in the database.")
        return

    print("Available Products:")
    for product in products:
        print(f"{product[0]}: {product[1]}")

    product_id = input("Enter product ID to delete: ")

    try:
        product_id = int(product_id)
        if product_id not in [prod[0] for prod in products]:
            raise ValueError("Invalid Product ID")
    except ValueError:
        print("Error: Invalid Product ID")
        return

    try:
        delete_product_by_id(connection, product_id)
        print("Product deleted successfully")
    except Exception as e:
        print(f"Failed to delete product: {str(e)}")


def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit) "
             "VALUES (%s, %s, %s)")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()
    last_row_id = cursor.lastrowid
    cursor.close()
    return last_row_id

def delete_product_by_id(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" +str(product_id))
    cursor.execute(query)
    connection.commit()

if __name__ == '__main__':
    connection = get_sql_connection()

    while True:
        print("1. Add Product")
        print("2. Delete Product")
        print("3. Show All Products")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_product(connection)
        elif choice == '2':
            delete_product(connection)
        elif choice == '3':
            products = get_all_products(connection)
            for product in products:
                print(product)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
