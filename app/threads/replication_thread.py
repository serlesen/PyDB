import requests

from threading import Thread

from app.threads.replication_stack import ReplicationStack
from app.tools.database_context import DatabaseContext

class ReplicationThread(Thread):
    """ Thread which sends the queries from ReplicationStack to update the connected slaves. """

    def __init__(self):
        Thread.__init__(self)
        self.item = ReplicationStack.get_instance().pop()


    def run(self):
        try:
            url = self.item['url']
            del self.item['url']
            self.auth(url)

            response = self.make_query(url)
            if response.status_code == 401 or response.status_code == 403:
                self.auth(url)
                response = self.make_query(url)

            if response.status_code != 200:
                self.make_query(url)
        except:
            try:
                self.make_query(url)
            except Exception as e:
                print(f'Replication thread failed with {e}')
                self.item['error'] = str(e)
                ReplicationStack.get_instance().push_error(self.item)

    def make_query(self, url):
        if 'doc' in self.item:
            return requests.post(url = url + '/admin/replicate/sync', data = self.item, headers={'Authorization': f'Bearer {DatabaseContext.SLAVES[url]}'})
        return requests.delete(url = url + '/admin/replicate/sync', data = self.item, headers={'Authorization': f'Bearer {DatabaseContext.SLAVES[url]}'})

    def auth(self, url):
        if DatabaseContext.SLAVES[url] is None:
            response = requests.post(url = url + '/admin/replicate/auth')
            DatabaseContext.SLAVES[url] = response.json()['token']
