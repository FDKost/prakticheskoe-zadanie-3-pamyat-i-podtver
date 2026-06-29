def is_critical_action(action_name: str) -> bool:
    """
    Determine if an action is considered critical and requires confirmation.
    """
    critical_actions = {"send_message", "change_setting", "delete_data"}
    return action_name in critical_actions

def confirm_action(action_name: str, auto_confirm: bool = False) -> bool:
    """
    Prompt the user for confirmation before executing a critical action.
    If auto_confirm is True, the action is automatically approved.
    """
    if auto_confirm:
        return True
    prompt = f"Action '{action_name}' requires confirmation. Proceed? (y/n): "
    while True:
        resp = input(prompt).strip().lower()
        if resp in ("y", "yes"):
            return True
        elif resp in ("n", "no"):
            return False
        else:
            print("Please enter 'y' or 'n'.")
