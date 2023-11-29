# Swetro Tecnical Test API

## Description
The api was developed using Python as programming language together with the Django rest framework.

It consists of 2 services:

process_data: In charge of processing the file or files and getting records of possible "cheaters".

check_patterns: It is in charge of processing the file or files and obtaining records with unusual patterns using the Isolation Forest algorithm.

### Logic of process_data

The logic for obtaining records of potential cheaters was approached in three ways:

Step 1: Records that have values above what an average person would have are filtered out. For this, the metrics of speed, pace and distance are taken because they are the metrics that I consider most relevant in terms of suspicious behavior.  Therefore, records containing a speed greater than 7 meters/second or a pace less than 2.381 minutes/kilometer or a distance greater than 42,000 meters are obtained.

Step 2: With the records obtained in step 1, each record is taken and all the records associated with the user of that record are obtained. This is done in order to check if the record is within the normal range for that user. To see if the record data are outliers, the lower and upper limits of each user metric are calculated using the concept of the interquartile range. Subsequently, the values of each metric in the record are compared and if they are outside the lower limit or the upper limit then the value of that metric is considered to be an outlier for the user. Finally, with all records that have at least one outlier metric, a last step is applied.

Step 3: The third and last step consists of validating if the records obtained from step 2 can really be considered as "cheaters" by applying predefined conditions that I considered typical of a "cheater", these consist of the following:

-If a user's speed is above his average therefore his heart rate should also be above his average, furthermore, his distance, duration and pace should be below average. If any of these conditions are not met, the user is classified as a "cheater".

-On the contrary, if the user's speed is below his average then the distance traveled, duration and pace should be greater than his average. If any of these conditions are not met, the user is categorized as a "cheater".

The records that are categorized as "cheaters" in step 3 are the ones that the service returns as a response.

### Logic of check_patterns

As for the logic of the service that obtains the records with unusual patterns using the Isolation Forest algorithm.Its operation is based on executing the algorithm mentioned above and with the records returned as suspicious, step 2 of the service process_data is applied, in order to understand which were the atypical metrics that the algorithm may have found. The records obtained with step 2 are the ones that are returned in the service.

## Installation

Note: all commands must be executed in the root project.

It is recommended to create a virtual environment to install the libraries.

```bash
python -m venv .venv
```

```bash
.venv/Scripts/activate
```

To install the libraries, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

To run the application execute the following commands:

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```


