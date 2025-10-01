from time import sleep
from beaupy import confirm
from .backend import config_manager

from .utils.input import detect_key
from .utils.console import console, text_wrap
from .utils.cli import (
    get_user_confirmation,
    select_category,
    select_config,
    yap,
    COMMANDS,
)

is_running = False


def run():
    global is_running
    is_running = True

    config_manager.start()
    yap("greet")

    while is_running:
        command = get_command()

        if command not in COMMANDS:
            yap("_unavailable")

        elif command in ("help", "exit"):
            yap(command)
            if command == "exit":
                is_running = False

        elif command == "list":
            list_configs()

        elif command == "add":
            add_config()

        elif command == "edit":
            edit_config()

        elif command == "delete":
            delete_config()

        elif command == "reset all":
            reset_all_configs()


def get_command() -> str:
    command = console.input("\n[bold plum1]>>> [/bold plum1]").strip()
    print()
    return command


def list_configs() -> None:
    console.print(f"+{"":->12}+{"":->25}+{"":->25}+{"":->15}+")
    console.print(f"|{"category":^12}|{"from":^25}|{"to":^25}|{"active":^15}|")

    for category, configs in config_manager.config.items():
        console.print(f"+{"":->12}+{"":->25}+{"":->25}+{"":->15}+")

        if not configs:
            console.print(f"|{category:^12}|{"(none)":^67}|")
            continue

        for config in configs.values():
            key_from = text_wrap(config["from"], 18)
            key_to = text_wrap(config["to"], 18)
            active = "true" if config["active"] else "false"

            console.print(f"|{category:^12}|{key_from:^25}|{key_to:^25}|{active:^15}|")
    console.print(f"+{"":->12}+{"":->25}+{"":->25}+{"":->15}+")


def add_config() -> None:
    def get_key(prompt: str) -> str:
        console.print(prompt, end="")
        key = detect_key()
        console.print(key, style="bold yellow")

        sleep(0.8)
        return key

    def add():
        config = {"from": key_from, "to": key_to, "active": active}
        config_manager.add_config(category, config)
        console.print(f"\nAdded!")

    category = select_category()
    console.print(f"Category: [bold yellow]{category.title()}[/bold yellow]")

    console.print("(Press any key to register...)")
    key_from = get_key(prompt="[bold]from: ")
    key_to = get_key(prompt="[bold]to: ")
    active = confirm(
        "[bold]active: ", yes_text="True", no_text="False", default_is_yes=True
    )

    get_user_confirmation(
        f"Add a new {category}: [bold yellow]{key_from}[/bold yellow] - [bold yellow]{key_to}[/bold yellow]?",
        true_callback=add,
    )


def edit_config() -> None:
    def edit():
        config_manager.edit_config(category, key_from)
        console.print("\nEdited!")

    category = select_category()
    config = select_config(category, config_manager.config)

    key_from = config["from"]
    key_to = config["to"]
    status_after_edit = "Deactivate" if config["active"] else "Activate"

    get_user_confirmation(
        f"{status_after_edit} {category} [bold yellow]{key_from.title()} - {key_to.title()}[/bold yellow]?",
        true_callback=edit,
    )


def delete_config() -> None:
    def delete():
        config_manager.delete_config(category, key_from)
        console.print("\nDeleted!")

    category = select_category()
    config = select_config(category, config_manager.config)

    key_from = config["from"]
    key_to = config["to"]

    get_user_confirmation(
        f"Delete {category} [bold yellow]{key_from.title()} - {key_to.title()}[/bold yellow]?",
        true_callback=delete,
    )


def reset_all_configs() -> None:
    def reset():
        config_manager.reset_all_config()
        console.print("\nAll configs reset.")

    get_user_confirmation(
        "Reset [bold red]ALL[/bold] configs[red]?", true_callback=reset
    )


if __name__ == "__main__":
    run()
