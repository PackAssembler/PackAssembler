#!/bin/bash
lsc -c common.ls
browserify wrapper.js -o bundled/wrapper.js
rm common.js
