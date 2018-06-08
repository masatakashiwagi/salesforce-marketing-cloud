#!/usr/bin/env pythonn
# -*- coding: utf-8 -*-

import sys
import csv
from FuelSDKWrapper import ET_API, ObjectType

params = {
    "clientid":"your client id",
    "clientsecret":"your client secret"
}

client = ET_API(params=params, debug=False)

para = ["Name", "CustomerKey", "ObjectID", "CreatedDate", "Description"]
response = client.get_objects(ObjectType.DATA_EXTENSION, property_list=para)
#info = client.get_info(ObjectType.DATA_EXTENSION)
#print info

"""
if response.code == 200:
    if response.more_results:
        for i in range(len(response.results)):
            print "{h1}番目:, Results:{h2}".format(h1=i, h2=response.results[i])
	    print "{h1}番目:, More_Results:{h2}".format(h1=i, h2=response.more_results[i])
    else:
        for j in range(len(response.results)):
	print "{h1}番目:, Results:{h2}".format(h1=j, h2=response.results[j])
else:
    print response.message
"""

def get_ckey(de_name):
    """Get a customer key from specified DataExtension.
       'de_name' is only English.
    """
    for de_num in range(len(response.results)):
        if response.results[de_num]["Name"] == de_name:
            ckey = response.results[de_num]["CustomerKey"]
            return ckey
        else:
            de_list = []
	    de_list.append(response.results[de_num]["Name"])
            if de_num == len(response.results)-1:
	        if de_name not in de_list:
		    raise Exception("de_name is not existence. Please run again!")
	    else:
		continue

#print get_ckey(de_name)

def get_column(key):
    """Get some columns from specified DataExtension based on a customer key.
    """
    response_column = client.get_data_extension_columns(customer_key=key)
    column = []
    for col_num in range(len(response_column.results)):
        column.append(response_column.results[col_num]["Name"])
    return column

#print get_column(key)

def get_row(key, column):
    """Get some records from specified DataExtension based on a customer key and some columns.
    """
    response_column = client.get_data_extension_columns(customer_key=key)
    response_row = client.get_data_extension_rows(customer_key=key, property_list=column)
    #print response_row.results
    records = []
    
    with open('output_test.csv', mode='a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(get_column(de_name))
        for i_prop in range(len(response_row.results)):
            if i_prop != 0:
                del records[:]
            for i_propsub in range(len(response_column.results)):
                fields = response_row.results[i_prop]["Properties"]["Property"][i_propsub]["Name"]
                values = response_row.results[i_prop]["Properties"]["Property"][i_propsub]["Value"]
		
		# Japanese characters are garbled, so I need to change the character codes.
                trans_fields = unicode(fields).encode('utf-8')
                trans_values = unicode(values).encode('utf-8')
                records.append(trans_values)
            writer.writerow(records)
        return records
    

if __name__ == '__main__':
    print "Please input a DataExtension Name."
    print "\---------------------------------"
    de_name = raw_input()
    for i in range(3):
        if not de_name:
            print "Please run a program again."
            print "\--------------------------"
	    de_name = raw_input()
	    if i == 2:
	        print "Quit the program."
	        sys.exit()
	    else:
		continue
        else:
            break
    key = get_ckey(de_name)
    column = get_column(key)
    get_row(key, column)
