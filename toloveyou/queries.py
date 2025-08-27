
from toloveyou import *

@with_cursor
def all_entries(cursor=None):
    cursor.execute('''
        SELECT DISTINCT entry
        FROM toloveyou 
    ''',) 

    return [entry[0] for entry in cursor.fetchall()]

@with_cursor
def outstanding(cursor=None):
    timestamp = get_next_start_of_day().timestamp() 
    
    cursor.execute('''
        SELECT entry
        FROM toloveyou 
        WHERE attribute = 'due'
        AND CAST(value AS INTEGER) <= ?
    ''', (timestamp,)) # TODO sort by priority here

    return [entry[0] for entry in cursor.fetchall()]

@with_cursor
def outstanding_priority_sort(cursor=None): # TODO TEST
    timestamp = get_next_start_of_day().timestamp() 

    cursor.execute('''
        SELECT due.entry
        FROM toloveyou AS due
        JOIN toloveyou AS prio
          ON due.entry = prio.entry
        WHERE due.attribute = 'due'
          AND CAST(due.value AS INTEGER) <= ?
          AND prio.attribute = 'priority'
        ORDER BY CAST(prio.value AS INTEGER) ASC
    ''', (timestamp,))

    return [entry[0] for entry in cursor.fetchall()]

@with_cursor
def outstanding_fsrs_priority_sort(cursor=None): # TODO TEST
    timestamp = get_next_start_of_day().timestamp() 

    cursor.execute('''
        SELECT e.entry
        FROM (
            SELECT entry FROM toloveyou WHERE attribute = 'due' AND CAST(value AS INTEGER) <= ?
            INTERSECT
            SELECT entry FROM toloveyou WHERE attribute = 'scheduler' AND value = '"fsrs"'
        ) AS entries
        JOIN toloveyou e ON entries.entry = e.entry
        WHERE e.attribute = 'priority'
        ORDER BY CAST(e.value AS INTEGER) ASC
    ''', (timestamp,))

    return [entry[0] for entry in cursor.fetchall()]
