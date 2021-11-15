#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import BadOptionError

import os
from trigger.cli.cmdparser import parse_opts, UpdatingDefaultsHelpFormatter
from trigger.cli.cmdoptions import general_group
from trigger.cli.commands import get_commands_summary, COMMANDS
from trigger.cli.utils import get_prog


def main():
    """
        main function
    """
    args = sys.argv[1:]
    try:
        parser_kw = {
            'usage': '\n%prog <command> [options]',
            'add_help_option': False,
            'formatter': UpdatingDefaultsHelpFormatter(),
            'name': 'global',
            'prog': get_prog(),
        }
        cmd_name, cmd_args = parse_opts(args, get_commands_summary(COMMANDS), parser_kw, general_group)
    except BadOptionError as e:
        sys.stderr.write(str(e))
        sys.stderr.write(os.linesep)
        sys.exit(1)

    try:
        command = COMMANDS[cmd_name]()
    except KeyError:
        sys.stderr.write("The command %s not support\n" % cmd_name)
        sys.exit(1)

    command.execute(cmd_args)


if __name__ == "__main__":
    main()