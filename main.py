from bench import TURNS
from bomb.bomb import Bomb
import defuser as defuser_harness
import technician as technician_harness
import prompts
from teminal_ui import print_bomb, print_start, print_win, print_loss, print_turn, print_panel

DEFUSER_MODEL = "openai/gpt-4o"
TECHNICIAN_MODEL = "openai/gpt-4o"

def main():
    """Bootstrapping project"""
    bomb = Bomb() # https://developers.openai.com/api/docs/guides/function-calling
    
    defuser_messages = [{ "role": "system", "content": prompts.DEFUSER_SYSTEM_PROMPT}]
    tech_messages = [{ "role": "system", "content": prompts.TECHNICIAN_SYSTEM_PROMPT + "\n\n" + prompts.MANUAL }]

    print_start()
    print_bomb(bomb)

    prev_defused = 0
    
    for i in range(TURNS):
        print_turn(i + 1)

        walkie = defuser_harness.take_turn(defuser_messages, bomb, DEFUSER_MODEL)
        defuser_messages.append({"role": "user", "content": walkie})
        print_panel("defuser", walkie)

        # check and see if bomb is completly defused
        if bomb.defused():
            print_win()
            return

        walkie = technician_harness.take_turn(tech_messages, bomb, TECHNICIAN_MODEL)
        tech_messages.append({"role": "user", "content": walkie})
        defuser_messages.append({"role": "user", "content": walkie})
        print_panel("technician", walkie)

        curr_defused = sum(1 for m in bomb.modules if m.is_defused())
        if curr_defused > prev_defused:
            print_bomb(bomb)
            prev_defused = curr_defused
    
    print_loss()
        


if (__name__ == "__main__"):
    main()
    pass
