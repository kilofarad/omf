import json
import os.path
import csv
#filelist = os.listdir('C:\\Users\\simon\\Desktop\\NRECA\\alltmy3a')
filelist = os.listdir('C:\\Users\\simon\\Documents\\GitHub\\omf\\omf\\solvers\\vbat\\alltmy3a') #put your own path
#print filelist

results = []

for filename in filelist:
	if filename[-3:] == 'CSV':
		state = []
		city = []
		temp = []
		with open (filename) as f:
			rows = list(csv.reader(f, delimiter=','))

			state = rows[0][2]
			city = rows[0][1]
			for row in rows[2:]: #31 is the index of bulb temp
				temp.append(row[31])

			results.append({
				'State' : state,
				'City' : city,
				'Temperatures' : temp})


with open('data.json', 'w') as outfile:
        json.dump(results, outfile,sort_keys=True, indent=4)