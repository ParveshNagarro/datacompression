ENWIK__OUTPUT_FILENAME = "../data/enwik9"
ENWIK_FILENAME = "../data/enwik91"
EXPECTED_CHAR_COUNT = 1000


count  = 0
with open(ENWIK__OUTPUT_FILENAME, "w", encoding="utf-8", newline='\n') as f0:
    with open(ENWIK_FILENAME, encoding="utf8") as f:
      while True:
        c = f.read(1)
        if not c or count == EXPECTED_CHAR_COUNT:
          print("End of file")
          break
        count = count + 1
        f0.write(c)
        if count % 100 == 0:
          print("Read " + str(count) + " characters.")