#!/bin/bash

ls -rt footage/*.mp4 2>/dev/null | rev | cut -d '/' -f 1 | rev | sed 's/$/ /'
ls -rt footage/*.3gp 2>/dev/null | rev | cut -d '/' -f 1 | rev | sed 's/$/ /'
