#
# Class to map the resulting document to the desired output format.
#
class ResultsMapper(object):

    def map(results, search_context):
        if search_context.map == None:
            return results

        mapped_results = []
        if '$exclude' in search_context.map:
            exclusions = search_context.map['$exclude']
            for r in results:
                mapped_results.append(ResultsMapper.exclude_single_result(r, exclusions, ''))
        else:
            if '$include' in search_context.map:
                mapping = search_context.map['$include']
            else:
                mapping = search_context.map
            for r in results:
                mapped_results.append(ResultsMapper.map_single_result(r, mapping))
        return mapped_results

    def exclude_single_result(result, exclusions, prefix):
        doc = {}
        for k in result.keys():
            if prefix + k not in exclusions:
                if isinstance(result[k], dict):
                   doc[k] = ResultsMapper.exclude_single_result(result[k], exclusions, k + '.')
                else:
                    doc[k] = result[k]
        return doc

    def map_single_result(result, mapping):
        doc = {}
        for old_key in mapping.keys():
            new_key = mapping[old_key]
            if '.' in old_key:
                value = ResultsMapper.search_value(result, old_key)
            else:
                value = result[old_key]

            if '$itself' == new_key:
                doc[old_key] = value
            elif '.' in new_key:
                doc.update(ResultsMapper.build_doc(value, new_key))
            else:
                doc[new_key] = value
        return doc

    def search_value(result, field):
        inner_doc = result
        fields = field.split('.')
        for f in fields:
            inner_doc = inner_doc[f]

        return inner_doc

    def build_doc(value, field):
        doc = value
        fields = field.split('.')
        for f in reversed(fields):
            doc = {f: doc}

        return doc
