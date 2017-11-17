from collections import namedtuple


def NamedTuple(**kw):
    """ Convert a dictionary of any depth to nested NamedTuples """
    def _get_kws(**kw):
        kw_dict = {}
        for k, v in kw.items():
            if isinstance(v, dict):
                kw_dict[k] = NamedTuple(**v)
            else:
                kw_dict[k] = v

        return kw_dict

    kw = _get_kws(**kw)
    cls = namedtuple('NamedTuple', ' '.join(kw.keys()))
    return cls(**kw)


if __name__ == '__main__':
    data = {
        'regions': {
            'westcoast': {
                'cities': ['san francisco', 'portland', 'seattle', 'los angeles']
            },
            'eastcoast': {
                'cities': ['new york', 'washington dc', 'boston'] 
            }
        }
    }

    data_namedtuple = NamedTuple(**data)

    assert 'san francisco' in data_namedtuple.regions.westcoast.cities
