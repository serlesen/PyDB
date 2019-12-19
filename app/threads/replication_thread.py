import requests

from threading import Thread

from app.threads.replication_stack import ReplicationStack

class ReplicationThread(Thread):

    def run(self):
        try:
            item = ReplicationStack.get_instance().pop()

            response = self.make_query(item)
            if response.status_code != 200:
                self.make_query(item)
        except:
            try:
                self.make_query(item)
            except Exception as e:
                print(f'Replication thread failed with {e}')
                item['error'] = str(e)
                ReplicationStack.get_instance().push_error(item)

    def make_query(self, item):
        if 'doc' in item:
            return requests.post(url = item['url'] + '/admin/replicate', data = item)
        return requests.delete(url = item['url'] + '/admin/replicate', data = item)

