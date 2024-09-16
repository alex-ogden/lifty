#!/usr/bin/env bash

# Builds and runs the pychan app in Docker

app_name="lifty"
run_mode=${1:?"Please provide a run mode ('local' or 'docker')"}

help() {
    echo "${0}"
    echo "Usage:"
    echo "  ${0} [docker|local]"
    echo;echo
    echo "local - run the python program locally (requires Python 3.10 to be installed)"
    echo "docker - builds and runs the Docker container in Docker Compose (requires Docker and Compose to be installed)"
    echo;echo
}

build_image() {
    docker build -t "${app_name}" .
}
stop_compose() {
    docker compose down
}

start_compose() {
    docker compose up -d
}

install_prereqs() {
    local requirements_file="requirements.txt"
    echo -e "\n\nINSTALLING REQUIREMENTS"
    python3.10 -m pip install -r "${requirements_file}"
}

run_python() {
    echo -e "\n\nRUNNING PROGRAM"
    python3.10 run.py
}

echo "Run Mode: ${run_mode}"

if [[ "${run_mode}" == "docker" ]]; then
    # Build container and run compose
    stop_compose
    build_image
    start_compose
elif [[ "${run_mode}" == "local" ]]; then
    install_prereqs
    run_python
else
    help
fi

exit 0