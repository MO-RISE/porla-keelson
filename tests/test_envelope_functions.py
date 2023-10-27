import sys
import json
import base64
import subprocess
from typing import List, Tuple

import pytest


def run_binary(
    relative_path: str, arguments: List[str] = None, input: List[str] = None
) -> Tuple[List[str], str]:
    with subprocess.Popen(
        [sys.executable, relative_path] + arguments or [],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as p:
        try:
            input = "\n".join(input or [])
            stdout, stderr = p.communicate(input)

            output = filter(None, stdout.split("\n"))

            return list(output), stderr

        finally:
            p.terminate()


def to_base64(input: str) -> str:
    return base64.b64encode(input.encode()).decode()


def test_enclose():
    # JSON payload
    payload = json.dumps({"hej": "svejs"})
    stdout, stderr = run_binary("bin/enclose", [], [to_base64(payload)])

    assert stdout
    assert not stderr

    # Non-base64 encoded payload
    stdout, stderr = run_binary("bin/enclose", [], ["failure"])

    assert not stdout
    assert "Failed to handle payload..." in stderr

    # Using specifications
    stdout, stderr = run_binary(
        "bin/enclose",
        ["{bypassed} {payload}", "{bypassed} {envelope}"],
        [f"not_used {to_base64('hej')}"],
    )

    assert len(stdout) == 1
    assert "not_used" in stdout[0]
    assert not stderr

    # Using specifications - bad input spec
    stdout, stderr = run_binary(
        "bin/enclose",
        ["{bypassed}", "{bypassed} {envelope}"],
        [f"not_used {to_base64('hej')}"],
    )

    assert not stdout
    assert "Could not find the expected named argument" in stderr


def test_uncover():
    # Generate a valid envelope
    stdout, _ = run_binary("bin/enclose", [], [to_base64("payload")])
    envelope = stdout[0]

    # Default behavior
    stdout, stderr = run_binary("bin/uncover", [], [envelope])

    assert stdout
    assert not stderr

    # Non-base64 encoded envelope
    stdout, stderr = run_binary("bin/uncover", [], ["failure"])

    assert not stdout
    assert "Failed to handle envelope..." in stderr

    # Using specifications
    stdout, stderr = run_binary(
        "bin/uncover",
        ["{bypassed} {envelope}", "{bypassed} {enclosed_at} {payload} {received_at}"],
        [f"not_used {envelope}"],
    )

    assert len(stdout) == 1
    assert "not_used" in stdout[0]
    assert not stderr

    # Using specifications - bad input spec
    stdout, stderr = run_binary(
        "bin/uncover",
        ["{bypassed}", "{bypassed} {enclosed_at} {payload} {received_at}"],
        [f"not_used"],
    )

    assert not stdout
    assert "Could not find the expected named argument" in stderr
