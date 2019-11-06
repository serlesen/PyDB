class ArgumentParser(object):

    keywords = ['filter', 'size', 'map', 'skip', 'sort', 'map']

    def validate(input):
        for k in input.keys():
            if k not in self.keywords:
                return False
        return True
