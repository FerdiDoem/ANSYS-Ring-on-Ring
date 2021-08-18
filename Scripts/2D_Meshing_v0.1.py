import math
#meshing
##cleanup old Mesh Data
mesh_children = Model.Mesh.GetChildren(DataModelObjectCategory.Sizing, True)
for child in mesh_children:
    child.Delete()
mesh_children = Model.Mesh.GetChildren(DataModelObjectCategory.AutomaticMethod, True)
for child in mesh_children:
    child.Delete()
## get parts to mesh
parts = Model.Geometry.Children
##Meshing
x=0
###meshing for Layer
while x < parts.Count-2:
    MeshAssign = Model.Mesh.AddSizing()
    EleSize = parts[x].PropertyByName("BoundingBoxLengthY").InternalValue / 2
    MeshAssign.ElementSize = Quantity(" ".join((str(EleSize), "[mm]")))
    MeshAssign.Location = DataModel.GetObjectsByName(parts[x].Name + "_Body")[0]
    MeshAssign.Name = parts[x].Name + "_Mesh"
    MeshMethod = Model.Mesh.AddAutomaticMethod()
    MeshMethod.Location = DataModel.GetObjectsByName(parts[x].Name + "_Body")[0]
    MeshMethod.Method = MethodType.QuadTri
    MeshMethod.Name = parts[x].Name + "_Method"
    x += 1
###meshing for rings
MeshAssign = Model.Mesh.AddSizing()
EleSize = parts[parts.Count-3].PropertyByName("BoundingBoxLengthY").InternalValue / 2
MeshAssign.ElementSize = Quantity(" ".join((str(EleSize), "[mm]")))
MeshAssign.Location = DataModel.GetObjectsByName(parts[x].Name + "_Radius")[0]
MeshAssign.Name = parts[x].Name + "_Mesh"
MeshAssign = Model.Mesh.AddSizing()
EleSize = parts[0].PropertyByName("BoundingBoxLengthY").InternalValue / 2
MeshAssign.ElementSize = Quantity(" ".join((str(EleSize), "[mm]")))
MeshAssign.Location = DataModel.GetObjectsByName(parts[x+1].Name + "_Radius")[0]
MeshAssign.Name = parts[x+1].Name + "_Mesh"
#Model.Mesh.GenerateMesh()