fromfrom tkinter import ttk
from tkinter import *
from reportlab.pdfgen import canvas
from update_inventory import remove_product_invetory, add_product_invetory, get_products, update_products_db
from lector_QR import App

import sqlite3


class Product:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations
        self.wind = window
        self.wind.title('CAJA REGISTRADORA')

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text='Register new Product')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Name Input
        """
        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        """
        # Price Input
        """
        Label(frame, text='Precio: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)
        """

        # Code Input
        Label(frame, text='Sku: ').grid(row=3, column=0)
        self.code = Entry(frame)
        self.code.grid(row=3, column=1)


       # Button Scan CodeQR
        ttk.Button(frame, text='ESCANEAR QR', command=self.scan_qr).grid(
            row=4, columnspan=2, sticky=W + E)


        # Button Add Product
        ttk.Button(frame, text='Guardar Producto', command=self.add_product).grid(
            row=5, columnspan=2, sticky=W + E)

        # Button Sell Product
        ttk.Button(frame, text='Vender Producto', command=self.sell_product).grid(
            row=6, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=7, column=0, columnspan=2, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2'))
        self.tree.grid(row=8, column=0, columnspan=2)
        self.tree.heading('#0', text='Codigo', anchor=CENTER)
        self.tree.heading('#1', text='Sku', anchor=CENTER)
        self.tree.heading('#2', text='Precio', anchor=CENTER)
        self.tree.heading('#3', text='Cantidad', anchor=CENTER)

        # Buttons
        ttk.Button(text='ELIMINAR', command=self.delete_product).grid(
            row=9, column=0, sticky=W + E)
        ttk.Button(text='EDITAR', command=self.edit_product).grid(
            row=9, column=1, sticky=W + E)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        # LOCAL DATA BASE query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = get_products()

        # LOCAL DATA BASE Insert products to local data base
        # filling data
        query = 'DELETE FROM product'
        self.run_query(query)

        for row in db_rows:
            self.add_local_product(row)
            self.tree.insert('', 0, text=row[0], values=(
                row[1], row[2], row[3]))
    # User Input Validation

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 and len(self.code.get()) != 0

    def code_validation(self):
        return len(self.code.get()) != 0

    # Get product quantity
    def get_quantity(self, code):
        quantity = 'SELECT quantity FROM product WHERE code = ' + code
        db_quantity = self.run_query(quantity)
        current_quantity = 0
        for row in db_quantity:
            current_quantity = row[0]
        new_quantity = current_quantity + 1
        return new_quantity

    def add_product(self):        
        if self.code_validation():
            code = self.code.get()
            add_product_invetory(code)
            self.get_products()
        else:
            self.message['text'] = 'El campo de codigo es obligatorio'
        """
        LOCAL DATA BASE
        if self.validation():
            code = self.code.get()
            new_quantity = self.get_quantity(code)
            if new_quantity == 1:
                self.add_new_product()
            if new_quantity > 1:
                self.add_existing_product(new_quantity, code)
        else:
            self.message['text'] = 'Todos los campos son requeridos'
        self.get_products()
        """

    def add_local_product(self, product):
        print(product)
        query = 'INSERT INTO product VALUES(NULL, ?, ?, ?,?)'
        parameters = (product[1], float(product[2]), product[0], product[3])
        print(parameters)
        self.run_query(query, parameters)

    def add_existing_product(self, new_quantity, code):
        query = 'UPDATE product SET quantity = ? WHERE code = ?'
        parameters = (new_quantity, code)
        self.run_query(query, parameters)
        self.message['text'] = 'Product {} added Successfully'.format(
            self.name.get())

    def add_new_product(self):
        query = 'INSERT INTO product VALUES(NULL, ?, ?, ?,?)'
        parameters = (self.name.get(), self.price.get(), self.code.get(), 1)
        self.run_query(query, parameters)
        self.message['text'] = 'Product {} added Successfully'.format(
            self.name.get())

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.message['text'] = ''
            name = self.tree.item(self.tree.selection())['values']
            print(name[0])
        except IndexError:
            self.message['text'] = 'Please select a Record'
            return
        remove_product_invetory(name[0])
        self.get_products()

        """
        LOCAL DATA BASE
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE code = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()
        """

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'
        # Old Name
        Label(self.edit_wind, text='Old Name:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind,
                                                     value=name), state='readonly').grid(row=0, column=2)
        # New Name
        Label(self.edit_wind, text='New Price:').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        # Old Price
        Label(self.edit_wind, text='Old Price:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind,
                                                     value=old_price), state='readonly').grid(row=2, column=2)
        # New Price
        Label(self.edit_wind, text='New Name:').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text='Update', command=lambda: self.edit_records(
            new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_products()

    def sell_product(self):

        self.message['text'] = ''

        self.sell_wind = Toplevel()
        self.sell_wind.title = 'Sell Products'

        # Creating a Frame Container
        sell_frame = LabelFrame(self.sell_wind, text='Search new Product')
        sell_frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Code Input
        Label(sell_frame, text='Sku: ').grid(row=1, column=0)
        self.sell_code = Entry(sell_frame)
        self.sell_code.grid(row=1, column=1)

        # Name Input
        self.sell_name = StringVar()
        Label(sell_frame, text='Nombre: ').grid(row=2, column=0)
        Label(sell_frame, textvariable=self.sell_name).grid(row=2, column=1)

        # Price Input
        self.sell_price = StringVar()
        Label(sell_frame, text='Precio: ').grid(row=3, column=0)
        Label(sell_frame, textvariable=self.sell_price).grid(row=3, column=1)

        Button(sell_frame, text='Buscar', command=lambda: self.search_product()).grid(
            row=4, column=0, sticky=W)
        Button(sell_frame, text='Agregar', command=lambda: self.add_sell_product()).grid(
            row=4, column=1, sticky=W)
        Button(sell_frame, text='Escanear QR', command=lambda: self.sell_scan_qr()).grid(
            row=4, column=2, sticky=W)

        # Table
        self.sell_tree = ttk.Treeview(
            self.sell_wind, height=10, columns=('#0', '#1', '#2'))
        self.sell_tree.grid(row=5, column=0, columnspan=2)
        self.sell_tree.heading('#0', text='Codigo', anchor=CENTER)
        self.sell_tree.heading('#1', text='Nombre', anchor=CENTER)
        self.sell_tree.heading('#2', text='Precio', anchor=CENTER)
        self.sell_tree.heading('#3', text='Cantidad', anchor=CENTER)

        self.sell_total_label = StringVar()
        self.sell_total = 0

        # Creating a Frame Container
        sell_frame_print = LabelFrame(self.sell_wind, text='Resumen de venta')
        sell_frame_print.grid(row=6, column=0, columnspan=3, pady=20)

        Label(sell_frame_print, text='Total a pagar: ').grid(row=0, column=0)
        Label(sell_frame_print, textvariable=self.sell_total_label).grid(
            row=0, column=1)
        Button(sell_frame_print, text='Imprimir', command=lambda: self.print_pdf()).grid(
            row=2, column=0)

    def search_product(self):
        # getting data
        query = 'SELECT * FROM product WHERE name = \''  + self.sell_code.get() + '\''
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.sell_name.set(str(row[1]))
            self.sell_price.set(str(row[2]))

    def add_sell_product(self):
        # getting data
        query = 'SELECT * FROM product WHERE name = \'' + self.sell_code.get() +'\''
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            if (row[4] > 0):
                if self.group_by_code(row[3], row[4], row[2]):

                    total_payment = self.sell_total + row[2]
                    self.sell_total_label.set(str(total_payment))
                    self.sell_total += row[2]

                    self.sell_tree.insert('', 0, text=row[3], values=(
                        row[1], row[2], 1))

    def group_by_code(self, code, quantity, price):
        # getting data
        records = self.sell_tree.get_children()
        for element in records:

            sell_tree_code = str(self.sell_tree.item(element)['text'])
            sell_tree_quantity = self.sell_tree.item(element)['values'][2]
            if(sell_tree_code == str(code)):
                if (quantity > sell_tree_quantity):
                    sell_tree_name = str(
                        self.sell_tree.item(element)['values'][0])

                    sell_tree_quantity += 1
                    self.sell_tree.item(element, text=code,
                                        values=(sell_tree_name, price, sell_tree_quantity))

                    total_payment = self.sell_total + price
                    self.sell_total_label.set(str(total_payment))
                    self.sell_total += price

                    return False
                else:
                    return False
        return True

    def print_pdf(self):
        pdf = canvas.Canvas('Sell.pdf')
        pdf.setTitle('Resumen de venta')
        pdf.drawString(250, 800, 'Resumen de venta')
        pdf.drawString(50, 750, 'Codigo')
        pdf.drawString(200, 750, 'Nombre')
        pdf.drawString(350, 750, 'Precio unitario')
        pdf.drawString(500, 750, 'Cantidad')

        row_number = 725
        records = self.sell_tree.get_children()

        for element in records:

            sell_tree_code = str(self.sell_tree.item(element)['text'])
            sell_tree_quantity = str(self.sell_tree.item(element)['values'][2])
            sell_tree_name = str(self.sell_tree.item(element)['values'][0])
            sell_tree_price = str(self.sell_tree.item(element)['values'][1])

            pdf.drawString(50, row_number, sell_tree_code)
            pdf.drawString(200, row_number, sell_tree_name)
            pdf.drawString(350, row_number, sell_tree_price)
            pdf.drawString(500, row_number, sell_tree_quantity)
            row_number -= 25

            self.reduce_quantity(self.sell_tree.item(element)[
                                 'values'][2], sell_tree_code)

        pdf.drawString(50, row_number, 'Total a pagar')
        pdf.drawString(200, row_number, str(self.sell_total))

        pdf.save()
        self.sell_wind.destroy()
        self.get_products()

        return True

    def reduce_quantity(self, quantity, code):
        product_query = 'SELECT * FROM product WHERE name = \'' + code + '\''
        db_rows = self.run_query(product_query)
        new_quantity = 0
        sku = ""
        for row in db_rows:
            new_quantity = row[4] - quantity
            sku = row[1]

        # LOCAL DATA BASE
        #update_query = 'UPDATE product SET quantity = ? WHERE code = ?'
        #parameters = (new_quantity, code)
        #self.run_query(update_query, parameters)

        # TODO Review instok (description paramter) rule
        update_products_db(new_quantity, "instock", sku, code)
    
    def scan_qr(self):
        self.code.insert(1,'')
        App(self.code)

    def sell_scan_qr(self):
        self.sell_code.insert(1,'')
        App(self.sell_code)

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()



        # Button Add Product
        ttk.Button(frame, text='Save Product', command=self.add_product).grid(
            row=5, columnspan=2, sticky=W + E)

        # Button Sell Product
        ttk.Button(frame, text='Sell Product', command=self.sell_product).grid(
            row=6, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=7, column=0, columnspan=2, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2'))
        self.tree.grid(row=8, column=0, columnspan=2)
        self.tree.heading('#0', text='Codigo', anchor=CENTER)
        self.tree.heading('#1', text='Sku', anchor=CENTER)
        self.tree.heading('#2', text='Precio', anchor=CENTER)
        self.tree.heading('#3', text='Cantidad', anchor=CENTER)

        # Buttons
        ttk.Button(text='DELETE', command=self.delete_product).grid(
            row=9, column=0, sticky=W + E)
        ttk.Button(text='EDIT', command=self.edit_product).grid(
            row=9, column=1, sticky=W + E)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        # LOCAL DATA BASE query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = get_products()

        # LOCAL DATA BASE Insert products to local data base
        # filling data
        query = 'DELETE FROM product'
        self.run_query(query)

        for row in db_rows:
            self.add_local_product(row)
            self.tree.insert('', 0, text=row[0], values=(
                row[1], row[2], row[3]))
    # User Input Validation

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 and len(self.code.get()) != 0

    def code_validation(self):
        return len(self.code.get()) != 0

    # Get product quantity
    def get_quantity(self, code):
        quantity = 'SELECT quantity FROM product WHERE code = ' + code
        db_quantity = self.run_query(quantity)
        current_quantity = 0
        for row in db_quantity:
            current_quantity = row[0]
        new_quantity = current_quantity + 1
        return new_quantity

    def add_product(self):        
        if self.code_validation():
            code = self.code.get()
            add_product_invetory(code)
            self.get_products()
        else:
            self.message['text'] = 'El campo de codigo es obligatorio'
        """
        LOCAL DATA BASE
        if self.validation():
            code = self.code.get()
            new_quantity = self.get_quantity(code)
            if new_quantity == 1:
                self.add_new_product()
            if new_quantity > 1:
                self.add_existing_product(new_quantity, code)
        else:
            self.message['text'] = 'Todos los campos son requeridos'
        self.get_products()
        """

    def add_local_product(self, product):
        print(product)
        query = 'INSERT INTO product VALUES(NULL, ?, ?, ?,?)'
        parameters = (product[1], float(product[2]), product[0], product[3])
        print(parameters)
        self.run_query(query, parameters)

    def add_existing_product(self, new_quantity, code):
        query = 'UPDATE product SET quantity = ? WHERE code = ?'
        parameters = (new_quantity, code)
        self.run_query(query, parameters)
        self.message['text'] = 'Product {} added Successfully'.format(
            self.name.get())

    def add_new_product(self):
        query = 'INSERT INTO product VALUES(NULL, ?, ?, ?,?)'
        parameters = (self.name.get(), self.price.get(), self.code.get(), 1)
        self.run_query(query, parameters)
        self.message['text'] = 'Product {} added Successfully'.format(
            self.name.get())

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.message['text'] = ''
            name = self.tree.item(self.tree.selection())['values']
            print(name[0])
        except IndexError:
            self.message['text'] = 'Please select a Record'
            return
        remove_product_invetory(name[0])
        self.get_products()

        """
        LOCAL DATA BASE
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE code = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()
        """

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'
        # Old Name
        Label(self.edit_wind, text='Old Name:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind,
                                                     value=name), state='readonly').grid(row=0, column=2)
        # New Name
        Label(self.edit_wind, text='New Price:').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        # Old Price
        Label(self.edit_wind, text='Old Price:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind,
                                                     value=old_price), state='readonly').grid(row=2, column=2)
        # New Price
        Label(self.edit_wind, text='New Name:').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text='Update', command=lambda: self.edit_records(
            new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_products()

    def sell_product(self):

        self.message['text'] = ''

        self.sell_wind = Toplevel()
        self.sell_wind.title = 'Sell Products'

        # Creating a Frame Container
        sell_frame = LabelFrame(self.sell_wind, text='Search new Product')
        sell_frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Code Input
        Label(sell_frame, text='Codigo: ').grid(row=1, column=0)
        self.sell_code = Entry(sell_frame)
        self.sell_code.grid(row=1, column=1)

        # Name Input
        self.sell_name = StringVar()
        Label(sell_frame, text='Nombre: ').grid(row=2, column=0)
        Label(sell_frame, textvariable=self.sell_name).grid(row=2, column=1)

        # Price Input
        self.sell_price = StringVar()
        Label(sell_frame, text='Precio: ').grid(row=3, column=0)
        Label(sell_frame, textvariable=self.sell_price).grid(row=3, column=1)

        Button(sell_frame, text='Buscar', command=lambda: self.search_product()).grid(
            row=4, column=0, sticky=W)
        Button(sell_frame, text='Agregar', command=lambda: self.add_sell_product()).grid(
            row=4, column=1, sticky=W)

        # Table
        self.sell_tree = ttk.Treeview(
            self.sell_wind, height=10, columns=('#0', '#1', '#2'))
        self.sell_tree.grid(row=5, column=0, columnspan=2)
        self.sell_tree.heading('#0', text='Codigo', anchor=CENTER)
        self.sell_tree.heading('#1', text='Nombre', anchor=CENTER)
        self.sell_tree.heading('#2', text='Precio', anchor=CENTER)
        self.sell_tree.heading('#3', text='Cantidad', anchor=CENTER)

        self.sell_total_label = StringVar()
        self.sell_total = 0

        # Creating a Frame Container
        sell_frame_print = LabelFrame(self.sell_wind, text='Resumen de venta')
        sell_frame_print.grid(row=6, column=0, columnspan=3, pady=20)

        Label(sell_frame_print, text='Total a pagar: ').grid(row=0, column=0)
        Label(sell_frame_print, textvariable=self.sell_total_label).grid(
            row=0, column=1)
        Button(sell_frame_print, text='Imprimir', command=lambda: self.print_pdf()).grid(
            row=2, column=0)

    def search_product(self):
        # getting data
        query = 'SELECT * FROM product WHERE code = ' + self.sell_code.get()
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.sell_name.set(str(row[1]))
            self.sell_price.set(str(row[2]))

    def add_sell_product(self):
        # getting data
        query = 'SELECT * FROM product WHERE code = ' + self.sell_code.get()
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            if (row[4] > 0):
                if self.group_by_code(row[3], row[4], row[2]):

                    total_payment = self.sell_total + row[2]
                    self.sell_total_label.set(str(total_payment))
                    self.sell_total += row[2]

                    self.sell_tree.insert('', 0, text=row[3], values=(
                        row[1], row[2], 1))

    def group_by_code(self, code, quantity, price):
        # getting data
        records = self.sell_tree.get_children()
        for element in records:

            sell_tree_code = str(self.sell_tree.item(element)['text'])
            sell_tree_quantity = self.sell_tree.item(element)['values'][2]
            if(sell_tree_code == str(code)):
                if (quantity > sell_tree_quantity):
                    sell_tree_name = str(
                        self.sell_tree.item(element)['values'][0])

                    sell_tree_quantity += 1
                    self.sell_tree.item(element, text=code,
                                        values=(sell_tree_name, price, sell_tree_quantity))

                    total_payment = self.sell_total + price
                    self.sell_total_label.set(str(total_payment))
                    self.sell_total += price

                    return False
                else:
                    return False
        return True

    def print_pdf(self):
        pdf = canvas.Canvas('Sell.pdf')
        pdf.setTitle('Resumen de venta')
        pdf.drawString(250, 800, 'Resumen de venta')
        pdf.drawString(50, 750, 'Codigo')
        pdf.drawString(200, 750, 'Nombre')
        pdf.drawString(350, 750, 'Precio unitario')
        pdf.drawString(500, 750, 'Cantidad')

        row_number = 725
        records = self.sell_tree.get_children()

        for element in records:

            sell_tree_code = str(self.sell_tree.item(element)['text'])
            sell_tree_quantity = str(self.sell_tree.item(element)['values'][2])
            sell_tree_name = str(self.sell_tree.item(element)['values'][0])
            sell_tree_price = str(self.sell_tree.item(element)['values'][1])

            pdf.drawString(50, row_number, sell_tree_code)
            pdf.drawString(200, row_number, sell_tree_name)
            pdf.drawString(350, row_number, sell_tree_price)
            pdf.drawString(500, row_number, sell_tree_quantity)
            row_number -= 25

            self.reduce_quantity(self.sell_tree.item(element)[
                                 'values'][2], sell_tree_code)

        pdf.drawString(50, row_number, 'Total a pagar')
        pdf.drawString(200, row_number, str(self.sell_total))

        pdf.save()
        self.sell_wind.destroy()
        self.get_products()

        return True

    def reduce_quantity(self, quantity, code):
        product_query = 'SELECT * FROM product WHERE code = ' + code
        db_rows = self.run_query(product_query)
        new_quantity = 0
        sku = ""
        for row in db_rows:
            new_quantity = row[4] - quantity
            sku = row[1]

        # LOCAL DATA BASE
        #update_query = 'UPDATE product SET quantity = ? WHERE code = ?'
        #parameters = (new_quantity, code)
        #self.run_query(update_query, parameters)

        # TODO Review instok (description paramter) rule
        update_products_db(new_quantity, "instock", sku, code)
    
    def scan_qr(self):
        self.code.insert(1,'')
        App(self.code)

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
