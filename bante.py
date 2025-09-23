''' Bonion's Aurora4X Naming Theme Editor
    This software is released under the MIT license. See LICENSE for details.
    Copyright (C) 2025 boniondev
'''
import argparse
import sqlite3
import sys


def connect_ro(path : str) -> sqlite3.Connection:
    '''
        Reusable instructions to connect to the database, READ-ONLY
    '''
    try:
        connection : sqlite3.Connection = sqlite3.connect(f"file:{path if path else "AuroraDB.db"}?mode=ro", uri = True)
        return connection
    except sqlite3.OperationalError:
        print(  "Could not open database. Is the path correct and UNIX styled?" +
                "Am I in the same folder as AuroraDB.db?")
        print("basnse will close now!")
        sys.exit(1)

if __name__ == "__main__":

    PARSER : argparse.ArgumentParser = argparse.ArgumentParser(
        prog = "py[thon] bante.py",
        description = "Bonion's Aurora4X Naming Theme Editor",
        epilog = "Backup your DB before using this tool!",
    )
    MUTUALEXCGROUP : argparse._MutuallyExclusiveGroup = PARSER.add_mutually_exclusive_group(required = True)
    PARSER.add_argument(
        "-p", "--path",
        help =  "UNIX style absolute or relative path to Aurora.db " +
                "(Looks inside current directory if unspecified)",
        required = False
    )
    MUTUALEXCGROUP.add_argument(
        "-l", "--list", help = "List all naming theme", action ="store_true", dest = "list"
    )
    MUTUALEXCGROUP.add_argument(
        "-ln", "--list-names",
        help = "List all names from a given ThemeID",
        action = "store", dest = "themeid", type = int
    )
    MUTUALEXCGROUP.add_argument(
        "-dn", "--delete-name",
        help = "Delete name(s) from a given name theme." \
                " Insert the ThemeID, and then the rows you wish to delete, separated by spaces",
        action = "store", nargs = "+", metavar = ("THEMEID", "DELETIONS"), dest = "deletions"
    )

    ARGS : argparse.Namespace= PARSER.parse_args()
    if ARGS.list:
        CONN : sqlite3.Connection   = connect_ro(ARGS.path)
        cur  : sqlite3.Cursor       = CONN.cursor()
        cur.execute("SELECT * FROM DIM_NamingThemeTypes")
        rows : list = cur.fetchall()
        print("ThemeID | Description")
        print("---------------------")
        for row in rows:
            print(f"{row[0]} | {row[1]}")
        CONN.close()

    elif ARGS.themeid:
        CONN : sqlite3.Connection   = connect_ro(ARGS.path)
        cur  : sqlite3.Cursor       = CONN.cursor()
        cur.execute(f"SELECT Name FROM DIM_NamingTheme WHERE NameThemeID == '{ARGS.themeid}'")
        rows = cur.fetchall()
        NUM = 0
        for row in rows:
            print(f"{NUM}|{row[0]}")
            NUM = NUM + 1
        CONN.close()

    elif ARGS.deletions:
        if len(ARGS.deletions) < 2:
            print("ThemeID was provided, but no rows to delete were given.")
            print("Deleting nothing!")
            sys.exit(0)
