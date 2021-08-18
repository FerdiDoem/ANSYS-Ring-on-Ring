import math
#connections
parts = Model.Geometry.Children
##cleanup old connections
connections_children = Model.Connections.GetChildren(DataModelObjectCategory.ConnectionGroup, True)
for child in connections_children:
    child.Delete();
##Checker list for constructed rings, some ugly workaround 
ConstructedRings = [len(DataModel.GetObjectsByName("SupportRing_Body")), len(DataModel.GetObjectsByName("LoadRing_Body"))]
CountRings = sum(ConstructedRings)
##Add Contacts
Model.Connections.AddConnectionGroup()
###Add SupportRingContact
x=0
if ConstructedRings[0] == 1:
    Model.Connections.Children[0].AddContactRegion()
    contact_SupportRing = Model.Connections.Children[0].Children[0]
    E_Names = parts[0].Name + "_Face_Bottom"
    SLoc = DataModel.GetObjectsByName(E_Names)
    TLoc = DataModel.GetObjectsByName("SupportRing_Face_Radius")
    contact_SupportRing.ContactType = ContactType.Frictionless
    contact_SupportRing.SourceLocation = SLoc[0]
    contact_SupportRing.TargetLocation = TLoc[0]
    contact_SupportRing.InterfaceTreatment = ContactInitialEffect.AdjustToTouch
    contact_SupportRing.Name = " to ".join(("SupportRing", parts[x].Name))
###Add Contacts Between Layers
while parts.Count >1 and x < parts.Count-CountRings-1:
    Model.Connections.Children[0].AddContactRegion()
    contact_Layer = Model.Connections.Children[0].Children[x+ConstructedRings[0]]
    contact_Layer.ContactType = ContactType.Bonded
    E_Names_lower = parts[x].Name + "_Face_Top"
    E_Names_upper = parts[x+1].Name + "_Face_Bottom"
    SLoc = DataModel.GetObjectsByName(E_Names_upper)
    TLoc = DataModel.GetObjectsByName(E_Names_lower)
    contact_Layer.SourceLocation = SLoc[0]
    contact_Layer.TargetLocation = TLoc[0]
    contact_Layer.Name = " to ".join((parts[x].Name, parts[x+1].Name))
    x += 1
###Add LoadRingContact
if ConstructedRings[1] == 1:
    Model.Connections.Children[0].AddContactRegion()
    contact_LoadRing = Model.Connections.Children[0].Children[x+ConstructedRings[1]]
    contact_LoadRing.ContactType = ContactType.Frictionless
    E_Names = parts[parts.Count-3].Name + "_Face_Top"
    SLoc = DataModel.GetObjectsByName(E_Names)
    TLoc = DataModel.GetObjectsByName("LoadRing_Face_Radius")
    contact_LoadRing.SourceLocation = SLoc[0]
    contact_LoadRing.TargetLocation = TLoc[0]
    contact_LoadRing.InterfaceTreatment = ContactInitialEffect.AdjustToTouch
    contact_LoadRing.Name = " to ".join((parts[parts.Count-3].Name, "LoadRing"))
