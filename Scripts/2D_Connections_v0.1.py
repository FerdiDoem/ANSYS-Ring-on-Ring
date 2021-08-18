import math
#connections
parts = Model.Geometry.Children
##cleanup old connections
connections_children = Model.Connections.GetChildren(DataModelObjectCategory.ConnectionGroup, True)
for child in connections_children:
    child.Delete();
##Add Contacts
###Add SupportRingContact
Model.Connections.AddContactRegion()
contact_SupportRing = Model.Connections.Children[0].Children[0]
E_Names = parts[0].Name + "_Edge_Bottom"
SLoc = DataModel.GetObjectsByName(E_Names)
TLoc = DataModel.GetObjectsByName("SupportRing_Radius")
contact_SupportRing.ContactType = ContactType.Frictionless
contact_SupportRing.SourceLocation = SLoc[0]
contact_SupportRing.TargetLocation = TLoc[0]
contact_SupportRing.InterfaceTreatment = ContactInitialEffect.AdjustToTouch
contact_SupportRing.Name = "SupportRing to E0"
###Add Contacts Between Layers
x=0
while parts.Count >3 and x < parts.Count-3:
    Model.Connections.Children[0].AddContactRegion()
    contact_Layer = Model.Connections.Children[0].Children[x+1]
    contact_Layer.ContactType = ContactType.Bonded
    E_Names_lower = parts[x].Name + "_Edge_Top"
    E_Names_upper = parts[x+1].Name + "_Edge_Bottom"
    SLoc = DataModel.GetObjectsByName(E_Names_upper)
    TLoc = DataModel.GetObjectsByName(E_Names_lower)
    contact_Layer.SourceLocation = SLoc[0]
    contact_Layer.TargetLocation = TLoc[0]
    contact_Layer.Name = " to ".join((parts[x].Name, parts[x+1].Name))
    x += 1
###Add LoadRingContact
Model.Connections.Children[0].AddContactRegion()
contact_LoadRing = Model.Connections.Children[0].Children[x+1]
contact_LoadRing.ContactType = ContactType.Frictionless
E_Names = parts[parts.Count-3].Name + "_Edge_Top"
SLoc = DataModel.GetObjectsByName(E_Names)
TLoc = DataModel.GetObjectsByName("LoadRing_Radius")
contact_LoadRing.SourceLocation = SLoc[0]
contact_LoadRing.TargetLocation = TLoc[0]
contact_LoadRing.InterfaceTreatment = ContactInitialEffect.AdjustToTouch
contact_LoadRing.Name = " to ".join((parts[parts.Count-3].Name, "LoadRing"))