# Import necessary packages
import sys, os
import csv
import pdb

def parseString(string):
    return ' '.join(string.upper().replace("\'", "\'\'").split())

schools = []
schools_clean = []

# Attempt to take in command line arguments
if len(sys.argv) < 2:
    sys.exit("Usage: %s school_filename output_filename" % sys.argv[0])
school_filename = sys.argv[1]
if not os.path.exists(school_filename):
    sys.exit("Error: Input file '%s' not found" % sys.argv[1])

# Read list of schools from input file, use them to filter the data, and output the filtered data to the output file
with open(school_filename, "rb") as s:
    reader = csv.DictReader(s)
    for row in reader:
        schools.append(row)

# Filter out the invalid rows, and parse the rest of the data
for school in schools:
    if not school['OPEID'] or school['OPEID'].upper() == 'NULL':
        print("Found null OPEID. Ignoring row.")
        continue
    elif int(school['ProgramLengthCode']) not in range(0, 13):
        print("ProgramLengthCode out of range. Ignoring row.")
        continue
    elif int(school['SchoolTypeCode']) not in range(1, 8) or int(school['SchoolTypeCode']) == 4:
        print("SchoolTypeCode out of range. Ignoring row.")
        continue
    elif int(school['EthnicAffiliationCode']) not in range(1,6):
        print("EthnicAffliationCode out of range. Ignoring row.")
        continue
    else:
        try:
            school['OPEID'] = int(school['OPEID'])
            if int(school['OPEID']) <= 0:
                print("Invalid OPEID: %s. Ignoring row." % school['OPEID'])
                continue
        except ValueError:
            print("Invalid OPEID: %s. Ignoring row." % school['OPEID'])
            continue
        school['Street'] = parseString(school['Street'])
        school['City'] = parseString(school['City'])
        school['State'] = parseString(school['State'])
        school['StateDesc'] = parseString(school['StateDesc'])
        school['Zip'] = parseString(school['Zip'])
        school['ProgramLengthCode'] = int(school['ProgramLengthCode'])
        school['SchoolTypeCode'] = int(school['SchoolTypeCode'])
        school['EthnicAffiliationCode'] = int(school['EthnicAffiliationCode'])
        schools_clean.append(school)

print('Number of rows in original data: %d \nNumber of rows after cleanup: %d' % (len(schools), len(schools_clean)))

# Write the parsed data back to file
with open(school_filename, "w") as o:
    fieldnames = [
        'OPEID',
        'Street',
        'City',
        'State',
        'StateDesc',
        'Zip',
        'ProgramLengthCode',
        'SchoolTypeCode',
        'EthnicAffiliationCode'
    ]
    writer = csv.DictWriter(o, fieldnames=fieldnames)
    writer.writeheader()
    for school in schools_clean:
        writer.writerow(school)
