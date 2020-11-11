import random

samples = []

for x in range(0, 50):
    samples.append(random.sample([0, 1, 2, 3, 4, 5, 6, 7], 8))

with open("testp.txt", "w") as text_file:
    for sample in samples:
        print(sample)
        for index, x in enumerate(sample):
            text_file.write(str(x))
            if not (len(sample) - 1 == index):
                text_file.write(" ")
        text_file.write("\n")

