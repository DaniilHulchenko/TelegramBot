from foundation import db_connection

def ppprint(res:db_connection.cursor())->str:
    if len(res) > 1:
        temp = "["
        for i in res:
            temp += '\n"'
            for ii in i:
                if ii is list(i)[-1]:
                    temp += str(ii) + ": " + str(i[ii]) + '"\n'
                    continue
                temp += str(ii) + ": " + str(i[ii]) + "\n"
        temp += "]"
    elif len(res) == 1:
        temp = str(*res)
    return temp