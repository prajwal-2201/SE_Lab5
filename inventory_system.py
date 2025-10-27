"""
A simple inventory management system.
Demonstrates fixing static analysis issues.
"""
import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def add_item(item="default", qty=0, logs=None):
    """Adds an item to the global stock_data."""
    if logs is None:
        logs = []

    if not item:
        return

    # FIX 1: Input validation for data type
    if not isinstance(qty, (int, float)):
        logging.error("Quantity '%s' for item '%s' must be a number.", qty, item)
        return

    # FIX 2 (Business Logic): Added check for negative or zero quantity
    if qty <= 0:
        logging.warning("Cannot add zero or negative quantity ('%s') for '%s'.", qty, item)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")

def remove_item(item, qty):
    """Removes a quantity of an item from the stock_data."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning("Item '%s' not found in inventory. Cannot remove.", item)

def get_qty(item):
    """Gets the quantity of a single item, returning 0 if not found."""
    return stock_data.get(item, 0)

def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        logging.warning("File '%s' not found. Starting with empty inventory.", file)
        stock_data = {}
    except json.JSONDecodeError:
        logging.warning("Error decoding '%s'. Starting with empty inventory.", file)
        stock_data = {}

def save_data(file="inventory.json"):
    """Saves the current inventory to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)

def print_data():
    """Prints a formatted report of all items in stock."""
    print("\n--- Items Report ---")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------\n")

def check_low_items(threshold=5):
    """Returns a list of items below the stock threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]

def main():
    """Main function to run the inventory program."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    load_data()

    add_item("apple", 10)
    add_item("banana", -2)  # This will now be caught by our new check
    add_item(123, "ten")    # This will be caught by our type check
    remove_item("apple", 3)
    remove_item("orange", 1) 
    
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    
    print_data()
    save_data()
    
    print("Security check: 'eval()' function has been removed.")

if __name__ == "__main__":
    main()