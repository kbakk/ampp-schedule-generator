import json
import pathlib
from typing import Any

import jsondiff

from ampp_schedule_generator import generate


def load_example_schedule() -> dict[str, Any]:
    sample_dir = pathlib.Path(__name__).parent / "sample"
    with (sample_dir / "from-gv/nrktv7-prod.json").open() as f:
        data = json.load(f)
    return data


def test_generate_schedule():
    expected_dict = load_example_schedule()
    assert isinstance(expected_dict, dict)
    id_ = expected_dict["id"]
    name = expected_dict["name"]

    actual = generate.generate_schedule(id_, name)
    actual_dict = actual.model_dump(mode="json")

    diff = jsondiff.diff(expected_dict, actual_dict)
    assert not diff, diff
