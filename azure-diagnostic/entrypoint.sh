#!/bin/sh
set -e
service ssh start
python /azure_diagnostic_python/azure-diagnostic-python/azure_diagnostic_python.py