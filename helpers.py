# Helpers
import sys

def GetArgument(prompt: str, arg_no: int) -> str:
    # Get variable from CLI args. If no arg gien, will prompt.
    if len(sys.argv) > arg_no:
        arg = sys.argv[arg_no]
    else:
        arg = input(prompt)
    return arg
