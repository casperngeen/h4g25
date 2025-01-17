#Helper Functions for generating reports

#Imports
import sqlite3
import datetime
import pdfkit
import modules
import modules.products


class Reports:
    
    def generate_weekly_requests() -> dict:
        """
        Function that generates a weekly report of requests (Voucher Tasks, Product Requests, Preorders)
        """
        #Open connection
        conn = sqlite3.connect("../sqlite_db.db")
        
        #Get Voucher tasks
        voucher_tasks = conn.execute("SELECT * FROM Voucher_Tasks WHERE Created >= DATETIME('now', '-7 days');").fetchall()
        
        #Get Product Requests
        product_requests = conn.execute("SELECT * FROM Product_Requests WHERE Created >= DATETIME('now', '-7 days');").fetchall()
        
        #Get Product Preorders
        preorders = conn.execute("SELECT * FROM Preorders WHERE Created >= DATETIME('now', '-7 days');").fetchall()
        
        
                      
        # Generate PDF report
        
        #Heading
        html_content = "<html><head><title>Weekly Report</title></head><body>"
        html_content += "<h1>All Requests</h1>"
        
        #Voucher Tasks
        html_content += f"<h2>Voucher Tasks/h2>"
        html_content += f"<h4>{", ".join(voucher_tasks[0].keys())}</h4>"
        for task in voucher_tasks:
            html_content += f"<p>{", ".join(task.values())}</p>"
        
        
        #Product Requests
        html_content += f"<h2>Product Requests/h2>"
        html_content += f"<h4>{", ".join(product_requests[0].keys())}</h4>"
        for product_request in product_requests:
            html_content += f"<p>{", ".join(product_request.values())}</p>"
        
        
        #Preorders
        html_content += f"<h2>Preorders/h2>"
        html_content += f"<h4>{", ".join(preorders[0].keys())}</h4>"
        for preorder in preorders:
            html_content += f"<p>{", ".join(preorder.values())}</p>"
            
    
        html_content += "</body></html>"

        # Save to PDF
        path_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        path = f"../reports/weekly_report_{datetime.now().date()}.pdf"
        pdfkit.from_string(html_content, path, configuration=config)
        
        
        #Return the pdf path
        return {"Report_Path": path}
    
    
    def view_inventory() -> dict:
        """
        Function generating a pdf of all current inventory

        Returns:
            dict: pdf path
        """
        #Get all products
        products = modules.Products.get_products()["Products"]
        
        # Generate PDF report
        
        #Heading
        html_content = "<html><head><title>Inventory Report</title></head><body>"
        html_content += "<h1>All Products</h1>"
        
        html_content += f"<h2>Preorders/h2>"
        html_content += f"<h4>{", ".join(products[0].keys())}</h4>"
        for product in products:
            html_content += f"<p>{", ".join(product.values())}</p>"
            
        html_content += "</body></html>"

        # Save to PDF
        path_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        path = f"../reports/inventory_report_{datetime.now().date()}.pdf"
        pdfkit.from_string(html_content, path, configuration=config)
        
        
        #Return the pdf path
        return {"Report_Path": path}