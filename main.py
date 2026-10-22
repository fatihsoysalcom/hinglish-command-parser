import re

def parse_hinglish_command(command_text: str) -> dict:
    """
    Parses a Hinglish command to identify an action and potential parameters.
    This simulates a low-resource Natural Language Processing (NLP) approach
    without relying on complex Large Language Models (LLMs), suitable for
    platforms like Raspberry Pi.
    """
    command_text = command_text.lower() # Normalize input to lowercase for easier matching

    # Define action keywords in both English and transliterated Hindi (Hinglish)
    # This dictionary represents our "knowledge base" for commands, replacing an LLM.
    actions = {
        "move": ["move", "le jao", "ghumaao", "hatao", "shift", "aage badhao"],
        "grab": ["grab", "pakad", "pakad lo", "hold"],
        "release": ["release", "chhod", "chhod do", "drop"],
        "stop": ["stop", "ruko", "band karo", "halt"]
    }

    # Define direction/object keywords, also in Hinglish
    directions = {
        "up": ["up", "upar"],
        "down": ["down", "neeche"],
        "left": ["left", "baaye", "left side"],
        "right": ["right", "daaye", "right side"],
        "forward": ["forward", "aage"],
        "backward": ["backward", "peeche"]
    }

    objects = {
        "box": ["box", "dabba", "dibba"],
        "item": ["item", "cheez", "vastu"],
        "arm": ["arm", "haath"]
    }

    # Initialize detected parameters
    detected_action = "unknown"
    detected_direction = "none"
    detected_object = "none"
    detected_degree = "normal" # e.g., "thoda" (a little)

    # --- Action Detection ---
    # Iterate through each action type and its associated keywords.
    # This simple keyword matching is the core of the "no LLM" approach.
    for action_type, keywords in actions.items():
        for keyword in keywords:
            # Using 're.search' with word boundaries to avoid partial matches
            # (e.g., 'arm' matching 'alarm').
            if re.search(r'\b' + re.escape(keyword) + r'\b', command_text):
                detected_action = action_type
                # Once a keyword is found, we can remove it to simplify subsequent searches.
                # This is a basic form of token consumption.
                command_text = re.sub(r'\b' + re.escape(keyword) + r'\b', '', command_text, 1)
                break # Found an action, move to next detection phase
        if detected_action != "unknown":
            break # Stop searching for actions if one is found

    # --- Direction/Object Detection (after action) ---
    # Similar keyword matching for directions and objects.
    for direction_type, keywords in directions.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', command_text):
                detected_direction = direction_type
                command_text = re.sub(r'\b' + re.escape(keyword) + r'\b', '', command_text, 1)
                break
        if detected_direction != "none":
            break

    for object_type, keywords in objects.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', command_text):
                detected_object = object_type
                command_text = re.sub(r'\b' + re.escape(keyword) + r'\b', '', command_text, 1)
                break
        if detected_object != "none":
            break

    # --- Degree detection (e.g., "thoda" for a little, indicating fine movement) ---
    if re.search(r'\b(thoda|little|zara)', command_text):
        detected_degree = "slight"

    return {
        "action": detected_action,
        "direction": detected_direction,
        "object": detected_object,
        "degree": detected_degree,
        "original_command": command_text.strip() # Remaining text after parsing
    }

# --- Example Usage ---
if __name__ == "__main__":
    print("Hinglish Command Parser (No LLM)")
    print("---------------------------------")
    print("This script demonstrates a simple keyword-based approach to parse Hinglish commands.")
    print("It's designed for low-resource environments like Raspberry Pi, avoiding complex LLMs.\n")

    commands = [
        "Arm ko upar le jao",           # Move arm up
        "Robot arm thoda left ghumaao", # Turn robot arm a little left
        "Box pakad lo",                 # Grab the box
        "Cheez chhod do",               # Release the item
        "Stop the arm",                 # Stop the arm
        "Move forward",                 # Move forward
        "Kuchh bhi nahi",               # Unrecognized command
        "Arm ko neeche hatao",          # Move arm down
        "Thoda upar shift karo",        # Shift a little up
        "Zara aage badhao"              # Move a little forward
    ]

    for i, cmd in enumerate(commands):
        print(f"Command {i+1}: '{cmd}'")
        parsed = parse_hinglish_command(cmd)
        print(f"  -> Action: {parsed['action']}")
        print(f"  -> Direction: {parsed['direction']}")
        print(f"  -> Object: {parsed['object']}")
        print(f"  -> Degree: {parsed['degree']}")
        print("-" * 30)
