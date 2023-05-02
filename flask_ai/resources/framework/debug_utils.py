import os
from .colors import pr_light_purple, pr_yellow, pr_pink, pr_green, pr_red
from .constants import fields_dict

VERBOSE = os.getenv('VERBOSE')


def debug_steps(row, msg, level):
    if VERBOSE == "True":
        LOG = f"[DEBUG] - Level {level} - {msg}"
        current_message = row[fields_dict[level]]
        row[fields_dict[level]] = f"{current_message}\n{LOG}"
        pr_green(LOG)
        print("="*20)


def debug(msg):
    if VERBOSE == "True":
        pr_pink(f"[DEBUG] - {msg}")


def debug_attribute(attribute, value):
    if VERBOSE == "True":
        pr_light_purple(attribute, end="")
        pr_yellow(value, end="\n")


def debug_error(msg):
    pr_red(f"[ERROR] - {msg}")
