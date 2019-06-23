cdswctl login -n `id -un` --url http://cdsw16-demo-4.vpc.cloudera.com
cdswctl ssh-endpoint -p `id -un`/airline-sentiment -c 2 -m 4
