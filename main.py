import time
from bomb.bomb import Bomb
import defuser as defuser_harness
import technician as technician_harness
import prompts
from bomb.button import Button
from bomb.cyclo import Cyclogram
from bomb.wires import Wires
from bomb.dec import Dec

DEFUSER_MODEL = "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
TECHNICIAN_MODEL = "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
TURNS = 10
TURN_DELAY = 2          # seconds between defuser and technician turns
MESSAGE_LIMIT = 300     # max characters each agent can send over the walkie; None to disable

def _truncate(msg: str | None) -> str | None:
    if msg is None or MESSAGE_LIMIT is None:
        return msg
    if len(msg) > MESSAGE_LIMIT:
        return msg[:MESSAGE_LIMIT] + f"... [truncated at {MESSAGE_LIMIT} chars]"
    return msg


def main():
    bomb = Bomb([Button(), Cyclogram(), Dec()])

    limit_str = str(MESSAGE_LIMIT) if MESSAGE_LIMIT is not None else "unlimited"
    defuser_messages = [{"role": "system", "content": prompts.DEFUSER_SYSTEM_PROMPT.format(message_limit=limit_str)}]
    tech_messages = [{"role": "system", "content": prompts.TECHNICIAN_SYSTEM_PROMPT.format(message_limit=limit_str) + "\n\n" + prompts.MANUAL}]

    turns_taken = 0
    for i in range(TURNS):
        turns_taken += 1

        print(f"\n{'─'*60}")
        print(f"  TURN {i+1}  —  DEFUSER")
        print(f"{'─'*60}")
        walkie = _truncate(defuser_harness.take_turn(defuser_messages, bomb, DEFUSER_MODEL))
        print(f"\n  DEFUSER: {walkie}\n")
        tech_messages.append({"role": "user", "content": walkie})

        if bomb.defused():
            print(f"\n{'='*60}")
            print(f"  BOMB DEFUSED in {turns_taken} turn(s)!")
            print(f"{'='*60}\n")
            return

        time.sleep(TURN_DELAY)

        print(f"\n{'─'*60}")
        print(f"  TURN {i+1}  —  TECHNICIAN")
        print(f"{'─'*60}")
        walkie = _truncate(technician_harness.take_turn(tech_messages, bomb, TECHNICIAN_MODEL))
        print(f"\n  TECHNICIAN: {walkie}\n")
        defuser_messages.append({"role": "user", "content": walkie})

        time.sleep(TURN_DELAY)

    print(f"\n{'='*60}")
    print(f"  FAILED — bomb not defused after {turns_taken} turn(s).")
    print(f"{'='*60}\n")
        


if (__name__ == "__main__"):
    main()
