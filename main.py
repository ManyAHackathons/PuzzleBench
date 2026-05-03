import time
from bomb.bomb import Bomb
import defuser as defuser_harness
import technician as technician_harness
import prompts
from bomb.button import Button
from bomb.cyclo import Cyclogram
from bomb.wires import Wires
from bomb.dec import Dec

DEFUSER_MODEL = "openrouter/openai/gpt-oss-120b:free"
TECHNICIAN_MODEL = "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
TURNS = 10
TURN_DELAY = 2
MESSAGE_LIMIT = 300


def run_game(defuser_model: str, technician_model: str, turns: int, message_limit: int | None, modules=None, turn_delay: float = 0) -> dict:
    if modules is None:
        modules = [Button(), Cyclogram(), Dec()]

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

    turns_taken = 0
    for i in range(turns):
        turns_taken += 1

        print(f"\n{'─'*60}")
        print(f"  TURN {i+1}  —  DEFUSER")
        print(f"{'─'*60}")
        walkie = _truncate(defuser_harness.take_turn(defuser_messages, bomb, defuser_model))
        print(f"\n  DEFUSER: {walkie}\n")
        tech_messages.append({"role": "user", "content": walkie})

        if bomb.defused():
            print(f"\n{'='*60}")
            print(f"  BOMB DEFUSED in {turns_taken} turn(s)!")
            print(f"{'='*60}\n")
            return {"defused": True, "turns_taken": turns_taken, "defuser_messages": defuser_messages, "tech_messages": tech_messages}

        if turn_delay:
            time.sleep(turn_delay)

        print(f"\n{'─'*60}")
        print(f"  TURN {i+1}  —  TECHNICIAN")
        print(f"{'─'*60}")
        walkie = _truncate(technician_harness.take_turn(tech_messages, bomb, technician_model))
        print(f"\n  TECHNICIAN: {walkie}\n")
        defuser_messages.append({"role": "user", "content": walkie})

        if turn_delay:
            time.sleep(turn_delay)

    print(f"\n{'='*60}")
    print(f"  FAILED — bomb not defused after {turns_taken} turn(s).")
    print(f"{'='*60}\n")
    return {"defused": False, "turns_taken": turns_taken, "defuser_messages": defuser_messages, "tech_messages": tech_messages}


def main():
    run_game(DEFUSER_MODEL, TECHNICIAN_MODEL, TURNS, MESSAGE_LIMIT, turn_delay=TURN_DELAY)


if __name__ == "__main__":
    main()
