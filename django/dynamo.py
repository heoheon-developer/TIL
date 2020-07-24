import decimal
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from conf import settings

ACCESS_ID = settings.S3_ACCESS_ID
ACCESS_KEY = settings.S3_ACCESS_KEY


class DynamoService:
    ERROR_HELP_STRINGS = {
        # Common Errors
        'InternalServerError': 'Internal Server Error, generally safe to retry with exponential back-off',
        'ProvisionedThroughputExceededException': 'Request rate is too high. If you\'re using a custom retry strategy make sure to retry with exponential back-off.' +
                                                  'Otherwise consider reducing frequency of requests or increasing provisioned capacity for your table or secondary index',
        'ResourceNotFoundException': 'One of the tables was not found, verify table exists before retrying',
        'ServiceUnavailable': 'Had trouble reaching DynamoDB. generally safe to retry with exponential back-off',
        'ThrottlingException': 'Request denied due to throttling, generally safe to retry with exponential back-off',
        'UnrecognizedClientException': 'The request signature is incorrect most likely due to an invalid AWS access key ID or secret key, fix before retrying',
        'ValidationException': 'The input fails to satisfy the constraints specified by DynamoDB, fix input before retrying',
        'RequestLimitExceeded': 'Throughput exceeds the current throughput limit for your account, increase account level throughput before retrying',
    }

    def __init__(self):
        self.resource = boto3.resource('dynamodb', region_name="ap-northeast-2", aws_access_key_id=ACCESS_ID,
                                       aws_secret_access_key=ACCESS_KEY)
        self.client = boto3.client('dynamodb', region_name="ap-northeast-2", aws_access_key_id=ACCESS_ID,
                                   aws_secret_access_key=ACCESS_KEY)
        # Use the following function instead when using DynamoDB Local
        # def create_dynamodb_client(region):
        #    return

    def create_dynamodb_client(region="ap-northeast-2"):
        return boto3.client("dynamodb", region_name=region, aws_access_key_id=ACCESS_ID,
                            aws_secret_access_key=ACCESS_KEY)

    def getFileInfo(license_id, user_id):
        table_name = 'box_file_' + license_id

        try:

            #
            # response = self.resource.Table(table_name).get_items(
            #     Key={
            #         'id': file_id
            #     }
            # )
            # table_name = 'box_file_1'
            boto3.setup_default_session(profile_name='AOS', region_name='ap-northeast-2')
            resource = boto3.resource('dynamodb')
            # response = resource.Table(table_name).query(
            #     IndexName='gsi_fileId',
            #     KeyConditionExpression=Key('id').eq('b0523739-a06b-3a1b-a9e5-315a95c1325c'),
            # )

            response = resource.Table(table_name).query(
                IndexName='user_id-index',
                KeyConditionExpression=Key('user_id').eq(user_id)
            )

            # response = resource.Table(table_name).get_items(
            #     Key={
            #         'id': file_id
            #     }
            # )

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Items']
            return item

    def getFiles(self, license_id, storage_id):
        table_name = 'box_file_' + license_id

        try:

            #
            # response = self.resource.Table(table_name).get_items(
            #     Key={
            #         'id': file_id
            #     }
            # )
            # table_name = 'box_file_1'

            # response = resource.Table(table_name).query(
            #     IndexName='gsi_fileId',
            #     KeyConditionExpression=Key('id').eq('b0523739-a06b-3a1b-a9e5-315a95c1325c'),
            # )

            response = self.resource.Table(table_name).query(
                IndexName='storage_id-index',
                KeyConditionExpression=Key('storage_id').eq(storage_id)
            )

            # response = resource.Table(table_name).get_items(
            #     Key={
            #         'id': file_id
            #     }
            # )

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Items']
            return item

    def getDirectorys(self, license_id, storage_id):
        directory_table = 'box_directory_' + license_id
        # query_input = {
        #     'TableName': table_name,
        #     'KeyConditionExpression': 'storage_id = :storageId',
        #     'ExpressionAttributeValues': {
        #         ':storageId': {'S': storage_id}
        #     }
        # }
        folder_path = []
        folder_list = []
        folder_id = ''
        try:
            folders = self.resource.Table(directory_table).scan(
                FilterExpression=Attr('storage_id').eq(storage_id) & Attr('parent_id').eq('0')
            )

            folder_list = folders['Items']

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = {
                'folderList': folder_list,
                'fileList': [],
                'folderPath': folder_path,
                'folder_id': folder_id
            }

            return item

    def get_directory_file(self, license_id, id):
        directory_table = 'box_directory_' + license_id
        file_table = 'box_file_' + license_id

        folder_path = []
        parent_folder = {}

        folder_id = id

        try:
            folder_info = self.resource.Table(directory_table).query(
                IndexName='id-index',
                KeyConditionExpression=Key('id').eq(id)
            )
            parent_folder['dir_name'] = folder_info['Items'][0]['dir_name']
            parent_folder['full_path'] = folder_info['Items'][0]['full_path']
            parent_folder['storage_id'] = folder_info['Items'][0]['storage_id']
            parent_folder['id'] = folder_info['Items'][0]['id']
            parent_folder['parent_id'] = folder_info['Items'][0]['parent_id']
            folder_path.insert(0, parent_folder)

            parentId = folder_info['Items'][0]['parent_id']

            while parentId != '0':
                folder = self.resource.Table(directory_table).query(
                    IndexName='id-index',
                    KeyConditionExpression=Key('id').eq(parentId)
                )
                parentId = folder['Items'][0]['parent_id']
                folder['dir_name'] = folder['Items'][0]['dir_name']
                folder['full_path'] = folder['Items'][0]['full_path']
                folder['storage_id'] = folder['Items'][0]['storage_id']
                folder['id'] = folder['Items'][0]['id']
                folder['parent_id'] = folder['Items'][0]['parent_id']
                folder_path.insert(0, folder)

            folders = self.resource.Table(directory_table).query(
                IndexName='parent_id-index',
                KeyConditionExpression=Key('parent_id').eq(id)
            )

            if len(folders['Items']):
                folder_id = id

            files = self.resource.Table(file_table).query(
                IndexName='parent_id-index',
                KeyConditionExpression=Key('parent_id').eq(id)
            )

            print(" files['Items']", files['Items'])

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = {
                'folderList': folders['Items'],
                'fileList': files['Items'],
                'folderPath': folder_path,
                'folder_id': folder_id
            }
            return item

    def get_version_info(self, license_id, id):
        version_table = 'box_file_version_' + license_id
        try:
            version = self.resource.Table(version_table).query(
                IndexName='file_id-index',
                KeyConditionExpression=Key('file_id').eq(id)
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = {
                'versionList': version['Items']
            }
            return item

    def get_parent(self, license_id, id):
        directory_table = 'box_directory_' + license_id
        file_table = 'box_file_' + license_id
        folder_list = []
        file_list = []
        folder_path = []

        folder_id = ''

        try:
            parent_folder = self.resource.Table(directory_table).query(
                IndexName='id-index',
                KeyConditionExpression=Key('id').eq(id)
            )
            storage_id = parent_folder['Items'][0]['storage_id']
            parent_id = parent_folder['Items'][0]['parent_id']

            if parent_id == '0':
                folders = self.resource.Table(directory_table).scan(
                    FilterExpression=Attr('storage_id').eq(storage_id) & Attr('parent_id').eq('0')
                )
                folder_list = folders['Items']

            else:
                folders = self.resource.Table(directory_table).query(
                    IndexName='parent_id-index',
                    KeyConditionExpression=Key('parent_id').eq(parent_folder['Items'][0]['parent_id'])
                )

                folder_id = folders['Items'][0]['parent_id']

                folder_list = folders['Items']

            if parent_id != '0':
                files = self.resource.Table(file_table).query(
                    IndexName='parent_id-index',
                    KeyConditionExpression=Key('parent_id').eq(parent_folder['Items'][0]['parent_id'])
                )
                file_list = files['Items']



        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = {
                'folderList': folder_list,
                'fileList': file_list,
                'folderPath': folder_path,
                'folder_id': folder_id

            }
            return item

    def get_file_by_category(self, license_id, params):

        storage_id = params['storage_id']
        category = params['category']
        file_table = 'box_file_' + license_id
        directory_table = 'box_directory_' + license_id
        folder_list = []
        file_list = []
        folder_path = []
        folder_id = ''
        try:

            if category == 'all':
                files = self.resource.Table(file_table).scan(
                    FilterExpression=Attr('storage_id').eq(storage_id)
                )
                file_list = files['Items']
            elif category == 'folder':
                folders = self.resource.Table(directory_table).scan(
                    FilterExpression=Attr('storage_id').eq(storage_id)
                )
                folder_list = folders['Items']
            else:
                files = self.resource.Table(file_table).scan(
                    FilterExpression=Attr('storage_id').eq(storage_id) & Attr('type').eq(category)
                )
                file_list = files['Items']

                paginator = Paginator(file_list, 20)

                page = 1
                try:
                    contacts = paginator.get_page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    contacts = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    contacts = paginator.page(paginator.num_pages)

                file_list = contacts.object_list


        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = {
                'folderList': folder_list,
                'fileList': file_list,
                'folderPath': folder_path,
                'folder_id': folder_id

            }
            return item

    def getFileChunksMap(self, license_id, version_id):
        """
        # get chunk list sort by 'order' colunm
        # because 'order' is sort key of table, list is auto sorted by dynamodb
        :param license_id:
        :param version_id: 'id' of box_file_version_[licence_id]
        :return: Dynamodb query result object
        """
        table_name = "box_chunk_map_" + license_id
        query_input = {
            "TableName": table_name,
            "KeyConditionExpression": "version_id = :version_id",
            "ExpressionAttributeValues": {":version_id": {"S": version_id}}
        }
        result = self.execute_query(self.resource, query_input)
        return result['Items']

    def execute_query(self, dynamodb_client, input):
        try:
            response = dynamodb_client.query(**input)
            print("Query successful.")
            print(response)
        except ClientError as error:
            self.handle_error(error)
        except BaseException as error:
            print("Unknown error while querying: " + error.response['Error']['Message'])
        finally:
            return response

    def handle_error(self, error):
        error_code = error.response['Error']['Code']
        error_message = error.response['Error']['Message']

        error_help_string = self.ERROR_HELP_STRINGS[error_code]

        print('[{error_code}] {help_string}. Error message: {error_message}'
              .format(error_code=error_code,
                      help_string=error_help_string,
                      error_message=error_message))


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
