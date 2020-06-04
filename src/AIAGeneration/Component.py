from typing import List, Any

class Component:
    def __init__(self, label, confidence, centerX, centerY, width, height):
        # Given data
        self.label = label
        self.confidence = confidence
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height

        # Calculate corners
        self.x1 = centerX - (width / 2)
        self.x2 = self.x1 + width
        self.y1 = centerY - (height / 2)
        self.y2 = self.y1 + height

        # Calculate area
        self.area = width * height

        # List of inline components initialization:
        self.inLineX: List[Component] = list()
        self.inLineY: List[Component]  = list()

    def overlaps(self, component, tresh=0.5):
        # Calculate overlaping x and y values
        dx = min(self.x2, component.x2) - max(self.x1, component.x1)
        dy = min(self.y2, component.y2) - max(self.y1, component.y1)

        # If any is 0 or less, components do not overlap at all
        if dx <= 0 or dy <= 0:
            return False

        # Calculate overlapping area
        overlappingArea = dx * dy

        # Check if area is less than the treshold (Based on the smallest component), if so, components do not overlap
        if overlappingArea < (min(self.area, component.area) * tresh):
            return False

        # Components Overlap
        return True

    def inLine(self, component, tresh=0.5, axis='x'):
        # Test for horizontal alignment
        if axis == 'x':
            # Calculate overlapping y value
            dy = min(self.y2, component.y2) - max(self.y1, component.y1)

            # If it is 0 or less, components are not in line
            if dy <= 0:
                return False

            # Check if overlap is less than the treshold, if so, components are not in line
            if dy < (min(self.height, component.height) * tresh):
                return False

            # Components Overlap
            return True
        # Test for vertical alignment
        elif axis == 'y':
            # Calculate overlapping x value
            dx = min(self.x2, component.x2) - max(self.x1, component.x1)

            # If it is 0 or less, components are not in line
            if dx <= 0:
                return False

            # Check if overlap is less than the treshold, if so, components are not in line
            if dx < (min(self.width, component.width) * tresh):
                return False

            # Components Overlap
            return True
        # If none of the above cases were trigered, invalid axis given
        raise Exception('Invalid Axis')

    # def roundToScreen(self, screen, xNum, yNum):
    #     # Calculate new corner coordinates
    #     self.x1 = round((max((self.x1 - screen.x1), 0) / screen.width) * xNum)
    #     self.x2 = round((max((self.x2 - screen.x1), 0) / screen.width) * xNum)
    #     self.y1 = round((max((self.y1 - screen.y1), 0) / screen.height) * yNum)
    #     self.y2 = round((max((self.y2 - screen.y1), 0) / screen.height) * yNum)
    #
    #     # Calculate new values based on corners
    #     self.centerX = (self.x1 + self.x2) / 2.0
    #     self.centerY = (self.y1 + self.y2) / 2.0
    #     self.width = self.x2 - self.x1
    #     self.height = self.y2 - self.y1
    #
    #     # Calculate area
    #     self.area = self.width * self.height

    def getInLineComponents(self, componentList: list):
        for component in componentList:
            if self.inLine(component, axis='x'):
                self.inLineX.append(component)
                component.inLineX.append(self)
            if self.inLine(component, axis='y'):
                self.inLineY.append(component)
                component.inLineY.append(self)

    def __str__(self):
        return self.label + ' - (' + "{:.2f}".format(self.x1) + ',' + "{:.2f}".format(self.y1) + ') (' + "{:.2f}".format(self.x2) + ',' + "{:.2f}".format(self.y2) + ')'

    def __repr__(self):
        return self.__str__()
