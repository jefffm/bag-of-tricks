#!/usr/bin/python3

import asyncio
import asyncio.subprocess
import locale
import typing
import itertools
import sys


async def spin(msg: str) -> None:
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


def _build_command(*args: str, **flags: str) -> typing.Tuple[str, ...]:
    flag_args = tuple("--{}={}".format(k, v) for k, v in flags.items())
    return args + flag_args


async def run_command(command_args: typing.Tuple[str, ...]) -> int:
    proc = await asyncio.create_subprocess_exec(
        *command_args,
        stdout=asyncio.subprocess.PIPE,
    )

    # These sleeps are just added to show what the spinner does
    await asyncio.sleep(1)

    async for line in proc.stdout:
        print(line.decode(locale.getpreferredencoding(False)))

    await proc.wait()

    # (remove this sleep)
    await asyncio.sleep(1)

    return proc.returncode


async def supervisor(cmd: typing.Tuple[str, ...]) -> int:
    spinner = asyncio.ensure_future(
        spin('Running command: {}'.format(' '.join(cmd)))
    )

    result = await run_command(cmd)
    spinner.cancel()
    return result


def _run(cmd: typing.Tuple[str, ...]) -> int:
    event_loop = asyncio.get_event_loop()

    try:
        return_code = event_loop.run_until_complete(supervisor(cmd))
    finally:
        event_loop.close()

    return return_code


if __name__ == '__main__':
    command = _build_command('df', '-a', '-h', '/')
    _run(command)
