from colorama import Fore

from loggerric2 import Timestamp, LogManager

def prompt(text:str, options:list[str]=None, default_option:str=None,
           auto_complete_option:bool=True, loop_until_valid:bool=False,
           case_sensitive:bool=False) -> str:
    """
    **Prompt the user in the CLI.**
    
    *Parameters*:
    - `text` (str): The question/prompting text.
    - `options` (list[str]): The options the user can pick.
    - `default_option` (str): The default option if the user just submits an empty
    string.
    - `auto_complete_option` (bool): If true, the function will attempt to autocomplete
    what the user typed if the user didn't fully match any of the given options.
    - `loop_until_valid` (bool): If true, the prompt will loop until a valid option
    is chosen, this can be escaped with a keyboard interrupt.
    - `case_sensitive` (bool): If true, when comparing the users answer to the list of
    options, it will compare cases.
    
    *Returns*:
    - (str): The users answer.
    """

    if LogManager.is_blacklisted(LogManager.get_method_caller()): return

    try:
        while True:
            # Format the options
            options_f = ''
            if options:
                o = [(Fore.YELLOW if default_option == o else Fore.CYAN) + o + Fore.BLUE
                    for o in options]
                options_f = ' [' + f'{Fore.BLUE} | '.join(o) + ']'

            user_response = input(Timestamp.get() + LogManager.get_caller_file()
                                  + f'{Fore.BLUE}{text}{options_f}: {Fore.YELLOW}')

            # Break if not looping
            if not loop_until_valid: break

            # The user picked the default option
            if user_response == '' and default_option:
                user_response = default_option
                break

            if auto_complete_option and options:
                if case_sensitive:
                    matches = [o for o in options if o.startswith(user_response)]
                else:
                    response_lower = user_response.lower()
                    matches = [o for o in options if o.lower().startswith(response_lower)]

                if len(matches) > 0:
                    user_response = matches[0]
                    break

            # Check if user response matches any options, respect case sensitivity option
            if options:
                if case_sensitive:
                    if user_response in options: break
                else:
                    if user_response.lower() in [o.lower() for o in options]: break

            print(f'{Fore.RED}"{Fore.YELLOW}{user_response}{Fore.RED}" Is not valid!')

        return Fore.RESET + user_response.strip() + Fore.RESET
    except KeyboardInterrupt:
        print(f'\n{Fore.RED}Keyboard interrupt detected, closing prompt!{Fore.RESET}')
