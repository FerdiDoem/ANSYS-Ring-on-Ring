#symmetry elements
##cleanup old symmetry data
Symmetry_children0 = Model.Mesh.GetChildren(DataModelObjectCategory.MatchControl, True)
Symmetry_children1 = Model.Symmetry.GetChildren(DataModelObjectCategory.SymmetryRegion, True)
Symmetry_children2 = Model.Symmetry.GetChildren(DataModelObjectCategory.CyclicRegion, True)
Symmetry_children3 = Model.CoordinateSystems.GetChildren(DataModelObjectCategory.CoordinateSystem, True)

for child in Symmetry_children0:
    child.Delete()
for child in Symmetry_children1:
    child.Delete()
for child in Symmetry_children2:
    child.Delete()
for child in Symmetry_children3:
    #throws a error message because the global coordinate system cannot be deleted
    child.Delete()

##Find out which symmetry is needed
###get the named selections
named_selection = Model.NamedSelections.GetChildren(DataModelObjectCategory.NamedSelection, True)
###initalize some lists
half_SymRegions = []
mult_CyclicSymRegionsHigh = []
mult_CyclicSymRegionsLow = []
###check which symmetry is present and sort them into the lists
for selection in named_selection:
    if selection.Name.EndsWith('_SymPlane'):
        half_SymRegions.append(selection.Name)
    elif selection.Name.EndsWith('_SymPlaneHigh'):
        mult_CyclicSymRegionsHigh.append(selection.Name)
    elif selection.Name.EndsWith('_SymPlaneLow'):
        mult_CyclicSymRegionsLow.append(selection.Name)
##when symmetry are needed, add corresponding coordinate systems and symmetry elements
assert (half_SymRegions or mult_CyclicSymRegionsHigh), 'No symmetry detected.'
### half symmetry
if half_SymRegions:
    for regions in half_SymRegions:
        ###the coordinate system
        coord_region = Model.CoordinateSystems.AddCoordinateSystem()
        coord_region.Name = regions.Split('_')[0] + '_SymmetryCoordinatesystem'
        coord_region.OriginDefineBy = CoordinateSystemAlignmentType.Component
        coord_region.OriginLocation = DataModel.GetObjectsByName(regions)[0]
        coord_region.PrimaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalY
        coord_region.SecondaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalX
        ###the symmetry plane
        symmetry_region = Model.Symmetry.AddSymmetryRegion()
        symmetry_region.Name = regions.Split('_')[0] + ' _Symmetry'
        symmetry_region.Location = DataModel.GetObjectsByName(regions)[0]
        symmetry_region.CoordinateSystem = coord_region
        symmetry_region.PeriodicityDirection = PeriodicityDirectionType.ZAxis
else:
    ###the coordinate system, here just one!
    coord_region = Model.CoordinateSystems.AddCoordinateSystem()
    coord_region.Name =  'Cylindrical_SymmetryCoordinatesystem'
    coord_region.CoordinateSystemType = CoordinateSystemTypeEnum.Cylindrical
    coord_region.OriginDefineBy = CoordinateSystemAlignmentType.Component
    coord_region.OriginLocation = DataModel.GetObjectsByName(mult_CyclicSymRegionsHigh[0].Split('_')[0]+'_Edge_SymPlaneRotaAxis')[0]
    coord_region.SecondaryAxis = CoordinateSystemAxisType.PositiveZAxis
    coord_region.SecondaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalY
    for regions in zip(mult_CyclicSymRegionsHigh,mult_CyclicSymRegionsLow):
        ###the symmetry plane
        high,low = regions
        symmetry_region = Model.Symmetry.AddCyclicRegion()
        symmetry_region.Name = high.Split('_')[0]+'_Symmetry'
        symmetry_region.LowBoundaryLocation =  DataModel.GetObjectsByName(low)[0]
        symmetry_region.HighBoundaryLocation = DataModel.GetObjectsByName(high)[0]
        symmetry_region.CoordinateSystem = coord_region
        ###add matchcontrol for the meshing
        match_control = Model.Mesh.AddMatchControl()
        match_control.Name = high.Split('_')[0]+'_MatchControl'
        match_control.HighGeometrySelection = DataModel.GetObjectsByName(high)[0]
        match_control.LowGeometrySelection = DataModel.GetObjectsByName(low)[0]
        match_control.RotationAxis = coord_region
