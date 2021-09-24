import math
#material assignments
Model.Materials.RefreshMaterials()
##cleanup old assignments, "\" is a escape command, here for next line
materialAssignments_children = \
Model.Materials.GetChildren(DataModelObjectCategory.MaterialAssignment, True)

for child in materialAssignments_children:
    child.Delete()
##Gather all materials and create a reference list to iterate over
MatList = Model.Materials.GetChildren(DataModelObjectCategory.Material, True)
##Assigning the material name
for mat in MatList:
    try:
        Part = mat.Name.split( )[0]
        MatAssign = Model.Materials.AddMaterialAssignment()
        MatAssign.Material = mat.Name
        MatAssign.NonlinearEffects = False
        MatAssign.Location = DataModel.GetObjectsByName(Part + "_Body")[0]
    except:
        MatAssign.Suppressed = True