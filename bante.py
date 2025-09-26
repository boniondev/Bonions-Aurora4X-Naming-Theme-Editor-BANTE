''' Bonion's Aurora4X Naming Theme Editor
    This software is released under the MIT license. See LICENSE for details.
    Copyright (C) 2025 boniondev
'''
import argparse
import sqlite3
import sys

def check_for_num_id(string_id : str) -> int:
    '''
        Checks if the given string ID is an actual number,
        prints an error if it isn't,
        returns the ID as an integer if it is.
        return value may be freely discarded.
    '''
    if string_id.isnumeric() is False:
        print(
            "Error! Non numeric ID detected\n"
            "Please use numbers!"
        )
        sys.exit(1)
    else:
        int_id : int = int(string_id)
        return int_id

def connect(path : str, read_only : bool = True) -> sqlite3.Connection:
    '''
        Reusable instructions to connect to the database.\n
        READ-ONLY   by default\n
        READ-WRITE  if read_only is passed as false 
    '''
    try:
        connection : sqlite3.Connection = sqlite3.connect(
            f"file:{path if path else "AuroraDB.db"}?mode={"ro" if read_only else "rw"}",
            uri = True,
            isolation_level = "EXCLUSIVE",
        )
        return connection
    except sqlite3.OperationalError:
        print(  "Could not open database. Is the path correct and UNIX styled?" +
                "Am I in the same folder as AuroraDB.db?")
        print("banse will close now!")
        sys.exit(1)

