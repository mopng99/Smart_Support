# Smart_Support
Technical Assessment and Questions for Odoo Developer - Smar
Q1: Using Python and XML-RPC, write a simple script to log in and access user's invoices.
 import xmlrpc.client

# Odoo instance URL and database name
url = 'http://localhost:8069'
db = 'your_database_name'

# Odoo username and password
username = 'your_username'
password = 'your_password'

# Connect to the Odoo XML-RPC server
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')

# Authenticate and retrieve the user's UID (User ID)
uid = common.authenticate(db, username, password, {})

if uid:
    # Connect to the Odoo XML-RPC server as the authenticated user
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    # Search for invoices belonging to the user
    invoice_ids = models.execute_kw(db, uid, password, 'account.invoice', 'search', [[('user_id', '=', uid)]])

    # Retrieve invoice details
    invoices = models.execute_kw(db, uid, password, 'account.invoice', 'read', [invoice_ids], {'fields': ['number', 'amount_total']})

    # Print invoice details
    for invoice in invoices:
        invoice_number = invoice['number']
        invoice_amount = invoice['amount_total']
        print(f"Invoice Number: {invoice_number}")
        print(f"Amount Total: {invoice_amount}")
else:
    print("Login failed, please check your credentials.")
    
-------------------------------------------------------------------------------------------------------------------------------------
Q2: What different types of model inheritance are used in Odoo 16?
Class inheritance (extension)
Prototype inheritance.
Delegation inheritance.

-------------------------------------------------------------------------------------------------------------------------------------
Q3: Make a connection to a local database using psycopg2 and list all products in the system.
import psycopg2

# Database connection details
database = 'your_database_name'
user = 'your_username'
password = 'your_password'
host = 'localhost'
port = '5432'

