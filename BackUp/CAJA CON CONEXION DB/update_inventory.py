import mysql.connector
from mysql.connector import Error

host = 'hst.com.ec'
database = 'hstecu_wpd880'
user = 'hstecu_wpd880'
password = '7!51o]pSM1'


def get_product_quantity_and_id(sku):
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        query = "SELECT stock_quantity, product_id FROM wp0p_wc_product_meta_lookup WHERE sku = %s"
        cursor = connection.cursor()
        cursor.execute(query, (sku,))
        result = cursor.fetchone()
        return [result[0], result[1]]
    except Error as e:
        print("Error conectando a MySQL", e)
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()

# b003 = get_product_quantity_and_id("b003")
# print(b003)


def get_product_name(product_id):
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        query = "SELECT post_title FROM wp0p_posts WHERE ID = %s"
        cursor = connection.cursor()
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        print(result)
        return result[0]
    except Error as e:
        print("Error conectando a MySQL", e)
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()

# b003 = get_product_name(19)


def update_products_db(quantity, description, sku, product_id):
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        # UPDATE product_meta_lookup
        query = "UPDATE wp0p_wc_product_meta_lookup SET stock_quantity = %s, stock_status = %s WHERE wp0p_wc_product_meta_lookup.sku = %s"
        values = (quantity, description, sku)
        cursor = connection.cursor()
        cursor.execute(query, values)

        # UPDATE postmeta
        query_2 = "UPDATE wp0p_postmeta SET meta_value = %s WHERE wp0p_postmeta.post_id = %s AND wp0p_postmeta.meta_key = %s"
        values_2 = (quantity, product_id, "_stock")
        cursor.execute(query_2, values_2)
        query_3 = "UPDATE wp0p_postmeta SET meta_value = %s WHERE wp0p_postmeta.post_id = %s AND wp0p_postmeta.meta_key = %s"
        values_3 = (description, product_id, "_stock_status")
        cursor.execute(query_3, values_3)

        connection.commit()
        # print(cursor.rowcount, "record(s) affected")

    except Error as e:
        print("Error conectando a MySQL", e)
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()

# update_products_db("3", "instock", "A001", "67")


def add_product_invetory(sku):
    [products_in_stock, product_id] = [
        int(x) for x in get_product_quantity_and_id(sku)]
    update_products_db(str(products_in_stock + 1),
                       "instock", sku, str(product_id))

# add_product_invetory("A001")


def remove_product_invetory(sku):
    [products_in_stock, product_id] = [
        int(x) for x in get_product_quantity_and_id(sku)]
    if products_in_stock == 1:
        update_products_db(str(products_in_stock - 1),
                           "outofstock", sku, str(product_id))
    elif products_in_stock > 1:
        update_products_db(str(products_in_stock - 1),
                           "instock", sku, str(product_id))
    else:
        print("Error: actualmente el producto esta fuera de stock")
        return False

# remove_product_invetory("A001")


def get_products():
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        query = "SELECT product_id,min_price ,sku, stock_quantity FROM wp0p_wc_product_meta_lookup"
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        products = []

        for result in results:
            #product_name = get_product_name(result[0])
            product_name = result[2]
            product_id = result[0]
            product_quantity = result[3]
            product_priece = round(result[1], 2)
            sku = result[2]
            result = (product_id, product_name, product_priece,
                      product_quantity, sku)
            products.append(result)
        return products

# result[2],result[0],product_name,round(result[1], 2),result[3]
#result[3], product_name, result[2],result[0], round(result[1], 2)
#(7.0, 'Display Huawei P10', 'QR001', 19, Decimal('10.00'))
# text=row[3], values=(row[1], row[2], row[4]))
#codigo, nombre, precio, cantidad
    except Error as e:
        print("Error conectando a MySQL", e)
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()

# b003 = get_product_quantity_and_id("b003")
# print(b003)


# add_product_invetory()
