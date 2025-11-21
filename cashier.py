import customtkinter as ctk
from datetime import datetime
import json
import os
import tkinter.messagebox as messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CashierApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HardTrack - Cashier Panel")
        self.geometry("1200x810")

        # Data files
        self.inventory_file = "inventory_data.json"
        self.transaction_file = "transactions.json"

        self.cart = []
        self.inventory_data = []

        # Load inventory data
        self.load_inventory()

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create UI
        self.create_ui()

    def load_inventory(self):
        """Load inventory from shared JSON file"""
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, 'r') as f:
                    data = json.load(f)
                    self.inventory_data = data.get("inventory", [])
            except:
                self.load_default_inventory()
        else:
            self.load_default_inventory()

    def load_default_inventory(self):
        """Load default inventory"""
        self.inventory_data = [
        ]

    def create_ui(self):
        """Create main UI"""
        main_frame = ctk.CTkFrame(self, fg_color="#0f0f0f")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.create_header(main_frame)

        # Content
        content_frame = ctk.CTkFrame(main_frame, fg_color="#0f0f0f")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=0)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left - Products
        self.create_products_section(content_frame)

        # Right - Cart
        self.create_cart_section(content_frame)

    def create_header(self, parent):
        """Create header"""
        header = ctk.CTkFrame(parent, fg_color="#1a1a1a", height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="💳 HardTrack Cashier",
            font=("Arial", 28, "bold"),
            text_color="#00a8ff"
        )
        title.pack(side="left", padx=20, pady=20)

        time_label = ctk.CTkLabel(
            header,
            text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            font=("Arial", 12),
            text_color="#808080"
        )
        time_label.pack(side="right", padx=20, pady=20)

    def create_products_section(self, parent):
        """Create products section"""
        products_frame = ctk.CTkFrame(parent, fg_color="transparent")
        products_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        products_frame.grid_rowconfigure(2, weight=1)
        products_frame.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(
            products_frame,
            text="Available Products",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Search
        search_frame = ctk.CTkFrame(products_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=("Arial", 12),
            text_color="#ffffff"
        )
        search_label.pack(side="left", padx=(0, 10))

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Product ID or Name",
            font=("Arial", 11),
            width=250
        )
        search_entry.pack(side="left", fill="x", expand=True)
        self.search_var.trace("w", lambda *args: self.update_products_display())

        # Products scroll
        self.products_scroll = ctk.CTkScrollableFrame(
            products_frame,
            fg_color="#1a1a1a",
            corner_radius=10
        )
        self.products_scroll.grid(row=2, column=0, sticky="nsew")
        self.products_scroll.grid_columnconfigure(0, weight=1)

        self.update_products_display()

    def update_products_display(self):
        """Update products display based on search"""
        # Clear
        for widget in self.products_scroll.winfo_children():
            widget.destroy()

        search_text = self.search_var.get().lower()

        for item in self.inventory_data:
            # Filter by search
            if search_text and search_text not in item['id'].lower() and search_text not in item['name'].lower():
                continue

            # Skip out of stock
            if item['status'] == 'Out of Stock':
                continue

            self.create_product_card(self.products_scroll, item)

    def create_product_card(self, parent, item):
        """Create product card"""
        card = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=8)
        card.pack(fill="x", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        # Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=12)

        # Name and ID
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"🛍️ {item['name']} ({item['id']})",
            font=("Arial", 13, "bold"),
            text_color="#ffffff"
        )
        name_label.pack(anchor="w", pady=(0, 5))

        # Category and quantity
        details_label = ctk.CTkLabel(
            info_frame,
            text=f"{item['category']} | Available: {item['quantity']} | Price: ${item['price']:.2f}",
            font=("Arial", 11),
            text_color="#808080"
        )
        details_label.pack(anchor="w")

        # Add button
        add_btn = ctk.CTkButton(
            card,
            text="Add",
            font=("Arial", 12, "bold"),
            width=80,
            height=35,
            fg_color="#00a8ff",
            hover_color="#0088cc",
            command=lambda: self.add_to_cart(item)
        )
        add_btn.pack(side="right", padx=15, pady=12)

    def create_cart_section(self, parent):
        """Create cart section"""
        cart_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=12, width=300)
        cart_frame.grid(row=0, column=1, sticky="nsew")
        cart_frame.grid_propagate(False)
        cart_frame.grid_rowconfigure(2, weight=1)

        # Title
        title = ctk.CTkLabel(
            cart_frame,
            text="🛒 Shopping Cart",
            font=("Arial", 18, "bold"),
            text_color="#00a8ff"
        )
        title.pack(pady=15, padx=15, anchor="w")

        # Item count
        self.items_label = ctk.CTkLabel(
            cart_frame,
            text="Items: 0",
            font=("Arial", 11),
            text_color="#808080"
        )
        self.items_label.pack(padx=15, anchor="w", pady=(0, 10))

        # Cart items scroll
        self.cart_scroll = ctk.CTkScrollableFrame(
            cart_frame,
            fg_color="#252525",
            corner_radius=8
        )
        self.cart_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Divider
        divider = ctk.CTkFrame(cart_frame, height=2, fg_color="#404040")
        divider.pack(fill="x", padx=15, pady=(0, 10))

        # Totals
        totals_frame = ctk.CTkFrame(cart_frame, fg_color="transparent")
        totals_frame.pack(fill="x", padx=15, pady=10)

        # Subtotal
        subtotal_lbl = ctk.CTkLabel(
            totals_frame,
            text="Subtotal:",
            font=("Arial", 12),
            text_color="#808080"
        )
        subtotal_lbl.pack(anchor="w")
        self.subtotal_val = ctk.CTkLabel(
            totals_frame,
            text="$0.00",
            font=("Arial", 12, "bold"),
            text_color="#ffffff"
        )
        self.subtotal_val.pack(anchor="e", pady=(0, 8))

        # Tax
        tax_lbl = ctk.CTkLabel(
            totals_frame,
            text="Tax (12%):",
            font=("Arial", 12),
            text_color="#808080"
        )
        tax_lbl.pack(anchor="w")
        self.tax_val = ctk.CTkLabel(
            totals_frame,
            text="$0.00",
            font=("Arial", 12, "bold"),
            text_color="#ffffff"
        )
        self.tax_val.pack(anchor="e", pady=(0, 10))

        # Total divider
        divider2 = ctk.CTkFrame(totals_frame, height=1, fg_color="#404040")
        divider2.pack(fill="x", pady=(0, 10))

        # Grand Total
        total_lbl = ctk.CTkLabel(
            totals_frame,
            text="TOTAL:",
            font=("Arial", 13, "bold"),
            text_color="#00a8ff"
        )
        total_lbl.pack(anchor="w")
        self.total_val = ctk.CTkLabel(
            totals_frame,
            text="$0.00",
            font=("Arial", 15, "bold"),
            text_color="#00cc88"
        )
        self.total_val.pack(anchor="e")

        # Buttons
        button_frame = ctk.CTkFrame(cart_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=15)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear Cart",
            font=("Arial", 12),
            fg_color="#ff5555",
            hover_color="#cc4444",
            command=self.clear_cart
        )
        clear_btn.pack(fill="x", pady=(0, 8))

        checkout_btn = ctk.CTkButton(
            button_frame,
            text="💰 Checkout",
            font=("Arial", 13, "bold"),
            fg_color="#00cc88",
            hover_color="#00aa66",
            command=self.checkout
        )
        checkout_btn.pack(fill="x")

    def add_to_cart(self, item):
        """Add item to cart"""
        # Check if already in cart
        for cart_item in self.cart:
            if cart_item['id'] == item['id']:
                if cart_item['qty'] < item['quantity']:
                    cart_item['qty'] += 1
                else:
                    messagebox.showwarning("Stock Limit", f"Only {item['quantity']} available!")
                self.update_cart_display()
                return

        # Add new item
        self.cart.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'qty': 1,
            'max_qty': item['quantity']
        })

        self.update_cart_display()

    def update_cart_display(self):
        """Update cart display"""
        # Clear
        for widget in self.cart_scroll.winfo_children():
            widget.destroy()

        if not self.cart:
            empty = ctk.CTkLabel(
                self.cart_scroll,
                text="Cart is empty",
                font=("Arial", 12),
                text_color="#808080"
            )
            empty.pack(pady=30)
        else:
            for cart_item in self.cart:
                self.create_cart_item(self.cart_scroll, cart_item)

        # Update totals
        self.update_totals()

    def create_cart_item(self, parent, cart_item):
        """Create cart item"""
        item_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=6)
        item_frame.pack(fill="x", padx=5, pady=5)
        item_frame.grid_columnconfigure(0, weight=1)

        # Info
        info_label = ctk.CTkLabel(
            item_frame,
            text=f"{cart_item['name']}\n${cart_item['price']:.2f} × {cart_item['qty']} = ${cart_item['price'] * cart_item['qty']:.2f}",
            font=("Arial", 10),
            text_color="#ffffff",
            justify="left"
        )
        info_label.pack(anchor="w", padx=10, pady=(8, 5), side="left", expand=True)

        # Qty controls
        qty_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        qty_frame.pack(side="right", padx=8, pady=8)

        minus_btn = ctk.CTkButton(
            qty_frame,
            text="−",
            font=("Arial", 11, "bold"),
            width=28,
            height=28,
            fg_color="#ff5555",
            hover_color="#cc4444",
            command=lambda: self.decrease_qty(cart_item)
        )
        minus_btn.pack(side="left", padx=2)

        qty_display = ctk.CTkLabel(
            qty_frame,
            text=str(cart_item['qty']),
            font=("Arial", 11, "bold"),
            text_color="#ffffff",
            width=25
        )
        qty_display.pack(side="left", padx=4)

        plus_btn = ctk.CTkButton(
            qty_frame,
            text="+",
            font=("Arial", 11, "bold"),
            width=28,
            height=28,
            fg_color="#00a8ff",
            hover_color="#0088cc",
            command=lambda: self.increase_qty(cart_item)
        )
        plus_btn.pack(side="left", padx=2)

        del_btn = ctk.CTkButton(
            qty_frame,
            text="✕",
            font=("Arial", 10),
            width=28,
            height=28,
            fg_color="#808080",
            hover_color="#606060",
            command=lambda: self.remove_from_cart(cart_item)
        )
        del_btn.pack(side="left", padx=2)

    def increase_qty(self, cart_item):
        """Increase quantity"""
        if cart_item['qty'] < cart_item['max_qty']:
            cart_item['qty'] += 1
            self.update_cart_display()
        else:
            messagebox.showwarning("Stock Limit", f"Only {cart_item['max_qty']} available!")

    def decrease_qty(self, cart_item):
        """Decrease quantity"""
        if cart_item['qty'] > 1:
            cart_item['qty'] -= 1
        else:
            self.remove_from_cart(cart_item)
        self.update_cart_display()

    def remove_from_cart(self, cart_item):
        """Remove from cart"""
        self.cart = [item for item in self.cart if item['id'] != cart_item['id']]
        self.update_cart_display()

    def clear_cart(self):
        """Clear cart"""
        if messagebox.askyesno("Clear Cart", "Remove all items from cart?"):
            self.cart = []
            self.update_cart_display()

    def update_totals(self):
        """Update totals"""
        subtotal = sum(item['price'] * item['qty'] for item in self.cart)
        tax = subtotal * 0.12
        total = subtotal + tax
        total_items = sum(item['qty'] for item in self.cart)

        self.items_label.configure(text=f"Items: {total_items}")
        self.subtotal_val.configure(text=f"${subtotal:.2f}")
        self.tax_val.configure(text=f"${tax:.2f}")
        self.total_val.configure(text=f"${total:.2f}")

    def checkout(self):
        """Process checkout"""
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add items to cart first!")
            return

        # Checkout window
        checkout_win = ctk.CTkToplevel(self)
        checkout_win.title("Checkout")
        checkout_win.geometry("450x350")
        checkout_win.grab_set()

        # Title
        title = ctk.CTkLabel(
            checkout_win,
            text="Payment Method",
            font=("Arial", 18, "bold"),
            text_color="#00a8ff"
        )
        title.pack(pady=20)

        # Payment method
        payment_var = ctk.StringVar(value="Cash")

        methods = ["💵 Cash", "💳 Card", "📱 Online Banking"]
        for method in methods:
            btn = ctk.CTkRadioButton(
                checkout_win,
                text=method,
                variable=payment_var,
                value=method.split()[1],
                font=("Arial", 13)
            )
            btn.pack(pady=10, anchor="w", padx=80)

        # Divider
        divider = ctk.CTkFrame(checkout_win, height=2, fg_color="#404040")
        divider.pack(fill="x", padx=50, pady=20)

        # Amount
        total = sum(item['price'] * item['qty'] for item in self.cart) * 1.12
        amount_label = ctk.CTkLabel(
            checkout_win,
            text=f"Total Amount: ${total:.2f}",
            font=("Arial", 15, "bold"),
            text_color="#00cc88"
        )
        amount_label.pack(pady=10)

        # Buttons
        def confirm():
            # Save transaction
            transaction = {
                'id': datetime.now().strftime('%Y%m%d%H%M%S'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'items': self.cart.copy(),
                'subtotal': total / 1.12,
                'tax': total - (total / 1.12),
                'total': total,
                'method': payment_var.get()
            }

            self.save_transaction(transaction)

            # Update inventory
            for cart_item in self.cart:
                for inv_item in self.inventory_data:
                    if inv_item['id'] == cart_item['id']:
                        inv_item['quantity'] -= cart_item['qty']

            # Save inventory
            data = {"inventory": self.inventory_data, "suppliers": []}
            with open(self.inventory_file, 'w') as f:
                json.dump(data, f, indent=2)

            messagebox.showinfo("Payment Successful",
                                f"Transaction ID: {transaction['id']}\n"
                                f"Total: ${total:.2f}\n"
                                f"Method: {payment_var.get()}")

            self.cart = []
            self.update_cart_display()
            checkout_win.destroy()

        confirm_btn = ctk.CTkButton(
            checkout_win,
            text="✓ Confirm Payment",
            font=("Arial", 13, "bold"),
            fg_color="#00cc88",
            hover_color="#00aa66",
            command=confirm
        )
        confirm_btn.pack(pady=10, padx=50, fill="x")

        cancel_btn = ctk.CTkButton(
            checkout_win,
            text="✕ Cancel",
            font=("Arial", 12),
            fg_color="#ff5555",
            hover_color="#cc4444",
            command=checkout_win.destroy
        )
        cancel_btn.pack(padx=50, fill="x")

    def save_transaction(self, transaction):
        """Save transaction"""
        transactions = []
        if os.path.exists(self.transaction_file):
            try:
                with open(self.transaction_file, 'r') as f:
                    transactions = json.load(f)
            except:
                pass

        transactions.append(transaction)

        with open(self.transaction_file, 'w') as f:
            json.dump(transactions, f, indent=2)


if __name__ == "__main__":
    app = CashierApp()
    app.mainloop()
