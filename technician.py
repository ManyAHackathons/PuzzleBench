import litellm
import json
from bomb.bomb import Bomb

litellm.suppress_debug_info = True
litellm.set_verbose = False

LABEL_W = 12

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_manual",
            "description": "Look up the manual entry for a module type based on what the defuser described. Use the module type name (e.g. 'Button', 'Wires') as inferred from the defuser's description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "module_name": {
                        "type": "string",
                        "description": "The module type name as inferred from the defuser's description (e.g. 'Button', 'Wires')",
                    }
                },
                "required": ["module_name"],
            },
        },
    }
]


def _log_call(name: str, args: dict):
    args_str = ", ".join(f"{k}={repr(v)}" for k, v in args.items())
    print(f"[{'TECH':<{LABEL_W}}] >> {name}({args_str})")


def _log_resp(resp: str):
    preview = resp.replace("\n", " ")
    if len(preview) > 120:
        preview = preview[:117] + "..."
    print(f"{'':<{LABEL_W + 4}}    {preview}")


def take_turn(messages: list, bomb: Bomb, model: str) -> str | None:
    response = litellm.completion(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    response_message = response.choices[0].message  # type: ignore[union-attr]
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)
        for tc in tool_calls:
            function_name = tc.function.name

            if function_name == "get_manual":
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except Exception:
                    args = {}
                module_name = args.get("module_name")
                _log_call("get_manual", {"module_name": module_name})
                if module_name is None:
                    resp = "Error: missing module_name"
                else:
                    resp = bomb.get_manual(module_name)

            else:
                _log_call(function_name, {})
                resp = f"Error: unknown function '{function_name}'"

            _log_resp(resp)
            messages.append({
                "tool_call_id": tc.id,
                "role": "tool",
                "name": function_name,
                "content": resp,
            })

        return take_turn(messages, bomb, model)
    else:
        return response_message.content
