"""
File Handling & Error Management
Date: Jun 26

This session:
✅ Reads and writes text files
✅ Handles errors gracefully
✅ Reads and writes CSV files
✅ Builds a simple to-do list app that saves to a file
"""

import csv

# --------------------------------------------
# 🐣 Example 1: Write to a text file
# --------------------------------------------
with open('example.txt', 'w') as file:
    file.write('Hello, file handling in Python!\n')
    file.write('This is the second line.\n')
print('✅ example.txt created.')

# --------------------------------------------
# 🐣 Example 2: Read from a text file
# --------------------------------------------
with open('example.txt', 'r') as file:
    content = file.read()
print('📖 Content of example.txt:\n', content)

# --------------------------------------------
# 🐣 Example 3: Error handling with try/except
# --------------------------------------------
filename = 'missing_file.txt'
try:
    with open(filename, 'r') as file:
        data = file.read()
except FileNotFoundError:
    print(f'❌ Error: {filename} does not exist.')

# --------------------------------------------
# 🐣 Example 4: Write CSV file
# --------------------------------------------
rows = [
    ['Name', 'Score'],
    ['Alice', 90],
    ['Bob', 85]
]

with open('scores.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print('✅ scores.csv created.')

# --------------------------------------------
# 🐣 Example 5: Read CSV file
# --------------------------------------------
with open('scores.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# --------------------------------------------
# 🐣 To-Do list App
# --------------------------------------------
filename = 'todo_list.txt'

# Load existing todos
try:
    with open(filename, 'r') as file:
        todos = file.read().splitlines()
except FileNotFoundError:
    todos = []
    print('🔄 No existing file found. Starting a new list.')

# Show existing todos
print('📝 Current To-Do List:')
for i, todo in enumerate(todos, 1):
    print(f"{i}. {todo}")

# Get new todo input
new_todo = input('➕ Enter a new to-do item: ')
todos.append(new_todo)

# Save updated list
with open(filename, 'w') as file:
    file.write('\n'.join(todos))

print('✅ To-Do list updated and saved!')
