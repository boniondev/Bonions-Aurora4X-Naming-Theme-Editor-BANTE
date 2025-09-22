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
        connection = sqlite3.connect(f"file:{path if path else "AuroraDB.db"}?mode=ro", uri = True)
        return connection
    except sqlite3.OperationalError:
        print(  "Could not open database. Is the path correct and UNIX styled?" +
                "Am I in the same folder as AuroraDB.db?")
        print("basnse will close now!")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="py[thon] bante.py",
        description="Bonion's Aurora4X Naming Theme Editor",
        epilog="Backup your DB before using this tool!",
    )
    mutualexcgroup = parser.add_mutually_exclusive_group(required = True)
    parser.add_argument(
        "-p", "--path",
        help =  "UNIX style absolute or relative path to Aurora.db " +
                "(Looks inside current directory if unspecified)",
        required = False
    )
    mutualexcgroup.add_argument(
        "-l", "--list", help = "List all naming theme", action ="store_true", dest = "list"
    )
    mutualexcgroup.add_argument(
        "-ln", "--list-names",
        help = "List all names from a given ThemeID",
        action = "store", dest = "themeid", type = int
    )
    mutualexcgroup.add_argument(
        "-dn", "--delete-name",
        help = "Delete name(s) from a given name theme." \
                " Insert the ThemeID, and then the rows you wish to delete, separated by spaces",
        action = "store", nargs = "+", metavar = ("THEMEID", "DELETIONS"), dest = "deletions"
    )

    args = parser.parse_args()
    if args.list:
        conn = connect_ro(args.path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM DIM_NamingThemeTypes")
        rows = cur.fetchall()
        print("ThemeID | Description")
        print("---------------------")
        for row in rows:
            print(f"{row[0]} | {row[1]}")
        conn.close()
    elif args.themeid:
        conn = connect_ro(args.path)
        cur = conn.cursor()
        cur.execute(f"SELECT Name FROM DIM_NamingTheme WHERE NameThemeID == '{args.themeid}'")
        rows = cur.fetchall()
        num = 0
        for row in rows:
            print(f"{num}|{row[0]}")
            num = num + 1
        conn.close()
    elif args.deletions:
        if len(args.deletions) < 2:
            print("ThemeID was provided, but no rows to delete were given.")
            print("Deleting nothing!")
            sys.exit(0)
