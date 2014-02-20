#!/bin/bash
lsc -c *.ls
browserify wrapper.js -o bundled/wrapper.js
