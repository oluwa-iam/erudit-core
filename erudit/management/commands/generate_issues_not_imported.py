# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from eulfedora.util import RequestFailed
from ...fedora.repository import rest_api
import lxml.etree as et

from ...models import Issue


class Command(BaseCommand):
    """ Checks if issues in fedora are all in eruditorg database.
        Then generates a list of pid of the missing one
    """

    help = 'generate missing issues in database'

    def handle(self, *args, **options):
        issue_fedora_query = "pid~erudit:erudit.*.* label='Publication Erudit'"
        issue_pids = self._get_pids_to_import(
            issue_fedora_query)

        nb_missing_issues = 0
        with open('missing_issues.txt', 'w') as report:
            for index, ipid in enumerate(issue_pids):
                try:
                    Issue.objects.get(localidentifier=ipid.split('.')[-1])
                except Issue.DoesNotExist:
                    nb_missing_issues += 1
                    report.write('{}\n'.format(ipid))
                    self.stdout.write('PID {}: {}'.format(index, ipid))

        print('Total Missing issues: {}'.format(nb_missing_issues))

    def _get_pids_to_import(self, query):
        """ Returns the PIDS corresponding to a given Fedora query. """
        self.stdout.write('  Determining PIDs to import...', ending='')

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
