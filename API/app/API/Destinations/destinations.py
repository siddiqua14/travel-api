try:
    from flask import Flask
    from flask_restful import Resource, Api
    from apispec import APISpec
    from marshmallow import Schema, fields
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec
    from flask_apispec.views import MethodResource
    from flask_apispec import marshal_with, doc, use_kwargs

    print("ok ...")

except Exception as e:
    print("error: {}".format(e))
    
class DestninationList(MethodResource, Resource): 
    @doc(description='this is destination list', tags= ['destinations'])
    def get(self):
        
        return{'message':'api working fine'}, 200