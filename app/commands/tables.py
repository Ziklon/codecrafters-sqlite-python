from app.command import Command
from app.models.page_header import PageHeader
from app.parse_record import parse_record
from app.parse_varint import parse_varint


class Tables(Command):
    command_str = ".tables"
    def _execute_impl(self):
        with open(self._database, "rb") as database_file:
            database_file.seek(100) #skip the header section
            page_header = PageHeader.parse_from(database_file)

            database_file.seek(
                100 + 8
            ) # Skip the database header & b-tree page header, get to the cell pointer array

            cell_pointers = [
                int.from_bytes(database_file.read(2), "big")
                for _ in range(page_header.number_of_cells)
            ]

            sqlite_schema_rows = []

            # each of those cells represents a row in the sqlite_schema table

            for cell_pointer in cell_pointers:
                database_file.seek(cell_pointer)
                _number_of_bytes_in_payload = parse_varint(database_file)
                rowid = parse_varint(database_file)
                record = parse_record(database_file, 5)

                sqlite_schema_rows.append(
                    {
                        "type": record[0],
                        "name": record[1],
                        "tbl_name": record[2],
                        "rootpage": record[3],
                        "sql": record[4]
                    }
                )

            rows_names = [row["name"].decode("utf-8") for row in sqlite_schema_rows]
            filter_interals = filter(
                lambda name: name
                not in {
                    "sqlite_sequence"
                },
                rows_names
            )
            print(" ".join(filter_interals))