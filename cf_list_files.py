import cloudfiles
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials
import sys

verbose=0

def list_files(connection,container_name,verbose=0):
	# get the container object
	try:
		container = connection.get_container(container_name)
	except(cloudfiles.errors.NoSuchContainer):
		print '-Error- Sorry, but there is no container named \'%s\'' % container_name
		return
	else:
		if verbose >=2: print '-Debug- container object obtained for %s' % container_name
	# print some container details
	if verbose > 1:
		print  "total size of \'%s\' container: %d bytes" %(container, container.size_used)
		print "total number of objects in \'%s\' container: %d" % (container, container.object_count)
	
	# build the list 10000 at a time
	last_marker = ''
	counter = 0 
	mainlist = []  
	if verbose > 1: print "Just populating the list..."
	while (counter < container.object_count):
	    mylist = container.get_objects(marker=last_marker)
	    if verbose > 1: print "Just grabbing files %d to %d" % (counter, counter + len(mylist))
	    counter += 10000
	    last_marker = mylist[-1]
	    # extend mainlist by adding current iteration of mylist
	    mainlist += mylist
	
	# print the entire main list out
	obnum = 1 
	for object in mainlist:
	    if verbose > 1: print "object number %d: %s" % (obnum, object)
	    else: print "%s" % object
	    obnum += 1
	

if __name__ == '__main__':
	if verbose > 1:
		print '-Debug- Called as standalone file'
		c = open_connection_with_configfile(verbose=True)
	else:
		c = open_connection_with_configfile()
	try:
		if (sys.argv[1] != ""):
			container_name = sys.argv[1]
			if verbose > 1: print '-Debug- Container name passed in argv[1]:', container_name
			list_files(c,container_name,verbose)
		else:
			if verbose > 1: print '-Debug- Nothing got passed as an argument', sys.argv
	finally:
		if verbose > 1: print '-Debug- list_files_end'
