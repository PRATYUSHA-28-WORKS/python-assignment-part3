
import requests
from datetime import datetime
# =========================================================
# Product Explorer & Error-Resilient Logger
# Assignment Part 3 - File I/O, APIs & Exception Handling
# =========================================================

import requests
from datetime import datetime


# -----------------------------
# Task 1 — File Read & Write
# -----------------------------

notes = [
"Topic 1: Variables store data. Python is dynamically typed.",
"Topic 2: Lists are ordered and mutable.",
"Topic 3: Dictionaries store key-value pairs.",
"Topic 4: Loops automate repetitive tasks.",
"Topic 5: Exception handling prevents crashes."
]

# Write to file
with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in notes:
        f.write(line + "\n")

print("File written successfully.")

# Append new lines
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions help organize reusable code.\n")
    f.write("Topic 7: APIs allow applications to communicate.\n")

print("Lines appended successfully.")

# Read file
print("\nReading file contents:\n")

line_count = 0

with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    print(f"{i}. {line.strip()}")
    line_count += 1

print("Total lines:", line_count)

keyword = input("Enter keyword to search: ").lower()

found = False

for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True

if not found:
    print("No matching lines found.")


# -----------------------------
# Task 2 — API Integration
# -----------------------------

print("\nFetching products from API...\n")

try:

    url = "https://dummyjson.com/products?limit=20"
    response = requests.get(url, timeout=5)

    data = response.json()
    products = data["products"]

    print("ID | Title | Category | Price | Rating")

    for p in products:
        print(p["id"], "|", p["title"], "|", p["category"], "|", p["price"], "|", p["rating"])

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check internet.")

except requests.exceptions.Timeout:
    print("Request timed out.")

except Exception as e:
    print("Unexpected error:", e)


# Filter rating >= 4.5 and sort by price
filtered = []

for p in products:
    if p["rating"] >= 4.5:
        filtered.append(p)

filtered.sort(key=lambda x: x["price"], reverse=True)

print("\nFiltered Products (rating >= 4.5):")

for p in filtered:
    print(p["title"], "-", p["price"], "-", p["rating"])


# Search laptops category
try:

    print("\nLaptop Products:\n")

    laptop_url = "https://dummyjson.com/products/category/laptops"
    response = requests.get(laptop_url, timeout=5)

    data = response.json()

    for p in data["products"]:
        print(p["title"], "-", p["price"])

except Exception as e:
    print("Laptop API error:", e)


# POST request simulation
try:

    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    post_url = "https://dummyjson.com/products/add"

    response = requests.post(post_url, json=payload, timeout=5)

    print("\nPOST Response:")
    print(response.json())

except Exception as e:
    print("POST request failed:", e)


# -----------------------------
# Task 3 — Exception Handling
# -----------------------------

def safe_divide(a, b):

    try:
        return a / b

    except ZeroDivisionError:
        return "Error: Cannot divide by zero"

    except TypeError:
        return "Error: Invalid input types"


print("\nSafe Divide Tests:")
print(safe_divide(10,2))
print(safe_divide(10,0))
print(safe_divide("ten",2))


# Safe file reader
def read_file_safe(filename):

    try:
        with open(filename,"r") as f:
            return f.read()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    finally:
        print("File operation attempt complete.")


print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))


# Product lookup with validation
while True:

    user_input = input("\nEnter product ID (1-100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Invalid input. Enter a number.")
        continue

    pid = int(user_input)

    if pid < 1 or pid > 100:
        print("ID must be between 1 and 100.")
        continue

    try:

        url = f"https://dummyjson.com/products/{pid}"
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            print("Product not found.")

        elif response.status_code == 200:
            product = response.json()
            print(product["title"], "-", product["price"])

    except Exception as e:
        print("API error:", e)


# -----------------------------
# Task 4 — Logging
# -----------------------------

def log_error(location, message):

    time = datetime.now()

    with open("error_log.txt","a") as log:
        log.write(f"[{time}] ERROR in {location}: {message}\n")


# Trigger connection error
try:

    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)

except requests.exceptions.ConnectionError:
    log_error("fetch_products","ConnectionError — No connection could be made")


# Trigger HTTP error
response = requests.get("https://dummyjson.com/products/999")

if response.status_code != 200:
    log_error("lookup_product","HTTPError — 404 Not Found for product ID 999")


# Print log contents
print("\nError Log:\n")

try:

    with open("error_log.txt","r") as log:
        print(log.read())

except FileNotFoundError:
    print("No log file found.")x
