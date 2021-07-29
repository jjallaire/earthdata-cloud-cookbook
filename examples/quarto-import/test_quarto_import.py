import os
import shutil

import nbformat as nbf
import pytest

from quarto_import import open_json, import_remote, inject_content

LOCAL_IMPORT_PATH = '.imported'

def test_quarto_import_can_read_json():
    file_path = 'test.json'
    json_input = open_json(file_path)
    assert len(json_input) == 2
    assert json_input[0]['title'] == 'Test document'
    assert json_input[1]['url'] == 'https://raw.githubusercontent.com/nasa-jpl/itslive-explorer/main/notebooks/itslive-notebook-rendered.ipynb'

def test_quarto_import_can_import_remote():
    if os.path.exists(LOCAL_IMPORT_PATH):
        shutil.rmtree(LOCAL_IMPORT_PATH)
    remote_url = 'https://raw.githubusercontent.com/nasa-jpl/itslive-explorer/main/notebooks/itslive-notebook-rendered.ipynb'
    import_remote(remote_url, 'test.ipynb')
    assert os.path.exists(f'{LOCAL_IMPORT_PATH}/test.ipynb') is True


def test_quarto_import_can_inject_content():
    remote_url = 'https://raw.githubusercontent.com/nasa-jpl/itslive-explorer/main/notebooks/itslive-notebook-rendered.ipynb'

    notebook = 'test.ipynb'
    content = f"""\
    # This is a test, should be at the top
    """
    inject_content(content, notebook)
    nb = nbf.read(f'{LOCAL_IMPORT_PATH}/test.ipynb', as_version=4)
    assert nb['cells'][0]['cell_type'] == 'markdown'
    assert content in nb['cells'][0]['source']
    # Needs to be refactored into a local clean
    import_remote(remote_url, notebook)
