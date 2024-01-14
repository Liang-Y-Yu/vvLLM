import ast
import os
import sys
from typing import Union, List

if os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))))

from src.middleware.gpt_langchain import path_to_docs, create_or_update_db, \
    get_persist_directory, get_existing_db
from src.backend.utils import get_ngpus_vis, gpt_fire


def glob_to_db(user_path, chunk=True, chunk_size=512, verbose=False,
               fail_any_exception=False, n_jobs=-1, url=None,

               # urls
               use_unstructured=True,
               use_playwright=False,
               use_selenium=False,

               # pdfs
               use_pymupdf=True,
               use_unstructured_pdf=False,
               use_pypdf=False,
               enable_pdf_ocr='auto',
               try_pdf_as_html=True,
               enable_pdf_doctr=False,

               # images
               enable_ocr=False,
               enable_doctr=False,
               enable_pix2struct=False,
               enable_captions=True,
               captions_model=None,
               caption_loader=None,

               # json
               jq_schema='.[]',

               db_type=None,
               selected_file_types=None):
    assert db_type is not None
    sources1 = path_to_docs(user_path, verbose=verbose, fail_any_exception=fail_any_exception,
                            n_jobs=n_jobs,
                            chunk=chunk,
                            chunk_size=chunk_size, url=url,

                            # urls
                            use_unstructured=use_unstructured,
                            use_playwright=use_playwright,
                            use_selenium=use_selenium,

                            # pdfs
                            use_pymupdf=use_pymupdf,
                            use_unstructured_pdf=use_unstructured_pdf,
                            use_pypdf=use_pypdf,
                            enable_pdf_ocr=enable_pdf_ocr,
                            try_pdf_as_html=try_pdf_as_html,
                            enable_pdf_doctr=enable_pdf_doctr,

                            # images
                            enable_ocr=enable_ocr,
                            enable_doctr=enable_doctr,
                            enable_pix2struct=enable_pix2struct,
                            enable_captions=enable_captions,
                            captions_model=captions_model,
                            caption_loader=caption_loader,

                            # json
                            jq_schema=jq_schema,

                            db_type=db_type,
                            selected_file_types=selected_file_types,
                            )
    return sources1


