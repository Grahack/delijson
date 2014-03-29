#!/usr/bin/env python3

"""Parse HTML exports of Delicious bookmarks to create JSON reports.

See the README.md and LICENCE for more informations.
http://https://github.com/Grahack/delijson

"""

import sys
from collections import defaultdict
import json

RELEVANCE = 20  # only tags that have this count are involved in relations

def main(delicious_export, formats):
    # partition (dict from tags_lists to list of links)
    partition = defaultdict(list)
    # tag counts
    tags = defaultdict(int)
    # couples of tags count
    relations = defaultdict(int)
    for line in open(delicious_export):
        tags_list = tags_list_from_line(line)
        tags_str = ','.join(tags_list)
        if tags_list:
            partition[tags_str].append(get_html_attribute(line, 'HREF'))
            for tag in tags_list:
                tags[tag] += 1
            for relation in ordcouples_in_list(tags_list):
                relation_str = relation[0] + ' ' + relation[1]
                if tags[relation[0]] >= RELEVANCE and \
                   tags[relation[1]] >= RELEVANCE:
                    relations[relation_str] +=1
    # Some post processing:
    data = {}
    # Count and sort partition of tag combinations.
    data['partition'] = [{'tags': tags,
                        'links': partition[tags],
                        'count': len(partition[tags])} for tags in \
                          sorted(partition.keys(),
                                 key = lambda tags: (-len(partition[tags]), tags))]
    # Sort tag counts.
    data['tags'] = [{'tag': tag, 'count': tags[tag]} for tag in \
                     sorted(tags, key = lambda tag: -tags[tag])]
    # Sort relations
    data['relations'] = [{'relation': rel, 'count': relations[rel]} for rel in \
                          sorted(relations, key = lambda rel: -relations[rel])]

    # Now write demanded files.
    for type_of_data in formats:
        f = open(type_of_data + '.json', 'w')
        json.dump(data[type_of_data], f, separators=(',\n', ':'))
        f.close()

def get_html_attribute(line, attr_name):
    idx_name = line.find(attr_name)
    if idx_name > 0:
        attr_start = idx_name + len(attr_name) + 2  # 2 for ="
        attr_end = line.find('"', attr_start)
        return line[attr_start:attr_end].strip()
    else:
        return None

def tags_list_from_line(line):
    tags_str = get_html_attribute(line, 'TAGS')
    if tags_str is not None:
        tags_list = [tag.strip() for tag in tags_str.split(',')]
        return sorted(tags_list)
    else:
        return []

def ordcouples_in_range(n):
    """Given 0, 1,... n-1, return a list of ordered couples."""
    if n <= 1:
        return []
    else:
        return [(i, n-1) for i in range(n-1)] + ordcouples_in_range(n-1)

def ordcouples_in_list(l):
    """Given a list, return a list of couples of elements (sorting is kept)."""
    return [(l[i], l[j]) for i,j in ordcouples_in_range(len(l))]

if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit("Please specify a Delicious export file (.html).")
    delicious_export = sys.argv[1]
    if len(sys.argv) == 2:
        formats = ['partition', 'tags', 'relations']
    else:
        formats = sys.argv[2:]
    main(delicious_export, formats)
