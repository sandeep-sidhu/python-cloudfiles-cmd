import cloudfiles
import os
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials
import sys

verbose=2

def download_file(connection,container_name,file_name,dstpath,verbose=0):
	# get the container object
	container = connection.get_container(container_name)
	dstpath = os.path.normpath(dstpath)
	full_path = os.path.join(dstpath,file_name)

	if verbose > 2: print '-Debug- inside download_file'
	if verbose >= 1:
		print '-Debug- container_name', container_name
		print '-Debug- file_name', file_name
		print '-Debug- dstpath', dstpath	
		print '-Debug- full_path:', full_path
	file_obj = container.get_object(file_name)
	file_obj.save_to_filename(full_path)
	if verbose > 1: print '-Debug- file saved as %s' % (full_path)

if __name__ == '__main__':
	if verbose > 1:
		print '-Debug- Called as standalone file'
		c = open_connection_with_configfile(verbose=True)
	else:
		c = open_connection_with_configfile()
	try:
		if (sys.argv[1] != "" and sys.argv[2] != ""):
			container_name = sys.argv[1]
			file_name = sys.argv[2]
			if sys.argv[3]: dstpath = sys.argv[3]
			if verbose > 1:
				print '-Debug- Container name passed in argv[1]:', container_name
				print '-Debug- File name passed in argv[2]:', file_name
				print '-Debug- Destination path in argv[3]', dstpath
			download_file(c,container_name,file_name,dstpath,verbose)
		else:
			if verbose > 1: print '-Debug- Nothing got passed as an argument', sys.argv
	finally:
		if verbose > 1: print '-Debug- list_files_end'
