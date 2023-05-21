from app.command import  Command
from app.models.page_header import PageHeader
from app.parse_record import parse_record
from app.parse_varint import parse_varint


class DbInfo(Command):

    command_str = ".dbinfo"

    def _execute_impl(self):
        with open(self._database, "rb") as database_file:
            database_file.seek(16)

            page_size = int.from_bytes(database_file.read(2), byteorder="big")

            database_file.seek(100) # Skip the header section

            page_header = PageHeader.parse_from(database_file)
            database_file.seek(
                100 + 8
            ) # skip the database header & b-tree page header, get the cell pointer array
            cell_points = [
                int.from_bytes(database_file.read(2), "big")
                for _ in range(page_header.number_of_cells)
            ]
            sqlite_schema_rows = []
            for cell_pointer in cell_points:
                database_file.seek(cell_pointer)
                _number_of_bytes_in_payload = parse_varint(database_file)
                rowid = parse_varint(database_file)
                record = parse_record(database_file, 5)

                sqlite_schema_rows.append(
                    {
                        "type" : record[0],
                        "name" : record[1],
                        "tbl_name" : record[2],
                        "rootpage" : record[3],
                        "sql" : record[4]
                    }
                )
            #print(sqlite_schema_rows, page_header)
            print(f"database page size: {page_size}")
            #print(f"database page size: {page_size}")
            print(f"number of tables: {len(sqlite_schema_rows)}")


