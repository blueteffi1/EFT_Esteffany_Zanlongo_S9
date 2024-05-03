from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class MiUsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, nombres, apellidos, email, fecha_nacimiento, direccion=None, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            nombre_usuario=nombre_usuario,
            nombres=nombres,
            apellidos=apellidos,
            email=self.normalize_email(email),
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, nombre_usuario, nombres, apellidos, email, fecha_nacimiento, password):
        usuario = self.create_user(
            nombre_usuario=nombre_usuario,
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            fecha_nacimiento=fecha_nacimiento,
            password=password,
        )
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario

class MiUsuario(AbstractBaseUser, PermissionsMixin):
    nombre_usuario = models.CharField(max_length=150, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)

    objects = MiUsuarioManager()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos', 'fecha_nacimiento']

    def __str__(self):
        return self.nombre_usuario

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


    @property
    def is_admin(self):
        return self.is_staff  
    

class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True, verbose_name='Id de la categoria')
    nombre = models.CharField(max_length=60, verbose_name='Categoría')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True, verbose_name='id_producto')
    nombre = models.CharField(max_length=60, verbose_name='Nombre')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class ItemCarrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.producto.precio * self.cantidad


class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(ItemCarrito, related_name='carrito_items')
    creado_en = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())
