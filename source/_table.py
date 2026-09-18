from colorama import Fore

from source import Timestamp, LogManager

class Table:
    """
    **Creates CLI based tables from given headers and rows.**
    
    *Methods*:
    - `minimalistic(headers:tuple, rows:tuple[tuple]) -> None`: Create a table with the
    minimalistic style.
    - `boxed(headers:tuple, rows:tuple[tuple]) -> None`: Create a table with the boxed
    style.
    - `borderless(headers:tuple, rows:tuple[tuple]) -> None`: Create a table with the
    borderless style.
    """

    # -------------------------------------------
    #  Private Methods
    # -------------------------------------------

    def _is_items_consistant(headers:tuple, rows:tuple[tuple]) -> bool:
        """
        **Check the consistancy of the header and rows, specifically the lengths.**
        
        *Parameters*:
        - `headers` (tuple): The table headers.
        - `rows` (tuple[tuple]): The table rows.
        
        *Returns*:
        - (bool): True if all items passed the check.
        """

        if len({len(row) for row in rows}) != 1: return False
        if len(headers) != len(rows[0]): return False

        return True

    def _sanitize_items(headers:tuple, rows:tuple[tuple]) -> list[list, list[list]]:
        """
        **Sanitize the headers and rows, stringifying all items.**
        
        *Parameters*:
        - `headers` (tuple): The table headers.
        - `rows` (tuple[tuple]): The table rows.
        
        *Returns*:
        - (list[list, list[list]]): Returns the headers and rows.
        """

        headers = [str(h) for h in headers]
        rows = [[str(i) for i in r] for r in rows]

        return headers, rows

    def _get_column_lengths(headers:list, rows:list[list]) -> list[int]:
        """
        **Get the length that would best fit all items in each column.**
        
        *Parameters*:
        - `headers` (list): The table headers.
        - `rows` (list[list]): The table rows.
        
        *Returns*:
        - (list[int]): A list of each columns best fitting length.
        """

        column_lengths = []

        for index, head in enumerate(headers):
            rows_items = [row[index] for row in rows] + [head]

            column_lengths.append(max([len(item) for item in rows_items]))

        return column_lengths

    # -------------------------------------------
    #  Public Methods
    # -------------------------------------------

    @staticmethod
    def minimalistic(headers:tuple, rows:tuple[tuple]):
        """
        **Create a table with the minimalistic style.**
        
        *Parameters*:
        - `headers` (tuple): The table headers.
        - `rows` (tuple[tuple]): The table rows.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return
        if not Table._is_items_consistant(headers, rows): return

        headers, rows = Table._sanitize_items(headers, rows)
        column_lengths = Table._get_column_lengths(headers, rows)

        # Print headers
        header = ''
        for index, length in enumerate(column_lengths):
            header += headers[index] + (' ' * (length - len(headers[index]))) + '   '
        print(f'{Timestamp.get()}{LogManager.get_caller_file()}\n{Fore.BLUE}{header}')

        # Print separator
        print(Fore.BLUE + '-' * (sum(column_lengths) + ((len(column_lengths) - 1) * 3)))

        # Print rows
        for row in rows:
            row_str = ''
            for index, item in enumerate(row):
                row_str += item + (' ' * (column_lengths[index] - len(item))) + '   '

            print(Fore.CYAN + row_str + Fore.RESET)

    @staticmethod
    def boxed(headers:tuple, rows:tuple[tuple]):
        """
        **Create a table with the boxed style.**
        
        *Parameters*:
        - `headers` (tuple): The table headers.
        - `rows` (tuple[tuple]): The table rows.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return
        if not Table._is_items_consistant(headers, rows): return

        headers, rows = Table._sanitize_items(headers, rows)
        column_lengths = Table._get_column_lengths(headers, rows)

        # Separator lambda function
        sep = lambda: '+' + '+'.join(['-' * (l + 5) for l in column_lengths]) + '+'

        print(f'{Timestamp.get()}{LogManager.get_caller_file()}')

        # Print separator
        print(Fore.BLUE + sep())

        # Print headers
        header = ''
        for index, length in enumerate(column_lengths):
            header += ('| ' + headers[index]
                       + (' ' * (length - len(headers[index]))) + '    ')
        print(f'{Fore.BLUE}{header}|')

        # Print separator
        print(Fore.BLUE + sep())

        # Print rows
        for row in rows:
            row_str = ''
            for index, item in enumerate(row):
                row_str += (f'{Fore.BLUE}| {Fore.CYAN}{item}'
                            + (' ' * (column_lengths[index] - len(item) + 4)))
        
            print(Fore.CYAN + row_str + f'{Fore.BLUE}|')

        # Print separator
        print(Fore.BLUE + sep() + Fore.RESET)

    @staticmethod
    def borderless(headers:tuple, rows:tuple[tuple]):
        """
        **Create a table with the borderless style.**
        
        *Parameters*:
        - `headers` (tuple): The table headers.
        - `rows` (tuple[tuple]): The table rows.
        """

        if LogManager.is_blacklisted(LogManager.get_method_caller()): return
        if not Table._is_items_consistant(headers, rows): return

        headers, rows = Table._sanitize_items(headers, rows)
        column_lengths = Table._get_column_lengths(headers, rows)

        # Print headers
        header = ''
        for index, length in enumerate(column_lengths):
            header += headers[index] + (' ' * (length - len(headers[index]))) + '   '
        print(f'{Timestamp.get()}{LogManager.get_caller_file()}\n{Fore.BLUE}{header}')

        # Print rows
        for row in rows:
            row_str = ''
            for index, item in enumerate(row):
                row_str += item + (' ' * (column_lengths[index] - len(item))) + '   '

            print(Fore.CYAN + row_str + Fore.RESET)
