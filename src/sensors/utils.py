import os
import board


def get_board_pin(env_var_name: str) -> object:
    pin_name = os.getenv(env_var_name)
    if not pin_name:
        raise EnvironmentError(
            f"Missing environment variable: {env_var_name}. "
            f"Please define it in your .env file (e.g., {env_var_name}=D24)"
        )
    try:
        return getattr(board, pin_name)
    except AttributeError:
        raise ValueError(f"Invalid pin name '{pin_name}' in {env_var_name}.")
