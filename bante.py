''' Bonion's Aurora4X Naming Theme Editor
    This software is released under the MIT license. See LICENSE for details.
    Copyright (C) 2025 boniondev
'''
import argparse
import sqlite3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="py bante.py",
        description="Bonion's Aurora4X Naming Theme Editor",
        epilog="Backup your DB before using this tool!",
    )
    parser.add_argument(
        "-p", "--path",
        help =  "UNIX style absolute or relative path to Aurora.db " +
                "(Looks inside current directory if unspecified)",
        required = False
    )
    parser.add_argument(
        "-l", "--list", help = "List all naming theme", action ="store_true", dest = "list"
    )
    parser.add_argument(
        "-ln", "--list-names",
        help = "List all names from a given ThemeID",
        action = "store", dest = "themeid", type = int
    )
    args = parser.parse_args()
    if args.path:
        path = args.path
    if args.list:
        try:
            conn = sqlite3.connect(f"file:{path if path else "AuroraDB.db"}?mode=ro", uri = True)
        except sqlite3.OperationalError as e:
            print("Could not open database. Is the path correct and UNIX styled?")
            print("basnse will close now!")
            exit(1)
        cur = conn.cursor()
        cur.execute("SELECT * FROM DIM_NamingThemeTypes")
        rows = cur.fetchall()
        print("ThemeID | Description")
        print("---------------------")
        for row in rows:
            print(f"{row[0]} | {row[1]}")
        conn.close()
