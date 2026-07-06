#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django non risulta installato o non è disponibile. "
            "Hai attivato l'ambiente virtuale?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
