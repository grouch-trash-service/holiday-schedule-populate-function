# Holiday Schedule Populate Function
Lambda function for populating trash pickup holiday schedule.

## Build
This project uses sam to build. The following command can be used
```shell script
sam build
```

## Running locally

The function can be ran locally using the following command
```shell script
pip install -r requirements-dev.txt
PYTHONPATH=holiday python holiday/function.py
```
## Tests
Unit tests can be ran with the following command
```shell script
PYTHONPATH=holiday pytest
```

## Deploy
The code will automatically be built and deployed with a [github action.](.github/workflows/build.yml)
To deploy the function manually first use the `aws configure` command to setup credentials for aws, then run
```shell script
sam deploy
```

## Code Scanning
### Snyk OSS Scanning
OSS scanning is done using Snyk as part of the deployment pipeline and results can be viewed on the github action logs. You can run a scan locally by running this command.
```shell script
snyk monitor --file=holiday/requirements.txt -- --allow-missing
```

### Sonar Scanning
Sonar quality scans are done as part of the deployment pipeline and results can be viwed on the github action logs. Results can also be found on [Sonarcloud.](https://sonarcloud.io/dashboard?id=grouch-trash-service_holiday-schedule-populate-function)
