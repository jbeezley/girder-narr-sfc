import json

from netCDF4 import Dataset, num2date
import numpy as np


def np_to_list(value):
    if isinstance(value, (np.ndarray, np.number)):
        value = value.tolist()
    return value


def coerce_object(obj):
    if isinstance(obj, dict):
        return {
            key: coerce_object(value) for key, value in obj.items()
        }
    elif isinstance(obj, (list, tuple)):
        return [
            coerce_object(value) for value in obj
        ]
    return np_to_list(obj)


def get_attributes(nc):
    return {
        attr: nc.getncattr(attr) for attr in nc.ncattrs()
    }


def get_times(time):
    return [
        t.isoformat() for t in num2date(time[:], time.units)
    ]


def summarize_slice(slice_):
    return {
        'min': slice_.min(),
        'max': slice_.max(),
        'mean': slice_.mean(),
        'var': slice_.var(),
        'chicago': slice_[25, 145],
        'north pole': slice_[0, 0],
        'south pole': slice_[-1, 0],
        'adelaide': slice_[65, 74],
        'barcelona': slice_[25, 1],
        'pacific': slice_[45, 105]
    }


def get_values(nc):
    return [
        summarize_slice(nc[index])
        for index in range(nc.shape[0])
    ]


def get_mean(key, values):
    return sum([v[key] for v in values]) / len(values)


def get_stats(values):
    if not values:
        return
    count = len(values)
    return {
        'count': count,
        'min': min([v['min'] for v in values]),
        'max': max([v['max'] for v in values]),
        'mean': get_mean('mean', values),
        'var': get_mean('var', values),
        'chicago': get_mean('chicago', values),
        'north pole': get_mean('north pole', values),
        'south pole': get_mean('south pole', values),
        'adelaide': get_mean('adelaide', values),
        'barcelona': get_mean('barcelona', values),
        'pacific': get_mean('pacific', values)
    }


def process_variable(nc):
    values = get_values(nc)
    return {
        'attributes': get_attributes(nc),
        'values': values,
        'stats': get_stats(values)
    }


def extract_file_metadata(file_path):
    nc = Dataset(file_path, 'r')
    metadata = {
        'attributes': get_attributes(nc),
        'variables': {
            'skt': process_variable(nc.variables['skt'])
        },
        'times': get_times(nc.variables['time'])
    }
    return coerce_object(metadata)


def main(*files):
    for file in files:
        with open(file + '.json', 'w') as f:
            f.write(json.dumps(extract_file_metadata(file), default=np_to_list))


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
