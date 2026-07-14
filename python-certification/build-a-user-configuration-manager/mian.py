test_settings = {
    'theme': 'light',
    'language': 'english',
    'notifications': 'enabled'
}

def add_setting(settings, setting_tuple):
    key, value = setting_tuple
    key = key.lower()
    value = value.lower()
    
    if key in settings:
        return f"Setting '{key}' already exists! Cannot add a new setting with this name."
    else:
        settings[key] = value
        return f"Setting '{key}' added with value '{value}' successfully!"

def update_setting(settings, setting_tuple):
    key, value = setting_tuple
    key = key.lower()
    value = value.lower()
    
    if key in settings:
        settings[key] = value
        return f"Setting '{key}' updated to '{value}' successfully!"
    else:
        return f"Setting '{key}' does not exist! Cannot update a non-existing setting."

def delete_setting(settings, key):
    key = key.lower()
    
    if key in settings:
        del settings[key]
        return f"Setting '{key}' deleted successfully!"
    else:
        return "Setting not found!"  # Make sure there's no extra space

def view_settings(settings):
    if not settings:
        return "No settings available."
    
    result = "Current User Settings:\n"
    for key, value in settings.items():
        capitalized_key = key.capitalize()
        result += f"{capitalized_key}: {value}\n"
    return result

# Example usage (for testing):
if __name__ == "__main__":
    # Test the functions
    print(view_settings(test_settings))
    
    print(add_setting(test_settings, ('volume', 'high')))
    print(view_settings(test_settings))
    
    print(update_setting(test_settings, ('theme', 'dark')))
    print(view_settings(test_settings))
    
    print(delete_setting(test_settings, 'language'))
    print(view_settings(test_settings))
    
    # Test error cases
    print(add_setting(test_settings, ('theme', 'dark')))
    print(update_setting(test_settings, ('brightness', 'auto')))
    print(delete_setting(test_settings, 'nonexistent'))