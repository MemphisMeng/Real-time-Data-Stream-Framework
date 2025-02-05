# Real-time Data Stream Framework
Tutorial of Real-time Data Streaming Architecture Based on AWS Kinesis Firehose & AWS GLue Crawlers

## ERD
![](./real-time_data_stream.png)

## Execution

- Dependency Installation
```
pip install -r */requirements.txt
```
- Build:
```
sam build -u
```
- Local Testing:
```
sam local invoke "StreamingFunction" -e event.json --env-vars channels/variables.json
```
- Deploy:
```
for file in channels/*.json; do
    environment=$(jq -r '.Parameters.Environment' "$file")
    data_source=$(jq -r '.Parameters.DATA_SOURCE' "$file")
    data_source_arn=$(jq -r '.Parameters.DATA_SOURCE_ARN' "$file")
    sam deploy --parameter-overrides Environment=$environment DataSource=$data_source DataSourceArn=$data_source_arn --stack-name test-stack --confirm-changeset --no-fail-on-empty-changeset --capabilities CAPABILITY_NAMED_IAM
done
```