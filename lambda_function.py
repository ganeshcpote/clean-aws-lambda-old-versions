from __future__ import absolute_import, print_function, unicode_literals
import boto3
import json

# This script removes all versions except $LATEST and the newest 50 version
# This script also checks if any version has any alias. It won't delete any version where any alias is using,
# boto3 will throw an exception and the script will exit

client = boto3.client('lambda')

def check_alias_exist(_function, version):                  
    response_alias = client.list_aliases(FunctionName=_function, FunctionVersion=str(version))
    if len(response_alias['Aliases']) > 0:
        return True
    return False


def clean_old_lambda_versions(event, context):
    functions = client.list_functions()['Functions']
    print("function length = " + str(len(functions)))

    for function in functions:
        paginator = client.get_paginator('list_versions_by_function')
        versions = paginator.paginate(FunctionName=function).build_full_result()['Versions']
        
        numVersions = len(versions)
        print("Function Name = " + str(function) + "| Total Version = " + str(numVersions))
        
        retain_count = numVersions-50
        print("Now {} no. of versions will be deleted...".format(retain_count))

        if retain_count > 50:
            for index in range(retain_count):        
                current_version = versions[retain_count]['Version']
                arn = versions[retain_count]['FunctionArn']
                if not check_alias_exist(function, current_version) and not current_version == '$LATEST':
                    #print('delete_function(FunctionName={})'.format(arn))
                    client.delete_function(FunctionName=arn) 
                    print("=>   Version {} deleted with success...".format(arn))
                else:
                    print("=>   Version {} has alias mapped...".format(current_version))   
                retain_count=retain_count-1
        else:
            print("There is nothing to be deleted at this moment since we are keeping latest 50 verionss")
    return {
      'statusCode': 200,
      'body': json.dumps('Success')
    }

#if __name__ == '__main__':
#    clean_old_lambda_versions()
