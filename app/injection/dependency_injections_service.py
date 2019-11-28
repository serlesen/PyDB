class DependencyInjectionsService(object):

    instance = None

    def __init__(self):
        self.services = {}

    @staticmethod
    def get_instance():
        if DependencyInjectionsService.instance is None:
            DependencyInjectionsService.instance = DependencyInjectionsService()
        return DependencyInjectionsService.instance
    
    def get_service(self, service_name):
        if str(service_name) not in self.services:
            self.services[str(service_name)] = service_name()
        return self.services[str(service_name)]

