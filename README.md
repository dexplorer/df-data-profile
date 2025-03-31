# df-data-profile

This application uses a Natural Language Processing (NLP) Named Entity Recognition (NER) model to classify the data as PII vs Non-PII.

Application can be invoked using CLI or REST API end points. This allows the app to be integrated into a larger data ingestion / distribution framework.

### Define the environment variables

Create a .env file with the following variables.

```
APP_ENV=dev
APP_ROOT_DIR=/workspaces/df-data-profile
NAS_ROOT_DIR=/workspaces/nas
```

### Install

- **Install via Makefile and pip**:
  ```
    make install
  ```

### Usage Examples

- **Profile a dataset via CLI**:
  ```sh
    dp-app-cli profile-dataset --dataset_id "dataset_3"
  ```

- **Profile a dataset via CLI with cycle date override**:
  ```sh
    dp-app-cli profile-dataset --dataset_id "dataset_3" --cycle_date "2024-12-26"
  ```

- **Profile a dataset via API**:
  ##### Start the API server
  ```sh
    dp-app-api
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