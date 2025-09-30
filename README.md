# Bonion's Aurora4X Naming Theme Editor (BANTE)
> [!CAUTION]
> This software makes heavy use of SQL queries in a way that would be unsafe in any other circumstance. If in the future you find yourself in a setting where ANYONE other than you accesses the database, DO NOT replicate this code.<br>
> Using SQL statements like this leaves you open to [SQL Injection](https://en.wikipedia.org/wiki/SQL_injection). Use [Prepared Statements](https://en.wikipedia.org/wiki/Prepared_statement) instead.

## **What is this?**<br>
This software is a tool that can be used on Aurora4X's database to add, remove, or edit Name Theme(s), which is not possible in-game (Only making Name Themes is supported in-game, and Naming Themes cannot be edited once created), and normally requires one to have an SQLite Browser, and knowledge of SQL.

## **Current Features:**
- See Naming Themes
- See Names of Naming Themes
- Delete Names inside Naming Themes
- Delete Naming Themes
- Add Names to Naming Themes
- Create Naming Themes

## **Planned Features:**<br>
- GUI (Maybe, eventually, possibly)

## **How do I use this?**<br>
**While this software doesn't generally fail (or it gracefully does so if it does) it is recommended to backup your db before making modifications.**<br>
Every operation that writes to the db will ask for confirmation, along with showing the actions that are about to be taken. **Once confirmation is given, the changes cannot be undone.** <br>
Use `python bante.py [commands]`, or `py bante.py [commands]` if you are on Windows.<br><br>
Use of this software while the game is open is **not** recommended. Save and close Aurora, and reopen it again after you have made your modifications.
The commands are as follows, and all of them are mutually exclusive unless specified otherwise:
- Use `-h` or `--help` to see the help page.
- Use `-p` or `--path` along a UNIX styled relative or absolute `PATH` to the db you wish to edit. This flag may be used alongside any other that reads or writes into the db. If not supplied, it will always look for an `AuroraDB.db` in the same folder it's placed in.
- Use `-l` or `--list` to list all the naming themes inside the db.
- Use `-ln` or `--list-names`to list Names belonging to a Naming Theme. A numeric `THEMEID` must be supplied.
- Use `-dn` or `--delete-name` to delete Names from a Naming Theme. A numeric `THEMEID` must be given as the first argument, and an unlimited number of numeric `DELETIONS` may be supplied. `DELETIONS` are the row numbers next to the names printed by using the `-ln` command.
- Use `-dt` or `--delete-theme` to delete one or multiple Naming Themes, and optionally delete or keep the Names assigned to them. A `y`or `n` must be supplied as the first argument, and an unlimited amount of `THEMEID`s may be supplied.<br>If `y` is supplied, **ALL** of the names associated with the provided `THEMEID`s will be deleted.
- Use `-an` or `--add-names` to add any number of Names to a single Naming Theme. The `PATH` to a text file containing names separated by newlines must be provided as the first argument, followed by the `THEMEID` of the Naming Theme to add them to.
- Use `at` or `--add-theme` to add any number of Names to a *new* Naming Theme. The `PATH` to a text file containing names separated by newlines must be provided as the first argument, followed by the `NAME` of the Naming Theme to you wish to create.

## **What do I need to use this?**<br>
This project was written using Python 3.13, but *should* run with versions as old as 3.10. Anyhing under that will not work.
