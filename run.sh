#!/bin/bash
prompt_sys="""
You are a helpful, respectful and honest assistant. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
If you don't know the answer to a question, please don't share false information.
"""
CUDA_VISIBLE_DEVICES=0,1 GRADIO_SERVER_PORT=8089 TOKENIZERS_PARALLELISM=False HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python generate.py \
    --auth="[('guest','guest')]" \
    --base_model=TheBloke/Llama-2-7b-Chat-AWQ --load_awq="model" --revision="main" \
    --max_seq_len=4096 --use_safetensors=True --prompt_type=llama2 \
    --score_model=None --save_dir='save7b_awq' --langchain_modes="['UserData','MyData']" \
    --gpu_id=-1 --user_path=user_path \
    --gradio_size=small --share=False --gradio_offline_level=2 \
    --local_files_only=True --height=1100 --visible_system_tab=False --system_prompt="${prompt_sys}" \
    --prompt_query="Do not give me any information about service features that are not mentioned in the PROVIDED CONTEXT. According to only the information in the document sources provided within the context above," \
    --visible_chat_history_tab=False --visible_login_tab=False --visible_models_tab=True --visible_expert_tab=True --visible_doc_view_tab=True  --visible_doc_track=True --visible_tos_tab=True \
    --enable_pdf_doctr=on --enable_url_upload=True --enable_text_upload=True \
    --top_k_docs=5 --do_sample=True --top_p=0.95 --top_k=40 --repetition_penalty=1.1 \
    --verbose
