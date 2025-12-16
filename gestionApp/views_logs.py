from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import LogSistema

class LogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LogSistema
    template_name = 'Gestion/Logs/log_list.html'
    context_object_name = 'logs'
    paginate_by = 20
    ordering = ['-fecha_hora']

    def test_func(self):
        # Solo superusuarios o administradores pueden ver los logs
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        search = self.request.GET.get('search')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        accion = self.request.GET.get('accion')

        if search:
            queryset = queryset.filter(
                Q(usuario__username__icontains=search) |
                Q(usuario__first_name__icontains=search) |
                Q(usuario__last_name__icontains=search) |
                Q(detalle__icontains=search) |
                Q(ip_address__icontains=search)
            )

        if fecha_inicio:
            queryset = queryset.filter(fecha_hora__date__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(fecha_hora__date__lte=fecha_fin)
            
        if accion:
            queryset = queryset.filter(accion__icontains=accion)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mantener parámetros de búsqueda en paginación
        context['search'] = self.request.GET.get('search', '')
        context['fecha_inicio'] = self.request.GET.get('fecha_inicio', '')
        context['fecha_fin'] = self.request.GET.get('fecha_fin', '')
        context['accion'] = self.request.GET.get('accion', '')
        return context
