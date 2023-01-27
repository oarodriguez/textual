from textual.app import App, ComposeResult
from textual.widgets import Input


class InputTester(App[None]):
    """Input widget testing app."""

    def compose(self) -> ComposeResult:
        for value, input_id in (
            ("", "empty"),
            ("Shiny", "single-word"),
            ("Curse your sudden but inevitable betrayal", "multi-no-punctuation"),
            (
                "We have done the impossible, and that makes us mighty.",
                "multi-punctuation",
            ),
            ("Long as she does it quiet-like", "multi-and-hyphenated"),
        ):
            yield Input(value, id=input_id)


async def test_input_home() -> None:
    """Going home should always land at position zero."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.action_home()
            assert input.cursor_position == 0


async def test_input_end() -> None:
    """Going end should always land at the last position."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.action_end()
            assert input.cursor_position == len(input.value)


async def test_input_right_from_home() -> None:
    """Going right should always land at the next position, if there is one."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.action_cursor_right()
            assert input.cursor_position == (1 if input.value else 0)


async def test_input_right_from_end() -> None:
    """Going right should always stay put if doing so from the end."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.action_end()
            input.action_cursor_right()
            assert input.cursor_position == len(input.value)


async def test_input_left_from_home() -> None:
    """Going left from home should stay put."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.action_cursor_left()
            assert input.cursor_position == 0


async def test_input_left_from_end() -> None:
    """Going left from the end should go back one place, where possible."""
    async with InputTester().run_test() as pilot:
        for input in pilot.app.query(Input):
            input.action_end()
            input.action_cursor_left()
            assert input.cursor_position == (len(input.value) - 1 if input.value else 0)


# TODO: more tests.
