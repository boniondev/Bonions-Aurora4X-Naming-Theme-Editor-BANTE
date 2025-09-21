''' Bonion's Aurora4X Naming Theme Editor
    This software is released under the MIT license. See LICENSE for details.
    Copyright (C) 2025 boniondev
'''
import argparse
import sqlite3
import sys


def connect_ro(path) -> sqlite3.Connection:
    '''
        Reusable instructions to connect to the database, READ-ONLY
    '''
    try:
        connection = sqlite3.connect(f"file:{path if path else "AuroraDB.db"}?mode=ro", uri = True)
        return connection
    except sqlite3.OperationalError:
        print("Could not open database. Is the path correct and UNIX styled? Am I in the same folder as AuroraDB.db?")
        print("basnse will close now!")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="py bante.py",
        description="Bonion's Aurora4X Naming Theme Editor",
        epilog="Backup your DB before using this tool!",
    )
    mutualexcgroup = parser.add_mutually_exclusive_group()
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
