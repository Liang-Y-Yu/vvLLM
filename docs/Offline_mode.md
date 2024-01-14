# Offline Mode:

## Download transformers:

In offline mode, ensuring to use LLM and upload docs using same parsers as would want in offline mode.  The `~/.cache` folder will be filled, and one can use that in offline mode.

```
python generate.py --score_model=None --gradio_size=small --model_lock="[{'base_model': 'thebloke/llama2-7b-chat'}]" --save_dir=save_fastup_chat --prepare_offline_level=1
```

## Run in offline mode

```bash
HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python generate.py --base_model='llama' --gradio_offline_level=2 --share=False
```
For more info for transformers, see [Offline Mode](https://huggingface.co/docs/transformers/installation#offline-mode).

Some code is always disabled that involves uploads out of user control: Huggingface telemetry, gradio telemetry, chromadb posthog.

The additional option `--gradio_offline_level=2` changes fonts to avoid download of google fonts. This option disables google fonts for downloading, which is less intrusive than uploading, but still required in air-gapped case.  The fonts don't look as nice as google fonts, but ensure full offline behavior.

### To fully disable Chroma telemetry, which documented options still do not disable, run:

```bash
sp=`python -c 'import site; print(site.getsitepackages()[0])'`
sed -i 's/posthog\.capture/return\n            posthog.capture/' $sp/chromadb/telemetry/posthog.py
```
or the equivalent for windows/mac using.  Or edit the file manually to just return in the `capture` function.

Set the ENV `H2OGPT_ENABLE_HEAP_ANALYTICS=False` pass `--enable-heap-analytics=False` to `generate.py`.