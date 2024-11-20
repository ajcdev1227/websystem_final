#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

bash -i <<< "source $SCRIPT_DIR/env/bin/activate; cd $SCRIPT_DIR; exec < /dev/tty"
