import tkinter as tk
from tkinter import messagebox, filedialog
from fpdf import FPDF

class InvoicePDF(FPDF):
    def __init__(self, background_image='template.png'):
        super().__init__()
        self.background_image = background_image

    def header(self):
        self.image(self.background_image, x=0, y=0, w=210, h=297)  # A4 size in mm
        self.add_font('Futura2', '', 'futura_light.ttf', uni=True)
        self.add_font('Futura', 'B', 'futura_bold.ttf', uni=True)

    def invoice_body(self, date, name, place, reference, items, total_amount):
        self.set_font('Futura', 'B', 13)
        self.set_xy(10, 58)
        self.cell(0, 10, f'{name}', ln=True)
        
        self.set_font('Futura2', '', 11)
        y_place = 65  # Starting y position for multi-line place text
        for line in place.split('\n'):
            self.set_xy(10, y_place)
            self.cell(0, 10, line, ln=True)
            y_place += 7  # Adjust spacing between lines

        self.set_font('Futura', 'B', 13)
        self.set_xy(160, 51)
        self.cell(0, 10, f'{date}', ln=True)

        self.set_xy(160, 61.5)
        self.cell(0, 10, f'{reference}', ln=True)

        y_position = 95
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

            y_position += 7

        self.set_font('Futura', 'B', 16)
        self.set_xy(150, 156.5)
        self.cell(0, 10, f'RM {total_amount:.2f}', ln=True)

def create_invoice(date, name, place, reference, items, total_amount, output_file):
    background_image = 'template.png'  # Fixed background image
    pdf = InvoicePDF(background_image)
    pdf.add_page()
    pdf.invoice_body(date, name, place, reference, items, total_amount)
    pdf.output(output_file)

class InvoiceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Invoice Generator")
        self.geometry("400x500")
        self.items = []
        self.total_amount = 0

        # Input fields
        tk.Label(self, text="Date (dd/mm/yyyy)").pack()
        self.date_entry = tk.Entry(self)
        self.date_entry.pack()

        tk.Label(self, text="Name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Place (multi-line)").pack()
        self.place_text = tk.Text(self, height=4)  # Multi-line text box for place
        self.place_text.pack()

        tk.Label(self, text="Invoice Reference").pack()
        self.reference_entry = tk.Entry(self)
        self.reference_entry.pack()

        tk.Button(self, text="Add Item", command=self.add_item).pack()

        # Display added items
        self.items_listbox = tk.Listbox(self)
        self.items_listbox.pack()

        # Generate PDF button
        tk.Button(self, text="Generate Invoice", command=self.generate_invoice).pack()

    def add_item(self):
        item_window = tk.Toplevel(self)
        item_window.title("Add Item")
        item_window.geometry("300x200")

        tk.Label(item_window, text="Description").pack()
        description_entry = tk.Entry(item_window)
        description_entry.pack()

        tk.Label(item_window, text="Price (RM)").pack()
        price_entry = tk.Entry(item_window)
        price_entry.pack()

        tk.Label(item_window, text="Quantity").pack()
        quantity_entry = tk.Entry(item_window)
        quantity_entry.pack()

        def add_to_items():
            description = description_entry.get()
            price = float(price_entry.get())
            quantity = int(quantity_entry.get())

            item = {'description': description, 'price': price, 'quantity': quantity}
            self.items.append(item)
            self.total_amount += price * quantity

            self.items_listbox.insert(tk.END, f"{description} (x{quantity}) - RM{price:.2f}")
            item_window.destroy()

        tk.Button(item_window, text="Add", command=add_to_items).pack()

    def generate_invoice(self):
        date = self.date_entry.get()
        name = self.name_entry.get()
        place = self.place_text.get("1.0", tk.END).strip()  # Get multi-line text
        reference = self.reference_entry.get()

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Invoice As")

        if output_file and self.items:
            create_invoice(date, name, place, reference, self.items, self.total_amount, output_file)
            messagebox.showinfo("Success", "Invoice generated successfully!")
            self.reset_app()  # Reset the app fields after generating the invoice
        else:
            messagebox.showerror("Error", "Please fill all fields and add at least one item.")

    def reset_app(self):
        """Clear all fields and reset the item list and total amount."""
        self.date_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.place_text.delete("1.0", tk.END)
        self.reference_entry.delete(0, tk.END)
        self.items_listbox.delete(0, tk.END)
        self.items = []
        self.total_amount = 0

if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()