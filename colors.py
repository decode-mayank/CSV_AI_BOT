# Reference - https://www.geeksforgeeks.org/print-colors-python-terminal/

def pr_red(skk,end="\n"): print(f"\033[91m {skk}\033[00m",end=end)
def pr_green(skk,end="\n"): print(f"\033[92m {skk}\033[00m",end=end)
def pr_yellow(skk,end="\n"): print(f"\033[93m {skk}\033[00m",end=end)
def pr_light_purple(skk,end="\n"): print(f"\033[94m {skk}\033[00m",end=end)
def pr_purple(skk,end="\n"): print(f"\033[95m {skk}\033[00m",end=end)
def pr_cyan(skk,end="\n"): print(f"\033[96m {skk}\033[00m",end=end) 
def pr_light_gray(skk,end="\n"): print(f"\033[90m {skk}\033[00m",end=end)
def pr_black(skk,end="\n"): print(f"\033[95m {skk}\033[00m",end=end)
def pr_pink(skk,end="\n"): print(f"\033[95m {skk}\033[00m",end=end)


def pr_bot_response(msg,end="\n"):
    pr_cyan(f"Bot: {msg}",end=end)