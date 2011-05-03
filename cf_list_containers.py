import cloudfiles
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials
from cf_list_files import list_files

verbose=0
def list_containers(connection,verbose=0):
	if verbose > 1 : print "-Debug- inside - list_containers"
	if verbose > 0: print "-Debug- trying to get a list all the containers"
	all_containers = connection.get_all_containers()
	
	for container in all_containers:
		print container.name	

def list_public_containers(connection,verbose=0):
	if verbose > 1 : print "-Debug- inside - list_public_containers"
	if verbose > 0: print "-Debug- trying to get a list all the public containers"
	public_containers = connection.list_public_containers()
	
	for container in public_containers:
		print container	

if __name__ == '__main__':
	try:
		if verbose > 1:	print '-Debug- cf_list_containers called as standalone'
		c = open_connection_with_configfile()
		if verbose > 1: print '-Debug - connection to cloud files made successfully'
		list_containers(c,verbose)	
	finally:
		if verbose > 1: print "End Container listing"
