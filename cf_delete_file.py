import cloudfiles
import os
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials
import sys

verbose=2

def delete_file(connection,container_name,filename,verbose=0):
	# get the container object
	container = connection.get_container(container_name)

	if verbose > 2: print '-Debug- cf_upload_file.py - upload_file START'
	if verbose >= 1:
		print '-Debug- container_name', container_name
		print '-Debug- filename', filename

	try:
		container.delete_object(filename)
	except(cloudfiles.errors.NoSuchObject):
		print 'Sorry, but no such file \'%s\' exists in container \'%s\' ' % filename,container_name
	else:
		print 'File \'%s\' deleted successfully ' % filename


	if verbose > 1: print '-Debug- file deleted from the container %s' % container_name

if __name__ == '__main__':
	if verbose > 1:
		print '-Debug- cf_delete_file.py START - Called as standalone file'
		c = open_connection_with_configfile(verbose=True)
	else:
		c = open_connection_with_configfile()
	try:
		if (sys.argv[1] != "" and sys.argv[2] != ""):
			container_name = sys.argv[1]
			filename = sys.argv[2]
			if verbose > 1:
				print '-Debug- Container name passed in argv[1]:', container_name
				print '-Debug- File name passed in argv[2]:', filename
			delete_file(c,container_name,filename,verbose)
		else:
			if verbose > 1: print '-Debug- Nothing got passed as an argument', sys.argv
	finally:
		if verbose > 1: print '-Debug- cf_delete_file.py END'
