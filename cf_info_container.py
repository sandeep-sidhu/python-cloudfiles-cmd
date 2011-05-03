import cloudfiles
import sys
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials

verbose=1
def info_container(connection,container_name,verbose=0):
	if verbose >2: print '-Debug- inside info_container functin'
	if verbose >0: print '-Debug- info_container, name passed \'%s\'' % container_name
	container = connection.get_container(container_name)
	print 'Container Name:', container.name
	print 'Size used:', container.size_used
	if container.is_public == True:
		print 'Published to CDN: Yes'
		print 'Public URL:', container.public_uri()
	
if __name__ == '__main__':
	if verbose > 1: print '-Debug- called as a standalone file'
	c = open_connection_with_configfile(verbose)
	try:
		if (sys.argv[1] != ""):
			container_name = sys.argv[1]
			if verbose >1: print '-Debug- Container name passed in argv[1]:', container_name
			info_container(c,container_name,verbose)
		else:
			if verbose >1: print '-Debug- Nothing got passed as an argument', sys.argv
	finally:
		if verbose >1: print '-Debug- info_container end'

