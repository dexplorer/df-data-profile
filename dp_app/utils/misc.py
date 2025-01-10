def check_if_any_list_item_in_str(items: list, text: str) -> bool:
    '''
    Check if any item in the list is in the given text string.
    '''
    return any(item in text for item in items) 

def dedupe_list_of_dict(records: list) -> list:
    '''
    Dedupe the list of dict items by converting the dict item to a string. Return the list of unique dict items. 
    '''
    deduped_items_dict = {str(item): item for item in records}
    print(deduped_items_dict)
    deduped_items = [item_val for item_val in deduped_items_dict.values()]
    return deduped_items 
