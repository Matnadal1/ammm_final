from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):

        # Validate that all input parameters were found
        for paramName in ['D', 'n', 'N', 'd', 'm']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate D (Number of departments)
        D = data.D
        if not isinstance(D, int) or (D <= 0):
            raise AMMMException('D(%s) has to be a positive integer value.' % str(D))

        # Validate n (Number of professors per department)
        data.n = list(data.n)
        n = data.n
        if not isinstance(n, list) or len(n) != D:
            raise AMMMException('n should be a list of size D(%d). Current n is: %s with length %d' % (D, n, len(n)))

        for value in n:
            if not isinstance(value, int) or (value <= 0):
                raise AMMMException('Invalid value(%s) in n. Each value should be a positive integer.' % str(value))

        # Validate N (Total number of professors)
        N = data.N
        if not isinstance(N, int) or (N <= 0):
            raise AMMMException('N(%s) has to be a positive integer value.' % str(N))

        # Validate d (Department membership list for each professor)
        data.d = list(data.d)
        d = data.d
        if not isinstance(d, list) or len(d) != N:
            raise AMMMException('d should be a list of size N(%d). Current d is: %s with length %d' % (N, d, len(d)))

        for value in d:
            if not isinstance(value, int) or (value < 1) or (value > D):
                raise AMMMException('Invalid value(%s) in d. Each value should be an integer between 1 and D(%d).' % (str(value), D))

        # Validate m (Compatibility matrix between professors)
        data.m = list(data.m)
        m = data.m
        if not isinstance(m, list) or len(m) != N:
            raise AMMMException('m should be a list of size N(%d). Current m has length %d.' % (N, len(m)))

        for row in m:
            row = list(row)
            if not isinstance(row, list) or len(row) != N:
                raise AMMMException('Each row in m should be a list of size N(%d). Current row has length %d.' % (N, len(row)))

            for value in row:
                if not isinstance(value, (int, float)) or (value < 0.0) or (value > 1.0):
                    raise AMMMException('Invalid value(%s) in m. Each value should be a float between 0.0 and 1.0.' % str(value))
