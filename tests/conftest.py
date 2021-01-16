from pathlib import Path

import pytest
from TextCompiler import TextParser


@pytest.fixture
def u_compiler():
    return TextParser()


@pytest.fixture
def compiler():
    return TextParser(Path('./tags.mspa').read_text('utf-8'))