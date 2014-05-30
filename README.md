# ABOUT

MiFlux is a destop application that provides users of the [Flux High Performance Computing Cluster](http://arc.research.umich.edu/flux-and-other-hpc-resources/flux/) at the University of Michigan a way to get started using Flux without needing to learn Linux first.

MiFlux is not intended to provide all of the functionality of Flux, nor to meet the needs of advanced HPC users.  Instead, MiFlux is intended to be a set of "training wheels" that researchers can use to quickly and easily get started on Flux.  Unlike other desktop HPC interfaces, MiFlux attempts to expose everything that is happening in order to familiarize the researcher with how the cluster works and how to perform various tasks on the cluster.  As the researcher becomes familiar with the cluster, it is anticipated that they will gradually switch to Linux command line environment or a web-based workflow management system.

In particular, MiFlux is not a replacement for a workflow management systems such as [Apache Airavata](https://airavata.apache.org/).


# BUILDING

## Server

A small amount of code needs to be installed on the cluster for MiFlux to work.  This code can be found in the [server](http://github.com/markmont/miflux/server) directory.

Note that the location of the server code on the cluster is currently hard-coded into the client.


## Client

Currently, the MiFlux client (desktop application) is only installable on MacOS X by developers who are able to compile the toolchain from source.  Instructions are available in the file [client/doc/setup-mac.md](http://github.com/markmont/miflux/client/doc/setup-mac.md)


# SUPPORT

Please send any questions, feedback, requests, or patches to [lsait-ars-hpc-staff@umich.edu](mailto:lsait-ars-hpc-staff@umich.edu).

Additional resources may be available at [http://github.com/markmont/miflux](http://github.com/markmont/miflux)


# LICENSE

MiFlux is Copyright (C) 2014 Regents of The University of Michigan.

MiFlux is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

MiFlux is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with MiFlux.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)

