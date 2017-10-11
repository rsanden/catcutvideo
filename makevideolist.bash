#!/bin/bash

ls -rt footage/*.mp4 | rev | cut -d '/' -f 1 | rev
ls -rt footage/*.3gp | rev | cut -d '/' -f 1 | rev
