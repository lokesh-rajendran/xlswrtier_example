import xlsxwriter
import datetime
from queries import GET_BUILD_INFO
from db import DBConnection

db_connection = DBConnection()

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

data = {
    "EX_TRUNK_SOM": [
        [1, "SUCCESS", "01:13:12", 5, 4, 3],
        [2, "SUCCESS", "00:23:12", 5, 4, 3],
        [3, "FAILURE", "00:03:12", 5, 4, 3],
        [4, "ABORTED", "00:13:12", 5, 4, 3]],
    "EX_TRS_ME": [
        [11, "SUCCESS", "01:13:12", 5, 4, 3],
        [12, "SUCCESS", "00:23:12", 5, 4, 3],
        [13, "FAILURE", "00:03:12", 5, 4, 3],
        [14, "ABORTED", "00:13:12", 5, 4, 3]],
    "EX_MT": [[]]
}


def write_data_to_excel(data):
    # get Current Month
    current_month = months[datetime.datetime.now().month - 1]

    # create a excel document
    workbook = xlsxwriter.Workbook(f'Automation-{current_month}.xlsx')
    # time_format = workbook.add_format()
    # time_format.set_num_format(21)
    # adding background color to the rows
    header_format = workbook.add_format({
                            "bg_color": "#f1e740",
                            "border": 1,
                            "border_color": "#000000"})
    time_format = workbook.add_format({'num_format': "hh:mm:ss",
                                      "bg_color": "#f1e740",
                                       "border": 1,
                                       "border_color": "#000000",
                                       'align': 'right'})
    # Worksheet headers
    headers = [
        "BUILD_ID", "BUILD_STATUS", "DURATION",
        "PASSED_TESTCASE", "FAILED_TESTCASE", "TOTAL_TESTCASE"]

    # reports
    build_reports = {
        "Success": '=COUNTIF(B2:B655366,"SUCCESS")',
        "Failed": '=COUNTIF(B2:B655366,"FAILURE")',
        "Total": "=COUNT(A:A)",
        "Total Build Time": "=SUM(C2:C655366)",
        "Average Time": "=AVERAGE(C2:C655366)",
        "Average Test Case": "=AVERAGE(F2:F655366)",
        "Average Failure": "=AVERAGE(E2:E655366)",
        "Average Success": "=AVERAGE(D2:D655366)"
    }

    # Loop the dict and save in a worksheet
    for job_name, records in data.items():
        # create worksheet with the job name
        current_worksheet = workbook.add_worksheet(job_name)
        # insert headers
        for indx, value in enumerate(headers):
            current_worksheet.set_column(indx, indx, 12)
            current_worksheet.write(0, indx, value, header_format)
        # loop through each job name
        for row, record in enumerate(records):
            # Loop through all the job ids of the job
            for col, data in enumerate(record):
                if col == 2:
                    data = datetime.datetime.strptime(data, '%H:%M:%S')
                    print(data)
                    current_worksheet.write(row + 1, col, data, time_format)
                    continue
                # write to the workbook
                current_worksheet.write(row + 1, col, data)

        row = 1
        for property, formula in build_reports.items():
            col = len(headers) + 3
            current_worksheet.set_column(col, col, 18)
            current_worksheet.set_column(col + 1, col + 1, 18)
            current_worksheet.write(row, col, property, header_format)
            if property in ["Total Build Time", "Average Time"]:
                current_worksheet.write(row, col + 1, formula, time_format)
                row += 1
                continue
            current_worksheet.write(row, col + 1, formula, header_format)
            row += 1

    workbook.close()


def get_data_from_db():
    current_month = months[datetime.datetime.now().month - 1]
    current_year = datetime.datetime.now().year
    build_data = db_connection.run_query(GET_BUILD_INFO.format(
        month=current_month,
        year=current_year
    ), req_data=True)
    return_data = {}

    for record in build_data:
        if not return_data.get(record.get("job_name")):
            return_data[record.get("job_name")] = []

        return_data[record.get("job_name")].append([
            record.get("job_id"),
            record.get("build_status"),
            record.get("build_exec_time"),
            record.get("total_ut_test_case") - record.get("failed_test_case"),
            record.get("failed_test_case"),
            record.get("total_ut_test_case")
        ])

    return return_data


def main():
    build_data = get_data_from_db()
    write_data_to_excel(build_data)


main()
