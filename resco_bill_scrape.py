"""
This file scrapes all the data from a bill and formats it into
a timesheet as defined by a resco
"""

# imported from standard library
import calendar
import logging
import os
import pandas as pd
import xlrd

# imported from third party repos

# imported from local directories
from bill_templates import MyBill
import config as cfg
import my_functions as myfnc

# TODO: finish docstrings
# logging info
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # change to DEBUG when required
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler(cfg.log_files + '\\' + 'resco_bill_scrape.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

"""
These methods are a component of an excel data scrape tool which includes
a function spinner from the my_functions.py file. You will not they are numbered
to help identify in which order the dataframe requires the data.  All require four 
arguments as defined by the function spinner.
"""

def resco_0_mos(read_sheet, info_block, dummy2, dummy3):
    """"This function pulls the calendar month from a call block header on a bill.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param info_block: This is the first row of the call block.
    :type info_block: integer
    :param dummy2: Unused variable.
    :type first_infoblock_row: null
    :param dummy3: Unused variable.
    :type first_infoblock_row: null
    :return: The calendar number of a month.
    :rtype: integer
    """
    try:
        data = read_sheet.cell_value(info_block+1, 0)
        logger.info(f'the resco_0_mos has grabbed {data} to parse')
        shift_date_tuple = xlrd.xldate_as_tuple(data, 0)
        logger.info(f'the resco_0_mos has turned it into {shift_date_tuple}')
        month_num = f"{shift_date_tuple[1]}"
        logger.info(f'the month number is {month_num}')
        name_of_month = calendar.month_name[int(month_num)]
        logger.info(f'the month name is {name_of_month}')
        return name_of_month
    except:
        data = "No Date data available"
        return data


def resco_0b_mos(read_sheet, dummy1, dummy2, dummy3):
    """This function grabs the calendar month from the date in the header
    from the bill. This one is for the prep time and inventory items loops.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The calendar number of a month.
    :rtype: integer
    """
    try:
        data = read_sheet.cell_value(0, 10)
        logger.info(f'the resco_0b_mos has grabbed {data} to parse')
        shift_date_tuple = xlrd.xldate_as_tuple(data, 0)
        logger.info(f'the resco_0b_mos has turned it into {shift_date_tuple}')
        month_num = f"{shift_date_tuple[1]}"
        logger.info(f'the month number is {month_num}')
        name_of_month = calendar.month_name[int(month_num)]
        logger.info(f'the month name is {name_of_month}')
        return name_of_month
    except:
        data = "No Date data available"
        return data


def resco_1_date(read_sheet, info_block, dummy2, dummy3):
    """This function grabs the date in the header from the call block. This one
    is for the prep time and inventory items loops.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param info_block: This is the first row of the call block.
    :type info_block: integer
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The date as a string.
    :rtype: string
    """
    try:
        data = read_sheet.cell_value(info_block+1, 0)
        logger.info(f'the date_grabber has grabbed {data} to parse')
        shift_date_tuple = xlrd.xldate_as_tuple(data, 0)
        logger.info(f'the date_grabber has turned it into {shift_date_tuple}')
        day = f"{shift_date_tuple[2]}"
        month = f"{shift_date_tuple[1]}"
        year = f"{shift_date_tuple[0]}"
        shift_date = day + '/' + month + '/' + year
        return shift_date
    except:
        data = "No Date data available"
        return data


def resco_1b_date(read_sheet, dummy1, dummy2, dummy3):
    """This function grabs date from the header from the bill.
    This one is for the prep time and inventory items loops.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The date as a string.
    :rtype: string
    """
    try:
        data = read_sheet.cell_value(0, 10)
        logger.info(f'the date_grabber has grabbed {data} to parse')
        shift_date_tuple = xlrd.xldate_as_tuple(data, 0)
        logger.info(f'the date_grabber has turned it into {shift_date_tuple}')
        day = f"{shift_date_tuple[2]}"
        month = f"{shift_date_tuple[1]}"
        year = f"{shift_date_tuple[0]}"
        shift_date = day + '/' + month + '/' + year
        return shift_date
    except:
        data = "No Date data available"
        return data


def resco_2_in(read_sheet, info_block, dummy2, dummy3):
    """This function grabs the start time of the call from the header of the call block.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param info_block: This is the first row of the call block.
    :type info_block: integer
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The date as a string.
    :rtype: string
    """
    try:
        data = read_sheet.cell_value(info_block, 0)

        if "Strike" in data:  # a strike has no time data so just return "Strike"
            return data
        else:
            logger.info(f'the start_time has grabbed {data} to parse')
            data = read_sheet.cell_value(info_block, 0)
            data_in_list = data.split('-')  # split to separate off the out time
            junk_w_intime = data_in_list[0].split()  # split to separate off the in time
            # logger.info(f'the start_time has turned it into {just_time}')
            time_list = list(junk_w_intime[-1])
            # adding a colon to create a the database typed
            if len(time_list) == 3:  # if the time is prior to 1000 and no leading 0
                time_w_colon = ''.join(time_list[0]) + ":" + ''.join(time_list[1:3])
                return time_w_colon
            else:
                if time_list[0] == '0':  # if the time is prior to 1000 with a leading 0
                    time_w_colon = ''.join(time_list[1]) + ":" + ''.join(time_list[2:4])
                    return time_w_colon
                else: # if time is =>1000
                    time_w_colon = ''.join(time_list[0:2]) + ":" + ''.join(time_list[2:4])
                    return time_w_colon
    except:
        return "No time data recorded"


def resco_3_out(read_sheet, info_block, dummy2, dummy3):
    """This function grabs the end time of the call from the header of the call block.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param info_block: This is the first row of the call block.
    :type info_block: integer
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The date as a string.
    :rtype: string
    """
    try:
        data = read_sheet.cell_value(info_block, 0)
        if "Strike" in data: # a strike has no time data so just return "Strike"
            return data
        else:
            logger.info(f'the end_time has grabbed {data} to parse')
            junk_w_outtime = data.rsplit('-') # split to separate off the out time
            # logger.info(f'the end_time has turned it into {just_time}')
            time_list = list(junk_w_outtime[1])
            # adding a colon to create a the database typed
            if len(time_list) == 3:  # if the time is prior to 1000 and no leading 0
                time_w_colon = ''.join(time_list[0]) + ":" + ''.join(time_list[1:3])
                return time_w_colon
            else:
                if time_list[0] == '0':  # if the time is prior to 1000 with a leading 0
                    time_w_colon = ''.join(time_list[1]) + ":" + ''.join(time_list[2:4])
                    return time_w_colon
                else:
                    time_w_colon = ''.join(time_list[0:2]) + ":" + ''.join(time_list[2:4])
                    return time_w_colon
    except:
        return "No time data recorded"


def resco_4_payee(dummy, dummy1, dummy2, dummy3):
    """This function creates a string of 'Arts Commons' to
    fill into the dataframe's 'payee' column.

    :param dummy: Unused variable..
    :type dummy: null
    :param dummy1: Unused variable.
    :type dummy1: null
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: Returns 'Arts Commons'
    :rtype: string
    """
    data = "Arts Commons"
    return data


def resco_5_type(read_sheet, info_block, dummy2, dummy3):
    """This function grabs type of call (ie - Setup, Strike) from the header of the call block.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param info_block: This is the first row of the call block.
    :type info_block: integer
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The call type as a string.
    :rtype: string
    """
    data = read_sheet.cell_value(info_block, 0)
    logger.info(f'the grab_call_type has grabbed {data} to parse')
    call = data.rsplit(' ', 1) # Seperate the call info from the time of the calls
    logger.info(f'the grab_call_type has turned it into {call}')
    return call[0]


def resco_5b_type(dummy, dummy1, dummy2, dummy3):
    """This function creates a string of 'PREP TIME' to fill into
     the dataframe's 'payee' column for use in the prep time loop.

    :param dummy: Unused variable..
    :type dummy: null
    :param dummy1: Unused variable.
    :type dummy1: null
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: Returns 'Arts Commons'.
    :rtype: string
    """
    data = "PREP TIME"
    return data


def resco_6_resource(read_sheet, dummy1, row, col):
    """This function returns a string which aligns with the labour
    definitions as they appear on the Venue Ops bills.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param col: The data column that is being scraped.
    :type col: integer
    :return: The labour type as defined by Venue Ops as a string.
    :rtype: string
    """

    head_charge_out = read_sheet.cell_value(95,2)
    hand_charge_out = read_sheet.cell_value(96,2)

    data = read_sheet.cell_value(row, 0)
    charge_out = read_sheet.cell_value(row, col +1) # This is the payout value
    if charge_out == hand_charge_out:
        return "JSCH - Stage Hand"
    elif charge_out == hand_charge_out*1.5:
        return "JSCH - Stage Hand - OT"
    elif charge_out == hand_charge_out*2:
        return "JSCH - Stage Hand - DT"
    elif charge_out == head_charge_out:
        if 'CASUAL' in data:
            return "JSCH Stage Lead"
        else:
            return "JSCH Stage Head"
    elif charge_out == head_charge_out*1.5:
        if 'CASUAL' in data:
            return "JSCH Stage Lead - OT"
        else:
            return "JSCH Stage Head - OT"
    elif charge_out == head_charge_out*2:
        if 'CASUAL' in data:
            return "JSCH Stage Lead - DT"
        else:
            return "JSCH Stage Head - DT"


def resco_7_description(read_sheet, dummy1, row, dummy3):
    """This function returns a string which contains the crew member who worked the call.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The crew member who worked the call as a string.
    :rtype: string
    """
    data = read_sheet.cell_value(row, 0)
    return data


def resco_7b_description(dummy, dummy1, dummy2, dummy3):
    """This function creates a string of 'Meal Penalty' to fill into
    the dataframe's 'description' column for use in the MP loop.

    :param dummy: Unused variable..
    :type dummy: null
    :param dummy1: Unused variable.
    :type dummy1: null
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: Returns 'Arts Commons'
    :rtype: string
    """
    data = "Meal Penalty"
    return data


def resco_8_unitprice(read_sheet, dummy1, row, col):
    """This function returns an integer which aligns with the unit/hourly cost of the billing item.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param col: The data column that is being scraped.
    :type col: integer
    :return: The cost of the item.
    :rtype: integer
    """
    data = read_sheet.cell_value(row, col +1) # the +1 realigns it.
    return data

# 9, 10, 11 are null

def resco_11b_qty(read_sheet, dummy1, row, col):
    """This function returns an integer which aligns with the quantity associated
    with the billing item.  This is for the Meal Penalty loop only.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param col: The data column that is being scraped.
    :type col: integer
    :return: The number or quantity of the item.
    :rtype: integer
    """
    data = read_sheet.cell_value(row, col)
    return data


def resco_12_hrs(read_sheet, dummy1, row, col):
    """This function returns an integer which aligns with the number of hours worked associated with the call.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param col: The data column that is being scraped.
    :type col: integer
    :return: The number of hours worked in the call.
    :rtype: integer
    """
    data = read_sheet.cell_value(row, col)
    return data


def resco_13_subtotal(read_sheet, dummy1, row, col):
    """This function returns the subtotaled cost of the billing items. The number
    cost of the billable items in the line item as a subtotal.  The
    formula is unit hrs * rate.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param col: The data column that is being scraped.
    :type col: integer
    :return: The number cost of the billable items in the line item is unit hrs * rate.
    :rtype: integer
    """
    hrs_qty = read_sheet.cell_value(row, col)
    logger.info(f'hrs_qty = {hrs_qty}')
    rate_price = read_sheet.cell_value(row, col + 1)
    logger.info(f'rate_price = {rate_price}')
    return hrs_qty * rate_price

# 14 is NULL

def resco_15_total(read_sheet, dummy1,row, col):
    """This function returns the totaled cost of the billing items. The number
    cost of the billable items in the line item as a subtotal.  The
    formula is unit hrs * rate.  In the future, this will distinguish itself
    from the subtotal formula by the inclusion of applicable taxes.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param col: The data column that is being scraped.
    :type col: integer
    :return: The number cost of the billable items in the line item is unit hrs * rate.
    :rtype: integer
    """
    hrs_qty = read_sheet.cell_value(row, col)
    rate_price = read_sheet.cell_value(row, col +1)
    return hrs_qty*rate_price


def resco_16_title(read_sheet, dummy1, dummy2, dummy3):
    """This function grabs the event name from the header from the bill.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param dummy2: Unused variable.
    :type dummy2: null
    :param dummy3: Unused variable.
    :type dummy3: null
    :return: The date as a string.
    :rtype: string
    """
    data = read_sheet.cell_value(0, 0)
    return data


def resco_x_generic(read_sheet, dummy1, row, col):
    """Just grab it and return it.

    :param read_sheet: The active .xlsx sheet defined by xlrd.
    :type read_sheet: object
    :param dummy1: Unused variable.
    :type dummy1: null
    :param row: The data row that is being scraped.
    :type row: integer
    :param col: The data column that is being scraped.
    :type col: integer
    :return: The data variable.
    :rtype: integer/string
    """
    data = read_sheet.cell_value(row, col)
    return data

# insert a NULL value
resco_x_NULL = lambda dummy, dummy1, dummy2, dummy3:""


def main():
    # set up the column headers in lists to receive the scraped data
    col_headers = ['month', 'date', 'IN_time',
                   'OUT_time', 'Payee', 'Type',
                   'resource_name', 'description', 'unit_price',
                   'discount', 'adj_price', 'qty',
                   'unit_hrs', 'subtotal', 'gst',
                   'total', 'Title']

    # these are required for the row_scrapper
    dummy, dummy1, dummy2, dummy3 = 0, 0, 0, 0

    # these are the bill instances
    # version_name, check, prep_row, first_infoblock_row, first_data_block_row, mp_row)
    bill1 = MyBill('bill_1819_version6', "Meal Penalty", 95, 102, 104, 60)
    bill2 = MyBill('bill_1819_version5', "Long & McQuade Rental", 81, 88, 90, 43)
    bill3 = MyBill('bill_1718_version', "Parking", 76, 83, 85, 37)

    # Creating empty dataframes with column names only
    df_bill_data = pd.DataFrame(columns=col_headers)

    # create a list of the read_books this is a list of the files which
    # we will need to read so we need a list to iterate over
    read_list = os.listdir(cfg.cpo_bill_dir)
    print(f"We need to read approximately {len(read_list)} files")
    print("Are you ready to read? RETURN for yes, CTRL+C for no.")
    input()

    # here is the loop to iterate through the read_list
    for i in range(len(read_list)):
        print()
        print()
        print("------------------------------------------------------------------------------------------------")
        logger.debug("")
        logger.debug("------------------------------------------------------------------------------------------------")
        read_file = (cfg.cpo_bill_dir + '\\' + read_list[i])
        print(f'File number {i+1} of {len(read_list)}')
        print(read_file)
        read_book = xlrd.open_workbook(read_file) # TODO: fix this permission denied error with a try block
        read_sheet = read_book.sheet_by_name('Entry Form')

        # start with this, let's find a cel unique to each template and save the data.
        checker = read_sheet.cell_value(60,0)

        for bill_template in MyBill._registry:
            if bill_template.check == checker:
               print(f"this is the {bill_template.version_name} template")
               # the prep time grab
               # reg time
               logger.debug(f"Entering Prep Time Reg")
               r_row = bill_template.prep_row
               col = 1
               for i in range(2):
                   logger.debug(f"r_row Now = {r_row}")
                   units = read_sheet.cell_value(r_row, col)

                   if units !='' and units != 0:
                       prep_time_reg = myfnc.row_scrapper(read_sheet, dummy, r_row, col,
                                                          resco_0b_mos, resco_1b_date, resco_x_NULL,
                                                          resco_x_NULL, resco_4_payee, resco_5b_type,
                                                          resco_6_resource, resco_7_description, resco_8_unitprice,
                                                          resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                          resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                          resco_15_total, resco_16_title)

                       row_data_list = [cel for cel in prep_time_reg]
                       print(row_data_list)
                       my_dict = dict(zip(col_headers, row_data_list))
                       df_bill_data = df_bill_data.append(my_dict, ignore_index=True)
                       r_row += 1
                   else:
                       r_row += 1
               # this loop covers the first two ot rows, FULLTIME and CASUAL
               logger.debug(f"Entering Prep Time OT")
               r_row = bill_template.prep_row
               for i in range(2):
                    logger.debug(f"r_row Now = {r_row}")
                    col = 5 # this is the location of the ot time data
                    units = read_sheet.cell_value(r_row, col)
                    if units !='' and units != 0:
                        prep_time_ot = myfnc.row_scrapper(read_sheet, dummy, r_row, col,
                                                          resco_0b_mos, resco_1b_date, resco_x_NULL,
                                                          resco_x_NULL, resco_4_payee, resco_5b_type,
                                                          resco_6_resource, resco_7_description, resco_8_unitprice,
                                                          resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                          resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                          resco_15_total,resco_16_title)

                        row_data_list = [cel for cel in prep_time_ot]
                        print(row_data_list)
                        my_dict = dict(zip(col_headers, row_data_list))
                        df_bill_data = df_bill_data.append(my_dict, ignore_index=True)
                        r_row += 1
                    else:
                        r_row += 1

               # this loop covers the first two dt rows, FULLTIME and CASUAL
               logger.debug(f"Entering Prep Time DT")
               r_row = bill_template.prep_row
               for i in range(2):
                    logger.debug(f"r_row Now = {r_row}")
                    col = 9 # this is the location of the dt time data
                    units = read_sheet.cell_value(r_row, col)
                    if units !='' and units != 0:
                        prep_time_dt = myfnc.row_scrapper(read_sheet, dummy, r_row, col,
                                                          resco_0b_mos, resco_1b_date, resco_x_NULL,
                                                          resco_x_NULL, resco_4_payee, resco_5b_type,
                                                          resco_6_resource, resco_7_description, resco_8_unitprice,
                                                          resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                          resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                          resco_15_total,resco_16_title)

                        row_data_list = [cel for cel in prep_time_dt]
                        print(row_data_list)
                        my_dict = dict(zip(col_headers, row_data_list))
                        df_bill_data = df_bill_data.append(my_dict, ignore_index=True)
                        r_row += 1
                    else:
                        r_row += 1

               # MP
               logger.debug(f"Entering MP")
               r_row = bill_template.mp_row

               if bill_template.version_name == "bill_1819_version6":
                   col =2
               else:
                   col = 1

               # this list of arguments is for the row_scrapper function
               units = read_sheet.cell_value(r_row, col)
               if units !='' and units != 0:
                    mp = myfnc.row_scrapper(read_sheet, dummy, r_row, col,
                                            resco_0b_mos, resco_1b_date, resco_x_NULL,
                                            resco_x_NULL, resco_4_payee, resco_x_NULL,
                                            resco_6_resource, resco_7b_description, resco_8_unitprice,
                                            resco_x_NULL, resco_x_NULL, resco_11b_qty,
                                            resco_x_NULL, resco_13_subtotal, resco_x_NULL,
                                            resco_15_total,resco_16_title)

                    row_data_list = [cel for cel in mp]
                    print(row_data_list)
                    my_dict = dict(zip(col_headers, row_data_list))
                    df_bill_data = df_bill_data.append(my_dict, ignore_index=True)

               # Now we come to the call blocks.
               #
               # first block starts at A103, last block starts at A1192
               # blocks are 33 rows wide, useful data is 22 rows wide

               start_r_row = bill_template.first_data_block_row
               # print(f'start row is {bill_template.first_data_block_row}')
               info_block = bill_template.first_infoblock_row # this is where the data and call info are

               # this is the loop over the differnt call blocks
               for call_loop in range(33):
                    logger.debug(f"r_row Now = {r_row}")
                    r_row = start_r_row + info_block - bill_template.first_infoblock_row
                    # this is the check for running out of calls
                    if read_sheet.cell_value(info_block, 0) == 'CALL':
                        break
                    else:
                        # this is a loop over the rows within a call block
                        # reg time
                        logger.debug(f"Entering callblock Reg")
                        for crew_loop in range(18):
                            col = 1
                            units = read_sheet.cell_value(r_row, col)
                            if units !='' and units != 0:
                                call_time_reg = myfnc.row_scrapper(read_sheet, info_block, r_row, col,
                                                                   resco_0_mos, resco_1_date, resco_2_in,
                                                                   resco_3_out, resco_4_payee, resco_5_type,
                                                                   resco_6_resource, resco_7_description, resco_8_unitprice,
                                                                   resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                                   resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                                   resco_15_total,resco_16_title)

                                row_data_list = [cel for cel in call_time_reg]
                                print(row_data_list)
                                my_dict = dict(zip(col_headers, row_data_list))
                                df_bill_data = df_bill_data.append(my_dict, ignore_index=True)
                                r_row += 1
                            else:
                                r_row += 1
                        # ot
                        logger.debug(f"Entering callblock OT")
                        r_row = start_r_row + info_block - bill_template.first_infoblock_row
                        for i in range(18):
                            logger.debug(f"r_row Now = {r_row}")
                            col = 5
                            units = read_sheet.cell_value(r_row, col)
                            if units !='' and units != 0:
                                call_time_ot = myfnc.row_scrapper(read_sheet, info_block, r_row, col,
                                                                  resco_0_mos, resco_1_date, resco_2_in,
                                                                  resco_3_out, resco_4_payee, resco_5_type,
                                                                  resco_6_resource, resco_7_description, resco_8_unitprice,
                                                                  resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                                  resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                                  resco_15_total,resco_16_title)

                                row_data_list = [cel for cel in call_time_ot]
                                print(row_data_list)
                                my_dict = dict(zip(col_headers, row_data_list))
                                df_bill_data = df_bill_data.append(my_dict, ignore_index=True)
                                r_row += 1
                            else:
                                r_row += 1
                        # dt
                        logger.debug(f"Entering callblock DT")
                        r_row = start_r_row + info_block - bill_template.first_infoblock_row
                        for i in range(18):
                            logger.debug(f"r_row Now = {r_row}")
                            col = 9
                            units = read_sheet.cell_value(r_row, col)
                            if units !='' and units != 0:
                                call_time_dt = myfnc.row_scrapper(read_sheet, info_block, r_row, col,
                                                                  resco_0_mos, resco_1_date, resco_2_IN,
                                                                  resco_3_OUT, resco_4_payee, resco_5_type,
                                                                  resco_6_resource, resco_7_description, resco_8_unitprice,
                                                                  resco_x_NULL, resco_x_NULL, resco_x_NULL,
                                                                  resco_12_hrs, resco_13_subtotal, resco_x_NULL,
                                                                  resco_15_total,resco_16_title)

                                row_data_list = [cel for cel in call_time_dt]
                                print(row_data_list)
                                my_dict = dict(zip(col_headers, row_data_list))
                                df_bill_data = df_bill_data.append(my_dict, ignore_index=True)
                                r_row += 1
                            else:
                                r_row += 1

                    info_block+=33

               print("-----------------------------------------------------------------------------------")
    else:
        print()
        print("We are done")

    print()
    print("All done! Time to save to...")
    print(f"{cfg.desktop_dir}\cpo_bills_records.xls")
    try:
        df_bill_data.to_excel(f'{cfg.desktop_dir}\cpo_bills_records.xlsx', index=False)
    except:
        print()
        print("Uh oh.........")
        print("The cpo_bills_records.xslx is blocked.  Do you have it open?")
        print("I'll just wait while you close it...")
        input()
        df_bill_data.to_excel(f'{cfg.desktop_dir}\cpo_bills_records.xlsx', index=False)
        print()
        print("That did it.  Closing everything up")


if __name__ == '__main__':
    logger.info('~~~~The fiile resco_bill_scrape.py has started~~~~')
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                resco_bill_scraper launched")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    main()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                          VICTORY!")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    logger.info('~~~~The fiile resco_bill_scrape.py has finished OK~~~~')
