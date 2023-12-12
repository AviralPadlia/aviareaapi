from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExtentSerializer, PolygonSerializer, GeometrySerializer
# from arcgis.geometry import Geometry, SpatialReference

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
                        x_coords = [xmin, xmin, xmax, xmax]
                        y_coords = [ymin, ymax, ymax, ymin]
                        
                        area = 0

                        # Use Shoelace formula to calculate the area
                        for i in range(4):
                            j = (i + 1) % 4
                            area += x_coords[i] * y_coords[j]
                            area -= x_coords[j] * y_coords[i]

                        area = abs(area) / 2
                        areas.append(area)
            return Response({'areas': areas})
        return Response(serializer.errors, status=400)


