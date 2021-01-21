from pathlib import Path

import pytest
from MSPACompiler import TextCompiler


@pytest.fixture
def u_compiler():
    return TextCompiler()


@pytest.fixture
def compiler():
    return TextCompiler(
        Path(
            './MSPACompiler/default/tags.mspa'
        ).read_text('utf-8'))
