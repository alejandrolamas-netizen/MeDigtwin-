from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from tools import benchmark_api, benchmark_inference


class FakeResponse:
    def __init__(self, payload: bytes, status: int = 200):
        self.payload = payload
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


class BenchmarkApiTests(unittest.TestCase):
    def test_percentile_interpolates_and_handles_empty_values(self):
        self.assertEqual(benchmark_api.percentile([10.0, 20.0, 30.0], 0.5), 20.0)
        self.assertIsNone(benchmark_api.percentile([], 0.95))

    @patch("tools.benchmark_api.urlopen")
    def test_request_once_records_success_status(self, mocked_urlopen):
        mocked_urlopen.return_value = FakeResponse(b'{"ok":true}', 201)
        result = benchmark_api.request_once(
            "http://localhost/api/v1/simulations", "synthetic-test", 2.0
        )
        self.assertEqual(result["status"], 201)
        self.assertIsNone(result["error"])
        self.assertGreaterEqual(result["latency_ms"], 0)


class BenchmarkInferenceTests(unittest.TestCase):
    def test_percentile_interpolates_and_handles_empty_values(self):
        self.assertEqual(benchmark_inference.percentile([1.0, 3.0], 0.5), 2.0)
        self.assertIsNone(benchmark_inference.percentile([], 0.99))

    @patch("tools.benchmark_inference.urlopen")
    def test_one_request_reads_server_reported_completion_tokens(self, mocked_urlopen):
        payload = {
            "choices": [{"message": {"content": "synthetic response"}}],
            "usage": {"completion_tokens": 12},
        }
        mocked_urlopen.return_value = FakeResponse(json.dumps(payload).encode())
        result = benchmark_inference.one_request(
            "http://localhost/v1/chat/completions",
            "test-model",
            "synthetic prompt",
            5.0,
            None,
            32,
        )
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["completion_tokens"], 12)
        self.assertGreater(result["tokens_per_second"], 0)
        self.assertIsNone(result["error"])

    @patch("tools.benchmark_inference.subprocess.check_output")
    def test_gpu_snapshot_parses_local_nvidia_smi_output(self, mocked_check_output):
        mocked_check_output.return_value = "NVIDIA Test GPU, 45, 1024, 8192, 75.5\n"
        result = benchmark_inference.gpu_snapshot()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "NVIDIA Test GPU")
        self.assertEqual(result[0]["utilization_pct"], "45")


if __name__ == "__main__":
    unittest.main()
