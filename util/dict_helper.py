import json


def merge_two_dicts(first_dict, second_dict):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    :param first_dict: Dict, first part of data to be merged. Ie, {'balance': 346.9}
    :param second_dict: Dict, second part of data to be merged. Ie, {'itp_id': 3}
    :return final_dict: Result of the merge of the given dicts. Ie, {'itp_id': 3, 'balance': 346.9}

    Examples:
        first_dict = {'itp_id': 3}
        second_dict = {'balance': 346.9}
        final_dict = merge_two_dicts(first_dict, second_dict)
        final_dict # {'itp_id': 3, 'balance': 346.9}
    """
    final_dict = first_dict.copy()
    final_dict.update(second_dict)
    return final_dict


def is_empty(dict):
    """
    Validate if any of the values in a dict are is None
    :param dict: Dict, dictionary of elements. Ie, {'lanlordName': None, 'address': 'Street 53'}
    :return Boolean, is empty or not. Ie, True

    Examples:
        my_dict = {'address': None, 'name': None}
        is_empty(my_dict) # return True
        my_dict = {'address': 'Street 52', 'name': None}
        is_empty(my_dict) # return False
    """

    for key, value in dict.iteritems():
        if value != None:
            return False

    return True


def get_sub_dict(large_dictionary, list_of_keys):
    """
    Return a subset of a given dict.
    :param large_dictionary: dict, Dic the subset dict will be created from. Ie, {'itp_id': 3, 'balance': 346.9}
    :param list_of_keys: list, keys that its values will be extracted from the dict. Ie, ['itp_id']
    :return: Final subset dictionary. Ie, {'itp_id': 3, 'balance': 346.9}

    Examples:
        big_dict = {'itp_id': 3, 'balance': 346.9, 'loan_amount': 20000, 'lender_bank_account': '234234234234'}
        keys_list = ['balance', 'loan_amount']
        subset_dict = get_sub_dict(big_dict, keys_list)
        subset_dict # {'balance': 346.9, 'loan_amount': 20000}
    """
    return dict(map(lambda key: (key, large_dictionary.get(key, None)), list_of_keys))


def remove_key_with_null_values(init_dict, fields=[]):
    """
    Remove from dict the keys that contains None values
    :param init_dict: dict, initial dictionary removed the None values from. Ie,
        {
            'term': 12,
            'product_type': None,
            'collection_method': None,
            'interest_rate': 1.2,
        }
    :fields List, list of fields to delete if are empty. Ie, ['bank_routing_number', 'bank_account_number']
    :return: dict, final with this values that are not None. Ie,

        {
            'term': 12,
            'interest_rate': 1.2,
        }

    Example:
        dict_with_none_values = {'term': 12, 'product_type': None, 'collection_method': None, 'interest_rate': 1.2}
        cleaned_dict = remove_key_with_null_values(dict_with_none_values)
        cleaned_dict # {'term': 12, 'interest_rate': 1.2}

    """
    if fields:
        for field in fields:
            if field in init_dict and (init_dict[field] in ['', None]):
                del init_dict[field]
        return init_dict

    return dict(filter(lambda x: x[1] is not None, init_dict.items()))


def remove_keys_from_dict(dict, remove_keys):
    """
    Remove keys from dict by keys list
    :param dict: dict, dictionary to return without keys. Ie,
        {
            'term': 12,
            'product_type': None,
            'collection_method': None,
            'interest_rate': 1.2,
        }
    :param remove_keys: list, list of keys want to remove. Ie, ['term', 'product_type']
    :return: dict, final dict without no needed keys. Ie
        {
            'collection_method': None,
            'interest_rate': 1.2,
        }
    """
    dict_to_return = dict.copy()
    for key in remove_keys:
        del dict_to_return[key]
    return dict_to_return


def clean_data(data):
    """
    Clean empty fields from received data
    :param data: JSON, data. Ie, {"key": "value", ...}
    """

    data_for_validations = data.copy()

    for key, value in data.iteritems():
        if value == '':
            data[key] = None
            del data_for_validations[key]

    return data_for_validations


def keys_exists(validation_dict, nested_keys, not_found_value=None):
    """
    Validate nested attributes on dictionary
    Based on https://stackoverflow.com/questions/43491287/elegant-way-to-check-if-a-nested-key-exists-in-a-python-dict/43491315
    :param validation_dict: dict, Dictionary to be checked. Ie, {"key": {"sub_key": "sub_value"}}
    :param nested_keys: list, dict keys to be validated on the dict. Ie, ["key", "sub_key"]
    :param not_found_value: Value returned when no element is found on the dict. Ie, None or []
    :return Tuple:
        - boolean, Confirms if nested key is found. Ie, True
        - Element found on the dict or the value of not_found_value. Ie, "sub_value" or None

    Usage examples:

        > # success example
        > validation_dict = {"key": {"sub_key": "sub_value"}}
        > nested_keys = ["key", "sub_key"]
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (True, 'sub_value')

        > # not found example
        > validation_dict = {"key": {"sub_key": "sub_value"}}
        > nested_keys = ["key", "sub_key_not_found"]
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (False, [])

        > # empty dict example
        > validation_dict = {}
        > nested_keys = ["key", "sub_key_not_found"]
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (False, [])

        > # empty key list example
        > validation_dict = {"key": {"sub_key": "sub_value"}}
        > nested_keys = []
        > not_found_value = []
        > keys_exists(validation_dict, nested_keys, not_found_value)
        (False, [])
    """

    if type(validation_dict) is not dict or not nested_keys:
        return False, not_found_value

    temp_validation_dict = validation_dict
    for key in nested_keys:
        try:
            temp_validation_dict = temp_validation_dict[key]
        except Exception:
            return False, not_found_value
    return True, temp_validation_dict


def get_nested_value_from_dict(base_dict, nested_keys, default_value=None):
    """
    Get a nested value from dict if exist or return default value
    :param base_dict: dict, Dictionary to be checked. Ie, {"key": 'value'}
    :param nested_keys: list, dict keys to be validated on the dict. Ie, ["key", "sub_key"]
    :param default_value: any, The default value you whant to return if no has in dict. Ie "key"
    :return Object: Element found on the dict or the value of default_value. Ie, "sub_value" or None
    """

    key_exist, keys_value = keys_exists(base_dict, nested_keys, not_found_value=default_value)

    return keys_value


def get(base_dict, nested_keys, default_value=None):
    """
    Get a nested value from dict if exist or return default value
    :param base_dict: dict, Dictionary to be checked. Ie, {"key": 'value'}
    :param nested_keys: list, dict keys to be validated on the dict. Ie, ["key", "sub_key"]
    :param default_value: any, The default value you whant to return if no has in dict. Ie "key"
    :return Object: Element found on the dict or the value of default_value. Ie, "sub_value" or None
    """

    key_exist, keys_value = keys_exists(base_dict, nested_keys, not_found_value=default_value)

    return keys_value


def get_value_from_dict(base_dict, key, default_value=None):
    """
    Get a value from dict if exist or return default value
    :param base_dict: dict, Dictionary to be checked. Ie, {"key": 'value'}
    :param key: string, key to get value. Ie "key"
    :param default_value: any, The default value you whant to return if no has in dict. Ie "key"
    """
    value = base_dict.get(key)
    if value not in ['', None]:
        return value
    return default_value


def merge_two_dicts_overwrite(first_dict, second_dict, overwrite=True):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    :param first_dict: Dict, first part of data to be merged. Ie, {'balance': 346.9}
    :param second_dict: Dict, second part of data to be merged. Ie, {'itp_id': 3}
    :param overwrite: Boolean, second dict values has more prevalence that first one flag. Ie, True
    :return final_dict: Result of the merge of the given dicts. Ie, {'itp_id': 3, 'balance': 346.9}
    """

    dict_merged = first_dict.copy()

    for key, value in dict_merged.iteritems():
        if overwrite:
            dict_merged[key] = get_value_from_dict(second_dict, key, value)
        else:
            dict_merged[key] = value or get_value_from_dict(second_dict, key)

    return dict_merged


