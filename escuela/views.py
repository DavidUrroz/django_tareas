# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions, status
from django.core.mail import send_mail
from demoEscuela.settings import EMAIL_HOST_USER


# from .permissions import IsOwnerOrReadOnly
from .models import Escuela, Estudiante, Maestro, Salon
from .serializers import EscuelaSerializer, EstudianteSerializer, MaestroSerializer, SalonSerializer

# Create your views here.


class EscuelaViewset(ModelViewSet):
    queryset = Escuela.objects.all()
    serializer_class = EscuelaSerializer

    def list(self, request):
        name = request.GET.get("name", None)
        email = request.GET.get("email", None)

        if name and email:
            return Response(
                self.serializer_class(
                    self.queryset.filter(name__icontains=name, email__icontains=email),
                    many=True,
                ).data
            )

        elif name:
            return Response(
                self.serializer_class(
                    self.queryset.filter(name__icontains=name),
                    many=True,
                ).data
            )

        elif email:
            return Response(
                self.serializer_class(
                    self.queryset.filter(email__icontains=email), many=True
                ).data
            )

        else:
            return Response(self.serializer_class(self.queryset, many=True).data)


class EstudianteViewset(ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        # serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            nombre = serializer.validated_data.get("name")
            grado = serializer.validated_data.get("school_grade")
            escuela = serializer.validated_data.get("school")
            salon = serializer.validated_data.get("salon")

            mensaje = f"El sistema de la escuela {escuela.name} ha creado el estudiante {nombre} y fue asignado al salón {salon.codigo} en el grado {grado}"

            try:
                send_mail(
                    "Aviso: Creación de estudiante",
                    mensaje,
                    EMAIL_HOST_USER,
                    [EMAIL_HOST_USER],
                    fail_silently=False
                )
                self.perform_create(serializer)
            except Exception as e:
                return Response({"error": e})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaestroViewset(ModelViewSet):
    queryset = Maestro.objects.all()
    serializer_class = MaestroSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            full_name = serializer.validated_data.get("full_name")
            field_of_study = serializer.validated_data.get("field_of_study")
            years_of_experience = serializer.validated_data.get("years_of_experience")
            on_duty = "Sí" if serializer.validated_data.get("on_duty") else "No"
            if on_duty:
                on_duty = ""
            school = serializer.validated_data.get("school")
            salon = serializer.validated_data.get("salon")

            mensaje = f"""El sistema de la escuela {school.name} ha creado al maestro {full_name} y fue asignado al salón {salon.codigo}:
Campo de especialización: {field_of_study}
Años de experiencia: {years_of_experience}
En servicio: {on_duty}"""

            try:
                send_mail(
                    "Aviso: Creación de maestro",
                    mensaje,
                    EMAIL_HOST_USER,
                    [EMAIL_HOST_USER],
                    fail_silently=False
                )
                self.perform_create(serializer)
            except Exception as e:
                return Response({"error": e})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SalonViewset(ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

    def list(self, request):
        desks_quant = request.GET.get("desks_quant", None)
        fans_quant = request.GET.get("fans_quant", None)
        acrylic_board = request.GET.get("acrylic_board", None)

        if desks_quant:
            return Response(self.serializer_class(self.queryset.filter(desks_quant=desks_quant), many=True).data)
        elif fans_quant:
            return Response(self.serializer_class(self.queryset.filter(fans_quant=fans_quant), many=True).data)
        elif acrylic_board:
            return Response(self.serializer_class(self.queryset.filter(acrylic_board=acrylic_board), many=True).data)
        else:
            return Response(self.serializer_class(self.queryset, many=True).data)