"""
Core features
"""
from datetime import datetime
# third party
import pandas as pd
import requests
# local
from lib.log import logger
from lib.model import Star, init_db

class StarFollower(object):
    API_GATEWAY = 'https://api.github.com'
    columns = Star.__table__.columns.keys()

    def __init__(self, db_path : str):
        self.session = init_db(db_path)
        self._stars = self.session.query(Star).all()
        self._following = []

    def __dict_to_star(self, star):
        return Star(
            starred_by  = self._following,
            repo_id     = int(star['id']),
            stars       = star['stargazers_count'],
            #owner_name  = star['owner']['login'],
            #owner_url   = star['owner']['html_url'],
            pushed_at   = datetime.strptime(star['pushed_at'], '%Y-%m-%dT%H:%M:%SZ'),
            repo_name   = star['name'],
            repo_url    = star['html_url'],
            description = star['description'],
            language    = star['language']
        )

    def __fetch_stars_by_page(self, username, per_page=100, page=1):
        _result = requests.get(
            f"{self.API_GATEWAY}/users/{username}/starred?"
            f"per_page={per_page}&page={page}&sort=created&direction=desc",
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        if _result.status_code != 200:
            raise RuntimeError(f"fetch stars failed:\n({_result.status_code}) {_result.text}")
        return _result.json()

    def __fetch_followings_by_page(self, username, per_page=100, page=1):
        _result = requests.get(
            f"{self.API_GATEWAY}/users/{username}/following?"
            f"per_page={per_page}&page={page}",
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        if _result.status_code != 200:
            raise RuntimeError(f"fetch following users failed:\n({_result.status_code}) {_result.text}")
        return _result.json()

    def __fetch_stars_all(self, username, page_limit=0):
        _page = 1 # header['link']: page=(\d+).*$
        while True:
            if page_limit > 0 and _page > page_limit:
                logger.warning(f"aborted dumping {username} due to --max page limit")
                break
            logger.debug(f"fetching stars: page {_page}")
            _stars = self.__fetch_stars_by_page(username, page=_page)
            if not _stars:
                break
            try:
                self.__save_to_db(_stars)
                _page += 1
            except RuntimeError as e:
                logger.debug(str(e))
                break

    def __fetch_followings_all(self, username):
        _followings = []
        _page = 1
        while True:
            logger.debug(f"fetching following users: page {_page}")
            _followings_page = self.__fetch_followings_by_page(username, page=_page)
            if not _followings_page:
                break
            _followings += [_following['login'] for _following in _followings_page]
            _page += 1
        return _followings

    def __save_to_db(self, stars):
        for _star in stars:
            _star = self.__dict_to_star(_star)
            _replicated = self.__replicated_repo(_star.repo_id)
            if _replicated:
                if _star.starred_by == _replicated.starred_by:
                    raise RuntimeError('star replicated in db')
                else:
                    continue
            self._stars.append(_star)
            self.session.add(_star)

    def __replicated_repo(self, repo_id):
        for _star in self._stars:
            if repo_id == _star.repo_id:
                return _star
        return None

    def __truncate_columns(self, column_name, length_limit):
        _mask = self._df[column_name].str.len() > length_limit
        self._df.loc[_mask, column_name] = self._df[_mask].apply(
            lambda _row: _row[column_name][0:length_limit] + ' ...',
            axis=1
        )

    def export(self, output_file : str, name_limit : int, descr_limit : int, file_format : int, order_by : str):
        _stars = self.session.query( Star ).order_by( getattr(Star, order_by).desc() )
        self._df = pd.read_sql(_stars.statement, self.session.bind)
        if name_limit > 0:
            self.__truncate_columns('repo_name', name_limit)
        if descr_limit > 0:
            self.__truncate_columns('description', descr_limit)

        try:
            if file_format == 'excel':
                self._df.to_excel(output_file, index=False, engine='xlsxwriter')
            elif file_format == 'json':
                self._df.to_json(output_file, index=False, force_ascii=False)
            elif file_format == 'html':
                self._df.to_html(output_file, index=False, render_links=True)
            elif file_format == 'markdown':
                self._df.to_markdown(output_file, index=False)
        except RuntimeError as e:
            logger.exception('failed to export database')

    def dump(self, username : str, include_root : bool, page_limit : int=0):
        _followings = self.__fetch_followings_all(username)
        if include_root:
            _followings = [username] + _followings
        logger.debug(_followings)
        for self._following in _followings:
            logger.info(f"fetching following user: {self._following}")
            try:
                self.__fetch_stars_all(self._following, page_limit)
                logger.debug('saving changes to database')
                self.session.commit()
            except RuntimeError as e:
                logger.critical(str(e))
                break
