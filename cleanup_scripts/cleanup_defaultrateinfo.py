# Import necessary packages
import sys, os
import decimal
import csv
import pdb

def parseString(string):
    return ' '.join(string.upper().replace("\'", "\'\'").split())

defaultrateinfo = []
defaultrateinfo_clean = []

# Attempt to take in command line arguments
if len(sys.argv) < 2:
    sys.exit("Usage: %s rate_filename" % sys.argv[0])
rate_filename = sys.argv[1]
if not os.path.exists(rate_filename):
    sys.exit("Error: Input file '%s' not found" % sys.argv[1])

# Read list of defaultrateinfo from input file, use them to filter the data, and output the filtered data to the output file
with open(rate_filename, "rb") as s:
    reader = csv.DictReader(s)
    for row in reader:
        defaultrateinfo.append(row)

# Filter out the invalid rows, and parse the rest of the data
for rate in defaultrateinfo:
    '''if not rate['OPEID'] or rate['OPEID'].upper() == 'NULL':
        print("Found null OPEID. Ignoring row.")
        continue
    if float(rate['DefaultRate']) not in range(0, 101):
        print("DefaultRate out of range. Ignoring row.")
        continue'''
    if str(rate['RateType']) not in ['A', 'B', 'S', 'P']:
        print("Invalid RateType: %s. Ignoring row." % rate['RateType'])
        continue
    else:
        try:
            rate['OPEID'] = int(rate['OPEID'])
            if int(rate['OPEID']) <= 0:
                print("Invalid OPEID: %s. Ignoring row." % rate['OPEID'])
                continue
        except ValueError:
            print("Invalid OPEID: %s. Ignoring row." % rate['OPEID'])
            continue
        rate['CohortYear'] = int(rate['CohortYear'])
        rate['NumDefault'] = int(rate['NumDefault'])
        rate['NumBorrowers'] = int(rate['NumBorrowers'])
        rate['DefaultRate'] = float(rate['DefaultRate'])
        rate['RateType'] = str(rate['RateType'].upper().strip())
        defaultrateinfo_clean.append(rate)

print('Number of rows in original data: %d \nNumber of rows after cleanup: %d' % (len(defaultrateinfo), len(defaultrateinfo_clean)))

# Write the parsed data back to file
with open(rate_filename, "w") as o:
    fieldnames = [
        'OPEID',
        'CohortYear',
        'NumDefault',
        'NumBorrowers',
        'DefaultRate',
        'RateType'
    ]
    writer = csv.DictWriter(o, fieldnames=fieldnames)
    writer.writeheader()
    for rate in defaultrateinfo_clean:
        writer.writerow(rate)
