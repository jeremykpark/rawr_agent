# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent

# Choose a container name for bookkeeping
export NIM_MODEL_NAME=baidu/paddleocr
export CONTAINER_NAME=$(basename $NIM_MODEL_NAME)

# Choose a NIM Image from NGC
export IMG_NAME="nvcr.io/nim/$NIM_MODEL_NAME:1.3.0"

# Choose a path on your system to cache the downloaded models
export LOCAL_NIM_CACHE=~/.cache/nim
mkdir -p "$LOCAL_NIM_CACHE"

# Start the NIM
docker run -it --rm --name=$CONTAINER_NAME \
  --runtime=nvidia \
  --gpus all \
  --shm-size=16GB \
  -e NGC_API_KEY \
  -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  -u $(id -u) \
  -p 8010:8000 \
  $IMG_NAME
