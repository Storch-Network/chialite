import click

from chialite import __version__
from chialite.cmds.configure import configure_cmd
from chialite.cmds.farm import farm_cmd
from chialite.cmds.init import init_cmd
from chialite.cmds.keys import keys_cmd
from chialite.cmds.netspace import netspace_cmd
from chialite.cmds.plots import plots_cmd
from chialite.cmds.show import show_cmd
from chialite.cmds.start import start_cmd
from chialite.cmds.stop import stop_cmd
from chialite.cmds.wallet import wallet_cmd
from chialite.util.default_root import DEFAULT_ROOT_PATH

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def monkey_patch_click() -> None:
    # this hacks around what seems to be an incompatibility between the python from `pyinstaller`
    # and `click`
    #
    # Not 100% sure on the details, but it seems that `click` performs a check on start-up
    # that `codecs.lookup(locale.getpreferredencoding()).name != 'ascii'`, and refuses to start
    # if it's not. The python that comes with `pyinstaller` fails this check.
    #
    # This will probably cause problems with the command-line tools that use parameters that
    # are not strict ascii. The real fix is likely with the `pyinstaller` python.

    import click.core

    click.core._verify_python3_env = lambda *args, **kwargs: 0  # type: ignore


@click.group(
    help=f"\n  Manage chialite blockchain infrastructure ({__version__})\n",
    epilog="Try 'chialite start node', 'chialite netspace -d 192', or 'chialite show -s'",
    context_settings=CONTEXT_SETTINGS,
)
@click.option("--root-path", default=DEFAULT_ROOT_PATH, help="Config file root", type=click.Path(), show_default=True)
@click.pass_context
def cli(ctx: click.Context, root_path: str) -> None:
    from pathlib import Path

    ctx.ensure_object(dict)
    ctx.obj["root_path"] = Path(root_path)


@cli.command("version", short_help="Show chialite version")
def version_cmd() -> None:
    print(__version__)


@cli.command("run_daemon", short_help="Runs chialite daemon")
@click.pass_context
def run_daemon_cmd(ctx: click.Context) -> None:
    from chialite.daemon.server import async_run_daemon
    import asyncio

    asyncio.get_event_loop().run_until_complete(async_run_daemon(ctx.obj["root_path"]))


cli.add_command(keys_cmd)
cli.add_command(plots_cmd)
cli.add_command(wallet_cmd)
cli.add_command(configure_cmd)
cli.add_command(init_cmd)
cli.add_command(show_cmd)
cli.add_command(start_cmd)
cli.add_command(stop_cmd)
cli.add_command(netspace_cmd)
cli.add_command(farm_cmd)


def main() -> None:
    monkey_patch_click()
    cli()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
