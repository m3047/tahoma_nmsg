#!/bin/bash

[[ -a tahoma_nmsg ]] || ln -s ../tahoma_nmsg

./all_tests.py

