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
    sys.exit("Usage: %s school_filename" % sys.argv[0])
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
    elif school['PublicPrivate'].upper() not in ['PUBLIC', 'PRIVATE', 'NULL']:
        print("ProgramLengthCode out of range. Ignoring row.")
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
        school['InstitutionName'] = parseString(school['InstitutionName'])
        school['PublicPrivate'] = parseString(school['PublicPrivate'])
        schools_clean.append(school)

print('Number of rows in original data: %d \nNumber of rows after cleanup: %d' % (len(schools), len(schools_clean)))

# Write the parsed data back to file
with open(school_filename, "w") as o:
    fieldnames = [
        'OPEID',
        'InstitutionName',
        'PublicPrivate'
    ]
    writer = csv.DictWriter(o, fieldnames=fieldnames)
    writer.writeheader()
    for school in schools_clean:
        writer.writerow(school)