def find_in_dict(obj, key):
    """
    Get key value from a dict
    :param obj: Dict, dict to be checked
    :param key: String, key to search
    :return: String, value found
    """
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            return find_in_dict(v, key)


def string_to_dict(string_dict):
    """
    Transforms a string with the syntax of a dict into a dictionary
    :param string_dict: String, String with dict syntax. Ie, '{"key": value}'
    :return: Dict, String transformed into a dictionary.
    """
    if string_dict:
        return json.loads(string_dict)
    return None


def string_to_json(string):
    """
    Convert Unicode variable to JSON
    :param string: String, variable Unicode to convert, Ie. {u'key': u'Some text'}
    return: JSON. Output or conversion, Ie. { 'key': 'Some text' }
    """

    try:
        string = string.replace('\"\\"', '')
        string = string.replace('\\"\"', '')
        string = string.encode("utf-8")
        string = string.replace('u\'', '\'')
        string = string.replace('\'', '\"')
        string = string.replace('False', '"False"')
        string = string.replace('True', '"True"')

        return json.loads(string)
    except:
        return {}


def clean_null_args(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = clean_null_args(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean


def remove_key_from_dict(data, key):
    if get(data, [key]) or get(data, [key]) == 0:
        r = dict(data)
        del r[key]
        return r
    return data
