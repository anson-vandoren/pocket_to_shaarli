#!/usr/bin/python3

import sys
import os
import re
import time

LINK_ATTR = re.compile(r'<a href="([^"]+)"')
TIME_ATTR = re.compile(r'time_added="(\d+)"')
TAG_ATTR = re.compile(r'tags="([^"]+)"')
DESCR = re.compile(r">([^<]+)</a>")


def check_files(input_file, output_file):
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f"{input_file} does not exist!")
        return False
    if os.path.exists(output_file):
        print(f"Cannot overwrite output file {output_file}!")
        return False
    return True


def convert(args):
    if len(args) != 3:
        print("Must supply input and output files!")
    input_file = args[1]
    output_file = args[2]
    if not check_files(input_file, output_file):
        exit()

    links = []

    with open(input_file, "r") as in_file:
        for count, line in enumerate(in_file):
            print("Line:", count, end="\r")
            link = re.search(LINK_ATTR, line)
            if not link:
                continue
            else:
                link = link.group(1)
            timestamp = re.search(TIME_ATTR, line)
            if not timestamp:
                timestamp = time.time()
            else:
                timestamp = timestamp.group(1)
            tags = re.search(TAG_ATTR, line)
            if not tags:
                tags = ""
            else:
                tags = tags.group(1)
            tags = ",".join([tag.replace(" ", "_") for tag in tags.split(",")])
            description = re.search(DESCR, line)
            if not description:
                description = ""
            else:
                description = description.group(1)

            new_link = f'<DT><a href="{link}" add_date="{timestamp}" tags="{tags}">{description}</a></dt>'
            links.append(new_link)
    print(f"Found {len(links)} links")

    with open(output_file, "w") as out_file:
        out_file.write(
            """
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<!-- This is an automatically generated file.
     It will be read and overwritten.
     Do Not Edit! -->
<TITLE>Anson's Links</TITLE>
<H1>Shaarli export of all bookmarks on Mon, 30 Dec 19 16:29:54 -0800</H1>
<DL><p>
"""
        )
        for link in links:
            out_file.write(f"{link}\n")
        out_file.write("</DL><p>\n")


if __name__ == "__main__":
    convert(sys.argv)
