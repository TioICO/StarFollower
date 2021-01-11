## About
A simple tool that dumps the projects starred by the people you are following on GitHub!

The author knows nothing about OOP, clean coding, Python, etc. It just works.

### Built With
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [pandas](https://pandas.pydata.org/)
* [GitHub REST API](https://developer.github.com/v3/)

## Getting Started
```bash
git clone https://github.com/vungsung/StarFollower.git && cd StarFollower
pip3 install -r requirements.txt
python3 star_follower.py -h
```

## Usage
```
usage: star_follower.py [-h] [--db <URI>] [--dump <username>] [--self] [--pages <max number of pages>]
                        [--nlen <max length of repo name>] [--ulen <max length of repo url>]
                        [--dlen <max length of repo description>] [--export </path/to/file>]
                        [-f {excel,json,html,markdown}]
                        [--orderby {starred_by,repo_id,stars,pushed_at,repo_name,repo_url,description,language}] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --db <URI>            Set the SQL database as specified URI
  --dump <username>     Dump data from the specified username and update the database
  --self                Include root account (--username) when dumping stars
  --pages <max number of pages>
                        Set the max limit of pages to dump (100 projects per page)
  --nlen <max length of repo name>
                        Truncate repo names longer than length limit
  --ulen <max length of repo url>
                        Truncate repo urls longer than length limit
  --dlen <max length of repo description>
                        Truncate repo descriptions longer than length limit
  --export </path/to/file>
                        Export the database to specified file
  -f {excel,json,html,markdown}
                        Set the exporting format (default: excel)
  --orderby {starred_by,repo_id,stars,pushed_at,repo_name,repo_url,description,language}
                        Set the column name used by sorting (default: stars)
  -v, --verbose         Display verbose info
```

### Examples
* Dump projects starred by \<your_username\>'s following users and save them into the database
```bash
python3 star_follower.py --dump <your_username> --self --pages 10
```

* Query records from the database and export as a table in HTML, with the length limit set to 30 on repo names, 50 on repo urls and 250 on repo descriptions
```bash
python3 star_follower.py --export stars.html -f html --nlen 30 --ulen 50 --dlen 250
```
