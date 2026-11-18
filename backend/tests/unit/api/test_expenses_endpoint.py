import pytest
from pydantic import ValidationError

from app.schemas.expenses import InterpretRequest


def test_trim_before_length():
    assert InterpretRequest(texto=" " * 50 + "taxi 8000" + " " * 280).texto == "taxi 8000"


@pytest.mark.parametrize("text", ["", " " * 10, "a" * 281])
def test_text_limits(text):
    with pytest.raises(ValidationError):
        InterpretRequest(texto=text)
