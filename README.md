# Python CLI Template

Cookie cutter for python cli 

-----


High level

    trigger

    Usage:
    trigger <command> [options]

    Commands:
    action_one                  action_one command
    action_two                  action_two command
    show                        show the information for the matrix

    General Options:
    -h, --help     Show help.
    -v, --version  Show version and exit.


Sub Command

    trigger action_one -h

    Usage:   trigger action_one

    --start-from <start_from>  the fake option of action_one

    General Options:
    -h, --help                Show help.
    -v, --version             Show version and exit.
    (pythonclitemplate)


Nest Sub Command

    trigger show

    Usage:
    trigger show <command> [options]

    Commands:
    env                         show the information for the matrix
    image                       show the information for the matrix

    General Options:
    -h, --help     Show help.
    -v, --version  Show version and exit.


Furthermore

    trigger show env -h

    Usage:   trigger show env

    --envname <envname>  the name of environment

    General Options:
    -h, --help          Show help.
    -v, --version       Show version and exit.