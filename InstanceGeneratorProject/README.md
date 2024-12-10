# Instance generator
Generate instances based on read configuration.

## Describing an instance
The instance is randomly generated given the parameters in the configuration file (described later).
Each instance is then used to run the experiment.
```python
D=2;                        # Number of departments.

n=[4 1];                    # Vector describing how many teacher should belong to
                            # each department (2 departments in this case) in the
                            # final solution,
                            # Eg. 4 teacher from dep. 1 and 1 from dep. 2

N=10;                       # Number of teachers in the experiment. Each teacher
                            # is assigned an id ranging from 1 to N.

d=[1 1 1 2 1 2 1 2 2 1];    # Vector describing the department of each teacher.
                            # The index corresponds to the teacher ID.
m = [
  [1.00 0.55 0.92 0.90 0.24 0.99 0.12 0.04 0.52 0.68]
  [0.55 1.00 0.15 0.59 0.86 0.32 0.57 0.72 0.88 0.12]
  [0.92 0.15 1.00 0.24 0.91 0.22 0.26 0.59 0.91 0.18]
  [0.90 0.59 0.24 1.00 0.20 0.27 0.70 0.87 0.22 0.36]
  [0.24 0.86 0.91 0.20 1.00 0.79 0.09 0.19 0.52 0.18]
  [0.99 0.32 0.22 0.27 0.79 1.00 0.15 0.25 0.98 0.61]
  [0.12 0.57 0.26 0.70 0.09 0.15 1.00 0.93 0.28 0.75]
  [0.04 0.72 0.59 0.87 0.19 0.25 0.93 1.00 0.95 0.35]
  [0.52 0.88 0.91 0.22 0.52 0.98 0.28 0.95 1.00 0.21]
  [0.68 0.12 0.18 0.36 0.18 0.61 0.75 0.35 0.21 1.00]
];                          # Compatibility matrix describing the relationship of
                            # each teacher with all the others.
```

## Describing the configuration file
```python
instancesDirectory = output;
fileNamePrefix = project50;
fileNameExtension = dat;
numInstances = 10;
N = 10;                     # Number of teachers in the experiment
```

## How to run the code
`$ python -m InstanceGeneratorProject.Main`

## Authors
The original code from professor Luis Velasco was adapted to be used to run experiments by:
- Virginia Nicosia
- Mathias Nadal