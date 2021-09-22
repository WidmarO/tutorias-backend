
class Req_Parser():

    params = {}
    ans = {}

    def __init__(self):

        self.params = {}
        self.ans = {}

    def add_argument(self, name, type=str, required=False):
        '''Set up an argument for parse received data of http request.\n
          \n

          Parameters:\n

          1. name (string): The name of argument, should be equal to name of argument that you expect receive to return in the dict.\n
          2. type (type): The type of variable that should be the value of the argument received.\n
          3. required (bool): If is True, the value of the argument should existing and should be diferent to empty "" if type is str\n
          4. esp_attr (bool): By default when argument have "required":False and not exist in request.data then this argument is added to answer dictionary  with the value  "None" but if the parameter "esp_attr" is True so, this argument will be not adding to dictionary asnwer.\n
        '''
        self.params[name] = {'type': type,
                             'required': required}

    def parse_args(self, request):
        self.ans = {}
        for p in self.params:
            # verify if the required fields exists
            if self.params[p]['required']:
                if p not in request:
                    return False, {"help": "Field '{}' is required".format(p)}
                if self.params[p]['type'] is not type(request[p]):
                    return False, {"help": "Diferent type of variable in '{}' argument".format(p)}
                else:
                    if self.params[p]['type'] is str:
                        if request[p].strip() == '':
                            return False, {"help": "Field '{}' is required".format(p)}
                        self.ans[p] = request[p]
            else:
                if self.params[p]['type'] is not type(request[p]):
                    return False, {"help": "Diferent type of variable in '{}' argument".format(p)}
                else:
                    if self.params[p]['type'] is str:
                        if request[p].strip() == '':
                            return False, {"help": "Field '{}' is required".format(p)}
                        self.ans[p] = request[p]
            
            if self.params[p]['type'] is list:
                self.ans[p] = request[p]

            if self.params[p]['type'] is list:
                self.ans[p] = request[p]
                
        return True, self.ans

    # def parse_args(self, request):
    #     self.ans = {}
    #     for p in self.params:
    #         if self.params[p]['required']:
    #             if p not in request:
    #                 return False, {"help": "Field '{}' is required".format(p)}
    #             if (p.strip() != ""):
    #                 if self.params[p]['type'] is type(request[p]):
    #                     self.ans[p] = request[p]
    #                 else:
    #                     return False, {"help": "Diferent type of variable in '{}' argument".format(p)}
    #             else:
    #                 return False, {"help": "Field '{}' is required".format(p)}
    #         else:
    #             if (p in request.keys()):
    #                 if self.params[p]['type'] is type(request[p]):
    #                     self.ans[p] = request[p]
    #                 else:
    #                     return False, {"help": "Diferent type of variable in '{}' argument".format(p)}
    #             else:
    #                 if self.params[p]['esp_attr']:
    #                     pass
    #                 else:
    #                     self.ans[p] = None

    #     return True, self.ans
