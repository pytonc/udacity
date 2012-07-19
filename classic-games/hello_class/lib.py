#!/usr/bin/env python

# returns number of possible columns given, box-width, item(col)-width and padding
def get_cols(box_w, padding, item_w):
    return (box_w - padding)/(padding + item_w)
