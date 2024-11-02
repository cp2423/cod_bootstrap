import os

DIR = "letters"
if not os.path.exists(DIR):
    os.mkdir(DIR)

letters = [
    range(48, 58),  # digits
    range(65, 91),  # uppercase
    range(97, 123)  # lowercase
]

for rng in letters:
    chars = [chr(i) for i in rng]
    for char in chars:
        dir = os.path.join(DIR, char)
        if not os.path.exists(dir):
            os.mkdir(dir)