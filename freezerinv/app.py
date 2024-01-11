from tinydb import TinyDB,Query
import json
import datetime
import os

import logging
import traceback

db = TinyDB('freezerinv\\frezeerdb.json', sort_keys=True, indent=4, separators=(',', ': '))
item = Query()
directory = 'freezerinv'
log_file_path = os.path.join(directory, 'dbOutput.log')
os.makedirs(directory, exist_ok=True)

    #TODO: Format dates and force format
    #TODO: toString for items
    #TODO: Look into proper documentation


def create_freezer(new_freezer: str):
    """
    new_freezer (str) - name of the new freezer(table) that you want to create
    """
    try:
        if(new_freezer not in db.tables()):
            freezer = db.table(new_freezer)
        elif (new_freezer in db.tables()):
            logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            logging.error(f"Freezer, "+ new_freezer +", was requested to be created. But a freezer with that name already exists. No change has been made.")
            logging.error(traceback.format_exc())

        
    except Exception as e:
        logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.error(f"An error occurred: {repr(e)}")
        logging.error(traceback.format_exc())


def insert(freezer: str, item_name: str, expire_date: str, insert_date: str, qty: int):
    """ 
    Insert an item into the database.

    freezer     (str) - the freezer you want to insert the item into\n
    id          (int) - id of item. based on insertion order\n
    item_name   (str) - name of item\n
    expire_date (str) - expiration date of item (format: MMDDYYYY)\n
    insert_date (str) - insertion date of item (format: MMDDYYYY)\n
    qty         (int) - quantity of item
    """

    try:
        freezer = db.table(freezer)
        if not freezer.all():
            id = 1
        else:#increasing id number on insertion
            all_items = freezer.all()
            last_item = all_items[-1]
            id = last_item.get("id") + 1

        if not freezer.search(Query().item_name == item_name): #creation
            freezer.insert({'freezer':freezer.name,'id':int(id),'item_name':str(item_name), 'expire_date':str(expire_date),'insert_date':str(insert_date), 'qty':int(qty)})
            logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            logging.info(f"An error occurred: {repr(e)}")

    except TypeError as e:
        logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.error(f"\nTypeError: Insertion was unsuccessful. Please ensure the typing is as specified: (str)item_name, (str)expire_date (format: MMDDYYYY), (str)insert_date (format: MMDDYYYY), (int)qty")
    except Exception as e:
        logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.error(f"An error occurred: {repr(e)}")
        logging.error(traceback.format_exc())
        


def delete(freezer: str, item_name: str):
    """
    Deletes the specified item from specified freezer. 
    
    Deletion is of two types: Subtraction and Complete deletion.\n
    If there is more than one in the qty then the function will subtract 1. If there is only one then it will delete the item completely.\n

    (str) freezer - freezer where the item is being deleted from\n
    (str) item_name - item that is attempting to be deleted\n
    """
    try:
            table = db.table(freezer)
            if table.search(item.item_name.exists(item_name)) and table.search(item.field_to_query('qty') == 1):
                #Checks existance of item and that the item only has 1 qty left before attempting to delete from table. 
                #Delete method will not return error if item does not exist, it will simply delete nothing. This is to let the user know that nothing was deleted
                table.update(delete(item_name))
            elif table.search(item.field_to_query('qty')) > 1:
                #If there are multiple items it will subtract 1 instead of deleting
                table.update(item.qty - 1)
            elif not table.search(item.item_name.exists(item_name)):
                #If the item does not exist it will log an error
                logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
                logging.error(f"Attempted deletion on item that does not exist.")
    except Exception as e:
        logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.error(f"An error occurred: {repr(e)}")
        logging.error(traceback.format_exc())


def update(freezer: str, item_name: str, update_opt: str, update_value):
    """
    Update a part of an item within a freezer.

    (str) freezer - freezer where the item is being updated\n
    (str) item_name - item that is attempting to be updated\n
    (str) update_opt - which part of the item you want to update ex: freezer, id, item_name, expire_date, insert_date, qty\n
    (str)(int) update_value - new value being inserted into the item\n
    """

    try:
        #item_to_update=None
        freezer_table = db.table(freezer)
        doc_id = freezer_table.search(Query().item_name == item_to_update['item_name'])[0].doc_id
        if update_opt == "freezer":
            if freezer.search(item.item_name.exists(item_name)):
                item_to_update = find_item(freezer,item_name)
                insert(update_value,item_to_update,item_to_update.get('expire_date'),item_to_update.get('insert_date'),item_to_update.get('qty'))
                delete(freezer,item_to_update)
        elif update_opt == "id":
            item_to_update = find_item(freezer,item_name)
            item_to_update['id'] = int(update_value)
            freezer_table.update(item_to_update)
        elif update_opt == "item_name":
            item_to_update = find_item(freezer,item_name)
            print(item_to_update['item_name'])
            item_to_update['item_name'] = str(update_value)
            freezer_table.update(item_to_update['item_name'], doc_ids=[doc_id])
            print(item_to_update['item_name'])
        elif update_opt == "expire_date":
            item_to_update = find_item(freezer,item_name)
            item_to_update['expire_date'] = str(update_value)
            freezer_table.update(item_to_update)
        elif update_opt == "insert_date":
            item_to_update = find_item(freezer,item_name)
            item_to_update['insert_date'] = str(update_value)
            freezer_table.update(item_to_update)
        elif update_opt == "qty":
            item_to_update = find_item(freezer,item_name)
            item_to_update['qty'] = int(update_value)
            freezer_table.update(item_to_update)
    except Exception as e:
        logging.basicConfig(filename='freezerinv\\dbOutput.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.error(f"An error occurred: {repr(e)}")
        logging.error(traceback.format_exc())

def find_item(freezer, item_name):
    print(db.tables())
    if freezer in db.tables():
        table = db.table(freezer)
        
        result = table.search(Query().item_name == item_name)

        if result:
            return result[0]  # Return the first matching item
        else:
            return None  # Item not found
    else:
        print(f"The table '{freezer}' does not exist.")
        return None

#create_freezer("freezer2")
#insert("freezer2","taco","08212025","03022023",1)
update("freezer1","taco","item_name","ribs")