import litellm
import os
import json
from bomb.bomb import Bomb

def take_turn(messages, tools, bomb: Bomb):
    response = litellm.completion(
        model="openai/gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message

    tool_calls = response_message.tool_calls
    # check if model wants to call a tool
    if tool_calls:
        # TODO: should be a valid json check here
        # add the assistant message (with tool_calls) first
        messages.append(response_message)
        for tc in tool_calls:
            function_name = tc.function.name
            
            # THESE TOOLCALLS ARE FOR DEFUSER
            if function_name == "view_bomb":
                print("Defuser tool call: view_bomb")
                resp = bomb.view_bomb()

                messages.append({
                        "tool_call_id": tc.id,
                        "role": "tool",
                        "name": function_name,
                        "content": resp
                    })
                
            elif function_name == "view_module":
                print("Defuser tool call: view_module")
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except Exception:
                    args = {}
                module_id = args.get("module_id")
                if module_id is None:
                    resp = "Error: missing module_id in view_module call"
                else:
                    resp = bomb.view_module(int(module_id))

                messages.append({
                        "tool_call_id": tc.id,
                        "role": "tool",
                        "name": function_name,
                        "content": resp
                    })
                print(f"tool Resp: {resp}")

            elif function_name == "action_module":
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except Exception:
                    args = {}
                module_id = args.get("module_id")
                action = args.get("action")
                if module_id is None:
                    resp = "Error: missing module_id in action_module call"
                else:
                    if action is not None:
                        resp = bomb.action_module(int(module_id), action)
                print(f"tool Resp: {resp}")
                
                messages.append({
                        "tool_call_id": tc.id,
                        "role": "tool",
                        "name": function_name,
                        "content": resp
                    })
                
            # TOOLCALLS FOR TECHNICIAN GO HERE
            elif function_name == "get_manual":
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except Exception:
                    args = {}
                module_name = args.get("module_name")
                if module_name is None:
                    resp = "Error: missing module_name in get_manual call"
                else:
                    resp = bomb.get_manual(module_name)

                print(f"Technician tool call: get_manual for {module_name}")
                messages.append({
                        "tool_call_id": tc.id,
                        "role": "tool",
                        "name": function_name,
                        "content": resp
                    })

        # recursive function to take another step after tool call
        return take_turn(messages, tools, bomb)
    else:
        return response_message.content
