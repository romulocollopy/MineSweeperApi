#! /bin/bash
PORT=${PORT:-'8089'}
HOST=${HOST:-'0.0.0.0'}

UVICORN="uvicorn asgi:application --port ${PORT} --host ${HOST}"

COMMAND=$UVICORN

declare -a HOT_RELOAD_DIRS=(
  'src'
)

RELOAD_ARGS='--reload'
for dirname in ${HOT_RELOAD_DIRS[@]}; do
  RELOAD_ARGS="${RELOAD_ARGS} --reload-dir ${dirname}"
done

if [ ${DEBUG} = 'True' ]; then
  echo "Starting server in DEBUG mode and RELOAD"
  COMMAND="PYTHONASYNCIODEBUG=1 PYTHONTRACEMALLOC=1 ${UVICORN} ${RELOAD_ARGS}"
fi

set -x
eval ${COMMAND}