# Establish a connection to the database
connection = psycopg2.connect(
    dbname=database,
    user=user,
    password=password,
    host=host,
    port=port
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Execute a query to fetch all products
query = "SELECT * FROM product_table_name"
cursor.execute(query)

# Fetch all the rows from the resultset
rows = cursor.fetchall()

# Print the products
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()

-------------------------------------------------------------------------------------------------------------------------------------
Q4: What is an external ID, and how can you use it in building views?
External ID is a unique identifier that is assigned to a record or a view.
It serves as a reference to that particular record or view throughout the system. 
External IDs are used to locate and reference objects, even when their database identifiers change.

<record id="view_id" model="ir.ui.view">
    <field name="name">My View</field>
    <field name="model">model.name</field>
    <field name="arch" type="xml">
        <form string="My Form">
            <field name="field1"/>
            <field name="field2"/>
        </form>
    </field>
</record>
              
-------------------------------------------------------------------------------------------------------------------------------------
Q5: Given a model "smart_support" with a field "total_amount," how would you inherit the model and create a new field to calculate a 5% tax on "total_amount" using computed fields?
from odoo import models, fields

class SmartSupport(models.Model):
    _inherit = 'smart_support'

    tax_amount = fields.Float(compute='_compute_tax_amount', store=True)

    @api.depends('total_amount')
    def _compute_tax_amount(self):
        for record in self:
            record.tax_amount = record.total_amount * 0.05
            
-------------------------------------------------------------------------------------------------------------------------------------
Q6: Briefly explain Wizards, Reports, and Actions in Odoo 16.
Wizards: Wizards are interactive and dynamic forms used to guide users through specific processes or tasks.
Wizards are used for tasks such as data import, configuration setups, data exports, or any complex data manipulation.
They can be triggered from menu items, buttons, or other actions. Wizards are defined as models that inherit from models.TransientModel.

Reports: Reports in Odoo are used to generate formatted documents with data extracted from the system.
Reports can be in various formats such as PDF, Excel, HTML, or CSV.
it uses QWeb templating language. Reports can be associated with specific models and can be triggered from menu items, buttons, or scheduled actions. 

Actions: Actions define the behavior and interaction of the system in response to user actions or events. 
They are responsible for handling user input and triggering specific actions, such as opening a form view, executing a server action, showing a wizard, or redirecting to a specific URL.

-------------------------------------------------------------------------------------------------------------------------------------
Q7: What are OWL components, and how can you make a component inherit the ReceiptScreen of the Point Of Sale Module in Odoo 16? Please support your answer with example code.

-------------------------------------------------------------------------------------------------------------------------------------
Q8: How do you load existing fields from the database in Point Of Sale -> ReceiptScreen in Odoo 16?

-------------------------------------------------------------------------------------------------------------------------------------
Q9: Describe the composition (structure) of an Odoo Module in version 16.
1-Module Manifest File (__manifest__.py): The module starts with a manifest file that provides information about the module.
It is a Python file named __manifest__.py located in the root directory of the module. 
The manifest file contains metadata such as module name, version, dependencies, data files, views, models, and other module-specific configurations.

2-Models Directory: The models directory contains Python files that define the data models for the module.
These files inherit from the appropriate base models and define fields, methods, and other behavior related to the module's data.

3-Views Directory: The views directory contains XML or QWeb template files that define the user interface of the module.
These files specify the structure and appearance of forms, lists, reports, dashboards.

4-Security Directory: The security directory contains XML or CSV files that define access control rules for the module. 
These files specify access rights, groups, and permissions for the module's models, fields, and actions.

5-Data Directory: The data directory contains XML or CSV files that define initial or demo data for the module. 
These files can include records, configurations, or other data that needs to be loaded when the module is installed.

6-Static Directory: The static directory contains static files such as JavaScript, CSS, and image files used by the module. 

7-Reports Directory: The reports directory contains XML files that define the layout and structure of reports generated by the module. 
These files specify the content, formatting, and data sources for the module's reports.

8-i18n Directory: The i18n directory contains translation files for the module.
These files allow translation of the module's user interface and other text elements.

-------------------------------------------------------------------------------------------------------------------------------------
Q10: Write simple code to append a Menu Item called "Branches" to Odoo's user menu in version 16.
<odoo>
    <data>
        <record id="menu_branches" model="ir.ui.menu">
            <field name="name">Branches</field>
            <field name="action" ref="module_name.action_branches"/>
            <field name="parent_id" ref="base.menu_user_root"/>
            <field name="sequence" eval="15"/>
        </record>
    </data>
</odoo>

-------------------------------------------------------------------------------------------------------------------------------------
Q11: Explain the steps or provide Python code to import an invoice into the database, ensuring invoice validation and payment status, in Odoo 16.

from odoo import models, fields, api

class InvoiceImport(models.Model):
    _name = 'my_module.invoice_import'

    def import_invoice(self, data):
        # Data contains the invoice information to be imported
        # Perform validation and extract necessary information from the data

        # Create or update the invoice in the Odoo database
        invoice = self.env['account.move'].create({
            'partner_id': data['partner_id'],
            'move_type': 'entry',
            'amount_total': data['amount_total'],
            # Add more invoice fields as required
        })

        # Perform any additional operations, such as updating payment status
        if data['is_paid']:
            # Mark the invoice as paid
            invoice.payment_status = 'paid'
        else:
            # Mark the invoice as unpaid
            invoice.payment_status = 'unpaid'

        return invoice
        
-------------------------------------------------------------------------------------------------------------------------------------
Q12: Define method overloading and method overriding.
In languages like Java, method overloading refers to defining multiple methods with the same name but different parameter lists.
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public double add(double a, double b) {
        return a + b;
    }
}

While in overriding, the function is rebuilt with the same old name and parameter
public class Animal {
    public void makeSound() {
        System.out.println("Animal makes a sound");
    }
}

public class Cat extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Cat meows");
    }
}

-------------------------------------------------------------------------------------------------------------------------------------
Q13: What is inheritance in programming?
Inheritance is when one class inherits the attributes and methods of another class. 

-------------------------------------------------------------------------------------------------------------------------------------
Q14: Define a superclass in object-oriented programming.
In object-oriented programming, a class from which other classes inherit code is called a superclass. 
but, the class that inherits the code is called a subclass of that superclass.

-------------------------------------------------------------------------------------------------------------------------------------
Q15: Mention three field types used in Odoo 16 models.
Integer
Char
Text
Float
Boolean

-------------------------------------------------------------------------------------------------------------------------------------
Q16: Highlight the differences between Lists and Tuples in Python.
Lists are mutable	          
The List is better for performing operations, such as insertion and deletion.	
Lists consume more memory

Tuples are immutable
A Tuple data type is appropriate for accessing the elements	
Tuple consumes less memory as compared to the list

-------------------------------------------------------------------------------------------------------------------------------------

 
‏
