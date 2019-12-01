import os
import glob
import re


def parser():
    os.chdir("/home/jamie/Documents/things/DataPDF")
    
    # Html was the easiest to parse as it kept the data in the best structure compared to the other options.
    for file in glob.glob("*.pdf"):
        os.system("pdftotext -raw -htmlmeta " + "/home/jamie/Documents/things/DataPDF/" + file)


    for file in glob.glob("*.html"):
        dataInput = open(file, "r")
        dataRaw = dataInput.read()
        dataInput.close()

        # Ugly Regex and data formatting
        dataRaw = re.sub(r",", "", dataRaw)
        special_cases = re.findall(r"\d\d\/\d\d\/\d\d.{5,}[\d]{1,}\.[\d]{2,}.[\d]{1,}\.[\d]{2,}", dataRaw)

        dataRaw = re.sub(r"\d\d\/\d\d\/\d\d.{5,}[\d]{1,}\.[\d]{2,}.[\d]{1,}\.[\d]{2,}", "", dataRaw)
        dataRaw = re.findall(r"\d\d\/\d\d\/\d\d.*\n.*\d{1,}.*\n", dataRaw)

        debtOutput = open("/home/jamie/Documents/things/Data/" + file + "-Parsed-D", "w+")
        creditOutput = open("/home/jamie/Documents/things/Data/" + file + "-Parsed-C", "w+")

        for i in range(0, len(dataRaw)):
            holder = dataRaw[i].split("\n")
            line = holder[0] + " " + holder[1] + "\n"

            if "Deposit" in line:
                creditOutput.write(line)
            else:
                debtOutput.write(line)

        for line in special_cases:
            if "Deposit" in line:
                creditOutput.write(line + "\n")
            else:
                debtOutput.write(line + "\n")


def audit(type, filter):
    os.chdir("/home/jamie/Documents/things")
    for file in glob.glob("./Categories/" + type + "-*"):
        total_total = 0.0

        f = open(file, "r")
        flagHolder = f.read()

        for dataFiles in glob.glob("./Data/*-" + type):
            dataFile = open(dataFiles, "r")
            dataStr = dataFile.read()
            data = dataStr.split("\n")

            flags = flagHolder.split("\n")

            for lines in data:
                for flag in flags:
                    if (flag in lines):
                        line = lines.split(" ")

                        if (len(line) > 3):
                            if(line[-2] == "incl."):
                                total_total += float(line[-3])
                            else:
                                total_total += float(line[-2])
            dataFile.close()

        f.close()
        print(file)
        print(total_total)


def main():
    while True:
        user = input("Credits, Debts or Exit\n")
        print("\n")

        if(user == "Credits" or user == "C"):
            audit("C", "*")
            print("\n")

        if(user == "Debts" or user == "D"):
            audit("D", "*")
            print("\n")

        if(user == "Exit" or user == "X"):
            return 0


parser()
main()
