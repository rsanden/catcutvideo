#!/bin/bash
cat videolist.txt | rev | cut -d '/' -f 1 | rev > videolist.txt.TEMP
mv -f videolist.txt.TEMP videolist.txt
