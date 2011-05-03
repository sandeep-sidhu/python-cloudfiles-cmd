import cloudfiles
import sys
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials

verbose=2

def create_container(connection,new_container_name,verbose):
	if verbose > 2: print '-Debug- inside create_container function'
	if verbose > 1: print '-Debug- new container name passed \'%s\'' % new_container_name
	try:
		if verbose > 1: print '-Debug- trying to create a new container', new_container_name
		connection.create_container(new_container_name)
	except:
		print "-Info- There was a problem in creating container \'%s\'" %  new_contianer_name
	else:
		print "-Info- Container \'%s\' created successfully" % new_container_name	

if __name__ == '__main__':
	if verbose > 1:
		print '-Debug- called as a standalone file'
		c = open_connection_with_configfile(verbose=True)
	else:
		c = open_connection_with_configfile()
	try:
		if (sys.argv[1] != ""):
			container_name = sys.argv[1]
			if verbose > 1: print '-Debug- Container name passed in argv[1]:', container_name
			create_container(c,container_name,verbose)
		else:
			if verbose > 1: print '-Debug- Nothing got passed sa an argument', sys.argv
	finally:
		if verbose >1: print '-Debug- create_container end'
