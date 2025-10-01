from beaupy import select, confirm
from .console import console

YAP = {
    "greet": """
Type [bold green]help[/bold green] for more information, or [bold green]exit[/bold green] to quit. 
""",
    "exit": "[bold green]Key Remap[/bold green] exited",
    "help": """
Currently available commands:

    - [bold green]exit[/bold green]       |   Close this application
    - [bold green]list[/bold green]       |   List all the current configs
    - [bold green]add[/bold green]        |   Add a new config
    - [bold green]edit[/bold green]       |   Edit an existing config
    - [bold green]delete[/bold green]     |   Delete an existing config
    - [bold green]reset all[/bold green]  |   Reset all configs
    """,
    "_unavailable": 'Invalid command, type "help" for more information.',
}
COMMANDS = {"exit", "help", "list", "add", "edit", "delete", "reset all"}
CATEGORIES = ("keymap",)


def get_user_confirmation(prompt: str, true_callback, *args) -> None:
    """
    Ask the user to confirm their choice. Call `true_callback` if agreed.

    :param prompt: Question to ask
    :param true_callback: Function to call when user confirms

    :return:
    """
    is_confirmed = confirm(prompt, default_is_yes=True)

    if is_confirmed:
        true_callback(*args)
    else:
        console.print("\nCancelled")


def select_category() -> str:
    """
    Display an interactive category list for user to choose from.

    :return: The selected category
    """
    console.print("Choose a category:")
    return select(CATEGORIES, preprocessor=lambda category: category.title())


def select_config(category: str, configs):
    """
    Display an interactive list of configs for user to choose from.

    :param category: The selected category
    :param configs: The list of configs of the selected category

    :return: The selected config
    """
    console.print(
        f"Choose a config from [bold yellow]{category.title()}[/bold yellow]:"
    )
    configs = [config for config in configs[category].values()]
    return select(
        configs,
        preprocessor=lambda conf: f"from: [bold green]{conf['from'].title()}[/bold green] - to: [bold green]{conf['to'].title()}[/bold green] - active: [bold green]{"True" if conf['active'] else "False"}[/bold green]",
    )


def yap(about: str) -> None:
    console.print(YAP[about].strip())
