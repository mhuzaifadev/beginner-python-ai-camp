"""
Practice: File Handling & Error Management
Date: Jun 26

Students:
✅ Read a file's contents.
✅ Append new data.
✅ Handle errors with try-except.
✅ Count the number of lines in a file.
"""

filename = "practice_notes.txt"

# --------------------------------------------
# 🐣 Check if file exists and read its contents
# --------------------------------------------
try:
    with open(filename, "r") as file:
        lines = file.readlines()
    print(f"📖 {filename} contains {len(lines)} lines:")
    for line in lines:
        print(line.strip())
except FileNotFoundError:
    print(f"❌ {filename} not found. Creating a new one!")

# --------------------------------------------
# 🐣 Append new data
# --------------------------------------------
new_note = input("➕ Enter a new note to add: ")
with open(filename, "a") as file:
    file.write(new_note + "\n")
print("✅ Note added!")

# --------------------------------------------
# 🐣 Count number of lines after writing
# --------------------------------------------
with open(filename, "r") as file:
    total_lines = sum(1 for _ in file)
print(f"🧮 Total number of lines is now: {total_lines}")

# 🎯 Practice ideas:
# 1. Wrap the reading/writing in a function.
# 2. Add error handling for blank inputs.
# 3. Prompt the user multiple times until they type 'exit'.
