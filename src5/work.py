import io
import re

ENWIK_FILENAME = "../data/CMVariantProduct-20201027123227.csv"
NUMBER_OF_LINES =  1314702
MIN_FREQ_TO_BE_A_WORD = 50




division = 26

totallines = 26000

filelinesize = int(totallines / division)

print("------" + str(filelinesize))

for j in range(division):


    startindex = j * filelinesize
    endindex = (j+1) * filelinesize
    line_count = 0
    if j < 10:
        OUTPUT_ENWIK_FILENAME = "../data/tmp/CMVariantProduct-2020102712330" + str(j) +".csv"
    else :
        OUTPUT_ENWIK_FILENAME = "../data/tmp/CMVariantProduct-202010271233" + str(j) + ".csv"

    print(OUTPUT_ENWIK_FILENAME + "--------" + str(startindex) + "-----" + str(endindex))
    with open(ENWIK_FILENAME, "r", encoding="utf-8") as f:
        with open(OUTPUT_ENWIK_FILENAME, "w", encoding="utf-8", newline='\n') as f0:
            while True:
                line = f.readline()
                line_count = line_count + 1

                if line_count >= startindex:
                    f0.write(line)
                if line_count == endindex:
                    break
