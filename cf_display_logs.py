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


def generate_object_list(container, path_prefix="", mk=""):
    """Return a list of all files in the container that match the
    specified prefix. If no prefix supplied all objects returned.

    """
    obj_list = []
    obj_list_temp = container.list_objects(prefix=path_prefix, marker=mk)
    while obj_list_temp:
        obj_list.extend(obj_list_temp)
        mk = obj_list[-1]
        obj_list_temp = container.list_objects(prefix=path_prefix, marker=mk)
    return obj_list


def list_logs(log_container, search_term, num_files=0, start="", end=""):
    """List log objects.

    Search term must end with a '/'

    """
    first = ''.join((search_term, start))
    obj_list = generate_object_list(log_container, path_prefix=search_term,
                                    mk=first)
    s = len(search_term)
    e = len(end)
    last = ''
    if end:
        for obj in obj_list[::-1]:
            if end in obj[s:s + e]:
                last = obj
                break
        try:
            pos = obj_list.index(last) + 1
        except ValueError:
            pos = None
    else:
        pos = None
    date_filtered_list = obj_list[:pos]
    return date_filtered_list[-num_files:]


def get_logs(connection, container_search_term, cache=True, num_files=0,
             start_date='', end_date='', directory="DownloadedLogFiles"):
    """ Download log files for a container and cat them.

    cache=True controls whether or not the logs are cached not if the cache is
    read. The cache is always read.
    num_files is integer specifying number of files to download. The most
    recent file is num_files=1, if num_files is not specified or 0 all files
    downloaded
    start_date and end_date can be used to filter the logs. num_files is
    applied after the date filtering.

    """
    log_object_prefix = "".join((container_search_term, '/'))
    logs_container_name = ".CDN_ACCESS_LOGS"
    try:
        logs_container = connection.get_container(logs_container_name)
        log_list = list_logs(logs_container, log_object_prefix, num_files,
                             start_date, end_date)
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
    parser.add_argument('--start_date', default='',
                        help='display logs no older than date specified')
    parser.add_argument('--end_date', default='',
                        help='display logs older than date specified')
    args = parser.parse_args(line)
    print get_logs(connection, args.container, args.nocache, args.num_files,
                   args.start_date, args.end_date)

if __name__ == '__main__':
    conx = cf_connect.open_connection()
    cmd_parser(conx, argparse.ArgumentParser)
