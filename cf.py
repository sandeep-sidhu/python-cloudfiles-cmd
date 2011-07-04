__author__ = "Sandeep Sidhu <sandeep.pal.sidhu@gmail.com>"
import cmd
import os
import cf_display_logs
import cf_argparser

import cf_connect
from cf_list_containers import list_containers
from cf_list_containers import list_public_containers
from cf_list_files import list_files
from cf_delete_container import delete_container
from cf_create_container import create_container
from cf_info_container import info_container
from cf_download_file import download_file
from cf_upload_file import upload_file


class InteractiveCloudfiles(cmd.Cmd):
    """Simple interactive command line interface to cloud files."""
    prompt = 'CF>>'
    intro = '\nInteractive command line interface to cloud files'
    doc_header = 'Documented commands'
    misc_header = 'misc commands'
    undoc_header = 'Undocumented commands'
    ruler = '-'

    def __init__(self):
        self.use_container = ""
        self.dst_directory = "./"
        self.verbose = 3
        self.last_output = ''
        self.conx = cf_connect.open_connection()
        cmd.Cmd.__init__(self)

    def do_list(self, line):
        if (self.use_container == ".." or not self.use_container):
            if line:
                list_files(self.conx, line)
            else:
                list_containers(self.conx)
        else:
            list_files(self.conx, self.use_container)
    do_ls = do_list

    def do_list_public(self, line):
        list_public_containers(self.conx)

    def do_download(self, line):
        if line:
            arguments = line.split()
            if (self.use_container == ".." or not self.use_container):
                print("-Error- please select a container"
                      " first with use command")
            else:
                for argument in arguments:
                    print "-Info- now downloading '%s'" % argument
                    download_file(self.conx, self.use_container, argument,
                                  self.dst_directory, self.verbose)
        else:
            print '-Error- no filename[s] given to download'
            print "        use 'help download' to get more help"

    def do_upload(self, line):
        if line:
            arguments = line.split()
            if (self.use_container == ".." or not self.use_container):
                print("-Error- please select a container first with 'use' "
                      "command")
            else:
                for argument in arguments:
                    print "-Info- now uploading '%s'" % argument
                    upload_file(self.conx, self.use_container,
                                argument, self.verbose)
        else:
            print '-Error- no filename[s] given to upload'
            print "        use 'help upload' to know command usages"

    def do_create(self, line):
        if line:
            create_container(self.conx, line, self.verbose)
        else:
            print("-Info- no container named passed, please try 'help create' "
                  "to learn the command options")

    def help_create(self):
        print '\n'.join(['create [container_name]',
                         'Create a new container with a the given name'])

    def do_use(self, line):
        self.use_container = line
        if not self.use_container:
            print "No container selected."
        else:
            print "Current container in use '%s'" % self.use_container
    do_cd = do_use

    def help_use(self):
        print '\n'.join(['use [container_name] ',
                         ('default container to used for file'
                          ' upload and download operations '),
                         'cd [container_name] does the same job as well'])
    help_cd = help_use

    def do_pwd(self, line):
        if self.use_container:
            print self.use_container
        else:
            print "No container selected."

    def help_pwd(self):
        print '\n'.join([
            'pwd', "prints the current container setup with 'use' command"])

    def do_remove(self, line):
        if line:
            answer = raw_input(
                'Do you really want to remove the container? [yes/no]')
            if answer.lower() == "yes":
                delete_container(self.conx, line, self.verbose)
            else:
                print 'Container not deleted, canceled by user action'
        else:
            print("-Info- no container named passed, please try 'help remove' "
                  "to learn the command options")

    def help_remove(self):
        print '\n'.join([
                    'remove [container_name]',
                    'Remove the specified container from your cloud files',
                    'currently it only remove empty containers'])

    def do_info(self, line):
        if line:
            info_container(self.conx, line, self.verbose)
        else:
            info_container(self.conx, self.use_container, self.verbose)

    def help_info(self):
        print '\n'.join(['info [container_name]',
                         'Provide detailed information about the container',
                         'like container size, CDN publish status, CDN URI'])

    def do_logout(self, line):
        if self.verbose >= 2:
            print '-Debug- Logging off'
        self.conx.logout()
        if self.verbose >= 1:
            print '-Info- Logged off current session'

    def do_debug(self, line):
        print 'Current debug level:', self.verbose
        print '\n'.join(['0 = Error messages only',
                         '1 = Info messages',
                         '2 = Debug info ',
                         '3 = More debug info'])
        answer = raw_input('Set the debug level, press enter'
                           ' to leave the current level:')
        if answer:
            if self.verbose >= 2:
                print '-Debug- debug level passed:', answer
            self.verbose = int(answer)
            if self.verbose >= 1:
                print '-Info- current debug level:', self.verbose
        else:
            if self.verbose >= 1:
                print '-Info- current debug level:', self.verbose

    def do_shell(self, line):
        """Run a shell command"""
        print "running shell commands:", line
        output = os.popen(line).read()
        print output
        self.last_output = output

    def do_echo(self, line):
        """print the input, replacing '$out' with the output of the last shell
        command.
        """
        print line.replace('$out', self.last_output)

    def default(self, line):
        print '-Error- command not recognized'
        print "        Please type 'help' to get a list of available commands"

    def do_exit(self, line):
        return True

    do_EOF = do_exit
    do_quit = do_exit
    do_q = do_exit

    def help_exit(self):
        print "Exit the CF interpreter."
        print "You can also use the 'Ctrl-D' shortcut or press 'q'"

    help_q = help_exit
    help_quit = help_exit

    def do_display_logs(self, line):
        """Display CDN logs for a container."""
        try:
            cf_display_logs.cmd_parser(self.conx, cf_argparser.ArgParseThrower,
                                       line=line.split(),
                                       prog_name='display_logs')
        except cf_argparser.ArgumentError as arg_err:
            print arg_err

if __name__ == '__main__':
    InteractiveCloudfiles().cmdloop()
