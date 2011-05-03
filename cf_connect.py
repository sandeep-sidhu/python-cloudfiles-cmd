import cloudfiles
import ConfigParser
import os
verbose=3
config_file="~/.pycflogin"

def open_connection_with_configfile(config_file='~/.pycflogin',verbose=0):
    if verbose >=2: print '-Debug- open_connection_with_configfile - START'
    if verbose >=1: print '-Debug- config_file:', config_file
    config_file = os.path.expanduser(config_file)
    if verbose >=2: print '-Debug exapanded config_file:', config_file

    # Read the config file
    config = ConfigParser.ConfigParser()
    if os.path.exists(config_file):
    	config.read(config_file)
        # get the username and API
        username = config.get('account', 'username')
        apikey = config.get('account', 'apikey')
        location = config.get('account', 'location')
        if location == "uk" or location == "UK":
	   auth_url="https://lon.auth.api.rackspacecloud.com/v1.0"
        else:
	   auth_url="https://auth.api.rackspacecloud.com/v1.0"
        if verbose >= 1: print '-Info- Logging in as', username
        if verbose >= 2: print '-Debug- Using AUTH-URL as', auth_url
    else:
	if verbose >= 1: print '-Info- %s file does not exists' % config_file
	print '-Info- No existing configuration file found %s , would you like to create one?\n' % config_file
	answer = raw_input('Please enter yes to provide new credentials or no to exit. [yes/no]:')
	if answer == 'yes' or answer == 'YES':
		username = raw_input('username:')
		apikey = raw_input('api_key:')
		location = raw_input('location [us/uk]:')
		if (location == 'uk' or location == 'UK'):
			auth_url="https://lon.auth.api.rackspacecloud.com/v1.0"
		else:
			auth_url="https://auth.api.rackspacecloud.com/v1.0"
        	if verbose >= 1: print '-Info- Logging in as', username
        	if verbose >= 2: print '-Debug- Using AUTH-URL as', auth_url
		if verbose >= 1: print '-Info Saving credentials in %s file for future use' % config_file
		fo = open(config_file, "wb")
		fo.write("[account]\n")
		fo.write("username=")
		fo.write(username)
		fo.write("\n")
		fo.write("apikey=")
		fo.write(apikey)
		fo.write("\n")
		fo.write("location=")
		fo.write(location)
		fo.write("\n")
		fo.close()
		if verbose >= 1: print '-Debug- Credentials saved to the %s file' % config_file
	else:
		exit()

    connection = cloudfiles.get_connection(username,apikey,authurl=auth_url)
    return connection

def open_connection_with_credentials(username,api_key,auth_url,verbose=0):
	if auth_url == "uk" or auth_url == "UK":
		auth_url="https://lon.auth.api.rackspacecloud.com/v1.0"
		connection = cloudfiles.get_connection(username,api_key,authurl=auth_url)
	else:
		auth_url="https://auth.api.rackspacecloud.com/v1.0"
		connection = cloudfiles.get_connection(username,api_key,authurl=auth_url)
	return connection	

if __name__ == '__main__':
    conn = open_connection_with_configfile(config_file,verbose)
    try:
        print conn
    finally:
	if verbose >= 1: print "-Info- Logging out"
        conn.logout()
