# -*- coding: utf-8 -*-

import logging

from django.core.management.base import BaseCommand
from eulfedora.util import RequestFailed
from ...fedora.repository import rest_api
import lxml.etree as et

from ...models import Article, Issue

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """ Synchronize eruditorg database with Fedora
        1. Compare eruditorg objects(issues, articles) with those in Fedora
        2. Mark the ones deleted in Fedora as deleted in the database
    """

    help = 'Checks deleted objects in Fedora and mark them as deleted in database'

    def handle(self, *args, **options):
        logger.info("=" * 10 + "Deletion process started" + "=" * 10)

        # 1. Mark issues that are deleted in Fedora, as deleted in eruditorg database
        # get issues PID from fedora
        self.stdout.write('  Getting all issues PID in Fedora...')
        issues_fedora_query = "pid~erudit:erudit.*.* label='Publication Erudit'"
        issues_pids = self._get_pids_to_import(
            issues_fedora_query)

        issues_in_fedora = []
        for issue in issues_pids:
            issues_in_fedora.append(issue.split('.')[-1])

        # get issues identifier from database
        issues_in_database = []
        for issue in Issue.objects.filter(is_deleted=False).values('localidentifier'):
            issues_in_database.append(issue.get('localidentifier'))

        issues_to_delete = list(set(issues_in_database).difference(issues_in_fedora))
        self.stdout.write('  {} issues to delete in database'.format(len(issues_to_delete)))

        nb_deleted, nb_errors = 0, 0

        # mark those issues as deleted in the database
        for issue in issues_to_delete:
            try:
                del_issue = Issue.objects.get(localidentifier=issue)
                del_issue.is_deleted = True
                del_issue.save()
                nb_deleted += 1
                logger.info('    Issue with PID {} marked as deleted.'.format(del_issue.pid))
            except Issue.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    '      Failure deleting issue {0}. The issue is not available.'.format(
                        issue)))
                nb_errors += 1

        logger.info('Total issue deleted: {0}. Errors: {1}'.format(
            nb_deleted, nb_errors))

        # 2. Mark articles that are deleted in Fedora, as deleted in eruditorg database
        # get articles PID from fedora
        self.stdout.write('  Getting all articles PID in Fedora...')
        articles_fedora_query = "pid~erudit:erudit.*.*.* label='Unit Erudit'"
        articles_pids = self._get_pids_to_import(
            articles_fedora_query)

        articles_in_fedora = []
        for article in articles_pids:
            articles_in_fedora.append(article.split('.')[-1])

        # get articles identifier from database
        articles_in_database = []
        for article in Article.objects.filter(is_deleted=False).values('localidentifier'):
            articles_in_database.append(article.get('localidentifier'))

        articles_to_delete = list(set(articles_in_database).difference(articles_in_fedora))
        self.stdout.write('  {} articles to delete in database'.format(len(articles_to_delete)))

        nb_deleted, nb_errors = 0, 0

        # mark those articles as deleted in the database
        for article in articles_to_delete:
            try:
                del_article = Article.objects.get(localidentifier=article)
                del_article.is_deleted = True
                del_article.save()
                nb_deleted += 1
                logger.info('    Article with PID {} marked as deleted.'.format(
                    del_article.pid))
            except Article.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    '      Failure deleting article {0}. The article is not available.'.format(
                        article)))
                nb_errors += 1

        logger.info('Total articles deleted: {0}. Errors: {1}'.format(
            nb_deleted, nb_errors))

    def _get_pids_to_import(self, query):
        """ Returns the PIDS corresponding to a given Fedora query. """

        ns_type = {'type': 'http://www.fedora.info/definitions/1/0/types/'}
        pids = []
        session_token = None
        remaining_pids = True

        while remaining_pids:
            # The session token is used by the Fedora Commons repository to paginate a list of
            # results. We have to use it in order to construct the list of PIDs to import!
            session_token = session_token.text if session_token is not None else None
            try:
                response = rest_api.findObjects(query, chunksize=1000, session_token=session_token)
                # Tries to fetch the PIDs by parsing the response
                tree = et.fromstring(response.content)
                pid_nodes = tree.findall('.//type:pid', ns_type)
                session_token = tree.find('./type:listSession//type:token', ns_type)
                _pids = [n.text for n in pid_nodes]
            except RequestFailed as e:
                self.stdout.write(self.style.ERROR('  [FAIL]'))
                return
            else:
                pids.extend(_pids)

            remaining_pids = len(_pids) and session_token is not None

        self.stdout.write(self.style.SUCCESS('  [OK]'))
        if not len(pids):
            self.stdout.write(self.style.WARNING('  No PIDs found'))
        else:
            self.stdout.write('  {0} PIDs found!'.format(len(pids)))

        return pids
