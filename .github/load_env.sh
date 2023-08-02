# load_env.sh
#!/bin/bash
export $(egrep -v '^#' .env/.env.dev | xargs)
# export $(egrep -v '^#' .env.secret/.env.dev | xargs)
