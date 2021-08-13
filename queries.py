GET_BUILD_INFO = """
SELECT
    job_name,
    bld_id as job_id,
    build_status,
    build_exec_time,
    total_ut_test_case,
    filed_test_case
FROM buildstatus
WHERE month_name = "{month}" and week_no like "%{year}%"
"""
