import requests

from threading import Thread

from app.threads.replication_stack import ReplicationStack
from app.tools.database_context import DatabaseContext

class ReplicationThread(Thread):
    """ Thread which sends the queries from ReplicationStack to update the connected slaves. """

    def run(self):
        try:
            item = ReplicationStack.get_instance().pop()

            url = item['url']
            del item['url']
            self.auth(url)

            response = self.make_query(item, url)
            if response.status_code == 401 or response.status_code == 403:
                self.auth(url)
                response = self.make_query(item, url)

            if response.status_code != 200:
                self.make_query(item, url)
        except:
            try:
                self.make_query(item, url)
            except Exception as e:
                print(f'Replication thread failed with {e}')
                item['error'] = str(e)
                ReplicationStack.get_instance().push_error(item)

    def make_query(self, item, url):
        if 'doc' in item:
            return requests.post(url = url + '/admin/replicate/sync', data = item, headers={'Authorization': f'Bearer {DatabaseContext.SLAVES[url]}'})
        return requests.delete(url = url + '/admin/replicate/sync', data = item, headers={'Authorization': f'Bearer {DatabaseContext.SLAVES[url]}'})

    def auth(self, url):
        if DatabaseContext.SLAVES[url] is None:
            response = requests.post(url = url + '/admin/replicate/auth')
            DatabaseContext.SLAVES[url] = response.json()['token']
