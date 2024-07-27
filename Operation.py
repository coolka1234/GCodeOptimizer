import regex as re
class Operation:
    def __init__(self, line) -> None:
        pattern = re.compile(r'G\d+(?:A(?P<A>-?\d*\.?\d+))?(?:F(?P<F>-?\d*\.?\d+))?(?:X(?P<X>-?\d*\.?\d+))?(?:Y(?P<Y>-?\d*\.?\d+))?(?:Z(?P<Z>-?\d*\.?\d+))?')
        match=pattern.search(line)
        print(match)
        # self.X=match['X']
        # self.Y=match['Y']
        # self.Z=match['Z']
        # self.A=match['A']
        # self.F=match['F']
        if match:
            print({k: v for k, v in match.groupdict().items() if v is not None})

Operation('G01X114.6109Z27.0517A18.8177674F1600.0')
 