"""
Professional Restaurant Management System in Python (CLI-based)

Features:
- View Menu
- Add items to Order with quantity
- Calculate total with tax
- Accept payment input and show change due
- Use 'rich' library for professional output formatting

Dependencies:
- rich (for beautiful CLI tables and text formatting)

To install rich:
pip install rich

Usage:
Run `python restaurant_management.py` and follow the interactive prompts.
"""

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm, FloatPrompt

console = Console()

class MenuItem:
    def __init__(self, code: str, name: str, price: float):
        self.code = code
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{self.code} - {self.name}: ${self.price:.2f}"

class Menu:
    def __init__(self):
        self.items = {}

    def add_item(self, item: MenuItem):
        self.items[item.code] = item

    def get_item(self, code: str):
        return self.items.get(code)

    def display(self):
        table = Table(title="Restaurant Menu")
        table.add_column("Code", justify="center", style="cyan", no_wrap=True)
        table.add_column("Item", style="magenta")
        table.add_column("Price", justify="right", style="green")
        for item in self.items.values():
            table.add_row(item.code, item.name, f"${item.price:.2f}")
        console.print(table)

class OrderItem:
    def __init__(self, menu_item: MenuItem, quantity: int):
        self.menu_item = menu_item
        self.quantity = quantity

    def get_subtotal(self):
        return self.menu_item.price * self.quantity

    def __repr__(self):
        return f"{self.menu_item.name} x {self.quantity} = ${self.get_subtotal():.2f}"

class Order:
    TAX_RATE = 0.07  # 7% tax

    def __init__(self):
        self.items = []

    def add_order_item(self, order_item: OrderItem):
        self.items.append(order_item)

    def calculate_subtotal(self):
        return sum(item.get_subtotal() for item in self.items)

    def calculate_tax(self):
        return self.calculate_subtotal() * self.TAX_RATE

    def calculate_total(self):
        return self.calculate_subtotal() + self.calculate_tax()

    def display_order(self):
        table = Table(title="Current Order")
        table.add_column("Item Name", style="magenta")
        table.add_column("Quantity", justify="right", style="cyan")
        table.add_column("Price Each", justify="right", style="green")
        table.add_column("Subtotal", justify="right", style="yellow")
        for item in self.items:
            table.add_row(
                item.menu_item.name,
                str(item.quantity),
                f"${item.menu_item.price:.2f}",
                f"${item.get_subtotal():.2f}"
            )
        subtotal = self.calculate_subtotal()
        tax = self.calculate_tax()
        total = self.calculate_total()
        table.add_row("", "", "Subtotal:", f"${subtotal:.2f}")
        table.add_row("", "", "Tax (7%):", f"${tax:.2f}")
        table.add_row("", "", "[bold]Total:[/bold]", f"[bold]${total:.2f}[/bold]")
        console.print(table)

def main():
    console.print("[bold green]Welcome to the Professional Restaurant Management System[/bold green]\n")

    # Initialize menu with some items
    menu = Menu()
    menu.add_item(MenuItem("D1", "Margherita Pizza", 8.99))
    menu.add_item(MenuItem("D2", "Pepperoni Pizza", 10.99))
    menu.add_item(MenuItem("D3", "Caesar Salad", 6.50))
    menu.add_item(MenuItem("D4", "Grilled Chicken", 12.00))
    menu.add_item(MenuItem("D5", "Spaghetti Carbonara", 11.50))
    menu.add_item(MenuItem("D6", "Tiramisu", 5.00))
    menu.add_item(MenuItem("D7", "Coke", 1.75))
    menu.add_item(MenuItem("D8", "Coffee", 2.25))

    order = Order()

    while True:
        console.print("\n[bold]Please select an option:[/bold]")
        console.print("1 - View Menu")
        console.print("2 - Add Item to Order")
        console.print("3 - View Current Order")
        console.print("4 - Checkout")
        console.print("5 - Exit")

        choice = Prompt.ask("Enter choice", choices=["1","2","3","4","5"])

        if choice == "1":
            menu.display()

        elif choice == "2":
            menu.display()
            item_code = Prompt.ask("Enter item code to add to order").strip().upper()
            item = menu.get_item(item_code)
            if item is None:
                console.print(f"[red]Item code '{item_code}' not found. Please try again.[/red]")
                continue
            quantity = IntPrompt.ask(f"Enter quantity of {item.name}", default=1, show_default=True)
            if quantity < 1:
                console.print("[red]Quantity must be at least 1.[/red]")
                continue
            order.add_order_item(OrderItem(item, quantity))
            console.print(f"[green]{quantity} x {item.name} added to the order.[/green]")

        elif choice == "3":
            if not order.items:
                console.print("[yellow]Your order is empty.[/yellow]")
            else:
                order.display_order()

        elif choice == "4":
            if not order.items:
                console.print("[yellow]Your order is empty. Add items before checkout.[/yellow]")
                continue
            order.display_order()
            total = order.calculate_total()
            while True:
                payment = FloatPrompt.ask(f"Enter payment amount (total: ${total:.2f})")
                if payment < total:
                    console.print("[red]Payment is less than total amount. Please enter sufficient amount.[/red]")
                else:
                    change = payment - total
                    console.print(f"[green]Payment accepted. Change due: ${change:.2f}[/green]")
                    console.print("[bold blue]Thank you for your order![/bold blue]")
                    # Reset order for next customer
                    order = Order()
                    break

        elif choice == "5":
            confirm_exit = Confirm.ask("Are you sure you want to exit?")
            if confirm_exit:
                console.print("[bold green]Goodbye![/bold green]")
                break

if __name__ == "__main__":
    main()
