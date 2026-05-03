from bench import TURNS
from bomb.bomb import Bomb
import defuser as defuser_harness
import technician as technician_harness
import prompts

DEFUSER_MODEL = "openai/gpt-4o"
TECHNICIAN_MODEL = "openai/gpt-4o"

def main():
    """Bootstrapping project"""
    bomb = Bomb() # https://developers.openai.com/api/docs/guides/function-calling
    
    defuser_messages = [{ "role": "system", "content": prompts.DEFUSER_SYSTEM_PROMPT}]
    tech_messages = [{ "role": "system", "content": prompts.TECHNICIAN_SYSTEM_PROMPT + "\n\n" + prompts.MANUAL }]

    for i in range(TURNS):
        walkie = defuser_harness.take_turn(defuser_messages, bomb, DEFUSER_MODEL)
        print(f"\nDefuser says: {walkie}\n")
        tech_messages.append({"role": "user", "content": walkie})

        # check and see if bomb is completly defused
        if bomb.defused():
            print("Bomb defused! Congratulations!")
            return

        walkie = technician_harness.take_turn(tech_messages, bomb, TECHNICIAN_MODEL)
        print(f"\nTechnician says: {walkie}\n")
        defuser_messages.append({"role": "user", "content": walkie})
        


if (__name__ == "__main__"):
    main()
    pass
