from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExtentSerializer, PolygonSerializer, GeometrySerializer
from arcgis.geometry import Geometry, SpatialReference

class CalculateAreaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GeometrySerializer(data=request.data)
        if serializer.is_valid():
            geometry_data = serializer.validated_data['geometry']
            area_unit = serializer.validated_data['areaUnit']

            areas = []
            for item in geometry_data:
                if 'xmin' in item and 'xmax' in item and 'ymin' in item and 'ymax' in item:
                    # If extent coordinates are provided
                    extent_serializer = ExtentSerializer(data=item)
                    if extent_serializer.is_valid():
                        xmin = extent_serializer.validated_data['xmin']
                        xmax = extent_serializer.validated_data['xmax']
                        ymin = extent_serializer.validated_data['ymin']
                        ymax = extent_serializer.validated_data['ymax']
                        srs = extent_serializer.validated_data['srs']
                        
                        spatial_reference = SpatialReference(wkid=srs)
                        extent_geometry = Geometry({
                            "rings": [
                                [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin], [xmin, ymin]]
                            ],
                            "spatialReference": spatial_reference
                        })
                        area = extent_geometry.area
                        areas.append(area)
                elif 'rings' in item:
                    # If polygon coordinates are provided
                    polygon_serializer = PolygonSerializer(data=item)
                    if polygon_serializer.is_valid():
                        coordinates = polygon_serializer.validated_data['rings']
                        srs = polygon_serializer.validated_data['srs']

                        polygon_geometry = Geometry({
                            "rings": coordinates,
                            "spatialReference": {"wkid": srs}
                        })
                        area = polygon_geometry.area
                        areas.append(area)
            
            # Convert areas to specified unit
            # converted_areas = []
            # for area in areas:
            #     converted_area = self.convert_area(area, area_unit)
            #     converted_areas.append(converted_area)
            
            # return Response({'areas': converted_areas})
            return Response({'areas': areas})
        return Response(serializer.errors, status=400)

    def convert_area(self, area, target_unit):
        pass
