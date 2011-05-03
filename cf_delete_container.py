import cloudfiles
import sys
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials

verbose=1
def delete_container(connection,del_container_name,verbose=0):
	if verbose >2: print '-Debug- inside delete_container functin'
	if verbose >0: print '-Debug- delete_container, name passed \'%s\'' % del_container_name
	try:
		connection.delete_container(del_container_name)
	except(cloudfiles.errors.NoSuchContainer):
		print "Sorry, but there is no container called %s" % del_container_name
	except(cloudfiles.errors.ContainerNotEmpty):
		print "Sorry, but the container %s is not empty" % del_container_name
	else:
		print 'Container \'%s\' deleted successfully' % del_container_name

if __name__ == '__main__':
	if verbose > 1: print '-Debug- called as a standalone file'
	c = open_connection_with_configfile(verbose)
	try:
		if (sys.argv[1] != ""):
			container_name = sys.argv[1]
			if verbose >1: print '-Debug- Container name passed in argv[1]:', container_name
			delete_container(c,container_name,verbose)
		else:
			if verbose >1: print '-Debug- Nothing got passed as an argument', sys.argv
	finally:
		if verbose >1: print '-Debug- delete_container end'

