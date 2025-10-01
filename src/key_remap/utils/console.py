from rich.console import Console

console = Console()


def text_wrap(text: str, limit: int) -> str:
    """
    If `text` length exceeds `limit`, display the first `limit` characters and substitute the reset with ellipsis (`...`). Else return the whole `text`.
    """
    if len(text) <= limit:
        return text
    else:
        return f"{text[:limit]}..."


def hide_cursor() -> None:
    """Hide the blinking cursor in terminal."""
    print("\033[?25l", end="")


def show_cursor() -> None:
    """Show the blinking cursor in terminal."""
    print("\033[?25h", end="")


def delete_log_lines(number: int) -> None:
    """Delete the last `number` lines in terminal."""
    print(f"\x1b[{number}F")
