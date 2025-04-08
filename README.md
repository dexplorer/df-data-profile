# df-data-profile

This application uses a Natural Language Processing (NLP) Named Entity Recognition (NER) model to classify the data as PII vs Non-PII.

Application can be invoked using CLI or REST API end points. This allows the app to be integrated into a larger data ingestion / distribution framework.

### Define the environment variables

Update one of the following .env files which is appropriate for the application hosting pattern.

```
on_prem_vm_native.env
aws_ec2_native.env
aws_ec2_container.env
aws_ecs_container.env
```

### Install

- **Install via Makefile and pip**:
  ```
    make install-dev
  ```

### Usage Examples

#### App Hosted Natively on a VM/EC2

- **via CLI**:
  ```sh
    dp-app-cli --app_host_pattern "aws_ec2_native" profile-dataset --dataset_id "dataset_3"
  ```

- **via CLI with Cycle Date Override**:
  ```sh
    dp-app-cli --app_host_pattern "aws_ec2_native" profile-dataset --dataset_id "dataset_3" --cycle_date "2024-12-26"
  ```

- **via API**:
  ##### Start the API server
  ```sh
    dp-app-api --app_host_pattern "aws_ec2_native"
  ```
  ##### Invoke the API endpoint
  ```sh
    https://<host name with port number>/profile-dataset/?dataset_id=<value>
    https://<host name with port number>/profile-dataset/?dataset_id=<value>&cycle_date=<value>

    /profile-dataset/?dataset_id=dataset_3
    /profile-dataset/?dataset_id=dataset_3&cycle_date=2024-12-26
  ```
  ##### Invoke the API from Swagger Docs interface
  ```sh
    https://<host name with port number>/docs
  ```

#### App Hosted as Container on a VM/EC2

- **via CLI**:
  ```
	docker run \
	--mount=type=bind,src=/home/ec2-user/workspaces/nas,dst=/nas \
  --rm -it df-data-profile \
  dp-app-cli --app_host_pattern "aws_ec2_container" profile-dataset --dataset_id "dataset_3"
  ```

- **via CLI with Cycle Date Override**:
  ```
	docker run \
	--mount=type=bind,src=/home/ec2-user/workspaces/nas,dst=/nas \
  --rm -it df-data-profile:latest \
  dp-app-cli --app_host_pattern "aws_ec2_container" profile-dataset --dataset_id "dataset_3" --cycle_date "2024-12-26"
  ```

- **via API**:
  ##### Start the API server
  ```
	docker run \
	--mount=type=bind,src=/home/ec2-user/workspaces/nas,dst=/nas \
	-p 9090:9090 \
	--rm -it df-data-profile:latest \
  dp-app-api --app_host_pattern "aws_ec2_container"
  ```

#### App Hosted as a Container on AWS ECS

- **via CLI**:
  ##### Invoke CLI App by Deploying ECS Task using ECS Task Definition 
  Enter the following command override under 'Container Overrides'. 
  ```
  "dp-app-cli", "--app_host_pattern", "aws_ecs_container", "profile-dataset", "--dataset_id", "dataset_103", "--cycle_date", "2024-12-26"
  ```

- **via API**:
  ##### Invoke API App by Deploying ECS Task using ECS Task Definition 
  Enter the following command override under 'Container Overrides'. 
  ```
  "dp-app-api", "--app_host_pattern", "aws_ecs_container"
  ```

### Sample Input (customers_20241226.csv)

```
effective_date,first_name,last_name,full_name,ssn,dob,street_addr1,street_addr2,city,state,country
2024-12-26,John,Connor,John Connor,987-65-4321,1988-05-03,155 North Blvd,,New York City,NY,USA
2024-12-26,Jill,Valentine,Jill Valentine,123-45-6789,1990-06-25,155 North Blvd,,Los Angeles,CA,USA
```

### Sample Output 

```
[
    {
      "column_name": "city",
      "info_type": "GPE",
      "data_class": "NON PII"
    },
    {
      "column_name": "country",
      "info_type": "GPE",
      "data_class": "NON PII"
    },
    {
      "column_name": "dob",
      "info_type": "DATE OF BIRTH",
      "data_class": "PII"
    },
    {
      "column_name": "effective_date",
      "info_type": "DATE",
      "data_class": "NON PII"
    },
    {
      "column_name": "first_name",
      "info_type": "NAME",
      "data_class": "PII"
    },
    {
      "column_name": "full_name",
      "info_type": "NAME",
      "data_class": "PII"
    },
    {
      "column_name": "last_name",
      "info_type": "NAME",
      "data_class": "PII"
    },
    {
      "column_name": "ssn",
      "info_type": "SSN",
      "data_class": "PII"
    },
    {
      "column_name": "state",
      "info_type": "ORG",
      "data_class": "NON PII"
    },
    {
      "column_name": "street_addr1",
      "info_type": "ADDRESS",
      "data_class": "PII"
    },
    {
      "column_name": "street_addr2",
      "info_type": "",
      "data_class": "NON PII"
    }
  ]

```