# Import necessary packages
import sys, os
import csv
import pdb

def parseString(string):
    return ' '.join(string.upper().replace("\'", "\'\'").split())

avgnetprice = []
avgnetprice_clean = []
opeids = []

# Attempt to take in command line arguments
if len(sys.argv) < 2:
    sys.exit("Usage: %s price_filename" % sys.argv[0])
price_filename = sys.argv[1]
if not os.path.exists(price_filename):
    sys.exit("Error: Input file '%s' not found" % sys.argv[1])

# Read list of avgnetprice from input file, use them to filter the data, and output the filtered data to the output file
with open(price_filename, "rb") as s:
    reader = csv.DictReader(s)
    for row in reader:
        avgnetprice.append(row)

# Filter out the invalid rows, and parse the rest of the data
for price in avgnetprice:
    if not price['OPEID'] or price['OPEID'].upper() == 'NULL':
        print("Found null OPEID. Ignoring row.")
        continue
    if not price['AvgNetPrice'] or price['AvgNetPrice'].upper() == 'NULL':
        print("Found null AvgNetPrice. Ignoring row.")
        continue
    elif int(price['AvgNetPrice']) < 0:
        print("AvgNetPrice out of range. Ignoring row.")
        continue
    else:
        try:
            price['OPEID'] = int(price['OPEID'])
            if int(price['OPEID']) <= 0:
                print("Invalid OPEID: %s. Ignoring row." % price['OPEID'])
                continue
            if int(price['OPEID']) in opeids:
                print("Duplicate OPEID: %s. Ignoring row." % price['OPEID'])
                continue
            opeids.append(price['OPEID'])
        except ValueError:
            print("Invalid OPEID: %s. Ignoring row." % price['OPEID'])
            continue
        price['DisbursementYear'] = int(price['DisbursementYear'])
        price['IncomeBracket'] = parseString(price['IncomeBracket'])
        price['AvgNetPrice'] = int(price['AvgNetPrice'])
        avgnetprice_clean.append(price)

print('Number of rows in original data: %d \nNumber of rows after cleanup: %d' % (len(avgnetprice), len(avgnetprice_clean)))

# Write the parsed data back to file
with open(price_filename, "w") as o:
    fieldnames = [
        'OPEID',
        'DisbursementYear',
        'IncomeBracket',
        'AvgNetPrice',
    ]
    writer = csv.DictWriter(o, fieldnames=fieldnames)
    for price in avgnetprice_clean:
        writer.writerow(price)
