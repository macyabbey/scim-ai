#!/bin/bash

source "$HOME/.sdkman/bin/sdkman-init.sh"

sdk env
mvn clean generate-sources