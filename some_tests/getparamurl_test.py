def getParamURL(path, param):
    if param in path:
        splitted_path = path.split('/')
        for p in splitted_path:
            if param in p: 
                goal_param = p
                break
        start_of_param = goal_param.index('=')
        result = goal_param[start_of_param+1:]
        return result

    else:
        return None


def test():
    if getParamURL('/search/?query=smile/?page=3', 'query') != 'smile':
        print('WRONG: ', getParamURL('/search/?query=smile/?page=3', 'query'))
    else:
        print('OK')

    if getParamURL('/search/?query=smile/?page=3', 'page') != '3':
        print('WRONG: ', getParamURL('/search/?query=smile/?page=3', 'page'))
    else:
        print('OK')

    if getParamURL('/search/?query=smile', 'query') != 'smile':
        print('WRONG: ', getParamURL('/search/?query=smile', 'query'))
    else:
        print('OK')

    if getParamURL('/search/?page=3', 'page') != '3':
        print('WRONG: ', getParamURL('/search/?page=3', 'page'))
    else:
        print('OK')

    if getParamURL('/search/?query=smile', 'page') != None:
        print('WRONG: ', getParamURL('/search/?query=smile', 'page'))
    else:
        print('OK')

if __name__ == '__main__':
    test()
