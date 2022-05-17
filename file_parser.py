def get_data_from_file(file_name: str = "test.obj", absolute: bool = False):
    if absolute:
        objFile = open(file_name, 'r')
    else:
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

    print("Statistic for {0} file".format(file_name))
    print("Total vertexes: " + str(len(vertexes)))
    print("Total planes: " + str(len(planes)) + "\n")

    objFile.close()

    return [vertexes, planes]


def safe_data_from_editor(vertexes, planes, file_name):
    print("Saving...")
    with open(file_name, "w") as objFile:
        for i in vertexes:
            objFile.write("v {0} {1} {2}\n".format(i[0], i[1], i[2]))

        for i in planes:
            objFile.write("f {0} {1} {2}\n".format(find_index(vertexes, i.anchor),
                                                   find_index(vertexes, i.p1),
                                                   find_index(vertexes, i.p2)))

        print("Statistic for save {0} file".format(file_name))
        print("Total vertexes: " + str(len(vertexes)))
        print("Total planes: " + str(len(planes)))
    print("Success!" + "\n")


def find_index(vertexes, vertex):
    for i in range(len(vertexes)):
        if (vertexes[i] == vertex).all():
            return i + 1
