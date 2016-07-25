from collections import Counter


def process_localization_file(source: str) -> list:
    with open(source, encoding="cp1252") as openedsource:
        readsource = openedsource.readlines()
    dynlist = []
    #for localizationstring in readsource:
        #if localization[0] == '#':
            #continue
        #elif "_adj" in localizationstring:
            #continue
        #else:
            #splitloc = localizationstring.split(";")[1]
            ##if " " in splitloc:
                ##continue
            #dynlist.append(splitloc)
    dynlist = [localizationstring.split(";")[1] for localizationstring in
               readsource if not(localizationstring[0] == "#" or "_adj" in
                                 localizationstring)]
    dyndict = Counter(dynlist)
    dynlist_clean = [key for key in dyndict]
    return dynlist_clean

def process_prefix_file(source: str) -> list:
    with open(source, encoding="cp1252") as openedsource:
        readsource = openedsource.readlines()
    preflist = []
    #for prefixstring in readsource:
        #if prefixstring[0] == "#":
            #continue
        #prefsublist = prefixstring.split(";") 
        #preflist.append(prefsublist)[:-1]
    preflist = [prefixstring.split(";")[:-1] for prefixstring in readsource
                if prefixstring[0] != "#"]
    # Now create a list with weighted occurences
    # NOTE: TODO
    preflist_clean = []
    for prefsublist in preflist:
        for i in range(0, int(prefsublist[2])):
            preflist_clean.append(prefsublist[0:2])
    #preflist_clean = preflist # placeholder
    from random import shuffle
    shuffle(preflist_clean)
    return preflist_clean

def select_prefix_and_culture(preflist: list) -> (str, str):
    from random import choice
    return choice(preflist)[0:2]

def write_dynasties_to_file(target: str, dynlist: list, preflist: list,
                            startvalue: int):
    with open(target, mode="w", encoding="cp1252") as openedtarget:
        for dynasty in dynlist:
            (prefix, culture) = select_prefix_and_culture(preflist)
            gap = " "
            if prefix == "~":
                prefix = ""
                gap = ""
            openedtarget.write(str(startvalue) + " = {\n    name = \"" + prefix
                               + gap + dynasty + "\"")
            startvalue += 1
            openedtarget.write("\n    culture = " + culture)
            openedtarget.write("\n}\n")

if __name__ == "__main__":
    import argparse

    parser = \
        argparse.ArgumentParser(description="Generate a list of names",
                                formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", "--source", type=str, default="baronies.csv",
                        help="The file containing the title localization list"
                        " along with the path to the file. The default is "
                        "\"baronies.csv\".\n")
    parser.add_argument("-t", "--target", type=str, default="dynasties.txt",
                        help="The file where the new dynasty list will be "
                        "stored. The default is ""\"dynasties.txt\". Any "
                        "existing file with the same name will be "
                        "overwritten.\n")
    parser.add_argument("-p", "--prefix", type=str, default="prefixes.csv",
                        help="The file containing the list of prefixes to "
                        "randomly assign from. Input is a file.")
    parser.add_argument("--startvalue", type=int, default=1, help="The dynasty"
                        " generated first will have this value, and subsequent"
                        " dynasties will be increased in value by one.")

    args = parser.parse_args()
    dynlist = process_localization_file(args.source)
    preflist = process_prefix_file(args.prefix)  # format prefix;culture;weight;
    write_dynasties_to_file(args.target, dynlist, preflist, args.startvalue)
