def row_to_dict(row):
    if not row:
        return None
    return {key: row[key] for key in row.keys()}

def row_list_to_dict_list(row_list):
    dict_list = []
    for row in row_list:
        dict_list.append({key: row[key] for key in row.keys()})
    return dict_list

def getAvaliacaoDto(avaliacao) :
    return True