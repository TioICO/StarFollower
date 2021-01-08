import argparse
import logging
# local
from lib.core import StarFollower
from lib.log import logger

def parse_args():
    DOC_EXAMPLE = '''
examples:
### Dump projects starred by <username>'s following user and save them in the database
> python3 star_follower.py --dump <your_username> --self --pages 10

### Query records from the database and export as a table in HTML with the length limit set to 30 on repo names and 250 on repo descriptions
> python3 star_follower.py --export stars.html -f html --nlen 30 --dlen 250
'''

    parser = argparse.ArgumentParser()
    parser.add_argument('--db', metavar='<URI>', type=str, default='sqlite:///star_follower.db', help='Set the SQL database as specified URI')
    parser.add_argument('--dump', metavar='<username>', type=str, help='Dump data from the specified username and update the database')
    parser.add_argument('--self', action='store_true', help='Include root account (--username) when dumping stars')
    parser.add_argument('--pages', metavar='<max number of pages>', type=int, default=0, help='Set the max limit of pages to dump (100 projects per page)')
    parser.add_argument('--nlen', metavar='<max length of repo name>', type=int, default=0, help='Truncate repo names longer than length limit')
    parser.add_argument('--dlen', metavar='<max length of repo description>', type=int, default=0, help='Truncate repo descriptions longer than length limit')
    parser.add_argument('--export', metavar='</path/to/file>', type=str, help='Export the database to specified file')
    parser.add_argument('-f', dest='format', default='excel', choices=['excel', 'json', 'html', 'markdown'], type=str, help='Set the exporting format (default: excel)')
    parser.add_argument('--orderby', default='stars', choices=StarFollower.columns, type=str, help='Set the column name used by sorting (default: stars)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Display verbose info')

    args = parser.parse_args()
    if not args.dump and not args.export:
        parser.print_help()
        print(DOC_EXAMPLE)
        parser.exit(1)
    return args

def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    star_follower = StarFollower(db_path=args.db)
    if args.dump:
        star_follower.dump(args.dump, page_limit=args.pages, include_root=args.self)
        logger.info('[+] Finished dumping!')
    elif args.export:
        star_follower.export(args.export, name_limit=args.nlen, descr_limit=args.dlen, file_format=args.format, order_by=args.orderby)
        logger.info('[+] Finished exporting!')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        ...
