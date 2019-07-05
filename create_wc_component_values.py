def create_wc_component_values(components, temperatures=[-40, 85]):
    """
    Create a list of values dictionaries that contain the worst case extreme combinations of the supplied
    components data structure.
    The first element is the typical case.
    """

    # temperature to be used as baseline for temperature coefficients
    temperature_nominal = 27

    values_list = []

    # create dictionary with the nominal values
    values = {}
    for component in components.keys():
        values[component] = components[component]['nominal_value']

    # manually add the inductor series resistance
    values['L0_r'] = components['L0']['series_resistance']
    values_list.append(values)

    # create a list with
    values_high_low = {}
    for component in components.keys():

        # calculate the upper bound of the component value
        high = components[component]['nominal_value'] * (1 + components[component]['tolerance'])
        if components[component]['temperature_coefficient'] > 0:
            high = high * (1 + (temperatures[1]-temperature_nominal) * components[component]['temperature_coefficient'])
        else:
            high = high * (1 + (temperatures[0]-temperature_nominal) * components[component]['temperature_coefficient'])

        # calculate the lower bound of the component value
        low = components[component]['nominal_value'] * (1 - components[component]['tolerance'])
        if components[component]['temperature_coefficient'] > 0:
            low = low * (1 + (temperatures[0]-temperature_nominal) * components[component]['temperature_coefficient'])
        else:
            low = low * (1 + (temperatures[1]-temperature_nominal) * components[component]['temperature_coefficient'])

        # create a list with the upper and lower bounds of the component value
        values_high_low[component] = [high, low]

    # add all the permutations of upper and lower bounds
    for i in range(2**len(values_high_low)):

        values = {}
        for j, component in enumerate(values_high_low.keys()):
            values[component] = values_high_low[component][int((i/(2**j))%2)]

        # manually add the inductor series resistance
        values['L0_r'] = components['L0']['series_resistance']

        values_list.append(values)

    return values_list