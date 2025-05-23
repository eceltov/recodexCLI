import typer
from typing_extensions import Annotated
import typing
from collections.abc import Callable

from recodex_cli_lib import client_factory
from recodex_cli_lib.client import Client
import call_command.command as cmd
import call_command.cmd_utils as cmd_utils

app = typer.Typer()
state = { "verbose" : False }

@app.command()
def swagger(
):
    client = client_factory.get_client_interactive()
    print(client.endpoint_resolver.get_swagger())

@app.command()
def call(
    endpoint: Annotated[
        str, typer.Argument(help="Endpoint identifier in <presenter.handler> format", is_eager=True)
    ] = "",
    path: Annotated[
        list[str], typer.Option(help="Path Parameters", rich_help_panel="Request Parameters")
    ] = [],
    query: Annotated[
        list[str], typer.Option(help="Query Parameters", rich_help_panel="Request Parameters")
    ] = [],
    body: Annotated[
        str, typer.Option(help="JSON Body", rich_help_panel="Request Parameters")
    ] = "{}",
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity", is_eager=True)
    ] = False,
    help: Annotated[
        bool, typer.Option(help="Display Help", callback=cmd.help_callback)
    ] = False,
):
    """Calls a ReCodEx endpoint with the provided parameters.
    Requires an endpoint identifier in <presenter.handler> format.
    Use --path, --query, and --body options to pass a json string representing the parameters.
    """
    
    # help is handled in call_command.help_callback
    if help:
        return
    
    state["verbose"] = verbose
    client = get_client_with_verbosity()

    if endpoint == "":
        command = lambda: cmd.call_interactive(client, verbose)
    else:
        def command():
            #TODO: handle other params
            parsed_body = cmd_utils.parse_json(body)
            cmd.call(client, endpoint, path, query, parsed_body, verbose)

    execute_with_verbosity(command)

def get_client_with_verbosity() -> Client:
    return execute_with_verbosity(client_factory.get_client_interactive)

def execute_with_verbosity(command: Callable[[], typing.Any]):
    return cmd_utils.execute_with_verbosity(command, state["verbose"])

if __name__ == "__main__":
    app()
    ###TODO: handle files
