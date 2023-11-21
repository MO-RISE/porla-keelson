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


def test_encode():
    # Raw input (JSON)
    payload = json.dumps({"hej": "svejs"})
    stdout, stderr = run_binary("bin/brefv", ["encode", "{payload_raw}", "{envelope}"], [payload])

    assert stdout
    assert not stderr

    # Base64 encoded input (still JSON)
    payload = json.dumps({"hej": "svejs"})
    stdout, stderr = run_binary("bin/brefv", ["encode", "{payload_b64}", "{envelope}"], [to_base64(payload)])

    assert stdout
    assert not stderr



def test_decode():
    # Generate a valid envelope
    payload = json.dumps({"hej": "svejs"})
    stdout, _ = run_binary("bin/brefv", ["encode", "{payload_raw}", "{envelope}"], [payload])
    envelope = stdout[0]

    # Extract the raw payload
    stdout, stderr = run_binary("bin/brefv", ["decode", "{envelope}", "{payload_raw}"], [envelope])

    assert stdout
    assert not stderr

    # Extract the base64 encoded payload
    stdout, stderr = run_binary("bin/brefv", ["decode", "{envelope}", "{payload_b64}"], [envelope])

    assert stdout
    assert not stderr

    # Extract some other things
    stdout, stderr = run_binary("bin/brefv", ["decode", "{envelope}", "{enclosed_at} {received_at}"], [envelope])

    assert stdout
    assert not stderr

