import csv





FILENAME="Promotions-202011100637.csv"



SOURCE = "../data/"+FILENAME
NUMBER_OF_LINES =  1314702
MIN_FREQ_TO_BE_A_WORD = 50

active_schools =["211", "29", "465", "8090", "8349", "8339", "8062"]

print("nekfjrnk")
with open("../data/final/" + FILENAME, "w", encoding="utf-8", newline='\n') as f0:
    with open(SOURCE, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            final_line = line.strip()

            #print(line)

            if final_line:
                fields = []
                for l in  csv.reader(final_line):
                    fields.append(l)

                schoolconditionsstring = fields[14][0].split(',')[4]


                if not schoolconditionsstring:
                    #print("empty school encountered")
                    print(final_line)
                else:
                    schoolcodes = schoolconditionsstring.split(' ')
                    #print(schoolcodes)
                    for active_school in active_schools:
                        if active_school in schoolcodes:
                            print(final_line)
                            f0.write(final_line + "\n")
                            break

            if not line:
                break






