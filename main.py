import time
from bomb.bomb import Bomb
import defuser as defuser_harness
import technician as technician_harness
import prompts
from bomb.button import Button
from bomb.cyclo import Cyclogram
from bomb.wires import Wires
from bomb.dec import Dec
from teminal_ui import print_bomb, print_start, print_win, print_loss, print_turn, print_panel

DEFUSER_MODEL = "openrouter/~google/gemini-flash-latest"
TECHNICIAN_MODEL = "openrouter/~google/gemini-flash-latest"
TURNS = 15
TURN_DELAY = 2
MESSAGE_LIMIT = 300


def run_game(defuser_model: str, technician_model: str, turns: int, message_limit: int | None, modules=None, turn_delay: float = 0) -> dict:
    if modules is None:
        modules = [Button(), Cyclogram(), Dec(), Wires()]

    bomb = Bomb(modules)

    def _truncate(msg):
        if msg is None or message_limit is None:
            return msg
        if len(msg) > message_limit:
            return msg[:message_limit] + f"... [truncated at {message_limit} chars]"
        return msg

    limit_str = str(message_limit) if message_limit is not None else "unlimited"
    defuser_messages = [{"role": "system", "content": prompts.DEFUSER_SYSTEM_PROMPT.format(message_limit=limit_str)}]
    tech_messages = [{"role": "system", "content": prompts.TECHNICIAN_SYSTEM_PROMPT.format(message_limit=limit_str) + "\n\n" + prompts.MANUAL}]

    print_start()
    print_bomb(bomb)

    prev_defused = 0
    turns_taken = 0
    for i in range(turns):
        turns_taken += 1

        print_turn(i + 1)
        walkie = _truncate(defuser_harness.take_turn(defuser_messages, bomb, defuser_model))
        print_panel("defuser", walkie, defuser_model.split("/")[-1])
        tech_messages.append({"role": "user", "content": walkie})

        if bomb.defused():
            print_win()
            return {"defused": True, "turns_taken": turns_taken, "defuser_messages": defuser_messages, "tech_messages": tech_messages}

        if turn_delay:
            time.sleep(turn_delay)

        walkie = _truncate(technician_harness.take_turn(tech_messages, bomb, technician_model))
        print_panel("technician", walkie, technician_model.split("/")[-1])
        tech_messages.append({"role": "user", "content": walkie})
        defuser_messages.append({"role": "user", "content": walkie})

        curr_defused = sum(1 for m in bomb.modules if m.is_defused())
        if curr_defused > prev_defused:
            print_bomb(bomb)
            prev_defused = curr_defused

        if turn_delay:
            time.sleep(turn_delay)

    print_loss()
    return {"defused": False, "turns_taken": turns_taken, "defuser_messages": defuser_messages, "tech_messages": tech_messages}


def main():
    run_game(DEFUSER_MODEL, TECHNICIAN_MODEL, TURNS, MESSAGE_LIMIT, turn_delay=TURN_DELAY)


if __name__ == "__main__":
    main()