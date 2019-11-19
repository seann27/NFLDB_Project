import subprocess
lib_dir = 'C:\\Users\\skbla\\NFLDB_Project\\Database_Building\\lib\\'
packages = [
	'nfl_data_package',
	'nfl_metrics_package',
	'scraper_package',
	'team_references_package'
]
for package in packages:
	command = lib_dir+package+'\\.'
	subprocess.run(['pip','install', '--upgrade', command])
