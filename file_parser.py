def get_data_from_file(file_name: str = "test.obj"):
    objFile = open('files/' + file_name, 'r')

    vertexes = []
    planes = []

    for line in objFile:
        split = line.split()
        # if blank line, skip
        if not len(split):
            continue
        if split[0] == "v":
            vertexes.append([float(i) for i in split[1:]])
        elif split[0] == "f":
            plane = [int(split[i].split('/')[0]) - 1 for i in range(1, 4)]
            planes.append(plane)

    print("Total vertexes: " + str(len(vertexes)))
    print("Total planes: " + str(len(planes)))

    objFile.close()

    return [vertexes, planes]