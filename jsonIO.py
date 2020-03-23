import json
import re
import os

def read(filename):
	if (os.path.exists(filename) == False):
		f = open(filename, "w")
		f.write("{}")
		f.close()
	with open(filename) as json_file:
		data = json.load(json_file)
		return data

def write(data, filename):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile, indent='\t', separators=(',',':'), sort_keys=True)

def rawWrite(data, filename):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile, separators=(',',':'), sort_keys=True)
	file = open(filename).read()
	f = open(filename, "w")
	file = re.sub(',"',',\n"',file)
	file = re.sub('^{','{\n',file)
	file = re.sub('}$','\n}',file)
	f.write(file)
	f.close()