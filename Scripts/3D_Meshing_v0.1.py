import math
#meshing
##cleanup old Mesh Data
Mesh_children = Model.Mesh.GetChildren(DataModelObjectCategory.Sizing, True)
Mesh_children2 = Model.Mesh.GetChildren(DataModelObjectCategory.AutomaticMethod, True)
for child in Mesh_children:
    child.Delete()
for child2 in Mesh_children2:
    child2.Delete()
##Checker list for constructed rings
ConstructedRings = [len(DataModel.GetObjectsByName("SupportRing_Body")), len(DataModel.GetObjectsByName("LoadRing_Body"))]
CountRings = sum(ConstructedRings)
## get parts to mesh
parts = Model.Geometry.Children
##Meshing
x=0
###meshing for Layer
while x < parts.Count-CountRings:
    with Transaction():
        MeshSizing = Model.Mesh.AddSizing()
        EleSize = parts[x].PropertyByName("BoundingBoxLengthY").InternalValue
        MeshSizing.ElementSize = Quantity(" ".join((str(EleSize), "[mm]")))
        MeshSizing.Location = DataModel.GetObjectsByName(parts[x].Name + "_Body")[0]
        MeshSizing.Name = parts[x].Name + "_Sizing"
        if CountRings == 2:
            MeshMethod = Model.Mesh.AddAutomaticMethod()
            MeshMethod.Location = MeshSizing.Location
            MeshMethod.Method = MethodType.Sweep
            MeshMethod.SourceTargetSelection = 4
            MeshMethod.ElementOption = SweepElementOptionType.SolidShell
            MeshMethod.SweepNumberDivisions = 4
            MeshMethod.SourceLocation = DataModel.GetObjectsByName(parts[x].Name + "_Face_Top")[0]
            MeshMethod.Name = parts[x].Name + "_Method"
    x += 1
###meshing for rings
####support ring
if ConstructedRings[0]:
    GeometryRings = Model.Geometry.Children[x+1].Properties
    with Transaction():
        MeshSizing = Model.Mesh.AddSizing()
        EleSize = parts[0].PropertyByName("BoundingBoxLengthY").InternalValue
        MeshSizing.ElementSize = Quantity(" ".join((str(EleSize), "[mm]")))
        MeshSizing.Location = DataModel.GetObjectsByName("SupportRing_Face_Radius")[0]
        MeshSizing.Name = parts[x].Name + "_Sizing"
####load ring
if ConstructedRings[1]:
    with Transaction():
        MeshSizing = Model.Mesh.AddSizing()
        EleSize = parts[parts.Count-CountRings].PropertyByName("BoundingBoxLengthY").InternalValue
        MeshSizing.ElementSize = Quantity(" ".join((str(EleSize), "[mm]")))
        MeshSizing.Location = DataModel.GetObjectsByName("LoadRing_Face_Radius")[0]
        MeshSizing.Name = parts[x+1].Name + "_Sizing"
Model.Mesh.GenerateMesh()
