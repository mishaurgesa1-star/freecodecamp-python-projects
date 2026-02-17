full_dot = '●'
empty_dot = '○'

def create_character(char_name, strength, intellingence, charisma):
    if not isinstance(char_name, str):
        return "The character name should be a string"
    elif len(char_name) == 0:
        return "The character should have a name"

    elif len(char_name) > 10:
        return "The character name is too long"
    elif any(char == " " for char in char_name):
        return "The character name should not contain spaces"
    
    if any(isinstance(stat, int) == False for stat in [strength, intellingence, charisma]):
        return "All stats should be integers"
    elif any(stat < 1 for stat in [strength, intellingence, charisma]):
        return "All stats should be no less than 1"
    elif any(stat > 4 for stat in [strength, intellingence, charisma]):
        return "All stats should be no more than 4"

    elif sum([strength, intellingence, charisma]) != 7:
        return "The character should start with 7 points"

    a = full_dot * strength + empty_dot * (10 -strength)
    b = full_dot * intellingence + empty_dot * (10 -intellingence)
    c = full_dot * charisma + empty_dot * (10 -charisma)
    return f"{char_name}\nSTR {a}\nINT {b}\nCHA {c}"

res = create_character('ren', 4, 2, 1)
print(res)
