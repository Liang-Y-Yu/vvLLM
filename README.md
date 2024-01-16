# Linux

These instructions are for Ubuntu x86_64.

Steps in this document were verified with the following setting:
1. Python version 3.10.
2. CUDA version 12.3.
3. Ubuntu 22.04.

## Install:

* First one needs a Python 3.10 environment.
  ```
  Create new env:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
  
* Install dependencies:
    ```bash  
    # GPU only:
    ./install_deps.sh
    ```
---

## Run

1. Place all documents in `user_path`.

2. Prepare offline models:
  UI using GPU with at least 24GB with streaming:
  ```bash
  python generate.py --base_model=TheBloke/llama2-7B-Chat-AWQ --load_awq=model --revision="main" --score_model=None --langchain_mode='UserData' --user_path=user_path --prepare_offline_level=2
  ```

3. Run LLama-2-AWQ LLM:
  ```bash
  ./run.sh
  ```
