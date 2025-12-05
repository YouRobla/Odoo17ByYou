# Odoo 17 con Docker Compose

Este repositorio despliega una instancia de **Odoo 17** junto con **PostgreSQL 15** utilizando Docker Compose. Es ideal para entornos de desarrollo, pruebas y producción con Dokploy.

---

## 🧾 ¿Qué es Odoo?

**Odoo** es un conjunto de aplicaciones empresariales de código abierto que cubre todas las necesidades de gestión de una empresa: desde CRM, ventas, contabilidad, inventario y recursos humanos, hasta manufactura, comercio electrónico y más.

### ✅ Ventajas de usar Odoo

- Plataforma modular: puedes activar solo los módulos que necesites.
- Interfaz moderna y amigable.
- Altamente personalizable con módulos propios.
- Comunidad activa y soporte empresarial disponible.
- Código abierto, sin costos de licencia para la versión Community.

---

## 🚀 Cómo iniciar

### Opción 1: Docker Compose Local

1. Verifica o crea el archivo `.env` con el siguiente contenido:

   ```env
   ODOO_HOST=db
   ODOO_USER=odoo
   ODOO_PASSWORD=odoo
   ```

2. Levanta los servicios:

   ```bash
   docker compose up -d
   ```

3. Accede a Odoo en tu navegador:

   ```
   http://localhost:8090
   ```

### Opción 2: Despliegue en Dokploy

1. **En Dokploy, crea un nuevo proyecto tipo "Docker Compose"**

2. **Conecta tu repositorio de GitHub**

3. **Configura las variables de entorno en Dokploy:**
   - `ODOO_HOST=db`
   - `ODOO_USER=odoo`
   - `ODOO_PASSWORD=odoo` (usa una contraseña segura en producción)

4. **Asegúrate de que los siguientes archivos existan:**
   - `config/odoo.conf` (ya incluido en el repositorio)
   - `addons/` (carpeta para módulos adicionales)
   - `.env.example` (plantilla de variables de entorno)

5. **Despliega el proyecto**

6. **Accede a Odoo:**
   - Dokploy te proporcionará una URL pública
   - O accede via: `http://tu-dominio:8090`

---

## 🔐 Credenciales por defecto

* **Usuario:** `admin`
* **Contraseña:** `admin`

---

## 🛑 Detener los servicios

```bash
docker compose down
```

---

## ✅ Requisitos

* Docker
* Docker Compose

---

## ⚙️ Personalización

Puedes cambiar configuraciones como credenciales u otras opciones desde los archivos `.env` y `docker-compose.yml`.

---

## 📌 Notas

* Odoo expone su servicio en el puerto interno **8069**, pero se mapea al puerto **8090** externamente.
* Se recomienda usar un proxy reverso con HTTPS para producción.
* El archivo `config/odoo.conf` contiene la configuración de Odoo.
* La carpeta `addons/` es para módulos personalizados de Odoo.

## 🔧 Solución de problemas en Dokploy

Si obtienes errores como:
- `grep: /etc/odoo/odoo.conf: No such file or directory`
- `Database connection failure: could not translate host name "db"`

**Soluciones:**

1. **Asegúrate de que las variables de entorno estén configuradas en Dokploy**
2. **Verifica que ambos servicios (odoo y db) estén corriendo**
3. **Asegúrate de que la carpeta `config/` con `odoo.conf` esté en el repositorio**
4. **Verifica que los servicios estén en la misma red Docker**
5. **Espera a que la base de datos esté completamente iniciada antes de que Odoo se conecte** (esto está configurado con healthcheck)

## 🌐 Configuración de Red

El docker-compose.yml incluye:
- Red bridge personalizada (`odoo-network`) para comunicación entre contenedores
- Healthcheck en PostgreSQL para asegurar que esté listo antes de iniciar Odoo
- Valores por defecto para todas las variables de entorno


