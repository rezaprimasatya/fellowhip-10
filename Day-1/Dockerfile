# Base image
FROM apache/airflow:2.1.4-python3.8

# Install any additional dependencies
RUN pip install --no-cache-dir <additional-dependencies>

# Copy DAGs, plugins, and other files to the container
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY requirements.txt /opt/airflow/requirements.txt

# Install custom Python packages
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Set the Airflow home directory
ENV AIRFLOW_HOME=/opt/airflow

# Set the Airflow configuration file
COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# Expose the Airflow web server port
EXPOSE 8080

# Start the Airflow web server
CMD ["webserver"]
