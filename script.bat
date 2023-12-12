call .venv\Scripts\Activate.bat
python flow_lexer.py "examples/table.txt"
python flow_lexer.py "examples/merge.txt"

deactivate