"""
skele

Usage:
  jam hello
  jam init <name> [(--path | -p) PATH]
  jam trace <app_name> (--event | -e) <primary_event> (--secondary | -s) <se_1> [<se_2>...]
  jam input <app_name> ((--user | -u) <user_id> (--action | -a) <action> (--item | -i) <item_id> | (--file | -f) <datafile>)
  jam get <app_name> (--user | -u) <user_id> (--number | -n) <num_recs>
  jam deploy <app_name>
  jam -h | --help
  jam --version

Options:
  -h --help                         Show this screen.
  -n --name                         app name
  -p --path                         storage path [default: ~/Desktop/rec_apps]
  -e --event                        primary event, recommendation goal
  -s --secondary                    secondary events
  -u --user                         user name
  -a --action                       action name
  -i --item                         item name
  --version                         Show version.

Examples:
  jam hello
  jam init
Help:
  my git repo for issues
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import jam.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(skele.commands, k) and v:
            module = getattr(skele.commands, k)
            jam.commands = getmembers(module, isclass)
            command = [command[1] for command in skele.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
