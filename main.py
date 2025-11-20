import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import datetime
import json
import os

# Set appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class InventoryDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HardTrack")
        self.geometry("1240x700")

        # Configure grid weights for responsiveness
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Data file for persistence
        self.data_file = "inventory_data.json"
        self.load_data()

        # Create sidebar
        self.create_sidebar()

        # Create main content area
        self.create_main_content()

    def load_data(self):
        """Load data from JSON file or use default sample data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.inventory_data = data.get("inventory", [])
                    self.suppliers_data = data.get("suppliers", [])
            except:
                self.load_default_data()
        else:
            self.load_default_data()

    def load_default_data(self):
        """Load default sample data"""
        self.inventory_data = [
            {"id": "P001", "name": "Laptop", "category": "Electronics", "quantity": 15, "price": 899.99,
             "status": "In Stock"},
            {"id": "P002", "name": "Monitor", "category": "Electronics", "quantity": 3, "price": 299.99,
             "status": "Low Stock"},
            {"id": "P003", "name": "Keyboard", "category": "Accessories", "quantity": 0, "price": 79.99,
             "status": "Out of Stock"},
            {"id": "P004", "name": "Mouse", "category": "Accessories", "quantity": 45, "price": 29.99,
             "status": "In Stock"},
            {"id": "P005", "name": "USB Cable", "category": "Accessories", "quantity": 120, "price": 9.99,
             "status": "In Stock"},
            {"id": "P006", "name": "Headphones", "category": "Electronics", "quantity": 8, "price": 149.99,
             "status": "Low Stock"},
            {"id": "P007", "name": "Webcam", "category": "Electronics", "quantity": 25, "price": 79.99,
             "status": "In Stock"},
            {"id": "P008", "name": "Monitor Stand", "category": "Accessories", "quantity": 0, "price": 39.99,
             "status": "Out of Stock"},
        ]

        self.suppliers_data = [
            {"id": "101", "name": "ABC Electronics", "contact": "09171234567", "email": "contact@abcelectronics.com",
             "status": "Active"},
            {"id": "102", "name": "Tech Supplies Co.", "contact": "09281234567", "email": "info@techsupplies.com",
             "status": "Active"},
            {"id": "103", "name": "Gadgets Plus", "contact": "09391234567", "email": "sales@gadgetsplus.com",
             "status": "Inactive"},
            {"id": "104", "name": "Digital World", "contact": "09501234567", "email": "support@digitalworld.com",
             "status": "Active"},
            {"id": "105", "name": "Premium Components", "contact": "09611234567", "email": "sales@premiumcomp.com",
             "status": "Active"},
        ]

    def save_data(self):
        """Save data to JSON file"""
        data = {
            "inventory": self.inventory_data,
            "suppliers": self.suppliers_data
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def update_status(self, item):
        """Auto-update status based on quantity"""
        quantity = item["quantity"]
        if quantity == 0:
            item["status"] = "Out of Stock"
        elif quantity <= 10:
            item["status"] = "Low Stock"
        else:
            item["status"] = "In Stock"

    def create_sidebar(self):
        """Create left sidebar with navigation"""
        sidebar = ctk.CTkFrame(self, fg_color="#1e1e1e", width=250)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_propagate(False)

        # Logo section
        logo_label = ctk.CTkLabel(
            sidebar,
            text="📦 HardTrack",
            font=("Arial", 20, "bold"),
            text_color="#00a8ff"
        )
        logo_label.pack(pady=20, padx=20)

        # Separator
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#404040")
        separator.pack(fill="x", padx=20, pady=10)

        # Navigation buttons
        nav_items = [
            ("📊 Dashboard", lambda: self.show_section("dashboard")),
            ("📦 Inventory", lambda: self.show_section("inventory")),
            ("📈 Reports", lambda: self.show_section("reports")),
            ("🏢 Suppliers", lambda: self.show_section("suppliers")),
        ]

        for text, command in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Arial", 14),
                command=command,
                fg_color="#2d2d2d",
                hover_color="#3d3d3d",
                text_color="#ffffff",
                height=40
            )
            btn.pack(fill="x", padx=15, pady=8)

        # Footer info
        footer_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20, padx=20, fill="x")

    def create_main_content(self):
        """Create main content area"""
        main_frame = ctk.CTkFrame(self, fg_color="#0f0f0f")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.create_header(main_frame)

        # Content area
        self.content_frame = ctk.CTkFrame(main_frame, fg_color="#0f0f0f")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Show dashboard by default
        self.show_section("dashboard")

    def create_header(self, parent):
        """Create top header with title and stats"""
        header = ctk.CTkFrame(parent, fg_color="#1a1a1a", height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_propagate(False)

        # Title
        self.title_label = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=("Arial", 28, "bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(side="left", padx=20, pady=20)

        # Date/Time
        time_label = ctk.CTkLabel(
            header,
            text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            font=("Arial", 12),
            text_color="#808080"
        )
        time_label.pack(side="right", padx=20, pady=20)

    def create_stats_cards(self, parent):
        """Create statistics cards"""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))

        stats = [
            ("Total Products", str(len(self.inventory_data)), "#00a8ff"),
            ("In Stock", str(sum(1 for item in self.inventory_data if item['status'] == 'In Stock')), "#00cc88"),
            ("Low Stock", str(sum(1 for item in self.inventory_data if item['status'] == 'Low Stock')), "#ffaa00"),
            ("Out of Stock", str(sum(1 for item in self.inventory_data if item['status'] == 'Out of Stock')), "#ff5555"),
        ]

        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(cards_frame, fg_color="#1a1a1a", corner_radius=10)
            card.pack(side="left", fill="both", expand=True, padx=(0, 15) if i < 3 else 0)

            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 32, "bold"),
                text_color=color
            )
            value_label.pack(pady=(15, 5), padx=20)

            name_label = ctk.CTkLabel(
                card,
                text=label,
                font=("Arial", 12),
                text_color="#808080"
            )
            name_label.pack(pady=(0, 15), padx=20)

    def create_inventory_table(self, parent, data, columns, show_status=True, editable=False):
        """Create inventory table display with optional edit/delete buttons"""
        # Table header
        header_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        header_frame.pack(fill="x", pady=(0, 10))

        if show_status:
            widths = [70, 150, 130, 80, 100, 100, 100]
        else:
            widths = [90, 150, 120, 120, 120, 100]

        headers_to_show = columns + (["Actions"] if editable else [])

        for header, width in zip(headers_to_show, widths):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#00a8ff",
                width=width
            )
            label.pack(side="left", padx=10, pady=10)

        # Scrollable content frame
        table_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="#1a1a1a",
            corner_radius=10
        )
        table_scroll.pack(fill="both", expand=True)

        # Table rows
        for item in data:
            row_frame = ctk.CTkFrame(table_scroll, fg_color="#252525", corner_radius=5)
            row_frame.pack(fill="x", padx=5, pady=5)

            status_color_map = {
                "In Stock": "#00cc88",
                "Low Stock": "#ffaa00",
                "Out of Stock": "#ff5555",
                "Active": "#00cc88",
                "Inactive": "#ff5555"
            }

            # Prepare values based on data type
            if "status" in item and show_status:
                values = [item.get("id", ""), item.get("name", ""), item.get("category", ""),
                          str(item.get("quantity", "")), f"${item['price']:.2f}", item["status"]]
            else:
                values = [item.get("id", ""), item.get("name", ""), item.get("contact", ""),
                          item.get("email", ""), item["status"]]

            for value, width, header in zip(values, widths, columns):
                if header == "Status":
                    color = status_color_map.get(value, "#ffffff")
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        font=("Arial", 11),
                        text_color=color,
                        width=width
                    )
                else:
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        font=("Arial", 11),
                        text_color="#ffffff",
                        width=width
                    )
                label.pack(side="left", padx=10, pady=12)

            # Add action buttons if editable
            if editable:
                edit_btn = ctk.CTkButton(
                    row_frame,
                    text="✏️ Edit",
                    font=("Arial", 10),
                    width=40,
                    height=25,
                    fg_color="#00a8ff",
                    hover_color="#0088cc",
                    command=lambda i=item: self.edit_item(i)
                )
                edit_btn.pack(side="left", padx=5, pady=12)

                del_btn = ctk.CTkButton(
                    row_frame,
                    text="🗑️ Delete",
                    font=("Arial", 10),
                    width=40,
                    height=25,
                    fg_color="#ff5555",
                    hover_color="#cc4444",
                    command=lambda i=item: self.delete_item(i)
                )
                del_btn.pack(side="left", padx=5, pady=12)

    def show_section(self, section):
        """Show different sections"""
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.configure(text=section.capitalize())

        if section == "dashboard":
            self.show_dashboard()
        elif section == "inventory":
            self.show_inventory()
        elif section == "reports":
            self.show_reports()
        elif section == "suppliers":
            self.show_suppliers()

    def show_dashboard(self):
        """Display dashboard view"""
        # Stats cards
        self.create_stats_cards(self.content_frame)

        # Section label
        section_label = ctk.CTkLabel(
            self.content_frame,
            text="Inventory Overview",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(anchor="w", pady=(10, 15))

        # Inventory table
        self.create_inventory_table(self.content_frame, self.inventory_data,
                                    ["ID", "Product Name", "Category", "Quantity", "Price", "Status"])

    def show_inventory(self):
        """Display inventory view"""
        # Top controls frame
        controls_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        controls_frame.pack(fill="x", pady=(0, 15))

        section_label = ctk.CTkLabel(
            controls_frame,
            text="Full Inventory List",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(side="left", anchor="w")

        # Add item button
        add_btn = ctk.CTkButton(
            controls_frame,
            text="➕ Add Product",
            font=("Arial", 12),
            fg_color="#00a8ff",
            hover_color="#0088cc",
            command=self.add_item_dialog
        )
        add_btn.pack(side="right", padx=5)

        # Search box
        search_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=10)

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=("Arial", 12),
            text_color="#ffffff"
        )
        search_label.pack(side="left", padx=5)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Product name or ID",
            font=("Arial", 11),
            width=200
        )
        search_entry.pack(side="left", padx=5)
        self.search_var.trace("w", self.filter_inventory)

        # Inventory table with edit/delete
        self.create_inventory_table(self.content_frame, self.inventory_data,
                                    ["ID", "Product Name", "Category", "Quantity", "Price", "Status"],
                                    editable=True)

    def filter_inventory(self, *args):
        """Filter inventory based on search"""
        # This would require refreshing the table - for now, it's a placeholder
        pass

    def add_item_dialog(self):
        """Show dialog to add new product"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Product")
        dialog.geometry("450x430")
        dialog.grab_set()
        dialog.resizable(False, False)

        # Form fields
        fields = {
            "ID": ctk.StringVar(),
            "Product Name": ctk.StringVar(),
            "Category": ctk.StringVar(),
            "Quantity": ctk.StringVar(),
            "Price": ctk.StringVar(),
        }

        for i, (field, var) in enumerate(fields.items()):
            label = ctk.CTkLabel(dialog, text=field, font=("Arial", 12), text_color="#ffffff")
            label.pack(pady=(15 if i == 0 else 10, 5), padx=20, anchor="w")

            if field == "Category":
                entry = ctk.CTkOptionMenu(
                    dialog,
                    values=["Electronics", "Accessories", "Software", "Hardware"],
                    variable=var,
                    font=("Arial", 11)
                )
            else:
                entry = ctk.CTkEntry(dialog, textvariable=var, placeholder_text=f"Enter {field.lower()}",
                                     font=("Arial", 11))

            entry.pack(fill="x", padx=20, pady=5)

        # Submit button
        def submit():
            try:
                new_item = {
                    "id": fields["ID"].get(),
                    "name": fields["Product Name"].get(),
                    "category": fields["Category"].get(),
                    "quantity": int(fields["Quantity"].get()),
                    "price": float(fields["Price"].get()),
                    "status": "In Stock"
                }

                if not new_item["id"] or not new_item["name"]:
                    messagebox.showerror("Error", "ID and Product Name are required!")
                    return

                self.update_status(new_item)
                self.inventory_data.append(new_item)
                self.save_data()
                messagebox.showinfo("Success", "Product added successfully!")
                dialog.destroy()
                self.show_section("inventory")
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number and Price must be a decimal!")

        submit_btn = ctk.CTkButton(
            dialog,
            text="Add Product",
            command=submit,
            fg_color="#00a8ff",
            hover_color="#0088cc",
            font=("Arial", 12)
        )
        submit_btn.pack(pady=20, padx=20, fill="x")

    def edit_item(self, item):
        """Show dialog to edit product"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Product")
        dialog.geometry("450x400")
        dialog.grab_set()

        fields = {
            "ID": ctk.StringVar(value=item["id"]),
            "Product Name": ctk.StringVar(value=item["name"]),
            "Category": ctk.StringVar(value=item["category"]),
            "Quantity": ctk.StringVar(value=str(item["quantity"])),
            "Price": ctk.StringVar(value=str(item["price"])),
        }

        for i, (field, var) in enumerate(fields.items()):
            label = ctk.CTkLabel(dialog, text=field, font=("Arial", 12), text_color="#ffffff")
            label.pack(pady=(15 if i == 0 else 10, 5), padx=20, anchor="w")

            if field == "Category":
                entry = ctk.CTkOptionMenu(
                    dialog,
                    values=["Electronics", "Accessories", "Software", "Hardware"],
                    variable=var,
                    font=("Arial", 11)
                )
            else:
                entry = ctk.CTkEntry(dialog, textvariable=var, font=("Arial", 11))

            entry.pack(fill="x", padx=20, pady=5)

        def submit():
            try:
                item["name"] = fields["Product Name"].get()
                item["category"] = fields["Category"].get()
                item["quantity"] = int(fields["Quantity"].get())
                item["price"] = float(fields["Price"].get())
                self.update_status(item)
                self.save_data()
                messagebox.showinfo("Success", "Product updated successfully!")
                dialog.destroy()
                self.show_section("inventory")
            except ValueError:
                messagebox.showerror("Error", "Invalid input values!")

        submit_btn = ctk.CTkButton(
            dialog,
            text="Update Product",
            command=submit,
            fg_color="#00a8ff",
            hover_color="#0088cc",
            font=("Arial", 12)
        )
        submit_btn.pack(pady=20, padx=20, fill="x")

    def delete_item(self, item):
        """Delete product with confirmation"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {item['name']}?"):
            self.inventory_data.remove(item)
            self.save_data()
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.show_section("inventory")

    def show_reports(self):
        """Display reports view"""
        # Section label
        section_label = ctk.CTkLabel(
            self.content_frame,
            text="Reports",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(anchor="w", pady=(0, 15))

        # Report selector frame
        selector_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a1a", corner_radius=10)
        selector_frame.pack(fill="x", pady=(0, 20))

        label = ctk.CTkLabel(
            selector_frame,
            text="Select Report Type:",
            font=("Arial", 14),
            text_color="#ffffff"
        )
        label.pack(side="left", padx=15, pady=15)

        self.report_menu = ctk.CTkOptionMenu(
            selector_frame,
            values=["Inventory Status", "Low Stock Alert", "Out of Stock Items", "Total Inventory Value"],
            font=("Arial", 12),
            command=self.generate_report
        )
        self.report_menu.pack(side="left", padx=10, pady=15)
        self.report_menu.set("Inventory Status")

        # Report output area
        output_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        output_frame.pack(fill="both", expand=True)

        output_label = ctk.CTkLabel(
            output_frame,
            text="Report Output",
            font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        output_label.pack(anchor="w", pady=(0, 10))

        # Text area for report
        self.report_text = ctk.CTkTextbox(
            output_frame,
            font=("Arial", 11),
            fg_color="#1a1a1a",
            text_color="#ffffff",
            height=300
        )
        self.report_text.pack(fill="both", expand=True)
        self.generate_report("Inventory Status")

    def generate_report(self, report_type):
        """Generate different types of reports"""
        self.report_text.delete("1.0", "end")

        if report_type == "Inventory Status":
            report = "INVENTORY STATUS REPORT\n"
            report += "=" * 50 + "\n\n"
            for item in self.inventory_data:
                report += f"ID: {item['id']} | {item['name']}\n"
                report += f"Category: {item['category']} | Qty: {item['quantity']} | Price: ${item['price']:.2f}\n"
                report += f"Status: {item['status']}\n\n"

        elif report_type == "Low Stock Alert":
            low_stock = [item for item in self.inventory_data if item['status'] == "Low Stock"]
            report = "LOW STOCK ALERT\n"
            report += "=" * 50 + "\n\n"
            if low_stock:
                for item in low_stock:
                    report += f"⚠️  {item['name']} (ID: {item['id']})\n"
                    report += f"Current Quantity: {item['quantity']}\n"
                    report += f"Price: ${item['price']:.2f}\n\n"
            else:
                report += "No low stock items found!"

        elif report_type == "Out of Stock Items":
            out_of_stock = [item for item in self.inventory_data if item['status'] == "Out of Stock"]
            report = "OUT OF STOCK ITEMS\n"
            report += "=" * 50 + "\n\n"
            if out_of_stock:
                for item in out_of_stock:
                    report += f"❌ {item['name']} (ID: {item['id']})\n"
                    report += f"Price: ${item['price']:.2f}\n"
                    report += f"Category: {item['category']}\n\n"
            else:
                report += "No out of stock items!"

        elif report_type == "Total Inventory Value":
            total_value = sum(item['quantity'] * item['price'] for item in self.inventory_data)
            report = "TOTAL INVENTORY VALUE REPORT\n"
            report += "=" * 50 + "\n\n"
            report += f"Total Products: {len(self.inventory_data)}\n"
            report += f"Total Units: {sum(item['quantity'] for item in self.inventory_data)}\n"
            report += f"Total Inventory Value: ${total_value:,.2f}\n\n"
            report += "BREAKDOWN BY CATEGORY:\n"
            categories = {}
            for item in self.inventory_data:
                cat = item['category']
                if cat not in categories:
                    categories[cat] = 0
                categories[cat] += item['quantity'] * item['price']
            for cat, value in categories.items():
                report += f"{cat}: ${value:,.2f}\n"

        self.report_text.insert("1.0", report)

    def show_suppliers(self):
        """Display suppliers view"""
        # Top controls frame
        controls_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        controls_frame.pack(fill="x", pady=(0, 15))

        section_label = ctk.CTkLabel(
            controls_frame,
            text="Supplier Management",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(side="left", anchor="w")

        # Add supplier button
        add_btn = ctk.CTkButton(
            controls_frame,
            text="➕ Add Supplier",
            font=("Arial", 12),
            fg_color="#00a8ff",
            hover_color="#0088cc",
            command=self.add_supplier_dialog
        )
        add_btn.pack(side="right", padx=5)

        # Suppliers table with edit/delete
        self.create_inventory_table(self.content_frame, self.suppliers_data,
                                    ["Supplier ID", "Name", "Contact", "Email", "Status"],
                                    show_status=False, editable=True)

    def add_supplier_dialog(self):
        """Show dialog to add new supplier"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Supplier")
        dialog.geometry("450x400")
        dialog.grab_set()

        fields = {
            "ID": ctk.StringVar(),
            "Name": ctk.StringVar(),
            "Contact": ctk.StringVar(),
            "Email": ctk.StringVar(),
        }

        for i, (field, var) in enumerate(fields.items()):
            label = ctk.CTkLabel(dialog, text=field, font=("Arial", 12), text_color="#ffffff")
            label.pack(pady=(15 if i == 0 else 10, 5), padx=20, anchor="w")

            entry = ctk.CTkEntry(dialog, textvariable=var, placeholder_text=f"Enter {field.lower()}",
                                font=("Arial", 11))
            entry.pack(fill="x", padx=20, pady=5)

        # Status
        label = ctk.CTkLabel(dialog, text="Status", font=("Arial", 12), text_color="#ffffff")
        label.pack(pady=10, padx=20, anchor="w")

        status_var = ctk.StringVar(value="Active")
        status_menu = ctk.CTkOptionMenu(
            dialog,
            values=["Active", "Inactive"],
            variable=status_var,
            font=("Arial", 11)
        )
        status_menu.pack(fill="x", padx=20, pady=5)

        def submit():
            new_supplier = {
                "id": fields["ID"].get(),
                "name": fields["Name"].get(),
                "contact": fields["Contact"].get(),
                "email": fields["Email"].get(),
                "status": status_var.get()
            }

            if not new_supplier["id"] or not new_supplier["name"]:
                messagebox.showerror("Error", "ID and Name are required!")
                return

            self.suppliers_data.append(new_supplier)
            self.save_data()
            messagebox.showinfo("Success", "Supplier added successfully!")
            dialog.destroy()
            self.show_section("suppliers")

        submit_btn = ctk.CTkButton(
            dialog,
            text="Add Supplier",
            command=submit,
            fg_color="#00a8ff",
            hover_color="#0088cc",
            font=("Arial", 12)
        )
        submit_btn.pack(pady=20, padx=20, fill="x")

if __name__ == "__main__":
    app = InventoryDashboard()
    app.mainloop()
