class ResultsMapper(object):

    def map(results, search_context):
        if search_context.map == None:
            return results

        mapped_results = []
        for r in results:
            mapped_results.append(ResultsMapper.map_single_result(r, search_context))
        return mapped_results

    def map_single_result(result, search_context):
        doc = {}
        for old_key in search_context.map.keys():
            new_key = search_context.map[old_key]
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
