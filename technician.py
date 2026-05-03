import warnings
import litellm
import json
from bomb.bomb import Bomb
from teminal_ui import print_panel

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

litellm.suppress_debug_info = True
litellm.set_verbose = False

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
                if module_name is None:
                    resp = "Error: missing module_name"
                else:
                    resp = bomb.get_manual(module_name)

            else:
                resp = f"Error: unknown function '{function_name}'"
            print_panel("technician", f"Called tool '{function_name}' with args {tc.function.arguments}.")
            print_panel("tool response", resp)

            messages.append({
                "tool_call_id": tc.id,
                "role": "tool",
                "name": function_name,
                "content": resp,
            })

        return take_turn(messages, bomb, model)
    else:
        return response_message.content
