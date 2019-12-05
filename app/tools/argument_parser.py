#
# Parser to validate the input argument.
# Deprecated
#
class ArgumentParser(object):

    keywords = ['$filter', '$size', '$map', '$skip', '$sort', '$map']

    def validate(input):
        for k in input.keys():
            if k not in ArgumentParser.keywords:
                return False
        return True
