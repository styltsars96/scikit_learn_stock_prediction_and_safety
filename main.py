"""Main executable code."""

from sys import argv
from Stock_Prediction import get_data
from Stock_Safety import safe_shares

if __name__ == '__main__':
    if len(argv) == 1:
        print("Need arguements...")

    company = ""
    choice = 0

    for arg in argv:
        cur_arg = arg.lower()
        if cur_arg == "main.py":
            continue
        # collect arguments...
        elif cur_arg == "stock" or cur_arg == "prediction":
            choice = 1
            continue
        elif cur_arg == "share" or cur_arg == "safety":
            choice = 2
        elif "company=" in cur_arg:
            if choice == 1:
                company = cur_arg.split("=")[1].upper()
        else:
            print("Invalid arguement:", arg)

    if choice == 1:
        if company == "":
            get_data("prices-split-adjusted.csv", 'ORCL')
        else:
            get_data("prices-split-adjusted.csv", company)
    elif choice == 2:
        safe_shares("prices-split-adjusted.csv")
    else:
        print("I'm broken :(")
