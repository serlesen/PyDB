#
# Parser to validate the input argument.
#
class ArgumentParser(object):

    keywords = ['$filter', '$size', '$map', '$skip', '$sort', '$map']

    reserved_collection_names = ['users']

    def validate(input):
        for k in input.keys():
            if k not in ArgumentParser.keywords:
                return False
        return True

    def validate_collection_name(collection):
        if collection in ArgumentParser.reserved_collection_names:
            return False
        return True

