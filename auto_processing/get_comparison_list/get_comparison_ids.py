import csv
import MySQLdb

def get_dict_school_id():
    id_dict = {}
    with open('id_comparison_list_mapping.csv', 'r') as f_dict:
        for row in csv.reader(f_dict, delimiter = ','):
            id_dict[row[2]] = row[0]
            
    print len(id_dict)
    return id_dict
    
def get_dict_school_compare():
    comparison_dict = {}
    with open('comparison_list.csv', 'r') as f_dict:
        for row in csv.reader(f_dict, delimiter = ','):
            comparison_dict[row[0]] = row[1].split('|')
    print len(comparison_dict)
    return comparison_dict

if __name__ == '__main__':
    # get id-id mapping for comparison list
    id_dict = get_dict_school_id() # google name: id
    comparison_dict = get_dict_school_compare() # id: google list
    id_id_dict = {}
    for key in comparison_dict:
        id_list = []
        for name in comparison_dict[key]:
            try:
                id_list.append(id_dict[name])
            except:
                pass
        id_id_dict[key] = id_list
        print key, id_list
    
    # import to db
    # create connection to 'mediawatch_lu'
    conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediaWatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
    x = conn.cursor()
    for key in id_id_dict:
        for id in id_id_dict[key]:
            x.execute('insert into schools_comparison_id values (%s, %s)', (key, id))
    conn.commit()
            
            