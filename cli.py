#!/usr/bin/env python
# Copyright (C) 2012 Buttinsky Developers.
# See 'COPYING' for copying permission.

import cmd
import sys
import string
import xmlrpclib
import getopt


class CLI(cmd.Cmd):

    def __init__(self, connection):
        cmd.Cmd.__init__(self)
        self.prompt = '\033[1;30m>>\033[0m '
        self.conn = connection
        self.doc_header = 'Available commands (type help <topic>):'
        self.undoc_header = ''
        self.intro = "\
            ____        __  __  _            __        \n\
           / __ )__  __/ /_/ /_(_)___  _____/ /____  __\n\
          / __  / / / / __/ __/ / __ \/ ___/ //_/ / / /\n\
         / /_/ / /_/ / /_/ /_/ / / / (__  ) ,< / /_/ / \n\
        /_____/\__,_/\__/\__/_/_/ /_/____/_/|_|\__, /  \n\
                                              /____/   \n\
        \033[1;30mButtinsky Command Line Interface\n\tType 'help' for a list of commands\033[0m\n\n"

    def do_create(self, arg):
        """
        \033[1;30msyntax: create <id> <conf> -- create new configuration from JSON encoded string and identify it using id\033[0m
        """
        args = arg.split(' ')
        
        try:
            ret = self.conn.create(args[0], args[1])
            print ret
        except xmlrpclib.Fault as err:
            print "Operation denied\n"

    def do_echo(self, arg):
       """
       \033[1;30msyntax: echo <message> -- send message to echo function to test non-blocking functionality\033[0m
       """
       try:
           ret = self.conn.echo(arg)
           print ret
       except xmlrpclib.Fault as err:
           print "Operation denied\n"   

    def do_load(self, arg):
        """
        \033[1;30msyntax: load <id> <filename> -- load configuration from specified filename and identify it using id\033[0m
        """
        args = arg.split(' ')
        try:
            ret = self.conn.load(args[0], args[1])
            print ret
        except xmlrpclib.Fault as err:
            print "Operation denied\n"

    def do_status(self, arg):
        """
        \033[1;30msyntax: status -- show all running monitors\033[0m
        """
        try:
            ret = self.conn.status()
            print ret
        except xmlrpclib.Fault as err:
            print "Operation denied\n"

    def do_stop(self, arg):
        """
        \033[1;30msyntax: stop <id> -- stop execution of monitor identified by id\033[0m
        """
        try:
            ret = self.conn.stop(arg)
            print ret
        except xmlrpclib.Fault as err:
            print "Operation denied\n"

    def do_restart(self, arg):
        """
        \033[1;30msyntax: restart <id> -- restart execution of monitor identified by id\033[0m
        """
        try:
            ret = self.conn.restart(arg)
            print ret
        except xmlrpclib.Fault as err:
            print "Operation denied\n"

    def do_delete(self, arg):
        """
        \033[1;30msyntax: delete <id> -- delete configuration of monitor identified by id\033[0m
        """
        try:
            ret = self.conn.delete(arg)
            print ret
        except xmlrpclib.Fault as err:
            print "Operation denied\n"

    def do_quit(self, arg):
        """
        \033[1;30msyntax: quit -- exit the client gracefully, Shortcut: 'q'\033[0m
        """
        sys.exit(1)

    def help_help(self):
        print "\t\033[1;30msyntax: help <topic> -- Show help for a particular topic. List all commands if topic is not specified\033[0m"

    def default(self, arg):
        print "Unknown command: " + arg + "\n"

    def emptyline(self):
        pass

    # shortcuts
    do_q = do_quit


def usage():
    print "\nusage: cli.py [-h] [-s server] [-p port]\n\n"\
          "\t-h\t\tthis help text\n"\
          "\t-s server\thostname of the server, default: localhost\n"\
          "\t-p port\t\tport number of the server, default: 8000\n"

def main():
    server = "localhost"
    port = "8000"

    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "hs:p:")
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)   
           
    for opt, arg in opts:                
        if opt in ("-h"):      
            usage()                     
            sys.exit()                  
        elif opt in ("-s"):                
            server = arg                  
        elif opt in ("-p"): 
            port = arg

    url = "http://" + server + ":" + port + "/"
    conn = xmlrpclib.ServerProxy(url)
    try:
        ret = conn.echo("lets do some echoing")
    except xmlrpclib.Fault as err:
        print "Operation denied\n"
        sys.exit(2)

    CLI(conn).cmdloop()

if __name__ == "__main__":
    main()

