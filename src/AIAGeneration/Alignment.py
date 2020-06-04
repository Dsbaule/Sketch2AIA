from .Component import Component

def align(componentList, vertical = True):
    # Create a tuple for current alignment:
    curAlignment = ('vertical' if vertical else 'horizontal', list())

    # Sort list based on current alignment (By x for horizontal, by y for vertical)
    if vertical:
        componentList.sort(key=lambda x: x.y1)
    else:
        componentList.sort(key=lambda x: x.x1)

    # While componentList is not empty
    # print(str(len(componentList)) + str(componentList))
    while componentList:
        # Pop first component
        curComponent = componentList.pop(0)

        # Check if any components in list are in line with current component in the opposite axis
        toAnalyze: list[Component] = list()
        newComponentList: list[Component] = list()

        toAnalyze.append(curComponent)

        while toAnalyze:
            curAnalyzedComponent = toAnalyze.pop(0)
            #print(curAnalyzedComponent.label + ' in the ' + ('horizontal' if vertical else 'vertical') + ' aligned with:')
            for component in componentList:
                if curAnalyzedComponent.inLine(component, axis=('x' if vertical else 'y')):
                    #print('\t' + component.label)
                    if (component not in newComponentList) and (component not in toAnalyze):
                        newComponentList.append(component)
                        toAnalyze.append(component)

        # If list is not empty, align these first
        if newComponentList:
            componentList = [x for x in componentList if x not in newComponentList]
            newComponentList.append(curComponent)
            curAlignment[1].append(align(newComponentList, not vertical))
        # Otherwise, add component to alignment
        else:
            curAlignment[1].append(curComponent)

    return curAlignment