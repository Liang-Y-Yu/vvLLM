#!/bin/bash
set -o pipefail
set -ex

pip install --upgrade pip
pip uninstall -y pandoc pypandoc pypandoc-binary flash-attn
export CUDA_HOME=/usr/local/cuda-12.3
pip install -r requirements.txt --extra-index https://download.pytorch.org/whl/cu121
pip install torch==2.1.0+cu121 torchvision==0.16.0+cu121 torchaudio==2.1.0 torchtext==0.16.0+cpu torchdata==0.7.0 --index-url https://download.pytorch.org/whl/cu121
# GPTQ
pip uninstall -y auto-gptq ; pip install auto-gptq
pip install optimum
# Auto AWQ
pip uninstall -y autoawq ; pip install autoawq
# Exllama for GPTQ mainly
pip uninstall -y exllama ; pip install https://github.com/jllllll/exllama/releases/download/0.0.18/exllama-0.0.18+cu118-cp310-cp310-linux_x86_64.whl --no-cache-dir
#pip install xformers==v0.0.22

# fix pytube to avoid errors for restricted content
sp=`python3.10 -c 'import site; print(site.getsitepackages()[0])'`
sed -i "s/client='ANDROID_MUSIC'/client='ANDROID'/g" $sp/pytube/innertube.py

# fix asyncio same way websockets was fixed, else keep hitting errors in async calls
# https://github.com/python-websockets/websockets/commit/f9fd2cebcd42633ed917cd64e805bea17879c2d7
sp=`python3.10 -c 'import site; print(site.getsitepackages()[0])'`
sed -i "s/except OSError:/except (OSError, RuntimeError):/g" $sp/anyio/_backends/_asyncio.py

pip install -r docs/requirements_optional_doctr.txt
