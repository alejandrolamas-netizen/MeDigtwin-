#!/usr/bin/env python3
"""Reproducible HTTP load probe for the synthetic MedDigtwin API.

This measures API request latency and throughput. It is not a GPU benchmark.
Run only against an isolated synthetic-data environment, never production.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import math
import platform
import statistics
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PAYLOAD = {
    "patient_demand_pct": 112,
    "nursing_availability_pct": 94,
    "icu_capacity_pct": 100,
    "laboratory_throughput_pct": 105,
}


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * pct
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return round(ordered[lower], 3)
    weight = position - lower
    return round(ordered[lower] * (1 - weight) + ordered[upper] * weight, 3)


def request_once(url: str, tenant: str, timeout: float) -> dict:
    body = json.dumps(PAYLOAD, separators=(",", ":")).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Tenant-ID": tenant,
        },
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            response.read()
            return {
                "latency_ms": (time.perf_counter() - started) * 1000,
                "status": response.status,
                "error": None,
            }
    except HTTPError as exc:
        return {
            "latency_ms": (time.perf_counter() - started) * 1000,
            "status": exc.code,
            "error": f"HTTP {exc.code}",
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {
            "latency_ms": (time.perf_counter() - started) * 1000,
            "status": None,
            "error": type(exc).__name__,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="Base URL of an isolated synthetic MedDigtwin API")
    parser.add_argument("--requests", type=int, default=200, help="Total POST requests (default: 200)")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent workers (default: 10)")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-request timeout in seconds")
    parser.add_argument("--tenant", default="benchmark-synthetic", help="Synthetic tenant header")
    parser.add_argument("--output", help="Optional path for the JSON result")
    args = parser.parse_args()

    parsed = urlparse(args.base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        parser.error("--base-url must be an absolute HTTP(S) URL")
    if args.requests < 1 or args.concurrency < 1 or args.timeout <= 0:
        parser.error("requests, concurrency and timeout must be positive")

    endpoint = args.base_url.rstrip("/") + "/api/v1/simulations"
    started = time.perf_counter()
    results = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [
            pool.submit(request_once, endpoint, args.tenant, args.timeout)
            for _ in range(args.requests)
        ]
        for future in as_completed(futures):
            results.append(future.result())
    elapsed = time.perf_counter() - started

    latencies = [item["latency_ms"] for item in results]
    successes = sum(1 for item in results if item["status"] is not None and 200 <= item["status"] < 300)
    failures = len(results) - successes
    report = {
        "schema_version": "1.0",
        "benchmark_type": "http_api_load_probe",
        "gpu_benchmark": False,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": endpoint,
        "synthetic_data_only": True,
        "request_profile": {
            "method": "POST",
            "requests": args.requests,
            "concurrency": args.concurrency,
            "timeout_seconds": args.timeout,
            "tenant_header": args.tenant,
            "payload": PAYLOAD,
        },
        "client": {"python": platform.python_version(), "platform": platform.platform()},
        "results": {
            "elapsed_seconds": round(elapsed, 3),
            "throughput_requests_per_second": round(len(results) / elapsed, 3) if elapsed else None,
            "successes": successes,
            "failures": failures,
            "error_rate_pct": round(failures * 100 / len(results), 3),
            "latency_ms": {
                "mean": round(statistics.mean(latencies), 3) if latencies else None,
                "p50": percentile(latencies, 0.50),
                "p95": percentile(latencies, 0.95),
                "p99": percentile(latencies, 0.99),
                "max": round(max(latencies), 3) if latencies else None,
            },
            "status_counts": {
                str(status): sum(1 for item in results if item["status"] == status)
                for status in sorted({item["status"] for item in results}, key=lambda value: str(value))
            },
            "error_types": {
                error: sum(1 for item in results if item["error"] == error)
                for error in sorted({item["error"] for item in results if item["error"]})
            },
        },
        "limitations": [
            "Measures client-observed HTTP latency and throughput only.",
            "Does not measure server CPU, memory, GPU utilization, queue depth or model inference.",
            "The current simulation function is deterministic arithmetic; this is not evidence of GPU acceleration.",
            "Run against an isolated synthetic-data environment and retain the raw JSON output.",
        ],
    }

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as output_file:
            output_file.write(rendered + "\n")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
