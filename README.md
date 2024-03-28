# BMAT Music: CSV Processing

Project consists of two parts. CSV processing module and APIs to upload csv file and download output file.

## Tech Stack

- Python (3.10)
- Dask (2024.3.1)
- Flask (3.0.2)
- Celery (5.3.6)
- RabbitMQ

Tested on MacOS.

## Setup

First check if you have python installed by running command `python --version`. Most probably you have it already.
Otherwise, install corresponding version according to instructions of your OS.
For more details follow the [link](https://www.python.org/downloads/)

Next setup python environment:

- create virtual environment using `python -m venv <path_to_env>` or use instruction [here](https://docs.python.org/3/library/venv.html)
- activate virtual environment: `source <path_to_venv>/bin/activate`
- clone code or download zip anywhere in your local machine
- go to **bmat_music** project and install requirements: `pip install -r requirements.txt`

Here *Celery* uses *RabbitMQ* as a messsage broker, install it.
To install RabbitMQ on macOS, you can use Homebrew. Here are the steps to install RabbitMQ using Homebrew:

1. If you haven't installed *Homebrew*, install it
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Check if *Homebrew* is in your path running `echo $PATH`.

   If it's not there, add it by `export PATH="<path_to_homebrew>:$PATH"`
3. Install RabbitMQ: `brew install rabbitmq`
4. Start RabbitMQ: `brew services start rabbitmq`

You can check that RabbitMQ is running by using the following command `rabbitmqctl status`

More details about RabbitMQ installation on different operating systems could be found in [official documentation](https://www.rabbitmq.com/docs/download)

To use RabbitMQ with celery later in the application, you can create new user or use default guest user. 
For more details check [documentation](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html)

**_PLEASE NOTE_:** If you create a new user, update `RABBITMQ_USER` and `RABBITMQ_PASS` in config file.

Before running application you need to create folders for uploaded, downloaded and log files.

Go to *bmat_music* directory and create 3 new folders: `uploads`, `downloads` and `logs`.

When everything is done with setup, go to `api` folder and run the following command:
```
flask run
```

From `bmat_music` directory run celery worker

```
celery -A celery_tasks.tasks worker --loglevel=info --logfile='logs/csv_processing.log' 
```
If you want to run it in background add `--detach` option. Also, you can skip `--logfile` option or provide other path to log.

## Usage

Now when both celery and flask servers are running, you can use any API client to send requests.
One of the most popular applications is [Postman](https://www.postman.com/).

## API Endpoints: How they work

There are 2 API endpoints in the application

### 1: Schedule file to processing

### Method
- `POST`

### URL
- `/upload`

### Request Parameters
- `file`: The CSV file to be processed (multipart/form-data)

### Example Request
```
POST /upload
Content-Type: multipart/form-data

[file: example.csv]
```

### Response

- HTTP Status: 200 OK
- Body: JSON object containing the ID of the processing task.
  ```
  {
    "task_id": "076c2c00-a7ee-4d2e-a08f-7ddab652bad8"
  }
  ```

This one is used to upload csv file and process it creating new output file. It requires `file` in request. Attach file in postman request body.
As soon as request sent, it will create `task_id` for celery, copy uploaded file with the name `<task_id>_input.csv` in `uploads/` folder and run celery task.
Celery will do necessary processing and create output file in `download` folder with name `<task_id>_output.csv`.

### 2: Download the result

### Method
- `GET`

### URL
- `/download`

### Request Parameters
- `task_id`: The ID of the processing task.

### Example Request
```
GET /download/076c2c00-a7ee-4d2e-a08f-7ddab652bad8
```

### Response

- HTTP Status: 200 OK
- Body: The resulting CSV file.
```
Song,Date, Total Number of Plays for Date
Umbrella,2020-01-01,150
Umbrella,2020-01-02,250
In The End,2020-01-01,1500
In The End,2020-01-02,500
```

This API will download file `<task_id>_output.csv` from downloads folder with a new name `output.csv`.

## CSV Processing Module

For processing large csv files `csv_processing` module is created. `class LargeCSVProcessor` will do necessary job.

The `LargeCSVProcessor` class is designed to read large CSV files, process the data, and write the processed data into a new file.

As both input and output files can be larger than available memory, python library `dask` is used.

Dask is a flexible parallel computing library for Python that enables efficient handling of large datasets that don't fit into memory
by breaking them into smaller chunks and performing computations on those chunks in parallel. 
Dask DataFrames, used in this class, are similar to Pandas DataFrames but can handle datasets that are too large to fit into memory
by operating on smaller partitions of the data in parallel.

For more information about dask library check official [documentation](https://docs.dask.org/en/stable/)

### Complexity of data processing solution

Dask Dataframes will use chunks to read data from csv file, which are distributed across memory. It will read and process data in parallel.
Complexity of reading and processing data will depend on chunk size and number of chunks needed to read whole file. It is linear to the number of records in the dataset.
It means, the solution has a time complexity of **O(n)**, where **n** is the total number of records in the file.


## What to Add

1. Tests
2. Simple UI for upload and download files

## Some Notes

Flask is used in this project, which is a lightweight and flexible web framework for Python.
I have never used this framework before, my main stack was with Django framework. 

Here are some points why I chose Flask over Django for this project:
- Learn new framework, as before I worked only with django
- Django is a powerfull framework, it is full, complete and full-stack, with wide range of built-in features and everything, but in this project I don't need it
- Flask is microframework, with only the essential tools to start web development, allowing to add additional functionality later
- Flask is small and lightweight which makes it perfect choice for simple applications and APIs
- Last but not least: I had a chance to learn something new and use it meantime.

==================================

**Author:** Shushanik Hovhannesyan

**Email:** shushhovhannisyan@gmail.com
