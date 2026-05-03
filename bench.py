# handles benching a run
import json
import datetime
from bomb.button import Button
from bomb.cyclo import Cyclogram
from bomb.dec import Dec
from main import run_game

# ── Config ──────────────────────────────────────────────────────────────────
DEFUSER_MODEL = "openai/gpt-4o"
TECHNICIAN_MODEL = "openai/gpt-4o"
MESSAGE_LENGTH_LIMIT = 300   # -1 = unlimited
TURNS = 10
RUNS_PER_PAIRING = 3

MODEL_PAIRINGS = [
    ("openrouter/nvidia/nemotron-3-super-120b-a12b:free",      "openrouter/nvidia/nemotron-3-super-120b-a12b:free"),
    ("openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"),
    ("openrouter/nvidia/nemotron-3-super-120b-a12b:free",      "openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"),
    ("openrouter/openai/gpt-oss-120b:free",                      "openrouter/openai/gpt-oss-120b:free"),
    ("openrouter/google/gemma-4-26b-a4b-it:free",              "openrouter/google/gemma-4-26b-a4b-it:free"),
]

# ── Tracing ──────────────────────────────────────────────────────────────────
def setup_tracing():
    try:
        import phoenix as px
        from phoenix.otel import register
        from openinference.instrumentation.litellm import LiteLLMInstrumentor
        from opentelemetry import trace

        session = px.launch_app(use_temp_dir=False)
        print(f"\n  Phoenix UI → {session.url}\n")

        tracer_provider = register()
        LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)
        return trace.get_tracer(__name__)
    except ImportError:
        print("  [warn] Phoenix not installed — tracing disabled.")
        print("         pip install arize-phoenix openinference-instrumentation-litellm\n")
        return None


# ── Runner ───────────────────────────────────────────────────────────────────
def bench():
    tracer = setup_tracing()
    results = []
    message_limit = None if MESSAGE_LENGTH_LIMIT < 0 else MESSAGE_LENGTH_LIMIT

    for defuser_model, technician_model in MODEL_PAIRINGS:
        pairing_results = []
        print(f"\n{'='*60}")
        print(f"  {defuser_model}  (D)  x  {technician_model}  (T)")
        print(f"{'='*60}")

        for run_idx in range(RUNS_PER_PAIRING):
            print(f"\n  Run {run_idx + 1}/{RUNS_PER_PAIRING}")
            modules = [Button(), Cyclogram(), Dec()]
            span_name = f"{defuser_model} × {technician_model} · run {run_idx + 1}"

            if tracer:
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute("defuser_model", defuser_model)
                    span.set_attribute("technician_model", technician_model)
                    span.set_attribute("run_index", run_idx)
                    span.set_attribute("turns_limit", TURNS)

                    result = run_game(defuser_model, technician_model, TURNS, message_limit, modules)

                    span.set_attribute("defused", result["defused"])
                    span.set_attribute("turns_taken", result["turns_taken"])
            else:
                result = run_game(defuser_model, technician_model, TURNS, message_limit, modules)

            pairing_results.append({
                "run": run_idx + 1,
                "defused": result["defused"],
                "turns_taken": result["turns_taken"],
            })

        defuse_rate = sum(r["defused"] for r in pairing_results) / len(pairing_results)
        avg_turns = sum(r["turns_taken"] for r in pairing_results) / len(pairing_results)
        results.append({
            "defuser_model": defuser_model,
            "technician_model": technician_model,
            "runs": pairing_results,
            "defuse_rate": defuse_rate,
            "avg_turns": avg_turns,
        })

    # ── Save results ──────────────────────────────────────────────────────────
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"results_{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved → {out_path}")

    # ── Summary table ─────────────────────────────────────────────────────────
    print(f"\n{'─'*72}")
    print(f"  {'DEFUSER MODEL':<28} {'TECH MODEL':<28} {'DEFUSE%':>7} {'AVG T':>5}")
    print(f"{'─'*72}")
    for r in results:
        print(f"  {r['defuser_model']:<28} {r['technician_model']:<28} {r['defuse_rate']:>6.0%} {r['avg_turns']:>5.1f}")
    print(f"{'─'*72}\n")


if __name__ == "__main__":
    bench()
