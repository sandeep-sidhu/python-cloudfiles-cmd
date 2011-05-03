__author__ = "Sandeep Sidhu <sandeep.pal.sidhu@gmail.com>"
import cloudfiles
import cmd
import os
from cf_connect import open_connection_with_configfile
from cf_connect import open_connection_with_credentials
from cf_list_containers import list_containers
from cf_list_containers import list_public_containers
from cf_list_files import list_files
from cf_delete_container import delete_container
from cf_create_container import create_container
from cf_info_container import info_container
from cf_download_file import download_file
from cf_upload_file import upload_file

verbose=3
use_container="none"
dst_directory="./"
config_file="~/.pycflogin"

class InteractiveCloudfiles(cmd.Cmd):
	"""Simple interactive command line interface to cloud files"""	
	prompt = 'CF>>'
	intro = '\nInteractive command line interface to cloud files'
	doc_header = 'Documented commands'
	misc_header = 'misc commands'
	undoc_header = 'Undocumented commands'
	
	ruler = '-'

	def do_list(self,line):
		global use_container
		if (use_container == ".." or use_container == "none"):
			if line:
				list_files(conx,line)
			else:
				list_containers(conx)	
		else:
			list_files(conx,use_container)
	do_ls = do_list
	def do_list_public(self,line):
		list_public_containers(conx)
	def do_download(self,line):
		global use_container
		global dst_directory
		if line:
			arguments = line.split()
			if (use_container == ".." or use_container == "none"):
				print "-Error- please select a container first with use command"
			else:
				for argument in arguments:
					print '-Info- now downloading \'%s\'' % argument
					download_file(conx,use_container,argument,dst_directory,verbose)
		else:
			print '-Error- no filename[s] given to download'
			print '        use \'help download\' to get more help'
	def do_upload(self,line):
		global use_container
		if line:
			arguments = line.split()
			if (use_container == ".." or use_container == "none"):
				print "-Error- please select a container first with \'use\' command"
			else:
				for argument in arguments:
					print '-Info- now uploading \'%s\'' % argument
					upload_file(conx,use_container,argument,verbose)
		else:
			print '-Error- no filename[s] given to upload'
			print '        use \'help upload\' to know command usages'

	def do_create(self,line):
		if line:
			create_container(conx,line,verbose)
		else:
			print '-Info- no container named passed, please try \'help create\' to learn the command options'
	def help_create(self):
		print '\n'.join([ 'create [container_name]',
                                   'Create a new container with a the given name',
                                ])
	def do_use(self,line):
		global use_container
		use_container = line
		print 'Current container in use \'%s\'' % use_container
	do_cd = do_use
	def help_use(self):
		print '\n'.join([ 'use [container_name] ',
                                  'default container to used for file upload and download operations ',
				  'cd [container_name] does the same job as well',
                                ])
	help_cd = help_use
	def do_pwd(self,line):
		print use_container
	def help_pwd(self):
		print '\n'.join([ 'pwd',
                                  'prints the current container setup with \'use\' command',
                                ])
	def do_remove(self,line):
		if line:
			answer = raw_input('Do you really want to remove the container? [yes/no]')
			if answer == "yes" or answer == "YES":
				delete_container(conx,line,verbose)
			else:
				print 'Container not deleted, canceled by user action'
		else:
			print '-Info- no container named passed, please try \'help remove\' to learn the command options'
	def help_remove(self):
		print '\n'.join([ 'remove [container_name]',
                                   'Remove the specified container from your cloud files',
				   'currently it only remove empty containers',
                                ])
	def do_info(self,line):
		if line:
			info_container(conx,line,verbose)
		else:
			print '-Info- no container name given, please try \'help info\' to lear the command options'
	def help_info(self):
		print '\n'.join([ 'info [container_name]',
                                   'Provide detailed information about the container',
				   'like container size, CDN publish status, CDN URI',
                                ])
	def do_logout(self,line):
		if verbose >=2: print '-Debug- Logging off'
		conx.logout()
		if verbose >=1: print '-Info- Logged off current session'
	def do_debug(self,line):
		global verbose
		print 'Current debug level:',verbose
		print '\n'.join([  '0 = Error messages only',
                                   '1 = Info messages',
                                   '2 = Debug info ',
                                   '3 = More debug info',
                                ])
		answer = raw_input('Set the debug level, press enter to leave the current level:')
		if answer != "":
			if verbose >=2:  print '-Debug- debug level passed:', answer
			verbose = int(answer)
			if verbose >=1: print '-Info- current debug level:', verbose
		else:
			if verbose >=1: print '-Info- current debug level:', verbose
	def do_shell(self,line):
		"Run a shell command"
		print "running shell commands:", line
		output = os.popen(line).read()
		print output
		self.last_output = output
	def do_echo(self,line):
		"print the input, replacing '$out' with the output of the last shell command"
		# Obvisously not robuts
		print line.replace('$out', self.last_output)
	def default(self,line):
		print '-Error- command not recognized'
		print "        Please type \'help\' to get a list of available commands"
	def do_exit(self, line):
		return True
	def help_exit(self):
		print "Exit the CF interpreter."
        	print "You can also use the \'Ctrl-D\' shortcut or press \'q\'"
	do_EOF = do_exit
	do_quit = do_exit
	do_q = do_exit
	help_q = help_exit
	help_quit = help_exit

if __name__ == '__main__':
	answer = raw_input('Login with credentials from ~/.pycflogin file? [yes/no]')
	if answer == "yes" or answer == "YES":
		conx = open_connection_with_configfile(config_file,verbose)
	else:
		print 'Please provide the Cloud Files login details'
		username = raw_input('username:')
		api_key = raw_input('api_key:')
		auth_url = raw_input('auth_url, [us/uk]')
		conx = open_connection_with_credentials(username,api_key,auth_url)

	InteractiveCloudfiles().cmdloop()
