"""Script for searching spots' information using Google Maps API.

- Usage: python search.py -i input -o output -k api_key
- Example: python search.py -i input.txt -o output.json -k Alza...fff
- Requires Google Maps python client.
  (See https://github.com/googlemaps/google-maps-services-python)
"""

from __future__ import print_function

import getopt
import json
import sys

import googlemaps


def read_input(path_input):
    print('Reading the names of the spots from %s... ' % path_input, end='')

    with open(path_input, 'rb') as p:
        lines = p.readlines()

    list_names = []

    for s in lines:
        if s and (s[0] == '-'):
            list_names.append(s[1:].strip())

    print('Success!')
    return list_names


def write_output(dict_info, path_output):
    print('Writing the data to %s... ' % path_output, end='')

    with open(path_output, 'wb') as p:
        json.dump(dict_info, fp=p, indent=4)

    print('Success!')


def retrieve(dc, key_1, key_2=None):
    value = dc.get(key_1)

    if (key_2 is not None) and value:
        return value.get(key_2)
    else:
        return value


def search_info(list_names, api_key):
    dict_info = {}
    client = googlemaps.Client(api_key)

    for name in list_names:
        print('Searching "%s"... ' % name, end='')

        # (1) simple info (including place id)
        # noinspection PyUnresolvedReferences
        response = client.places(name)

        if response['status'] != 'OK' or (not response['results']):
            print('Failed!')
            continue

        info_simple = response['results'][0]

        # (2) detail info (ex. opening hours)
        # noinspection PyUnresolvedReferences
        response_detail = client.place(info_simple['place_id'])

        if response_detail['status'] != 'OK':
            print('Failed!')
            continue

        info_detail = response_detail['result']

        # pack the values we need
        dict_info[name] = {
            'name': retrieve(info_simple, 'name'),
            'place_id': retrieve(info_simple, 'place_id'),
            'location': retrieve(info_simple, 'geometry', 'location'),
            'website': retrieve(info_detail, 'website'),
            'url': retrieve(info_detail, 'url'),
            'rating': retrieve(info_detail, 'rating'),
            'utc_offset': retrieve(info_detail, 'utc_offset'),
            'phone': retrieve(info_detail, 'international_phone_number'),
            'vicinity': retrieve(info_detail, 'vicinity'),
            'address': retrieve(info_detail, 'formatted_address'),
            'types': retrieve(info_detail, 'types'),
            'opening_hours': retrieve(info_detail, 'opening_hours',
                                      'weekday_text'),
            'icon': retrieve(info_detail, 'icon')
        }

        print('Success!')

    return dict_info


def print_usage():
    print('\nUsage: %s [-i input] [-o output] -k api_key\n'
          '(Default: -i input.txt, -o output.json)' % sys.argv[0])


def parse_args():
    path_input = 'input.txt'
    path_output = 'output.json'
    api_key = None

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'i:o:k:')

        for o, a in opts:
            if o == '-i':
                path_input = a
            elif o == '-o':
                path_output = a
            elif o == '-k':
                api_key = a
            else:
                raise getopt.GetoptError('unhandled option')

        if api_key is None:
            raise getopt.GetoptError('option -k is necessary')
    except getopt.GetoptError as e:
        print(str(e))
        print_usage()

        return None

    return path_input, path_output, api_key


def main():
    args = parse_args()

    if args is None:
        return

    path_input, path_output, api_key = args

    list_names = read_input(path_input)
    dict_info = search_info(list_names, api_key)
    write_output(dict_info, path_output)


if __name__ == '__main__':
    main()
