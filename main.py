from bomb.bomb import Bomb
from harness import take_turn
import prompts

MESSAGE_LENGTH_LIMIT = 250

defuser_tools = [
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
                        "description": "id of the module to perform an action on"
                    },
                    "action": {
                        "type": "string",
                        "description": "The action to perform on the module"
                    }
                }
            }
        },
    }
]

technician_tools = [
    # Technician tools would go here, but for this demo, the technician doesn't have any tools since they don't need to interact with the bomb directly
    # technician can get manual for specific modules.
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
                        "description": "The module type name as inferred from the defuser's description (e.g. 'Button', 'Wires')"
                    }
                }
            }
        }
    }
]



def main():
    """Bootstrapping project"""
    bomb = Bomb() # https://developers.openai.com/api/docs/guides/function-calling
    
    defuser_messages = [{ "role": "system", "content": prompts.DEFUSER_SYSTEM_PROMPT}]
    tech_messages = [{ "role": "system", "content": prompts.TECHNICIAN_SYSTEM_PROMPT + "\n\n" + prompts.MANUAL }]

    for i in range(3): # each agent gets 3 turns to interact with the bomb and each other
        walkie = take_turn(defuser_messages, defuser_tools, bomb)
        print(f"Defuser says: {walkie}")
        # last thing the defuser says is the walkie talkie message to the technician, so we add that to the technician's messages before their turn
        tech_messages.append({ "role": "user", "content": walkie })
        # same goes other way
        walkie = take_turn(tech_messages, technician_tools, bomb)
        print(f"Technician says: {walkie}")
        defuser_messages.append({ "role": "user", "content": walkie })


if (__name__ == "__main__"):
    main()
    pass
