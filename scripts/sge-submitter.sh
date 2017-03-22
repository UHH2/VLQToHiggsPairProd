#!/bin/bash
#$ -l os=sld6
#$ -l site=hh
#$ -cwd
#$ -V
#$ -l h_rt=00:59:00
#$ -l h_vmem=8G
#$ -l mem_free=22G
#$ -l h_fsize=8G
#$ -pe local 4
#$ -j y
#$ -o .
#$ -t 1-40
source /usr/share/Modules/init/sh
export -f module
JOBTMP=/tmp/$JOB_NAME.$JOB_ID
echo "+++++++++" free -mh
free -mh
echo "+++++++++" $SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker -d $JOBTMP -m 16G -c 4 $@
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker -d $JOBTMP -m 16G -c 4 $@
