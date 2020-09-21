"""
This file contains the main function for the timesheet scrapper
is for taking collected timesheets, scrapping them, and placing that data
into the production database
"""

# imported from standard library
import os
import pandas as pd
import sqlalchemy as sa
import xlrd

# imported from third party repos

# imported from local directories
import config as cfg
import databaseFunctions as dbfnc
import kris_fix as kf  # added when kris broke the scrapper
import myClasses as myCls
from myClasses import searchDict
from timesheet import TS2015
from timesheet import TS2011
from timesheet import TSCasual

def main():
    # set up the column headers
    crew_keys = ["Shift", "CrewIDLetter", "CrewIDNumber",
                 "Date", "InTime", "OutTime",
                 "EventYrID", "EventID", "Reg",
                 "OT", "Double", "Acct",
                 "Blackscall", "MP", "ShiftType"]
    head_keys = ["Shift", "HeadIDLetter", "HeadIDNumber",
                 "Date", "InTime", "OutTime",
                 "EventYrID", "EventID", "Reg",
                 "OT", "Double", "Acct",
                 "Blackscall", "MP"]

    # # Creating empty dataframes with column names only
    df_head = pd.DataFrame(columns=head_keys)
    df_crew = pd.DataFrame(columns=crew_keys)

    # find the max number in the Shift number lists
    # this info is pulled directly from the db
    query = "SELECT * FROM HeadShiftWorkedTable"
    df_h_shift = pd.read_sql(query, cfg.conn)
    head_record = df_h_shift['HeadShiftWorkedID'].max()
    next_head_num = head_record + 1

    query = "SELECT * FROM CrewShiftWorkedTable"
    df_c_shift = pd.read_sql(query, cfg.conn)
    crew_record = df_c_shift['ShiftWorkedID'].max()
    next_crew_num = crew_record + 1

    # create a list of the read_books
    read_list = os.listdir(cfg.dir)
    print(f"We need to read approximately {len(read_list)} files")
    print("Are you ready to read? RETURN for yes, CTRL+C for no.")
    input()

    # a loop to iterate through the read_list
    i = 0  # where in the list are we?
    for i in range(len(read_list)):
        read_file = (cfg.dir + '\\' + read_list[i])
        print(read_file)
        read_book = xlrd.open_workbook(read_file)
        read_sheet = read_book.sheet_by_index(0)

        # is this actually a timesheet? And which one is it?
        # define timesheets - version, name_row, name_column, start_data_row,
        # start_data_col, spaces_per_day
        if read_sheet.cell_value(7, 0) == 'SUNDAY':
            print("This timesheet was designed in 2011. Begin data scrape")
            ts11 = TS2011('ts11', 3, 1, 7, 1, 55, 7)
            r_row = ts11.start_data_row

            print("This 2011 loop was deleted during the python2 to python3 upgrade")
            print("You'll probably want to re-write this 2011 loop someday")
            # TODO :write the 2011 loop

        elif read_sheet.cell_value(14, 0) == 'SUNDAY':
            print("This timesheet belongs to a casual. Begin data scrape")
            ts_cas = TSCasual('ts_cas', 9, 1, 14, 1, 55, 6)
            r_row = ts_cas.start_data_row

            # A loop to iterate through the time slots one at a time
            for r_row in range(ts_cas.start_data_row, ts_cas.end_data_row):
                r_col = ts_cas.start_data_col + 1
                if read_sheet.cell_type(r_row, r_col) != 0:
                    print("writing data")

                    # House keeping...
                    # create an empty list to store the data
                    crew_data_list = []

                    # write shift number
                    crew_data_list.append(next_crew_num)
                    next_crew_num += 1

                    # Grab a casual Alpha number from the db
                    data = read_sheet.cell_value(ts_cas.name_row, ts_cas.name_column)
                    cas_alpha_id = dbfnc.find_crew_Alpha_number(data)
                    print(cas_alpha_id)
                    crew_data_list.append(cas_alpha_id)

                    # Grab a casual id number from the db
                    data = read_sheet.cell_value(ts_cas.name_row, ts_cas.name_column)
                    cas_id = dbfnc.find_crew_number(data)
                    print(cas_id)
                    crew_data_list.append(cas_id)

                    # Grab ts date
                    data = ts_cas.ts_grab_date(read_sheet, r_row)
                    print(data)
                    crew_data_list.append(data)

                    # Grab in time
                    data = ts_cas.ts_write_time(read_sheet, r_row, 0)
                    print(data)
                    crew_data_list.append(data)

                    # Grab out time
                    data = ts_cas.ts_write_time(read_sheet, r_row, 1)
                    print(data)
                    crew_data_list.append(data)

                    # Grab event year
                    data = ts_cas.ts_grab_date(read_sheet, r_row)
                    #print(data + " prepped date")
                    evnt_yr = dbfnc.grabeventYR2(data)
                    crew_data_list.append(evnt_yr)

                    # Grab Event ID
                    data = ts_cas.ts_grab_date(read_sheet, r_row)
                    show = ts_cas.ts_cas_write_show_num(data)
                    crew_data_list.append(show)

                    # grab reg time, ot, dt
                    data = ts_cas.ts_grab_hrs(read_sheet, r_row, 2)
                    crew_data_list.append(data)

                    data = ts_cas.ts_grab_hrs(read_sheet, r_row, 3)
                    crew_data_list.append(data)

                    data = ts_cas.ts_grab_hrs(read_sheet, r_row, 4)
                    crew_data_list.append(data)

                    # write accounting code
                    data = ts_cas.ts_cas_write_acct()
                    crew_data_list.append(data)

                    # blackscall true/false
                    data = ts_cas.ts_blacks_call(read_sheet, r_row, 5)
                    crew_data_list.append(data)

                    # Grab MP
                    data = ts_cas.ts_mp(read_sheet, r_row, 6)
                    crew_data_list.append(data)

                    # Grab Shiftype
                    data = ts_cas.ts_cas_write_shift_type()
                    crew_data_list.append(data)

                    print(crew_data_list)

                    # add this row to the df
                    print("adding to crew df")
                    my_dict = dict(zip(crew_keys, crew_data_list))
                    df_crew = df_crew.append(my_dict, ignore_index=True)

                else:
                    print("no data in cel B" + str((r_row) + 1))  # move on to the next time slot
                    # TODO: what is this pycharm error above?

        elif read_sheet.cell_value(19, 0) == 'SUNDAY':
            print("This timesheet was designed in 2015. Begin data scrape")
            ts15 = TS2015('ts15', 15, 2, 19, 2, 69, 7)
            r_row = ts15.start_data_row

            # A loop to iterate through the time slots one at a time
            for r_row in range(ts15.start_data_row, ts15.end_data_row):
                # Find the first slot with data
                r_col = ts15.start_data_col
                if read_sheet.cell_type(r_row, r_col) != 0:
                    print("writing data")

                    # House keeping...
                    # create an empty list to store the data and increment the shift number
                    head_data_list = []

                    # write shift number
                    head_data_list.append(next_crew_num)
                    next_head_num += 1

                    # Grab a casual Alpha number from the db
                    # data = read_sheet.cell_value(ts15.name_row, ts15.name_column)
                    head_alpha_id = ts15.ts_15_grab_head_id_alpha()
                    head_data_list.append(head_alpha_id)

                    # Grab a head id number from the db
                    data = read_sheet.cell_value(ts15.name_row, ts15.name_column)
                    head_id = dbfnc.find_head_number(data)
                    #print(head_id)
                    head_data_list.append(head_id)

                    # Grab ts date
                    data = ts15.ts_grab_date(read_sheet, r_row)
                    print(data)
                    head_data_list.append(data)

                    # Grab in time w the kris fix
                    if head_id == 3:
                        r_col = ts15.start_data_col
                        data = ts15.kf_format(read_sheet,r_row,r_col)
                        print(data)
                        head_data_list.append(data)
                    else:
                        r_col = ts15.start_data_col
                        data = ts15.ts_write_time(read_sheet, r_row, r_col)
                        print(data)
                        head_data_list.append(data)

                    # Grab out time w the kris fix
                    if head_id == 3:
                        r_col = ts15.start_data_col + 1
                        data = ts15.kf_format(read_sheet,r_row,r_col)
                        print(data)
                        head_data_list.append(data)
                    else:
                        r_col = ts15.start_data_col + 1
                        data = ts15.ts_write_time(read_sheet, r_row, r_col)
                        print(data)
                        head_data_list.append(data)

                    # Grab event year
                    data = ts15.ts_grab_date(read_sheet, r_row)
                    evnt_yr = dbfnc.grabeventYR2(data)
                    head_data_list.append(evnt_yr)

                    # Grab Event ID
                    # this needs to pick up the acct num,
                    # but don't post to list yet
                    r_col = ts15.start_data_col + 6
                    head_acct = ts15.ts_15_write_acct(read_sheet, r_row, r_col)

                    data = ts15.ts_15_eventid(head_acct)
                    head_data_list.append(data)

                    # grab reg time, ot, dt
                    r_col = ts15.start_data_col + 2
                    data = ts15.ts_grab_hrs(read_sheet, r_row, r_col)
                    head_data_list.append(data)

                    r_col = r_col + 1
                    data = ts15.ts_grab_hrs(read_sheet, r_row, r_col)
                    head_data_list.append(data)

                    r_col = r_col + 1
                    data = ts15.ts_grab_hrs(read_sheet, r_row, r_col)
                    head_data_list.append(data)

                    # write accounting code
                    head_data_list.append(head_acct)

                    # showcall true/false
                    r_col = ts_cas.start_data_col+5
                    data = ts_cas.ts_blacks_call(read_sheet, r_row, r_col)
                    head_data_list.append(data)

                    # Grab MP
                    r_col = ts_cas.start_data_col+6
                    data = ts_cas.ts_mp(read_sheet, r_row, r_col)
                    head_data_list.append(data)

                    print(head_data_list)

                    # add this row to the df
                    print("adding to head df")
                    my_dict = dict(zip(head_keys, head_data_list))
                    df_head= df_head.append(my_dict, ignore_index=True)

                else:
                    print("no data in cel E" + str((r_row) + 1))  # move on to the next time slot

    else:
        print("this is NOT a timesheet")
    print()

    # send the df to the db
    tbl = 'TMPtblWeeklyHeadsData'
    tbl_exist = dbfnc.checkTableExists(cfg.conn, tbl)

    if tbl_exist:
        print("let's empty Heads the table")
        cur = cfg.conn.cursor()
        # cur.execute("TRUNCATE Table TMPtblWeeklyHeadsData")
        cur.execute("DROP Table TMPtblWeeklyHeadsData")
        cfg.conn.commit()

    else:
        print("let's build the Head table")
        # with engine.connect() as con:
        #     con.execute('ALTER TABLE TMPtblWeeklyHeadsData ADD PRIMARY KEY (Shift);')
        print("OOPS! IF YOU ARE READING THIS WE HAVE A PROBLEM!")
        print("NEXT COMES THE ERROR MESSAGE!")

    print("Table path cleared, let's write to the db")
    engine = sa.create_engine(cfg.alc_str)
    df_head.to_sql(tbl,
                  con=engine,
                  if_exists='append',
                  index=False,
                  dtype={'Shift': sa.types.INT,
                         'HeadIDLetter': sa.types.NVARCHAR(length=255),
                         'HeadIDNumber': sa.types.INT,  # notice this is an INT
                         'Date': sa.dialects.mssql.DATETIME2(0),
                         'InTime': sa.dialects.mssql.DATETIME2(0),
                         'OutTime': sa.dialects.mssql.DATETIME2(0),
                         'EventYrID': sa.types.NVARCHAR(length=255),
                         'EventID': sa.types.NVARCHAR(length=255),
                         'Reg': sa.types.FLOAT,
                         'OT': sa.types.FLOAT,
                         'Double': sa.types.FLOAT,
                         'Acct': sa.types.NVARCHAR(length=255),
                         'Blackscall': sa.dialects.mssql.BIT,
                         'MP': sa.dialects.mssql.BIT}
                  )
    print()

    # send the df to the db
    tbl = 'TMPtblWeeklyCrewData'
    tbl_exist = dbfnc.checkTableExists(cfg.conn, tbl)

    if tbl_exist:
        print("let's empty the Crew table")
        cur = cfg.conn.cursor()
        # cur.execute("TRUNCATE Table TMPtblWeeklyCrewData")
        cur.execute("DROP Table TMPtblWeeklyCrewData")
        cfg.conn.commit()

    else:
        print("let's build the Crew table")
        print("OOPS! IF YOU ARE READING THIS WE HAVE A PROBLEM!")
        print("NEXT COMES THE ERROR MESSAGE!")

    print("Table path cleared, let's write to the db")
    engine = sa.create_engine(cfg.alc_str)
    df_crew.to_sql(tbl,
                  con=engine,
                  if_exists='append',
                  index=False,
                  dtype={'Shift': sa.types.INT,
                         'CrewIDLetter': sa.types.NVARCHAR(length=255),
                         'CrewIDNumber': sa.types.NVARCHAR(length=255),  # notice this is a CHAR
                         'Date': sa.dialects.mssql.DATETIME2(0),
                         'InTime': sa.dialects.mssql.DATETIME2(0),
                         'OutTime': sa.dialects.mssql.DATETIME2(0),
                         'EventYrID': sa.types.NVARCHAR(length=255),
                         'EventID': sa.types.NVARCHAR(length=255),
                         'Reg': sa.types.FLOAT,
                         'OT': sa.types.FLOAT,
                         'Double': sa.types.FLOAT,
                         'Acct': sa.types.NVARCHAR(length=255),
                         'Blackscall': sa.dialects.mssql.BIT,
                         'MP': sa.dialects.mssql.BIT,
                         'ShiftType': sa.types.INT}
                  )
    print()

    cfg.conn.close()

    print("All done! Time to save to bailout")
    print()


if __name__ == '__main__':
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("         timesheetscrapper_python3.py file launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                        VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
