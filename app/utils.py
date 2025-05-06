# #enforce and validate sql 
# # app/utils.py
# import sqlparse

# # Keywords we must forbid anywhere in the SQL
# FORBIDDEN = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"}

# def is_select_query(sql: str) -> bool:
#     # 1) Strip whitespace and leading semicolons
#     stmt = sql.strip().lstrip(";-")
#     # 2) Must begin with SELECT (case-insensitive)
#     if not stmt.upper().startswith("SELECT"):
#         return False
#     # 3) Tokenize and ensure no forbidden keywords appear
#     tokens = {tok.value.upper() for tok in sqlparse.parse(stmt)[0].tokens if tok.value}
#     if FORBIDDEN.intersection(tokens):
#         return False
#     return True

# def validate_syntax(sql: str) -> bool:
#     try:
#         parsed = sqlparse.parse(sql)
#         return bool(parsed)  # empty parse = invalid
#     except Exception:
#         return False


import sqlparse

# Keywords we must forbid anywhere in the SQL
FORBIDDEN = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"}

def is_select_query(sql: str) -> bool:
    """
    Return True only if every statement in `sql`:
      1) starts with SELECT,
      2) contains no forbidden keywords.
    """
    # 1) Clean up whitespace & leading semicolons
    cleaned = sql.strip().lstrip(";-")

    # 2) Parse into statements
    statements = [stmt for stmt in sqlparse.parse(cleaned) if stmt.tokens]
    if not statements:
        return False

    # 3) Validate each statement
    for stmt in statements:
        text = stmt.value.strip()
        # 3a) Must start with SELECT
        if not text.upper().startswith("SELECT"):
            return False
        # 3b) No forbidden keywords in its tokens
        tokens = {tok.value.upper() for tok in stmt.tokens if tok.value}
        if FORBIDDEN.intersection(tokens):
            return False

    return True

def validate_syntax(sql: str) -> bool:
    """
    Return True only if sqlparse can parse non‑empty statements from it.
    """
    try:
        statements = [stmt for stmt in sqlparse.parse(sql) if stmt.tokens]
        return bool(statements)
    except Exception:
        return False
