import struct
import sys
import numpy
from stl import mesh

def main():
    if len(sys.argv) < 3:
        print("Usage: dme_to_stl.py <input> <output>", file=sys.stderr)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    f_in = open(input_file, "rb")
    #DMOD block
    magic = f_in.read(4)
    assert magic.decode("utf-8") == "DMOD", "Not a DME file"
    
    version = struct.unpack("<I", f_in.read(4))[0]
    assert 3 <= version <= 4, "Unsupported DME version"
    
    dmat_length = struct.unpack("<I", f_in.read(4))[0]
    
    #DMAT block
    dmat_data = f_in.read(dmat_length)
    
    #MESH block
    unknown_bytes = f_in.read(16)
    if version == 3:
        bytes_per_vertex, vertex_count, index_size, index_count = struct.unpack("<IIII", f_in.read(16))
        vert_stream_count = 1
    else:
        unknown_bytes += f_in.read(12)
        draw_offset, draw_count, bone_count, unknown = struct.unpack("<IIII", f_in.read(16))
        print("0x{:08x} 0x{:08} 0x{:08x} 0x{:08x}".format(draw_offset, draw_count, bone_count, unknown))
        assert unknown == 0xFFFFFFFF, "{:x}".format(unknown)
        vert_stream_count, index_size, index_count, vertex_count = struct.unpack("<IIII", f_in.read(16))
    
    vertices = [None] * vert_stream_count
    for i in range(vert_stream_count):
        vertices[i] = []
        if version == 4:
            bytes_per_vertex = struct.unpack("<I", f_in.read(4))[0]
        vertex_data = f_in.read(bytes_per_vertex * vertex_count)
        print(bytes_per_vertex / 4)
        struct_format = "<" + "f" * int(bytes_per_vertex / 4)
        for vertex in struct.iter_unpack(struct_format, vertex_data):
            vertices[i].append(vertex[0:3])
    
    indices = []
    index_data = f_in.read(index_size * index_count)

    for index_tuple in struct.iter_unpack("<H", index_data):
        indices.append(index_tuple[0])

    faces = []
    for i in range(0, len(indices), 3):
        faces.append((indices[i], indices[i+1], indices[i+2]))
    faces = numpy.array(faces)
    vertex_array = numpy.array(vertices[0])
    stl_mesh = mesh.Mesh(numpy.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertex_array[f[j], :]

    stl_mesh.save(output_file)
    f_in.close()
    print("Saved to {}".format(output_file))

main()
