def add_setting(settings, key_value):
    key, value = key_value[0].lower(), key_value[1].lower()
    if key in settings:
        return f"Setting '{key}' already exists! Cannot add a new setting with this name."
    settings[key] = value
    return f"Setting '{key}' added with value '{value}' successfully!"

def update_setting(settings, key_value):
    key, value = key_value[0].lower(), key_value[1].lower()
    if key in settings:
        settings[key] = value
        return f"Setting '{key}' updated to '{value}' successfully!"
    return f"Setting '{key}' does not exist! Cannot update a non-existing setting."

def delete_setting(settings, key):
    key = key.lower()
    if key in settings:
        del settings[key]
        return f"Setting '{key}' deleted successfully!"
    return "Setting not found!"

def view_settings(settings):
    if not settings:
        return "No settings available."
    result = "Current User Settings:"
    for key, value in settings.items():
        result += f"\n{key.capitalize()}: {value}"
    result += "\n"
    return result
test_settings = {'theme': 'dark', 'notifications': 'enabled', 'volume': 'high'}

print(view_settings(test_settings))
