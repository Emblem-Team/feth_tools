from app.binary.unpack import unpack_binary
from app.binary.update import update_binary
from app.binary.gz import decompress_gz, compress_gz
from app.text.unpack import unpack_text
from app.text.pack import pack_text
from app.csv.bundle import make_bundle, patch_bundle
from app.utils.clear import clear_all, clear_bin, clear_json, clear_mods
from app.graphic.tutorial import unpack_tutorials, decompress_tutorials
from app.graphic.tutorial import unpack_binary_archive

from time import perf_counter
from colorama import init as colorama_init, Fore, Style
from pathlib import Path
from dotenv import load_dotenv

import click

colorama_init()
load_dotenv()


@click.group()
def cli():
    pass


@cli.command("unpack-bin")
def cli_unpack_binary():
    print(f"{Fore.YELLOW}Unpacking binary...{Style.RESET_ALL}")
    unpack_binary()


@cli.command("update-bin")
def cli_update_binary():
    print(f"{Fore.YELLOW}Updating binary...{Style.RESET_ALL}")
    update_binary()


@cli.command("unpack-text")
def cli_unpack_text():
    print(f"{Fore.YELLOW}Unpacking text...{Style.RESET_ALL}")
    unpack_text()


@cli.command("pack-text")
def cli_pack_text():
    print(f"{Fore.YELLOW}Packing text...{Style.RESET_ALL}")
    pack_text()


@cli.command("make-bundle")
def cli_make_bundle():
    print(f"{Fore.YELLOW}Making bundle...{Style.RESET_ALL}")
    make_bundle()


@cli.command("patch-bundle")
def cli_patch_bundle():
    print(f"{Fore.YELLOW}Patching bundle...{Style.RESET_ALL}")
    patch_bundle()


@cli.command("clear-all")
def cli_clear_all():
    print(f"{Fore.YELLOW}Clearing files...{Style.RESET_ALL}")
    clear_all()


@cli.command("clear-bin")
def cli_clear_bin():
    print(f"{Fore.YELLOW}Clearing binary...{Style.RESET_ALL}")
    clear_bin()


@cli.command("clear-json")
def cli_clear_json():
    print(f"{Fore.YELLOW}Clearing json...{Style.RESET_ALL}")
    clear_json()


@cli.command("clear-mods")
def cli_clear_mods():
    print(f"{Fore.YELLOW}Clearing mods...{Style.RESET_ALL}")
    clear_mods()


@cli.command("unpack-tutorials")
def cli_unpack_tutorials():
    print(f"{Fore.YELLOW}Unpacking tutorials...{Style.RESET_ALL}")
    unpack_tutorials()


@cli.command("decompress-tutorials")
def cli_decompress_tutorials():
    print(f"{Fore.YELLOW}Decompressing tutorials...{Style.RESET_ALL}")
    decompress_tutorials()


@cli.command("decompress-gz")
@click.argument("input-file")
@click.argument("output-file")
def cli_decompress_gz(input_file: Path, output_file: Path):
    decompress_gz(input_file, output_file)


@cli.command("compress-gz")
@click.argument("input-file")
@click.argument("output-file")
def cli_compress_gz(input_file: Path, output_file: Path):
    compress_gz(input_file, output_file)


@cli.command("unpack-bin-arch")
@click.argument("archive-path")
@click.argument("output-path")
@click.argument("entry-ext")
def cli_unpack_binary_archive(archive_path: Path, output_path: Path, entry_ext: str):
    unpack_binary_archive(archive_path, output_path, entry_ext)


@cli.command("init")
@click.pass_context
def cli_hard_build(ctx: click.Context):
    print(f"{Fore.YELLOW}Initialize...{Style.RESET_ALL}")
    start_time = perf_counter()
    ctx.invoke(cli_clear_all)
    ctx.invoke(cli_unpack_binary)
    ctx.invoke(cli_update_binary)
    ctx.invoke(cli_unpack_text)
    ctx.invoke(cli_make_bundle)
    end_time = perf_counter()
    print(
        f"{Fore.CYAN}Initialize is done. Time: {end_time - start_time}s{Style.RESET_ALL}"
    )


@cli.command("build")
@click.pass_context
def cli_build(ctx: click.Context):
    print(f"{Fore.YELLOW}Building...{Style.RESET_ALL}")
    start_time = perf_counter()
    ctx.invoke(cli_clear_mods)
    ctx.invoke(cli_patch_bundle)
    ctx.invoke(cli_pack_text)
    end_time = perf_counter()
    print(f"{Fore.CYAN}Build is done. Time: {end_time - start_time}{Style.RESET_ALL}")


if __name__ == "__main__":
    print(
        f"{Fore.YELLOW}=== Fire Emblem: Three Houses - Translating tools ==={Style.RESET_ALL}"
    )
    print(f"{Fore.YELLOW}=== by bqio ==={Style.RESET_ALL}")
    cli()
