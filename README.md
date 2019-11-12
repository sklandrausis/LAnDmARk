# LAnDmARk -  Lofar Automated Data Access &amp; pRocessing 

# Table of Contents
* [Capabilities of LAnDmARk](#capabilities-of-landmark)
* [Dependencies](#dependencies)
* [Running LAnDmARk](#running-landmark)
* [LAnDmARk Output products](#landmark-output-products)
    + [Inspection plots](#inspection-plots)
* [Changelog](#changelog)
* [Getting Help](#getting-help)
* [Acknowledgements](#acknowledgements)

## Capabilities of LAnDmARk
LAnDmARk has been thought to make LOFAR data access (and processing) more automated and user friendly. Currently it allows users to perform:

- Data selection from LOFAR Long Term Archive (LTA [https://lta.lofar.eu](https://lta.lofar.eu/)).
- Data retrieval from LOFAR LTA
- Direction-independent processing of LOFAR LBA/HBA data via prefactor (v3) pipelines ([https://github.com/lofar-astron/prefactor](https://github.com/lofar-astron/prefactor))
  - Setup working environment and run prefactor pipelines

## Dependencies

- python 3
  - Coloredlogs 10.0
  - awlofar (necessary for staging and retrieval data) 2.7.1
  - matplotlib 3.0.3
  - Numpy 1.16.3
  - Seaborn 0.9.0
- Prefactor v3
- LOFAR software 3.2.0


## Running LAnDmARk

To run LAnDmARk a configuration file is needed and a template version is provided (see config.cfg). The configuration file contains the following sections: _Data, Operation, Paths, Cluster_. The _Data_ section collects needed info for data querying to LTA database and the _Operation_ section specifies the action(s) required. Enabled operations are: **selection**, **stage**, **retrieve** and **process**. Note that in order to query, to stage and to retrieve data, users must have registered to LOFAR LTA ([https://lta.lofar.eu](https://lta.lofar.eu/)). The _Paths_ section contains pointers to the needed software (i.e. where the software is installed) as well as the working directory (i.e. where archived data will be collected and processed). The _Cluster_ section allows users to set computing resources needed for data processing (maximum processes per single computing node, process data on a single computing node or on multiple nodes). In the _Data_ section _ProductType_ parameter specifies the if raw data must be downloaded or pipeline data products. In the _Operations_ section the optional parameter _which\_obj_ specifies which type of products - _calibrators_, _targets_ or _all_ - should be processed.

When the configuration file is ready users can execute the selected operations with the command:

python3 main.py

The main.py script can be run with additional options:

-v or --version to display current version

-h or --help for help

-c or --config to point to configuration file. Default path is: LAnDmARk/config.cfg

-d or --printlogs to display additional information

Currently LAnDmARk supports only simple queries. First it checks if the user is part of the selected project (or if data under the selected project are public). Next LAnDmARk will use the specified calibrator ids, target ids and target name to find data products. Note however that if the selected project is &quot;MSSS\_HBA\_2013&quot;, the user does not need to specify SAS id for the calibrator source. In this case the SAS ID of calibrator source(s) are obtained via the following logic:

Calirator SASid  = target source SASid-1.

Note that staging requests cannot exceed 5 TB in volume and 5000 files at any point of time (see[https://www.astron.nl/lofarwiki/doku.php?id=public:lta\_howto](https://www.astron.nl/lofarwiki/doku.php?id=public:lta_howto)). LAnDmARk will check if such constraints are satisfied before any staging of  data products and if necessary abort the run and report to the user.

Finally, the **process** option currently only supports prefactor (v3) pipelines ([https://github.com/lofar-astron/prefactor](https://github.com/lofar-astron/prefactor)). In case only the target products are processed, the user should add the proper path … the calibrator solution h5parm file.



| **Scripts** | **Description** |
| --- | --- |
| main.py | Run all scripts based on the config file |
| setup.py | Create working environment |
| selectionStaging.py | Perform **Selection** and **Stage** operations |
| retrieveDataproducts.py | Retrieve data products ( **Retrieve** operation), display staging progress. |
| runPipelines.py | Process the data ( **Process** operation) |

## LAnDmARk Output products

In the working directory specified via the configuration file LAnDmARk creates an output directory named as specified in the _TargetName_ field of the _Data_ section. Such a directory contains several subdirectories (as shown in the figure below):

- the LAnDmARk\_aux directory, which stores auxiliary files. Also, diagnostic plots for each selected operation in are collected in dedicated subfolders.
- the calibrators directory, where calibrator data products are stored and inspection plots for prefactor will be placed.
- the target directory, where target data products are stored and inspection plots for prefactor will be placed.
- the Image\_deep directory, where imaging pipeline inspection plots and output products will be placed.

if  **selection** operation is set both a calibrator_<SAS ID>_SURIs.txt. and a target_<SAS ID>_SURIs.txt files will be created, which will contain the selected URIs. If in addition data products are staged, they can be retrieved using command wget -i  calibrator_<SAS ID>_SURIs.txt and wget -i  target_<SAS ID>_SURIs.txt


### Inspection plots

For each enabled operation LAnDmARk will create inspection plots. For each selected SAS ID static plots will report on the number of valid dataproducts, and the count of array stations. Also a dynamic summary plot tracking the number and percentage of staged files.



| **Plot name** | **explanation** |
| --- | --- |
| valid\_data\_per\_sas\_id.png | Valid data per SAS ID |
| station\_count\_per\_sas\_id.png | Station count per SAS ID |
| staging\_progress.png | Percentage and number of files staged as a function of time |

## Changelog

Version 1.0

First release. Changes since version pre1.0 are:

- Enabled data selection from the LOFAR LTA
- Enabled data retrieval from the LOFAR LTA; added verification of size and number of data products at staging step
- Enabled direction-independent processing of LOFAR LBA/HBA data via prefactor (v3) pipelines ([https://github.com/lofar-astron/prefactor](https://github.com/lofar-astron/prefactor))
- Enabled to specify the output for data selection

## Getting Help

Bug reports, feature requests and make contributions (e.g. code patches) can be reported by opening a &quot;new issue&quot; ticket on GitHub. Please give as much information (e.g. the software component, version) as you can in the ticket. For bugs, it is extremely useful if a small self-contained code snippet that reproduces the problem is provided.

## Acknowledgements

This software was written by Janis Steinbergs, Kristaps Veitners, under the supervision of Marco Iacobelli and Vladislav Bezrukovs. If you make use of this software to get results that appear in a publication or presentation please include this acknowledgement: &quot;We have made use of LAnDmARk, a tool developed by Janis Steinbergs, Kristaps Veitners.&quot;
