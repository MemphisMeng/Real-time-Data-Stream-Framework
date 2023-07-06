from diagrams import Diagram
from diagrams.aws.database import Dynamodb
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.analytics import (
    KinesisDataStreams,
    KinesisDataFirehose,
    GlueCrawlers,
    GlueDataCatalog,
    Athena,
)
from diagrams.aws.storage import S3

with Diagram("Real-time Data Stream", show=False):
    dynamodb_table = Dynamodb("Staging Table")
    lambda_function = LambdaFunction("Processing Function")
    table_data_stream = KinesisDataStreams("DynamoDB Stream")
    data_stream = KinesisDataStreams("Source Data Stream")
    deliver_stream = KinesisDataFirehose("Deliver Stream")
    bucket = S3("Storage Bucket")
    crawler = GlueCrawlers("Crawler")
    data_catalog = GlueDataCatalog("Data Catalog")
    athena_query = Athena("Athena Query")

    dynamodb_table >> table_data_stream >> lambda_function >> data_stream >> deliver_stream >> bucket >> crawler >> data_catalog >> athena_query
