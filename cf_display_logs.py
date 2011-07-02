import sys
import cloudfiles
import gzip
import StringIO
import os
import argparse
import cf_connect


def format_filename(log_name):
    """Convert log object name to container name and file name.

    Input
    Log name:
    MyContainer/2011/06/10/04/e0c6bb6a9a704789c525bf5d022ce2b7.log.0.gz
    Output
    Container:
    MyContainer
    Filename:
    2011061004-e0c6bb6a9a704789c525bf5d022ce2b7.log

    """
    names = log_name.partition('/')
    filename = names[2].replace('/', '', 3)
    filename = filename.replace('/', '-', 1)
    filename = filename[:-3].rpartition('.')[0]
    container = names[0]
    return container, filename


def cache_log(container, filename, data, directory):
    """Write object to file in directory specified."""
    try:
        os.makedirs('/'.join((directory, container)))
    except os.error:
        pass
    with open('/'.join((directory, container, filename)), 'wb') as f:
        f.write(data)


def generate_object_list(container, path_prefix=""):
    """Return a list of all files in the container that match the
    specified prefix. If no prefix supplied all objects returned.

    """
    obj_list = []
    mark = ''
    obj_list_temp = container.list_objects(prefix=path_prefix, marker=mark)
    while obj_list_temp:
        obj_list.extend(obj_list_temp)
        mark = obj_list[-1]
        obj_list_temp = container.list_objects(prefix=path_prefix, marker=mark)
    return obj_list


def list_logs(container_object, search_term, num_files=0):
    """List num_files newest logs."""
    obj_list = generate_object_list(container_object, path_prefix=search_term)
    return  obj_list[-num_files:]


def get_logs(connection, container_search_term, cache=True, num_files=0,
             directory="DownloadedLogFiles"):
    """ Download log files for a container and cat them.

    cache=True controls whether or not the logs are cached not if the cache is
    read. The cache is always read.
    default downloads all log files
    num_files is integer specifying number of files to download. The most
    recent file is num_files=1, if num_files is not specified or 0 all files
    downloaded

    """
    obj = ""
    log_object_prefix = "/".join((container_search_term, obj))
    logs_container_name = ".CDN_ACCESS_LOGS"
    try:
        logs_container = connection.get_container(logs_container_name)
        log_list = list_logs(logs_container, log_object_prefix, num_files)
        data = []
        for log in log_list:
            container, filename = format_filename(log)
            try:
                file_path = (directory, container, filename)
                with open('/'.join(file_path), 'rb') as f:
                    data.append(f.read())
            except IOError:
                log_gz = logs_container.get_object(log).read()
                log_gz_fobj = StringIO.StringIO(log_gz)
                with gzip.GzipFile(fileobj=log_gz_fobj, mode='rb') as log_file:
                    log_data = log_file.read()
                    if cache:
                        cache_log(container, filename, log_data, directory)
                    data.append(log_data)
        data_string = ''.join(data)
        return data_string
    except cloudfiles.errors.NoSuchContainer:
        print "Either logs aren't enabled or no logs have been generated yet."


def cmd_parser(connection, parser_class,
               line=sys.argv[1:], prog_name=sys.argv[0]):
    """Provide commandline interface for get_logs."""
    parser = parser_class(description='Display container CDN logs.',
                          prog=prog_name)
    parser.add_argument('container',
                        help='name of CDN and log enabled container')
    # counter-intuitively if nocache is True, caching will be used.
    parser.add_argument('--nocache', default=True, action='store_false',
                        help='cache logs on local machine.')
    parser.add_argument(
        '--num_files',
        default=0,
        type=int,
        help='number of log files to display, starting with the most recent.')
    args = parser.parse_args(line)
    print get_logs(connection, args.container, args.nocache, args.num_files)

if __name__ == '__main__':
    conx = cf_connect.open_connection()
    cmd_parser(conx, argparse.ArgumentParser)
