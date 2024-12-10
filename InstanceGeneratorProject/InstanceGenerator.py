import os, random
from AMMMGlobals import AMMMException

class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = 'C:/Users/Utilisateur/OneDrive/Documents/cours_20242025/AMMM/final_project/InstanceGeneratorProject/output'
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances
        maxD = 200

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            with open(instancePath, 'w') as fInstance:

                # Get number of members from the configuration file
                N = self.config.N  
                
                # Calculate number of departments
                D = min(random.randint(2, max(2, N // 4)), maxD)

                # Generate the number of representatives needed from each department
                n = [random.randint(1, N // D) for _ in range(D)]
                
                # Adjust n to make sure the sum of representatives does not exceed N
                total_n = sum(n)
                while total_n > N:
                    idx = random.randint(0, D - 1)
                    if n[idx] > 1:
                        n[idx] -= 1
                    total_n = sum(n)

                # Generate department membership for each member
                d = []
                for dep in range(1, D + 1):
                    d += [dep] * n[dep - 1]
                # Fill the rest with random departments to reach N members
                while len(d) < N:
                    d.append(random.randint(1, D))
                random.shuffle(d)

                # Generate the compatibility matrix
                m = [[0.0] * N for _ in range(N)]
                for i in range(N):
                    for j in range(i, N):
                        if i == j:
                            m[i][j] = 1.0  
                        else:
                            compatibility = round(random.uniform(0, 1), 2)
                            m[i][j] = compatibility
                            m[j][i] = compatibility 

                # Write the instance to the file
                fInstance.write(f'D = {D};\n')
                fInstance.write(f'n = [{" ".join(map(str, n))}];\n')
                fInstance.write(f'N = {N};\n')
                fInstance.write(f'd = [{" ".join(map(str, d))}];\n')
                
                # Write the compatibility matrix
                fInstance.write('m = [\n')
                for row in m:
                    fInstance.write(f'  [{" ".join(map(lambda x: f"{x:.2f}", row))}]\n')
                fInstance.write('];\n')


