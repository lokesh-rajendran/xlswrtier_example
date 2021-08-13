"""
MYSQL error code and custom error message configurations
"""
ERROR_CONFIG = {
    1452: {
        "sql_msg": "Cannot add or update a child row, a foreign key constraint fails",
        "internal_msg": "",
        "status_code": 500
    },
    1045: {
        "sql_msg": "Database connection failure, Access denied for a user."
                   "Invalid user/password",
        "status_code": 500
    },
    1049: {
        "sql_msg": "Unknown database",
        "status_code": 500
    },
    1062: {
        "sql_msg": "Duplicate entry",
        "status_code": 409
    },
    1064: {
        "sql_msg": "SQL syntax error",
        "status_code": 500
    },
    1146: {
        "sql_msg": "No database table model available to perform your action",
        "status_code": 500
    },
    1449: {
        "sql_msg": "Database user does not exists",
        "internal_msg": "",
        "status_code": 500
    },
    1451: {
        "sql_msg": "Cannot delete or update a parent row, a foreign key"
                   "constraint fails",
        "status_code": 500
    },
    2003: {
        "sql_msg": "Can't connect to MySQL server on, Invalid host/port",
        "status_code": 500
    },
    "generic": {
        "sql_msg": "Unexpected database error - Could not process the request",
        "internal_msg": "",
        "status_code": 500
    },
    "db_err": {
        "sql_msg": "Unexpected error - Could not connect to MySQL instance",
        "internal_msg": "",
        "status_code": 500
    }
}
