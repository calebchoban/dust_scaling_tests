# MUSIC

## Usage

To compile:

```console
cd compile
HPC=tscc make
```

To run:

```console
cd run/{example_name}
../../compile/bin/MUSIC music.conf
```

## Notes

The following dependencies are needed to compile MUSIC:
- FFTW (both 2 and 3 are okay)
- GSL
- HDF5

To compile MUSIC on another HPC:
- Edit the Makefile according to the specific HPC
    - Make sure the MPI compiler is set correctly
    - Make sure the OpenMP option is set correctly
    - Make sure dependency paths are included
- `make`

Details of configuration file parameters could be found in the User's Manual.

## Links

- [Code repo](https://bitbucket.org/ohahn/music/)
- [User's Manual](https://bitbucket.org/ohahn/music/downloads/MUSIC_Users_Guide.pdf)
