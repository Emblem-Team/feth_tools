from app.binary.unpack import unpack_binary
from app.binary.update import update_binary
from app.text.unpack import unpack_text
from app.text.pack import pack_text
from app.csv.bundle import make_bundle, patch_bundle
from app.utils.clear import clear_all, clear_bin, clear_json, clear_mods
import click


@click.group()
def cli():
    pass


@cli.command("unpack-bin")
def cli_unpack_binary():
    unpack_binary()


@cli.command("update-bin")
def cli_update_binary():
    update_binary()


@cli.command("unpack-text")
def cli_unpack_text():
    unpack_text()


@cli.command("pack-text")
def cli_pack_text():
    pack_text()


@cli.command("make-bundle")
def cli_make_bundle():
    make_bundle()


@cli.command("patch-bundle")
def cli_patch_bundle():
    patch_bundle()


@cli.command("clear-all")
def cli_clear_all():
    clear_all()


@cli.command("clear-bin")
def cli_clear_bin():
    clear_bin()


@cli.command("clear-json")
def cli_clear_json():
    clear_json()


@cli.command("clear-mods")
def cli_clear_mods():
    clear_mods()


@cli.command("hard-build")
@click.pass_context
def cli_hard_build(ctx: click.Context):
    ctx.invoke(cli_unpack_binary)
    ctx.invoke(cli_update_binary)
    ctx.invoke(cli_unpack_text)
    ctx.invoke(cli_build)


@cli.command("build")
@click.pass_context
def cli_build(ctx: click.Context):
    ctx.invoke(cli_clear_mods)
    ctx.invoke(cli_patch_bundle)
    ctx.invoke(cli_pack_text)


if __name__ == "__main__":
    print("=== Fire Emblem: Three Houses - Translating tools ===")
    print("=== by bqio ===")
    cli()