if __name__ == "__main__":

    PARSER : argparse.ArgumentParser = argparse.ArgumentParser(
        prog = "py[thon] bante.py",
        description = "Bonion's Aurora4X Naming Theme Editor",
        epilog = "Backup your DB before using this tool!",
        formatter_class = argparse.RawTextHelpFormatter,
    )
    MUTUALEXCGROUP : argparse._MutuallyExclusiveGroup = PARSER.add_mutually_exclusive_group(required = True)
    PARSER.add_argument(
        "-p", "--path",
        help =  "UNIX style absolute or relative path to Aurora.db " +
                "(Looks inside current directory if unspecified)",
        required = False
    )
    MUTUALEXCGROUP.add_argument(
        "-l", "--list", help = "List all naming themes", action ="store_true", dest = "list"
    )
    MUTUALEXCGROUP.add_argument(
        "-ln", "--list-names",
        help = "List all names from a given ThemeID",
        action = "store", nargs = 1, dest = "list_from_themeid", type = int
    )
    MUTUALEXCGROUP.add_argument(
        "-dn", "--delete-name",
        help = "Delete name(s) from a given ThemeID."
                " Insert the ThemeID, and then the rows you wish to delete, separated by spaces",
        action = "store", nargs = "+", metavar = ("THEMEID", "DELETIONS"), dest = "deletenames"
    )
    MUTUALEXCGROUP.add_argument(
        "-dt", "--delete-theme",
        help =  "Delete NamingThemes from given ThemeIDs."
                "\nPut y or n at the beginning of the command to keep/delete orphan names.\n"
                "Deleting NamingThemes a Race is actively using may have unpredictable results. " 
                "Do so at your own risk.",
        action = "store", nargs = "+", metavar = ("DELETEORPHANS", "THEMEID"), dest = "deletetheme"
    )
    MUTUALEXCGROUP.add_argument(
        "-an", "--add-names",
        help =  "Add name(s) to a NameTheme."
                " A text file with names separated by newlines must be supplied,"
                " along with the ThemeID to add the names to.",
        nargs = 2, metavar = ("PATHTOFILE", "THEMEID"), dest = "addnames"
    )

    ARGS : argparse.Namespace= PARSER.parse_args()
    if ARGS.list:
        CONN : sqlite3.Connection   = connect(ARGS.path)
        cur  : sqlite3.Cursor       = CONN.cursor()
        cur.execute("SELECT * FROM DIM_NamingThemeTypes")
        ROWS : tuple[str, ...] = tuple(cur.fetchall())
        print("ThemeID | Description")
        print("---------------------")
        for ROW in ROWS:
            print(f"{ROW[0]} | {ROW[1]}")
        CONN.close()

    elif ARGS.list_from_themeid:
        CONN : sqlite3.Connection   = connect(ARGS.path)
        cur  : sqlite3.Cursor       = CONN.cursor()
        cur.execute(f"SELECT Name FROM DIM_NamingTheme WHERE NameThemeID = '{ARGS.list_from_themeid}'")
        ROWS : tuple[str, ...] = tuple(cur.fetchall())
        NUM = 0
        for ROW in ROWS:
            print(f"{NUM}|{ROW[0]}")
            NUM = NUM + 1
        CONN.close()

    elif ARGS.deletenames:
        if len(ARGS.deletenames) < 2:
            print("ThemeID was provided, but no rows to delete were given.")
            print("Deleting nothing!")
            sys.exit(0)

        THEMEID     : int                   = int(ARGS.deletenames[0])
        DELETIONS   : tuple[int, ...]       = tuple(map(int, ARGS.deletenames[1:]))
        CONN        : sqlite3.Connection    = connect(ARGS.path, False)
        cur         : sqlite3.Cursor        = CONN.cursor()

        cur.execute(f"SELECT Description FROM DIM_NamingThemeTypes WHERE ThemeID = '{THEMEID}'")
        RESULTS : list[str] = cur.fetchall()
        match len(RESULTS):
            case 0:
                print("No theme found with provided ThemeID.")
                print("Exiting...")
                sys.exit(1)
            case 1:
                cur.execute(f"SELECT Name FROM DIM_NamingTheme WHERE NameThemeID = '{THEMEID}'")
                ALL_ROWS            : tuple[str, ...]   = tuple([row[0] for row in cur.fetchall()])
                NAMESTODELETE       : tuple[str, ...]   = tuple([ALL_ROWS[i] for i in DELETIONS])
                NAMESTODELETESQL    : str               = " OR ".join([f"Name = '{name}'" for name in NAMESTODELETE])
                print(
                        "DELETE "
                        "FROM DIM_NamingTheme "
                        f"WHERE NameThemeID = '{THEMEID}' AND ({NAMESTODELETESQL})"
                )
                cur.execute(
                            "DELETE "
                            "FROM DIM_NamingTheme "
                            f"WHERE NameThemeID = '{THEMEID}' AND ({NAMESTODELETESQL})"
                            )
                print("You are about to delete " + ', '.join(f"{name}" for name in NAMESTODELETE) + f" from {RESULTS[0][0]}.")
                print("Are you sure? (y/N)")
                if input().lower() != 'y':
                    print("Aborting...")
                    CONN.rollback()
                    CONN.close()
                    sys.exit(0)
                else:
                    CONN.commit()
                    print("Changes committed successfully.")
                    CONN.close()
                    sys.exit(0)
            case _:
                print("Multiple Themes found with the same ThemeID!")
                print("This should never happen under normal circumstances!")
                print(  "If you have edited the db using this tool," +
                        " reload your backup " +
                        "(your db is possibly malformed) "
                        "and open an issue at https://github.com/boniondev/Bonions-Aurora4X-Naming-Theme-Editor-BANTE/issues"
                    )
                sys.exit(1)
    elif ARGS.deletetheme:
        DECISION : str = ARGS.deletetheme[0]
        match DECISION.lower():
            case 'y':
                DELETEORPHANS = True
            case 'n':
                DELETEORPHANS = False
            case _:
                print("No valid input given for flag -dt, y/n required!")
                sys.exit(1)
        
        THEMEID  : str
        THEMEIDS : tuple[str] = tuple(ARGS.deletetheme[1:])
        for THEMEID in THEMEIDS:
            check_for_num_id(THEMEID)

        CONN            : sqlite3.Connection    = connect(ARGS.path, False)
        cur             : sqlite3.Cursor        = CONN.cursor()

        THEMEIDNAMES    : tuple[str]            = cur.execute(f"SELECT Description FROM DIM_NamingThemeTypes WHERE {" OR ".join([f"ThemeID = {id}" for id in THEMEIDS])}").fetchall()

        WARNSTRING : str = (
                            "You are about to delete " +
                            ", ".join([f"{description[0]}" for description in cur.execute(f"SELECT Description FROM DIM_NamingThemeTypes WHERE {" OR ".join([f"Description = '{THEMEIDNAME[0]}'" for THEMEIDNAME in THEMEIDNAMES])}").fetchall()]) + # I am so sorry
                            (" along with the names inside, are you sure?"if DELETEORPHANS else ", are you sure?")
                            )

        for THEMEID in THEMEIDS:
            cur.execute(f"DELETE FROM DIM_NamingThemeTypes WHERE ThemeID = '{THEMEID}'")
            if DELETEORPHANS:
                cur.execute(f"DELETE FROM DIM_NamingTheme WHERE NameThemeID = '{THEMEID}'")
            print(THEMEID)
        
        print(WARNSTRING)
        print("[y/N]")
        if input().lower() != 'y':
            print("Aborting...")
            CONN.rollback()
            sys.exit(0)
        else:
            CONN.commit()
            print("Changes committed successfully.")
            CONN.close()
            sys.exit(0)

    elif ARGS.addnames:
        CONN        : sqlite3.Connection    = connect(ARGS.path, False)
        cur         : sqlite3.Cursor        = CONN.cursor()


        PATHTOFILE  : str = ARGS.addnames[0]
        THEMEID     : str = ARGS.addnames[1]
        THEMEID     : int = check_for_num_id(THEMEID)
        
        try:
            NAMES       : tuple[str] = open(PATHTOFILE,"r", encoding = "utf-8").read().split("\n")
        except FileNotFoundError:
            print("File not found. Is the path correct?")
            sys.exit(1)

        

        if len(cur.execute(f"SELECT * FROM DIM_NamingThemeTypes WHERE ThemeID = '{THEMEID}'").fetchall()) < 1:
            print("No NameTheme found with provided ThemeID")
            sys.exit(0)
        else:
            THEMENAME   : str = cur.execute(f"SELECT Description FROM DIM_NaminThemeTypes WHERE ThemeID = '{THEMEID}'").fetchone()
            for NAME in NAMES:
                cur.execute(f"INSERT INTO DIM_NamingTheme VALUES ('{THEMEID}', '{NAME}')")
            
            print("You are about to insert")
            for NAME in NAMES:
                print(NAME + "\n")
            print(f"inside {THEMENAME}, are you sure?")
            print("[y/N]")

            if input().lower() != 'y':
                print("Aborting...")
                CONN.rollback()
                CONN.close()
                sys.exit(0)
            else:
                CONN.commit()
                CONN.close()
                print("Committed successfully.")
                sys.exit(0)
