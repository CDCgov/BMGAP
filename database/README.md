# BMGAP Database

BMGAP stores data in a MongoDB v3 database. Example files for each of the collections are included in this directory 

    - internal, which is the primary data collection; 
    - sample_summary, which has an overview for each sample; 
    - run, which stores basic information about a sequencing run; and 
    - users, which holds information on the data a user is able to view. 

The Submitter field in the run, internal, and sample_summary collections is used to assess whether a users is permitted to view the record.

The system requires three users:

    - bmgap-reader, which should have read permission on the BMGAP database. This is used for the data API
    - bmgap-writer, which should have readWrite permission on the BMGAP database. This account is used by the pipeline to insert data into the database
    - bmgap-admin, which should have readWrite, dbAdmin, userAdmin, and backup permission on the BMGAP database. This account is used for administrative processes, such as backing up and restoring data


Passwords need to be created for each user and the configuration files in the data-api and pipeline must be updated to include them.

