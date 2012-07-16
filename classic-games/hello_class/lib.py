#!/usr/bin/env python

def format_items(items):
    l = []
    for item in items:
        l.append("%s: %s" % (items.index(item), item.name))
    return ', '.join(l)
