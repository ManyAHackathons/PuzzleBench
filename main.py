from bomb.bomb import Bomb
from harness import take_turn
import prompts

MESSAGE_LENGTH_LIMIT = 250

def main():
    """Bootstrapping project"""
    bomb = Bomb()

    defuser_system = prompts.DEFUSER_SYSTEM_PROMPT
    technician_system = prompts.TECHNICIAN_SYSTEM_PROMPT + "\n\n" + prompts.MANUAL
    
    defuser_messages = []
    tech_messages = []

    turn_count = 0
    max_turns = 30
    
    def tell_technician(message: str) -> str:
        """Send a message to the technician describing what you see on the bomb."""
        tech_messages.append(f"Defuser says: {message[:MESSAGE_LENGTH_LIMIT]}")
        return "Message received by technician."

    def tell_defuser(message: str) -> str:
        """Send instructions to the defuser about what action to take on the bomb."""
        defuser_messages.append(f"Technician says: {message[:MESSAGE_LENGTH_LIMIT]}")
        return "Message received by defuser."
    
    while turn_count < max_turns:
        # defuser turn
        result = take_turn(defuser_messages + [defuser_system], [bomb.look_at_bomb, tell_technician])
        defuser_messages.append(result)
        print(f"Defuser: {result}")
        # technician turn
        result = take_turn(tech_messages + [technician_system], [tell_defuser])
        tech_messages.append(result)
        print(f"Technician: {result}")

        if bomb.modules and bomb.modules[0].is_defused():
            print("Bomb defused! Technician wins!")
            break
    
    


if (__name__ == "__main__"):
    main()
    pass
