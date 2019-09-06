# LAnDmARk -  Lofar Automated Data Access & pRocessing

**The LAnDmARk scripts where developed by:  Janis Steinbergs, Kristaps Veitners**

LAnDmARk is automated data retrieval and processing tool. To retrieve data from LOFAR LTA and run calibrator and target pipeline to image FITS map. 
## LAnDmARk setup and run
### Dependencies
1. python 3
   - coloredlogs
   - awlofar (necessary for staging and retrieval data)
   - matplotlib
   - numpy
   - seaborn
2. Prefactor
3. LOFAR software
### Setup

Tool use config file template version is config.cfg. Config file contains this sections Data, Operation, Paths, Cluster. Data section is for data querying to LTA database, Operation section set options for tool what to do. Thies options are querying, stage, retrieve and process. To use querying, stage, retrieve options user must be registered to LOFAR LTA (https://lta.lofar.eu).  Process option currently use Prefactor (https://github.com/lofar-astron/prefactor)
