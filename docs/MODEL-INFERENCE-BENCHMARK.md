# Model-backed inference benchmark

`tools/benchmark_inference.py` is a client-side benchmark for an OpenAI-compatible `/v1/chat/completions` endpoint. It sends fixed synthetic hospital-operations prompts and records request latency, request throughput, server-reported completion tokens (when available), and local NVIDIA telemetry from `nvidia-smi`.

## Run

Start a model-serving runtime separately (for example, vLLM or another OpenAI-compatible server) on a machine with a supported NVIDIA GPU. Then run:

```bash
python tools/benchmark_inference.py \
  --endpoint http://127.0.0.1:8000/v1/chat/completions \
  --model <served-model-id> \
  --requests 40 \
  --concurrency 2 \
  --max-tokens 128 \
  --output artifacts/inference-benchmark.json
```

If the endpoint requires authentication, set `OPENAI_API_KEY` in the environment. Do not put credentials in command-line arguments, source files, or benchmark artifacts.

## Evidence required for a valid GPU claim

- Confirm the serving process is bound to the intended NVIDIA GPU.
- Record GPU model, driver, CUDA/runtime versions, model revision, quantization, serving runtime/version, context length and concurrency.
- Preserve the JSON report and server logs; verify GPU utilization and memory on the inference host while requests run.
- Run a CPU baseline with the same model, prompt set, request count and generation settings before claiming acceleration. Compare latency percentiles and completion tokens/second, not just request throughput.
- Repeat runs and report warm-up policy and variance.

## Scope and limitations

The script samples NVIDIA telemetry only on the host where the script itself runs. If the inference server is remote, collect `nvidia-smi` telemetry on that server separately; local samples cannot establish remote GPU utilization. An OpenAI-compatible endpoint does not by itself prove GPU execution. The report records telemetry availability without treating missing samples as proof of CPU-only execution.

This is a benchmark harness, not a deployed inference service, a DSX integration, a clinical model, or evidence of clinical validation. Use synthetic data only.