def make_db_main(use_openai_embedding: bool = False,
                 hf_embedding_model: str = None,
                 migrate_embedding_model=False,
                 auto_migrate_db=False,
                 persist_directory: str = None,
                 user_path: str = 'user_path',
                 langchain_type: str = 'shared',
                 url: Union[List[str], str] = None,
                 add_if_exists: bool = True,
                 collection_name: str = 'UserData',
                 verbose: bool = False,
                 chunk: bool = True,
                 chunk_size: int = 512,
                 fail_any_exception: bool = False,
                 n_jobs: int = -1,

                 # urls
                 use_unstructured=True,
                 use_playwright=False,
                 use_selenium=False,

                 # pdfs
                 use_pymupdf=True,
                 use_unstructured_pdf=False,
                 use_pypdf=False,
                 enable_pdf_ocr='auto',
                 try_pdf_as_html=True,
                 enable_pdf_doctr=False,

                 # images
                 enable_ocr=False,
                 enable_doctr=False,
                 enable_pix2struct=False,
                 enable_captions=True,
                 captions_model: str = "Salesforce/blip-image-captioning-base",
                 pre_load_caption_model: bool = False,
                 caption_gpu: bool = True,

                 # json
                 jq_schema='.[]',

                 db_type: str = 'chroma',
                 selected_file_types: Union[List[str], str] = None,
                 fail_if_no_sources: bool = True
                 ):
    """
    # To make UserData db for generate.py, put pdfs, etc. into path user_path and run:
    python src/make_db.py

    # once db is made, can use in generate.py like:

    python generate.py --base_model=TheBloke/llama-2-7b --langchain_mode=UserData

    :param use_openai_embedding: Whether to use OpenAI embedding
    :param hf_embedding_model: HF embedding model to use. Like generate.py, uses 'hkunlp/instructor-large' if have GPUs, else "sentence-transformers/all-MiniLM-L6-v2"
    :param migrate_embedding_model: whether to migrate to newly chosen hf_embedding_model or stick with one in db
    :param auto_migrate_db: whether to migrate database for chroma<0.4 -> >0.4
    :param persist_directory: where to persist db (note generate.py always uses db_dir_<collection name>
           If making personal database for user, set persistent_directory to users/<username>/db_dir_<collection name>
           and pass --langchain_type=personal
    :param user_path: where to pull documents from (None means url is not None.  If url is not None, this is ignored.)
    :param langchain_type: type of database, i.e.. 'shared' or 'personal'
    :param url: url (or urls) to generate documents from (None means user_path is not None)
    :param add_if_exists: Add to db if already exists, but will not add duplicate sources
    :param collection_name: Collection name for new db if not adding
           Normally same as langchain_mode
    :param verbose: whether to show verbose messages
    :param chunk: whether to chunk data
    :param chunk_size: chunk size for chunking
    :param fail_any_exception: whether to fail if any exception hit during ingestion of files
    :param n_jobs: Number of cores to use for ingesting multiple files

    :param use_unstructured: see gen.py
    :param use_playwright: see gen.py
    :param use_selenium: see gen.py

    :param use_pymupdf: see gen.py
    :param use_unstructured_pdf: see gen.py
    :param use_pypdf: see gen.py
    :param enable_pdf_ocr: see gen.py
    :param try_pdf_as_html: see gen.py
    :param enable_pdf_doctr: see gen.py

    :param enable_ocr: see gen.py
    :param enable_doctr: see gen.py
    :param enable_pix2struct: see gen.py
    :param enable_captions: Whether to enable captions on images
    :param captions_model: See generate.py
    :param pre_load_caption_model: See generate.py
    :param caption_gpu: Caption images on GPU if present

    :param db_type: Type of db to create. Currently only 'chroma' and 'weaviate' is supported.
    :param selected_file_types: File types (by extension) to include if passing user_path
       e.g. --selected_file_types="['pdf', 'html', 'htm']"
    :return: None
    """

    if isinstance(selected_file_types, str):
        selected_file_types = ast.literal_eval(selected_file_types)
    if persist_directory is None:
        persist_directory, langchain_type = get_persist_directory(collection_name, langchain_type=langchain_type)

    # match behavior of main() in generate.py for non-HF case
    n_gpus = get_ngpus_vis()
    if n_gpus == 0:
        if hf_embedding_model is None:
            # if no GPUs, use simpler embedding model to avoid cost in time
            hf_embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    else:
        if hf_embedding_model is None:
            # if still None, then set default
            hf_embedding_model = 'hkunlp/instructor-large'

    load_db_if_exists = True
    langchain_mode = collection_name
    langchain_mode_paths = dict(langchain_mode=None)
    langchain_mode_types = dict(langchain_mode='shared')
    db, use_openai_embedding, hf_embedding_model = \
        get_existing_db(None, persist_directory, load_db_if_exists, db_type,
                        use_openai_embedding,
                        langchain_mode, langchain_mode_paths, langchain_mode_types,
                        hf_embedding_model, migrate_embedding_model, auto_migrate_db,
                        verbose=False,
                        n_jobs=n_jobs)

    if enable_captions and pre_load_caption_model:
        # preload, else can be too slow or if on GPU have cuda context issues
        # Inside ingestion, this will disable parallel loading of multiple other kinds of docs
        # However, if have many images, all those images will be handled more quickly by preloaded model on GPU
        from src.middleware.image_captions import CustomImageCaptionLoader
        caption_loader = CustomImageCaptionLoader(None,
                                                  blip_model=captions_model,
                                                  blip_processor=captions_model,
                                                  caption_gpu=caption_gpu,
                                                  ).load_model()
    else:
        if enable_captions:
            caption_loader = 'gpu' if caption_gpu else 'cpu'
        else:
            caption_loader = False

    if verbose:
        print("Getting sources", flush=True)
    assert user_path is not None or url is not None, "Can't have both user_path and url as None"
    if not url:
        assert os.path.isdir(user_path), "user_path=%s does not exist" % user_path
    sources = glob_to_db(user_path, chunk=chunk, chunk_size=chunk_size, verbose=verbose,
                         fail_any_exception=fail_any_exception, n_jobs=n_jobs, url=url,

                         # urls
                         use_unstructured=use_unstructured,
                         use_playwright=use_playwright,
                         use_selenium=use_selenium,

                         # pdfs
                         use_pymupdf=use_pymupdf,
                         use_unstructured_pdf=use_unstructured_pdf,
                         use_pypdf=use_pypdf,
                         enable_pdf_ocr=enable_pdf_ocr,
                         try_pdf_as_html=try_pdf_as_html,
                         enable_pdf_doctr=enable_pdf_doctr,

                         # images
                         enable_ocr=enable_ocr,
                         enable_doctr=enable_doctr,
                         enable_pix2struct=enable_pix2struct,
                         enable_captions=enable_captions,
                         captions_model=captions_model,
                         caption_loader=caption_loader,
                         # Note: we don't reload doctr model

                         # json
                         jq_schema=jq_schema,

                         db_type=db_type,
                         selected_file_types=selected_file_types,
                         )
    exceptions = [x for x in sources if x.metadata.get('exception')]
    print("Exceptions: %s/%s %s" % (len(exceptions), len(sources), exceptions), flush=True)
    sources = [x for x in sources if 'exception' not in x.metadata]

    assert len(sources) > 0 or not fail_if_no_sources, "No sources found"
    db = create_or_update_db(db_type, persist_directory,
                             collection_name, user_path, langchain_type,
                             sources, use_openai_embedding, add_if_exists, verbose,
                             hf_embedding_model, migrate_embedding_model, auto_migrate_db,
                             n_jobs=n_jobs)

    assert db is not None or not fail_if_no_sources
    if verbose:
        print("DONE", flush=True)
    return db, collection_name


if __name__ == "__main__":
    gpt_fire(make_db_main)
