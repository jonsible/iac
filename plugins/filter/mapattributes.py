def mapattributes(list_of_dicts, list_of_keys):
    l = []
    for di in list_of_dicts:
        newdi = {}
        for key in list_of_keys:
            newdi[key] = di[key]
        l.append(newdi)
    return l


class FilterModule(object):
    def filters(self):
        return {"mapattributes": mapattributes}
