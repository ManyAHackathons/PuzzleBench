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
            "name": "view_bomb",
            "description": "Look at the bomb and its modules to get information about them",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "view_module",
            "description": "Look at a specific module to get information about it",
            "parameters": {
                "type": "object",
                "properties": {
                    "module_id": {
                        "type": "integer",
                        "description": "id of the module to look at",
                    }
                },
                "required": ["module_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "action_module",
            "description": "Perform an action on a module (cut a wire, press a button, etc...)",
            "parameters": {
                "type": "object",
                "properties": {
                    "module_id": {
                        "type": "integer",
                        "description": "id of the module to perform an action on",
                    },
                    "action": {
                        "type": "string",
                        "description": "The action to perform on the module",
                    },
                },
                "required": ["module_id", "action"],
            },
        },
    },
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

            if function_name == "view_bomb":
                resp = bomb.view_bomb()

            elif function_name == "view_module":
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except Exception:
                    args = {}
                module_id = args.get("module_id")
                if module_id is None:
                    resp = "Error: missing module_id"
                else:
                    resp = bomb.view_module(int(module_id))

            elif function_name == "action_module":
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except Exception:
                    args = {}
                module_id = args.get("module_id")
                action = args.get("action")
                if module_id is None:
                    resp = "Error: missing module_id"
                elif action is None:
                    resp = "Error: missing action"
                else:
                    resp = bomb.action_module(int(module_id), action)

            else:
                resp = f"Error: unknown function '{function_name}'"
            print_panel("defuser_tool", f"{function_name}({tc.function.arguments})")
            print_panel("defuser_sees", resp)
            messages.append({
                "tool_call_id": tc.id,
                "role": "tool",
                "name": function_name,
                "content": resp,
            })

        return take_turn(messages, bomb, model)
    else:
        return response_message.content
