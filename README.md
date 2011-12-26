# Overview

**depana** is a simple static dependency analyzer and tries to generate a dot file to show the dependency.


# Usage

1. build your project

2. run the script and redirect its output to a file
    * `$ depana.py > project.dot`

3. convert the dot file to any supported format
    * `$ dot -Tsvg -o project.svg project.dot`


# Author

> letoh <DOT tw AT gmail>


