class Parser:
    def parseAngle(angle, from_, to_):
        if from_ <= angle and angle <= to_:
            return angle
        if angle > to_:
            return to_
        else:
            return from_