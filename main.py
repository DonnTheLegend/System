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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.data_file = "inventory_data.json"
        self.load_data()

        self.create_sidebar()
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

        # keep a master copy for searching
        self.all_inventory_data = list(self.inventory_data)

    def load_default_data(self):
        """Load default sample data"""
        self.inventory_data = []
        self.suppliers_data = []
        self.all_inventory_data = []

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
        quantity = item.get("quantity", 0)
        try:
            quantity = int(quantity)
        except Exception:
            quantity = 0
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

        # Logo
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
            ("🚪 Logout", self.logout)
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

        # Footer
        footer_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20, padx=20, fill="x")

        version_label = ctk.CTkLabel(
            footer_frame,
            text="ADMIN",
            font=("Arial", 15),
            text_color="#808080"
        )
        version_label.pack()

    def logout(self):
        self.quit()
        self.destroy()

    def create_main_content(self):
        """Create main content area"""
        main_frame = ctk.CTkFrame(self, fg_color="#0f0f0f")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.create_header(main_frame)

        # Content frame
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
            ("In Stock", str(sum(1 for item in self.inventory_data if item.get('status') == 'In Stock')), "#00cc88"),
            ("Low Stock", str(sum(1 for item in self.inventory_data if item.get('status') == 'Low Stock')), "#ffaa00"),
            ("Out of Stock", str(sum(1 for item in self.inventory_data if item.get('status') == 'Out of Stock')), "#ff5555"),
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
        header_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        header_frame.pack(fill="x", pady=(0, 10))

        if show_status:
            widths = [70, 150, 130, 80, 100, 100, 100]  # last is for Actions if editable
        else:
            widths = [90, 150, 120, 120, 120, 100]  # last is for Actions if editable

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

        table_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="#1a1a1a",
            corner_radius=10
        )
        table_scroll.pack(fill="both", expand=True)

        # Determine if this table is for suppliers (used to call supplier handlers)
        editing_suppliers = False
        if len(columns) > 0 and str(columns[0]).lower().startswith("supplier"):
            editing_suppliers = True

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

            # Build the values list depending on whether it's inventory or supplier
            if "status" in item and show_status:
                # Inventory item expected keys: id, name, category, quantity, price, status
                price_display = ""
                try:
                    price_display = f"₱{float(item.get('price', 0)):.2f}"
                except Exception:
                    price_display = str(item.get('price', ''))
                values = [
                    item.get("id", ""),
                    item.get("name", ""),
                    item.get("category", ""),
                    str(item.get("quantity", "")),
                    price_display,
                    item.get("status", "")
                ]
            else:
                # Supplier expected keys: id, name, contact, email, status
                values = [
                    item.get("id", ""),
                    item.get("name", ""),
                    item.get("contact", ""),
                    item.get("email", ""),
                    item.get("status", "")
                ]

            # zip values with widths and columns (columns is shorter than headers_to_show when editable)
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

            if editable:
                # choose appropriate handlers based on table type
                if editing_suppliers:
                    edit_cmd = (lambda i=item: self.edit_supplier(i))
                    del_cmd = (lambda i=item: self.delete_supplier(i))
                else:
                    edit_cmd = (lambda i=item: self.edit_item(i))
                    del_cmd = (lambda i=item: self.delete_item(i))

                edit_btn = ctk.CTkButton(
                    row_frame,
                    text="✏️ Edit",
                    font=("Arial", 10),
                    width=40,
                    height=25,
                    fg_color="#00a8ff",
                    hover_color="#0088cc",
                    command=edit_cmd
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
                    command=del_cmd
                )
                del_btn.pack(side="left", padx=5, pady=12)

    def show_section(self, section):
        """Show different sections"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # nice title case
        title_text = section.capitalize() if isinstance(section, str) else str(section)
        self.title_label.configure(text=title_text)

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
        self.create_stats_cards(self.content_frame)

        section_label = ctk.CTkLabel(
            self.content_frame,
            text="Inventory Overview",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(anchor="w", pady=(10, 15))

        self.create_inventory_table(
            self.content_frame,
            self.inventory_data,
            ["ID", "Product Name", "Category", "Quantity", "Price", "Status"]
        )

    def show_inventory(self):
        """Display inventory view"""
        controls_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        controls_frame.pack(fill="x", pady=(0, 15))

        section_label = ctk.CTkLabel(
            controls_frame,
            text="Full Inventory List",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(side="left", anchor="w")

        add_btn = ctk.CTkButton(
            controls_frame,
            text="➕ Add Product",
            font=("Arial", 12),
            fg_color="#00a8ff",
            hover_color="#0088cc",
            command=self.add_item_dialog
        )
        add_btn.pack(side="right", padx=5)

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

        # container for table, so we can rebuild it when searching
        self.inventory_table_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.inventory_table_frame.pack(fill="both", expand=True)

        self.create_inventory_table(
            self.inventory_table_frame,
            self.inventory_data,
            ["ID", "Product Name", "Category", "Quantity", "Price", "Status"],
            editable=True
        )

    def filter_inventory(self, *args):
        """Filter inventory based on search box"""
        query = self.search_var.get().strip().lower()

        if not hasattr(self, "all_inventory_data"):
            self.all_inventory_data = list(self.inventory_data)

        if query == "":
            filtered = self.all_inventory_data
        else:
            filtered = [
                item for item in self.all_inventory_data
                if query in str(item.get("id", "")).lower()
                or query in str(item.get("name", "")).lower()
            ]

        # clear and rebuild table
        for widget in self.inventory_table_frame.winfo_children():
            widget.destroy()

        self.create_inventory_table(
            self.inventory_table_frame,
            filtered,
            ["ID", "Product Name", "Category", "Quantity", "Price", "Status"],
            editable=True
        )

    def add_item_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Product")
        dialog.geometry("450x500")
        dialog.grab_set()

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
                    values=["Electronics", "Accessories", "Hardware"],
                    variable=var,
                    font=("Arial", 11)
                )
            else:
                entry = ctk.CTkEntry(dialog, textvariable=var, placeholder_text=f"Enter {field.lower()}",
                                     font=("Arial", 11))

            entry.pack(fill="x", padx=20, pady=5)

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
                self.all_inventory_data = list(self.inventory_data)
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
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Product")
        dialog.geometry("450x400")
        dialog.grab_set()

        fields = {
            "ID": ctk.StringVar(value=item.get("id", "")),
            "Product Name": ctk.StringVar(value=item.get("name", "")),
            "Category": ctk.StringVar(value=item.get("category", "")),
            "Quantity": ctk.StringVar(value=str(item.get("quantity", ""))),
            "Price": ctk.StringVar(value=str(item.get("price", ""))),
        }

        for i, (field, var) in enumerate(fields.items()):
            label = ctk.CTkLabel(dialog, text=field, font=("Arial", 12), text_color="#ffffff")
            label.pack(pady=(15 if i == 0 else 10, 5), padx=20, anchor="w")

            if field == "Category":
                entry = ctk.CTkOptionMenu(
                    dialog,
                    values=["Electronics", "Accessories", "Hardware"],
                    variable=var,
                    font=("Arial", 11)
                )
            else:
                entry = ctk.CTkEntry(dialog, textvariable=var, font=("Arial", 11))

            entry.pack(fill="x", padx=20, pady=5)

        def submit():
            try:
                # ID is not editable (kept for reference), but you can allow editing if needed
                item["name"] = fields["Product Name"].get()
                item["category"] = fields["Category"].get()
                item["quantity"] = int(fields["Quantity"].get())
                item["price"] = float(fields["Price"].get())
                self.update_status(item)
                self.save_data()
                # refresh master copy
                self.all_inventory_data = list(self.inventory_data)
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
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {item.get('name','this item')}?"):
            try:
                self.inventory_data.remove(item)
            except ValueError:
                # item not present
                pass
            self.save_data()
            self.all_inventory_data = list(self.inventory_data)
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.show_section("inventory")

    def show_reports(self):
        section_label = ctk.CTkLabel(
            self.content_frame,
            text="Reports",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(anchor="w", pady=(0, 15))

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

        output_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        output_frame.pack(fill="both", expand=True)

        output_label = ctk.CTkLabel(
            output_frame,
            text="Report Output",
            font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        output_label.pack(anchor="w", pady=(0, 10))

        self.report_text = ctk.CTkTextbox(
            output_frame,
            font=("Arial", 18),
            fg_color="#1a1a1a",
            text_color="#ffffff",
            height=300
        )
        self.report_text.pack(fill="both", expand=True)
        self.generate_report("Inventory Status")

    def generate_report(self, report_type):
        self.report_text.delete("1.0", "end")

        if report_type == "Inventory Status":
            report = "INVENTORY STATUS REPORT\n\n"
            for i, item in enumerate(self.inventory_data, start=1):
                report += f"═══════════════ ITEM #{i} ═══════════════\n"
                report += f"Name       : {item.get('name','')}\n"
                report += f"Category   : {item.get('category','')}\n"
                report += f"Quantity   : {item.get('quantity','')}\n"
                try:
                    price_str = f"₱{float(item.get('price',0)):.2f}"
                except Exception:
                    price_str = str(item.get('price',''))
                report += f"Price      : {price_str}\n"
                report += f"Status     : {item.get('status','')}\n"
                report += "────────────────────────────────────────────\n\n"

        elif report_type == "Low Stock Alert":
            low_stock = [item for item in self.inventory_data if item.get('status') == "Low Stock"]
            report = "LOW STOCK ALERT\n"
            report += "=" * 50 + "\n\n"
            if low_stock:
                for item in low_stock:
                    report += f"⚠️  {item.get('name','')} (ID: {item.get('id','')})\n"
                    report += f"Current Quantity: {item.get('quantity','')}\n"
                    try:
                        report += f"Price: ₱{float(item.get('price',0)):.2f}\n\n"
                    except Exception:
                        report += f"Price: {item.get('price','')}\n\n"
            else:
                report += "No low stock items found!"

        elif report_type == "Out of Stock Items":
            out_of_stock = [item for item in self.inventory_data if item.get('status') == "Out of Stock"]
            report = "OUT OF STOCK ITEMS\n"
            report += "=" * 50 + "\n\n"
            if out_of_stock:
                for item in out_of_stock:
                    report += f"❌ {item.get('name','')} (ID: {item.get('id','')})\n"
                    try:
                        report += f"Price: ₱{float(item.get('price',0)):.2f}\n"
                    except Exception:
                        report += f"Price: {item.get('price','')}\n"
                    report += f"Category: {item.get('category','')}\n\n"
            else:
                report += "No out of stock items!"

        elif report_type == "Total Inventory Value":
            total_value = sum((item.get('quantity', 0) or 0) * (item.get('price', 0) or 0) for item in self.inventory_data)
            report = "TOTAL INVENTORY VALUE REPORT\n"
            report += "=" * 50 + "\n\n"
            report += f"Total Products: {len(self.inventory_data)}\n"
            report += f"Total Units: {sum((item.get('quantity', 0) or 0) for item in self.inventory_data)}\n"
            try:
                report += f"Total Inventory Value: ₱{float(total_value):,.2f}\n\n"
            except Exception:
                report += f"Total Inventory Value: {total_value}\n\n"
            report += "BREAKDOWN BY CATEGORY:\n"
            categories = {}
            for item in self.inventory_data:
                cat = item.get('category', 'Uncategorized')
                categories.setdefault(cat, 0)
                qty = item.get('quantity', 0) or 0
                price = item.get('price', 0) or 0
                try:
                    categories[cat] += float(qty) * float(price)
                except Exception:
                    pass
            for cat, value in categories.items():
                try:
                    report += f"{cat}: ₱{float(value):,.2f}\n"
                except Exception:
                    report += f"{cat}: {value}\n"

        self.report_text.insert("1.0", report)

    def show_suppliers(self):
        controls_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        controls_frame.pack(fill="x", pady=(0, 15))

        section_label = ctk.CTkLabel(
            controls_frame,
            text="Supplier Management",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        section_label.pack(side="left", anchor="w")

        add_btn = ctk.CTkButton(
            controls_frame,
            text="➕ Add Supplier",
            font=("Arial", 12),
            fg_color="#00a8ff",
            hover_color="#0088cc",
            command=self.add_supplier_dialog
        )
        add_btn.pack(side="right", padx=5)

        # supplier table
        self.create_inventory_table(
            self.content_frame,
            self.suppliers_data,
            ["Supplier ID", "Name", "Contact", "Email", "Status"],
            show_status=False,
            editable=True
        )

    def add_supplier_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Supplier")
        dialog.geometry("450x450")
        dialog.grab_set()

        fields = {
            "ID": ctk.StringVar(),
            "Name": ctk.StringVar(),
            "Contact": ctk.StringVar(),
            "Email": ctk.StringVar(),
            "Status": ctk.StringVar(value="Active")
        }

        for i, (field, var) in enumerate(fields.items()):
            label = ctk.CTkLabel(dialog, text=field, font=("Arial", 12), text_color="#ffffff")
            label.pack(pady=(15 if i == 0 else 10, 5), padx=20, anchor="w")

            if field == "Status":
                entry = ctk.CTkOptionMenu(
                    dialog,
                    values=["Active", "Inactive"],
                    variable=var,
                    font=("Arial", 11)
                )
            else:
                entry = ctk.CTkEntry(
                    dialog,
                    textvariable=var,
                    placeholder_text=f"Enter {field.lower()}",
                    font=("Arial", 11)
                )
            entry.pack(fill="x", padx=20, pady=5)

        def submit():
            new_supplier = {
                "id": fields["ID"].get(),
                "name": fields["Name"].get(),
                "contact": fields["Contact"].get(),
                "email": fields["Email"].get(),
                "status": fields["Status"].get()
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

    def edit_supplier(self, supplier):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Supplier")
        dialog.geometry("450x450")
        dialog.grab_set()

        fields = {
            "Name": ctk.StringVar(value=supplier.get("name", "")),
            "Contact": ctk.StringVar(value=supplier.get("contact", "")),
            "Email": ctk.StringVar(value=supplier.get("email", "")),
            "Status": ctk.StringVar(value=supplier.get("status", "Active"))
        }

        for i, (field, var) in enumerate(fields.items()):
            label = ctk.CTkLabel(dialog, text=field, font=("Arial", 12), text_color="#ffffff")
            label.pack(pady=(15 if i == 0 else 10, 5), padx=20, anchor="w")

            if field == "Status":
                entry = ctk.CTkOptionMenu(
                    dialog,
                    values=["Active", "Inactive"],
                    variable=var,
                    font=("Arial", 11)
                )
            else:
                entry = ctk.CTkEntry(dialog, textvariable=var, font=("Arial", 11))

            entry.pack(fill="x", padx=20, pady=5)

        def submit():
            supplier["name"] = fields["Name"].get()
            supplier["contact"] = fields["Contact"].get()
            supplier["email"] = fields["Email"].get()
            supplier["status"] = fields["Status"].get()

            self.save_data()
            messagebox.showinfo("Success", "Supplier updated successfully!")
            dialog.destroy()
            self.show_section("suppliers")

        submit_btn = ctk.CTkButton(
            dialog,
            text="Update Supplier",
            command=submit,
            fg_color="#00a8ff",
            hover_color="#0088cc",
            font=("Arial", 12)
        )
        submit_btn.pack(pady=20, padx=20, fill="x")

    def delete_supplier(self, supplier):
        if messagebox.askyesno("Confirm Delete", f"Delete supplier {supplier.get('name', '')}?"):
            try:
                self.suppliers_data.remove(supplier)
            except ValueError:
                pass
            self.save_data()
            messagebox.showinfo("Success", "Supplier deleted successfully!")
            self.show_section("suppliers")


if __name__ == "__main__":
    app = InventoryDashboard()
    app.mainloop()
