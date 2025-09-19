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
        help = "UNIX style absolute path to Aurora.db " +
                "(Looks inside current directory if unspecified)",
        required = False
    )
    parser.add_argument(
        "-l", "--list", help = "List all naming theme", action ="store_true", dest = "list"
    )
    args = parser.parse_args()
    if args.list:
        conn = sqlite3.connect("file:AuroraDB.db?mode=rw", uri = True)
        cur = conn.cursor()
        cur.execute("SELECT * FROM DIM_NamingThemeTypes")
        rows = cur.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]}")
        conn.close()
