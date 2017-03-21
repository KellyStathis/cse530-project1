# Import necessary packages
import sys, os
import csv
import pdb

def parseString(string):
    return ' '.join(string.upper().replace("\'", "\'\'").split())

loanbyschool = []
loanbyschool_clean = []

# Attempt to take in command line arguments
if len(sys.argv) < 2:
    sys.exit("Usage: %s loan_filename" % sys.argv[0])
loan_filename = sys.argv[1]
if not os.path.exists(loan_filename):
    sys.exit("Error: Input file '%s' not found" % sys.argv[1])

# Read list of loanbyschool from input file, use them to filter the data, and output the filtered data to the output file
with open(loan_filename, "rb") as s:
    reader = csv.DictReader(s)
    for row in reader:
        loanbyschool.append(row)

# Filter out the invalid rows, and parse the rest of the data
for loan in loanbyschool:
    if not loan['OPEID'] or loan['OPEID'].upper() == 'NULL':
        print("Found null OPEID. Ignoring row.")
        continue
    if not loan['NumReceivingFedLoan'] or loan['NumReceivingFedLoan'].upper() == 'NULL':
        if not loan['PercentReceivingFedLoan'] or loan['PercentReceivingFedLoan'].upper() == 'NULL':
            if not loan['TotalFedLoanAid'] or loan['TotalFedLoanAid'].upper() == 'NULL':
                print("NumReceivingFedLoad, PercentReceivingFedLoan, and TotalFedLoanAid are all null. Ignoring row.")
                continue
    else:
        try:
            loan['OPEID'] = int(loan['OPEID'])
            if int(loan['OPEID']) <= 0:
                print("Invalid OPEID: %s. Ignoring row." % loan['OPEID'])
                continue
        except ValueError:
            print("Invalid OPEID: %s. Ignoring row." % loan['OPEID'])
            continue
        loan['DisbursementYear'] = int(loan['DisbursementYear'])
        loan['NumReceivingFedLoan'] = int(loan['NumReceivingFedLoan'])
        loan['PercentReceivingFedLoan'] = int(loan['PercentReceivingFedLoan'])
        loan['TotalFedLoanAid'] = int(loan['TotalFedLoanAid'])
        try:
            loan['AvgFedLoanAid'] = int(loan['AvgFedLoanAid'])
        except ValueError:
            print("Invalid AvgFedLoanAid: %s. Ignoring row." % loan['AvgFedLoanAid'])
            continue
        loanbyschool_clean.append(loan)

print('Number of rows in original data: %d \nNumber of rows after cleanup: %d' % (len(loanbyschool), len(loanbyschool_clean)))

# Write the parsed data back to file
with open(loan_filename, "w") as o:
    fieldnames = [
        'OPEID',
        'DisbursementYear',
        'NumReceivingFedLoan',
        'PercentReceivingFedLoan',
        'TotalFedLoanAid',
        'AvgFedLoanAid'
    ]
    writer = csv.DictWriter(o, fieldnames=fieldnames)
    writer.writeheader()
    for loan in loanbyschool_clean:
        writer.writerow(loan)
