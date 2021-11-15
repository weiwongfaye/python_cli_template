import sys
import optparse

from optparse import Option, BadOptionError
from trigger.cli import cmdoptions
from trigger.cli.cmdparser import ConfigOptionParser, UpdatingDefaultsHelpFormatter, parse_opts
from trigger.cli.utils import get_prog, get_userinput_boolean,is_true
from trigger.log import Logger
from trigger.trigger_logic import FakeTrigger


class Command(object):
    name = None
    usage = None
    hidden = None
    summary = ""

    def __init__(self):
        self.parser_kw = {
            'usage': self.usage,
            'prog': '%s %s' % (get_prog(), self.name),
            'formatter': UpdatingDefaultsHelpFormatter(),
            'add_help_option': False,
            'name': self.name,
            'description': self.__doc__,
        }

        self.parser = ConfigOptionParser(**self.parser_kw)

        # Commands should add options to this option group
        optgroup_name = '%s Options' % self.name.capitalize()
        self.cmd_opts = optparse.OptionGroup(self.parser, optgroup_name)

        # Add the general options
        gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, self.parser)
        self.parser.add_option_group(gen_opts)

        # set logger
        self.logger = Logger()
        self.logger.add_consumers(
            (Logger.VERBOSE_DEBUG, sys.stdout),
        )

    def parse_args(self, args):
        # factored out for testability
        return self.parser.parse_args(args)

    def run(self, args):
        """
            The sub command class should overide this method
        """
        NotImplemented

    def execute(self, args=None):
        """
            The main interface for exectute the command
        """
        try:
            self.run(args)
        except Exception:
            sys.stderr.write("ERROR: %s \n" % str(sys.exc_info()[1]))
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)


class ActionOneCommand(Command):
    name = "action_one"
    usage = """%prog """
    summary = "action_one command"

    def __init__(self):
        super(ActionOneCommand, self).__init__()

        self.parser.add_option(Option(
            '--start-from',
            dest='start_from',
            action='store',
            default=None,
            help="the fake option of action_one"
        ))

    def run(self, args):
        try:
            options, _ = self.parse_args(args)
        except BadOptionError:
            sys.stderr.write("ERROR: %s \n" % str(sys.exc_info()[1]))
            return

        if not options.start_from:
            sys.stderr.write("ERROR: %s \s" % "please provide the start_from parameter")
        else:
            sys.stdout.write("start_from = {}\n".format(options.start_from))
            fake_obj = FakeTrigger()
            fake_obj.process("action_one")


class ActionTwoCommand(Command):
    name = "action_two"
    usage = """%prog """
    summary = "action_two command"

    def __init__(self):
        super(ActionTwoCommand, self).__init__()
        self.parser.add_option(Option(
            '--envname',
            dest='envname',
            action='store',
            help="the name of environment"
        ))

    def run(self, args):
        try:
            options, _ = self.parse_args(args)
            msg = "Do you really want to process this %s [y/n]: " % options.envname
            user_input = get_userinput_boolean(msg)
            if is_true(user_input):
                fake_obj = FakeTrigger()
                fake_obj.process("action_two")
                sys.stdout.write("the action on [%s] has been processed \n" % options.envname)
        except BadOptionError:
            sys.stderr.write("ERROR: %s" % str(sys.exc_info()[1]))
            return



class ShowCommand(Command):
    name = "show"
    usage = """%prog """
    summary = "show the information for the matrix"

    def __init__(self):
        super(ShowCommand, self).__init__()

    def get_prog(self):
        return "%s %s" % (get_prog(), self.name)

    def run(self, args):
        # define the subclass here
        class EnvCommand(self.__class__):
            name = "show env"
            subcommand = "env"
            usage = """%prog"""
            summary = "show the information for the matrix"

            def __init__(self):
                super(EnvCommand, self).__init__()
                self.parser.add_option(Option(
                    '--envname',
                    dest='envname',
                    action='store',
                    default=None,
                    help="the name of environment"
                ))

            def run(self, args):
                try:
                    options, _ = self.parse_args(args)
                    if options.envname:
                        sys.stdout.write(options.envname)
                        sys.stdout.write("\n")
                    else:
                        sys.stdout.write("\n")
                except BadOptionError:
                    sys.stderr.write("ERROR: %s" % str(sys.exc_info()[1]))
                    return

        class ImageCommand(self.__class__):
            name = "show image"
            subcommand = "image"
            usage = """%prog"""
            summary = "show the information for the matrix"

            def __init__(self):
                super(ImageCommand, self).__init__()

            def run(self, args):
                sys.stdout.write("show images")
                sys.stdout.write("\n")

        sub_commands = {
            EnvCommand.subcommand: EnvCommand,
            ImageCommand.subcommand: ImageCommand
        }

        parser_kw = {
            'usage': '\n%prog <command> [options]',
            'add_help_option': False,
            'formatter': UpdatingDefaultsHelpFormatter(),
            'name': 'global',
            'prog': self.get_prog(),
        }
        sub_command, args_else = parse_opts(args, get_commands_summary(sub_commands), parser_kw,
                                            cmdoptions.general_group)

        sub_commands[sub_command]().run(args_else)

COMMANDS = {
    ActionOneCommand.name: ActionOneCommand,
    ActionTwoCommand.name: ActionTwoCommand,
    ShowCommand.name: ShowCommand,
}


def get_commands_summary(commands):
    """Yields sorted (command name, command summary) tuples."""
    cmd_items = commands.items()
    for name, command_class in cmd_items:
        yield (name, command_class.summary)

