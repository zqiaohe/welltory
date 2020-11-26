import json
import os
import jsonschema 
import sys
import pandas as pd

schema_dir = "/home/zorigma/Документы/welltory/task_folder/schema/"
event_dir = "/home/zorigma/Документы/welltory/task_folder/event/"
schemas = os.listdir(schema_dir)
files = os.listdir(event_dir)

d = {'ErrorSchema': [], 'ErrorFileName': [], 'ErrorMessage': []}
df = pd.DataFrame(data=d)

for schemaname in schemas:
	with open(schema_dir+schemaname, 'r') as f:
		schema_file = f.read()
	schema = json.loads(schema_file)
	#print(schemaname)
	for filename in files:
		#print(filename)
		with open(event_dir+filename, 'r') as f:
			json_file = f.read()
		json_obj = json.loads(json_file)
		try:
			json_obj.fromkeys(schema.keys())
		except:
			row = [schemaname, filename, 'Empty file']
			df.loc[len(df)] = row
    
		try:
			jsonschema.validate(json_obj, schema)
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			row = [schemaname, filename, str(exc_value.message)]
			df.loc[len(df)] = row

styles = '''
<style>
table {
  font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
  border-collapse: collapse;
  color: #686461;
}
caption {
  padding: 10px;
  color: white;
  background: #8FD4C1;
  font-size: 18px;
  text-align: left;
  font-weight: bold;
}
th {
  border-bottom: 3px solid #B9B29F;
  padding: 10px;
  text-align: left;
}
td {
  padding: 10px;
}
tr:nth-child(odd) {
  background: white;
}
tr:nth-child(even) {
  background: #E8E6D1;
}
</style>
'''
with open("errortable.html", 'w', encoding='utf-8') as f:
	sys.stdout = f
	print(styles)
	print(df.to_html())

