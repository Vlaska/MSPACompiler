from pathlib import Path

import pytest
from TextCompiler import TextCompiler


@pytest.fixture
def u_compiler():
    return TextCompiler()


@pytest.fixture
def compiler():
    return TextCompiler(Path('./tags.mspa').read_text('utf-8'))
