import sys
from datetime import datetime
import csv
from pprint import pprint
from labelwriter import createAvery5160Spec, write_date , save_from_tuples



    
def pull_expiration_tuples(file_name):
	with open(file_name,encoding = 'utf-8') as file:
		reader =csv.DictReader(file)
		expiration_tuples =[(datetime.strptime(row["EXPIRATION DATE"],'%Y-%m-%d'),int(row["QUANTITY"])) for row in reader]
	return expiration_tuples

def main():
	expiration_tuples = pull_expiration_tuples(sys.argv[1])
	save_from_tuples(expiration_tuples)


if __name__ == '__main__':
	main()