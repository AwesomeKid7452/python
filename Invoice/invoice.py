from fpdf import FPDF
from tkinter.font import Font

class InvoicePDF(FPDF):
    def __init__(self, background_image):
        super().__init__()
        self.background_image = background_image

    def header(self):
        # Add background image on the entire page
        self.image(self.background_image, x=0, y=0, w=210, h=297)  # A4 size in mm
        
        # Add Futura font
        self.add_font('Futura', '', 'futura.ttf', uni=True)
        self.add_font('Futura', 'B', 'futura_bold.ttf', uni=True)
    
    def invoice_body(self, date, name, place, reference, items, total_amount):
        self.set_font('Futura', 'B', 13)

        # Coordinates for Bill To
        self.set_xy(10, 58)
        self.cell(0, 10, f'{name}', ln=True)
        
        self.set_font('Futura', 'B', 13)
        self.set_xy(10, 65)
        self.cell(0, 10, f'{place}', ln=True)

        # Coordinates for Date and Invoice Reference
        self.set_font('Futura', 'B', 13)
        self.set_xy(160, 51)
        self.cell(0, 10, f'{date}', ln=True)

        self.set_xy(160, 61.5)
        self.cell(0, 10, f'{reference}', ln=True)

        # Coordinates for Description and Price
        y_position = 95  # Starting position for items
        self.set_font('Futura', 'B', 13)

        for item in items:
            description, price, quantity = item['description'], item['price'], item['quantity']
            total = price * quantity

            self.set_xy(10, y_position)
            self.cell(0, 10, f'{description} (x{quantity})', ln=True)
            
            self.set_xy(135, y_position)
            self.cell(0, 10, f'{price:.2f}', ln=True)

            self.set_xy(178, y_position)
            self.cell(0, 10, f'{total:.2f}', ln=True)

            y_position += 7  # Move to next line for the next item

        # Coordinates for Total Amount
        self.set_font('Futura', 'B', 16)
        self.set_xy(150, 156.5)
        self.cell(0, 10, f'RM {total_amount:.2f}', ln=True)

# Function to create and save the PDF invoice
def create_invoice(background_image, date, name, place, reference, items, total_amount, output_file):
    pdf = InvoicePDF(background_image)
    pdf.add_page()
    pdf.invoice_body(date, name, place, reference, items, total_amount)
    pdf.output(output_file)

# Function to gather items from user
def get_items():
    items = []
    total_amount = 0

    while True:
        description = input("Enter the description of the item: ")
        price = float(input("Enter the price of the item (RM): "))
        quantity = int(input("Enter the quantity of the item: "))

        # Add the item to the list
        items.append({
            'description': description,
            'price': price,
            'quantity': quantity
        })

        # Calculate total
        total_amount += price * quantity

        # Ask if the user wants to add another item
        add_more = input("Would you like to add another item? (yes/no): ").strip().lower()
        if add_more != 'yes':
            break

    return items, total_amount

# Example user input
background_image = 'template.png'  # Path to your background image
#output_pdf_path = f'{name}_{reference}_{place}.pdf'
output_pdf_path = 'invoice.pdf'

date = input("Enter the date (dd/mm/yyyy): ")
name = input("Enter the name: ")
place = input("Enter the place: ")
reference = input("Enter the invoice reference: ")

# Get items and total amount
items, total_amount = get_items()

# Generate the invoice
create_invoice(background_image, date, name, place, reference, items, total_amount, output_pdf_path)

print("Invoice generated successfully!")
