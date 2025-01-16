#Helper functions for products

#Imports
import sqlite3

class Products:
    
    def get_products() -> dict:
        """
        Function to get all products

        Returns:
            dict: JSON with key "Products" for all products
        """
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get all the products
        products = conn.execute("SELECT * FROM Products").fetchall()
        conn.close()
        
        return {"Products": products}
    
    
    def get_product(productid:str) -> dict:
        """
        Function that takes in a productid and returns the product

        Args:
            productid (str): Unique identifier of a product

        Returns:
            dict: JSON with Product
        """
        
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get Product
        product = conn.execute("SELECT * FROM Products WHERE Productid = ?", (productid,)).fetchone()
        conn.close()
        
        return {"Product": product}


    def update_product(productid:str, productname:str, stock:int, price:float) -> dict:
        """
        Function to update product

        Args:
            productid (str): Product unique identifier
            productname (str): Product name
            stock (int): Stock left
            price (float): Pricing

        Returns:
            dict: _description_
        """
        
        #Get connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Update the product
        try:
            conn.execute("UPDATE Products SET Name = ?, Stock = ?, Price = ? WHERE Productid = ?",(productname, stock, price, productid))
            conn.commit()
            conn.close()
        
        except:
            conn.close()
            return {"Status": False, "Message": "Failed to update product"}
        
        return {"Status": True, "Message": "Product updated successfully"}
        
        
    