from dotenv import load_dotenv
load_dotenv()

try:
    from API import (app,
                     api,
                     DestninationList,docs
                     )
except Exception as e:
    print("module missing: {}".format(e))
    
api.add_resource(DestninationList, '/destninationlist')
docs.register(DestninationList)