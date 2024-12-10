import os
from argparse import ArgumentParser
from pathlib import Path
import sys

from datParser import DATParser
from AMMMGlobals import AMMMException
from validateInputDataP2 import ValidateInputData
from ValidateConfig import ValidateConfig
from solvers.solver_Greedy import Solver_Greedy
from solvers.solver_GRASP import Solver_GRASP
from problem.instance import Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self):
        try:
            input_dir = Path(self.config.inputDataFile)
            solution_csv = Path("solutions.csv")  

            input_files = [f for f in input_dir.iterdir() if f.is_file()]

            if self.config.verbose:
                print(f'Found {len(input_files)} input files in {input_dir}')

            for input_file in input_files:
                if self.config.verbose:
                    print(f'Processing file: {input_file.name}')

                data = DATParser.parse(input_file)

                instance = Instance(self.config, data)
                if self.config.verbose:
                    print('Solving the Problem...')
                if instance.checkInstance():
                    initialSolution = None
                    if self.config.solver == 'Greedy' or self.config.solver == 'Random':
                        solver = Solver_Greedy(self.config, instance)
                    elif self.config.solver == 'GRASP':
                        solver = Solver_GRASP(self.config, instance)
                    else:
                        raise AMMMException('Solver %s not supported.' % str(self.config.solver))
                    solution = solver.solve(solution=initialSolution)
                    numSolutionsConstructed, elapsed_time = solver.getPerformanceMetrics()
                    if solution.feasible:
                        print(f'Solution for {input_file.name} : {solution.committee}')
                        solution.saveToFile(
                            solution_csv,  
                            self.config.solver,
                            self.config.localSearch,
                            self.config.policy,
                            numSolutionsConstructed,
                            elapsed_time
                        )
                    else:
                        solution.saveToFile(
                            solution_csv,  
                            self.config.solver,
                            self.config.localSearch,
                            self.config.policy,
                            numSolutionsConstructed,
                            elapsed_time
                        )
                        print(f"Solution for {input_file.name} is infeasible: {solution.notFeasibleReason}")
                else:
                    print(f'Instance {input_file.name} is infeasible.')
                    solution = instance.createSolution()
                    solution.makeInfeasible()
                    solution.saveToFile(
                        solution_csv,  
                        self.config.solver,
                        self.config.localSearch,
                        self.config.policy,
                        numSolutionsConstructed,
                        elapsed_time
                    )
            return 0
        except AMMMException as e:
            print('Exception:', e)
            return 1


if __name__ == '__main__':
    parser = ArgumentParser(description='AMMM Lab Heuristics')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    # Parse the config file
    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)

    # Log details
    if config.verbose:
        print('AMMM Lab Heuristics')
        print('-------------------')
        print(f'Config file: {args.configFile}')
        print(f'Input Data directory: {config.inputDataFile}')

    # Run the main process
    main = Main(config)
    sys.exit(main.run())
