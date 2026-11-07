#!/usr/bin/env python3
"""Benchmark an OpenAI-compatible chat-completions endpoint with synthetic prompts.

This is a client-side inference benchmark. It only demonstrates GPU inference
when the configured endpoint is actually served by a GPU-backed runtime.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import math
import os
import platform
import statistics
import subprocess
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROMPTS = [
    "Summarize this synthetic hospital operations snapshot: ICU occupancy 82%, staffed beds 94%, elective demand 108%. Return three operational risks.",
    "Given synthetic staffing data (nurses available 91%, patient demand 113%), propose two capacity scenarios and state assumptions.",
    "Explain how a hospital operations digital twin can compare baseline and what-if scenarios using synthetic data only.",
    "Produce a concise synthetic operations report: emergency arrivals +12%, ICU capacity unchanged, nursing availability -4%.",
]


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * pct
    low, high = math.floor(position), math.ceil(position)
    if low == high:
        return round(ordered[low], 3)
    weight = position - low
    return round(ordered[low] * (1 - weight) + ordered[high] * weight, 3)


def gpu_snapshot() -> list[dict]:
    command = [
        "nvidia-smi",
        "--query-gpu=name,utilization.gpu,memory.used,memory.total,power.draw",
        "--format=csv,noheader,nounits",
    ]
    try:
        output = subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL, timeout=3)
    except (OSError, subprocess.SubprocessError):
        return []
    rows = []
    for line in output.strip().splitlines():
        fields = [part.strip() for part in line.split(",")]
        if len(fields) == 5:
            rows.append({
                "name": fields[0],
                "utilization_pct": fields[1],
                "memory_used_mb": fields[2],
                "memory_total_mb": fields[3],
                "power_w": fields[4],
            })
    return rows


class GpuSampler:
    def __init__(self, interval: float):
        self.interval = interval
        self.samples: list[dict] = []
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop.is_set():
            sample = gpu_snapshot()
            if sample:
                self.samples.append({"timestamp": datetime.now(timezone.utc).isoformat(), "gpus": sample})
            self._stop.wait(self.interval)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=max(1.0, self.interval + 1.0))


def one_request(url: str, model: str, prompt: str, timeout: float, api_key: str | None,
                max_tokens: int) -> dict:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": False,
    }).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(url, data=body, headers=headers, method="POST")
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            elapsed = time.perf_counter() - started
            usage = payload.get("usage") or {}
            completion_tokens = usage.get("completion_tokens")
            return {
                "latency_ms": elapsed * 1000,
                "status": response.status,
                "completion_tokens": completion_tokens,
                "tokens_per_second": completion_tokens / elapsed if completion_tokens and elapsed else None,
                "error": None,
            }
    except HTTPError as exc:
        return {"latency_ms": (time.perf_counter() - started) * 1000,
                "status": exc.code, "completion_tokens": None, "tokens_per_second": None,
                "error": f"HTTP {exc.code}"}
    except (URLError, TimeoutError, OSError, ValueError, KeyError) as exc:
        return {"latency_ms": (time.perf_counter() - started) * 1000,
                "status": None, "completion_tokens": None, "tokens_per_second": None,
                "error": type(exc).__name__}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", required=True, help="Full /v1/chat/completions URL")
    parser.add_argument("--model", required=True, help="Model identifier served by the endpoint")
    parser.add_argument("--requests", type=int, default=40)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--gpu-sample-interval", type=float, default=1.0)
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args()
    if not args.endpoint.startswith(("http://", "https://")):
        parser.error("--endpoint must be an absolute HTTP(S) URL")
    if min(args.requests, args.concurrency, args.max_tokens) < 1 or args.timeout <= 0 or args.gpu_sample_interval <= 0:
        parser.error("requests, concurrency, max-tokens, timeout and sample interval must be positive")

    sampler = GpuSampler(args.gpu_sample_interval)
    sampler.start()
    started = time.perf_counter()
    results = []
    api_key = os.environ.get("OPENAI_API_KEY")
    try:
        with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
            futures = [
                pool.submit(one_request, args.endpoint, args.model, PROMPTS[i % len(PROMPTS)],
                            args.timeout, api_key, args.max_tokens)
                for i in range(args.requests)
            ]
            for future in as_completed(futures):
                results.append(future.result())
    finally:
        elapsed = time.perf_counter() - started
        sampler.stop()

    latencies = [r["latency_ms"] for r in results]
    successful = [r for r in results if r["status"] is not None and 200 <= r["status"] < 300]
    token_values = [r["completion_tokens"] for r in successful if r["completion_tokens"] is not None]
    total_tokens = sum(token_values)
    report = {
        "schema_version": "1.0",
        "benchmark_type": "openai_compatible_model_inference",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": args.endpoint,
        "model": args.model,
        "synthetic_prompts_only": True,
        "client": {"python": platform.python_version(), "platform": platform.platform()},
        "configuration": {"requests": args.requests, "concurrency": args.concurrency,
                          "max_tokens": args.max_tokens, "timeout_seconds": args.timeout},
        "results": {
            "elapsed_seconds": round(elapsed, 3),
            "throughput_requests_per_second": round(len(results) / elapsed, 3) if elapsed else None,
            "successes": len(successful),
            "failures": len(results) - len(successful),
            "latency_ms": {"mean": round(statistics.mean(latencies), 3) if latencies else None,
                           "p50": percentile(latencies, .50), "p95": percentile(latencies, .95),
                           "p99": percentile(latencies, .99)},
            "completion_tokens_reported": total_tokens if token_values else None,
            "aggregate_completion_tokens_per_second": round(total_tokens / elapsed, 3) if token_values and elapsed else None,
            "gpu_samples": len(sampler.samples),
            "gpu_telemetry": sampler.samples,
        },
        "limitations": [
            "GPU telemetry is collected only on the machine running this script; remote server GPUs are not visible.",
            "A GPU-backed endpoint must be independently verified; an OpenAI-compatible API alone does not prove GPU execution.",
            "Token throughput is reported only when the server returns usage.completion_tokens.",
            "No clinical, PHI, patient-identifiable or production data is used or permitted by this benchmark profile.",
            "For reproducibility, record server runtime, model revision, quantization, GPU model, driver and serving configuration separately.",
        ],
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    return 0 if len(successful) == len(results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
