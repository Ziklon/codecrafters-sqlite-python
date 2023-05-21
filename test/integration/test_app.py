
# from pathlib import Path
#
# import pytest
#
# from app.main import main
#
# CWD = Path(__file__).parents[1]
#
# @pytest.mark.integration
# def test_db_info(capsys):
#     argv = ["", CWD / "../sample.db", ".dbinfo"]
#     main(argv)
#     assert capsys.readouterr().out.strip() == "number of tables: 3"
#
# @pytest.mark.integration
# def test_db_tables(capsys):
#     argv = ["", CWD / "../sample.db", ".tables"]
#     main(argv)
#     assert capsys.readouterr().out.strip() == "apples oranges"


#pytest = "7.3.1"