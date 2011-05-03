import cloudfiles
import os
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials
import sys

verbose=2

def upload_file(connection,container_name,source_filename,verbose=0):
	# get the container object
	container = connection.get_container(container_name)

	if verbose > 2: print '-Debug- cf_upload_file.py - upload_file START'
	if verbose >= 1:
		print '-Debug- container_name', container_name
		print '-Debug- source_filename', source_filename
	(filepath, filename) = os.path.split(source_filename)
	if verbose >= 2:
		print '-Debug- filepath:', filepath
		print '-Debug- filename:', filename

	file_obj = container.create_object(filename)
	file_obj.load_from_filename(source_filename)

	if verbose > 1: print '-Debug- file uploaded to cloud files container %s' % container_name

if __name__ == '__main__':
	if verbose > 1:
		print '-Debug- cf_upload_file.py START - Called as standalone file'
		c = open_connection_with_configfile(verbose=True)
	else:
		c = open_connection_with_configfile()
	try:
		if (sys.argv[1] != "" and sys.argv[2] != ""):
			container_name = sys.argv[1]
			source_filename = sys.argv[2]
			if verbose > 1:
				print '-Debug- Container name passed in argv[1]:', container_name
				print '-Debug- File name passed in argv[2]:', source_filename
			upload_file(c,container_name,source_filename,verbose)
		else:
			if verbose > 1: print '-Debug- Nothing got passed as an argument', sys.argv
	finally:
		if verbose > 1: print '-Debug- cf_upload_file.py END'
