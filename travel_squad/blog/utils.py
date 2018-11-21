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