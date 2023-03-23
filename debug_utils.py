import os
from colors import pr_light_purple,pr_yellow,pr_pink,pr_green

VERBOSE = os.getenv('VERBOSE')

def debug_steps(row,msg,attribute=""):
    if VERBOSE=="True":
        LOG = f"[DEBUG] - {msg} {attribute}"
        row.append(LOG)
        pr_green(LOG) 
        
def debug(msg):
    if VERBOSE=="True":
        pr_pink(f"[DEBUG] - {msg}")  
    
def debug_attribute(attribute,value):
    if VERBOSE=="True":
        pr_light_purple(attribute,end="")
        pr_yellow(value,end="\n")