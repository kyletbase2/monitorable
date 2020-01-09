import boto3

class Elasticache:

    def __init__(self,region):
        self.name = 'elasticache'
        self.region = region
        self.identifiers = []
        self.get_resources()
        
    def get_resources(self):
        try:
            client = boto3.client('elasticache', region_name=self.region)
            paginator = client.get_paginator('describe_cache_clusters')
            page_iterator = paginator.paginate()
            replication_groups = []
            for page in page_iterator:
                replication_groups.extend([item['CacheClusterId'] for item in page['CacheClusters']])
            for replication_group in replication_groups:
                account_id = boto3.client('sts').get_caller_identity().get('Account')
                tags = client.list_tags_for_resource(ResourceName='arn:aws:elasticache:' + self.region + ':' + account_id + ':cluster:' + replication_group)['TagList']
                self.identifiers.extend([{
                    'id': replication_group,
                    'tags': [{
                        'key': t['Key'],
                        'value': t['Value']
                    } for t in tags]
                }])
        except Exception:
            pass