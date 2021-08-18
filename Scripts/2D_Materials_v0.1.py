import math
#material assignments
Model.Materials.RefreshMaterials()
##cleanup old assignments
materialAssignments_children = Model.Materials.GetChildren(DataModelObjectCategory.MaterialAssignment, True)
for child in materialAssignments_children:
    child.Delete()
##Assigning the material name
MatList = Model.Materials.GetChildren(DataModelObjectCategory.Material, True)

for mat in MatList:
    try:
        Part = mat.Name.split( )[0]
        MatAssign = Model.Materials.AddMaterialAssignment()
        MatAssign.Material = mat.Name
        MatAssign.NonlinearEffects = False
        MatAssign.Location = DataModel.GetObjectsByName(Part + "_Body")[0]
    except:
        MatAssign.Suppressed = True

