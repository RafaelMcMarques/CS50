from cs50 import get_string

text = get_string("Text: ")
letters = 0
words = 0
sentences = 0

for i in range(0, len(text)):
    if text[i].isalpha():
        letters += 1
    elif text[i] == " ":
        words += 1
    elif text[i] == "." or text[i] == "?" or text[i] == "!":
        sentences += 1
words += 1

L = letters / words * 100
S = sentences / words * 100
grade = round(0.0588 * L - 0.296 * S - 15.8)

if grade < 1:
    print("Before Grade 1")
if grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade: {grade}")

