import io
import pickle
import re

#total_number_of_lines = 1128024
total_number_of_lines = 6400

enwik: str = "../../data/tmp/enwik8"
line_count = 0
with open("../../data/tmp/enwik81.txt", "w", encoding="utf-8") as f0:
    with open(enwik, "r", encoding="utf-8") as f:
        print("Creating a list of words... .")
        while True:
            line = f.readline()
            line_count = line_count + 1
            if line_count % 10000 == 0:
                print("Creating the words dict - " + str(line_count))
            if line_count == total_number_of_lines:
                print("End of file")
                break

            f0.write(line)
