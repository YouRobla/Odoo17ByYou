# 🚀 Guía de Despliegue en Dokploy

Esta guía te ayudará a desplegar Odoo 17 en Dokploy sin errores.

## ⚠️ Problemas Comunes y Soluciones

### Error: `grep: /etc/odoo/odoo.conf: No such file or directory`

**Causa:** El archivo de configuración de Odoo no se encuentra en el contenedor.

**Solución:**
1. Asegúrate de que la carpeta `config/` con el archivo `odoo.conf` esté en tu repositorio
2. Verifica que el volumen esté correctamente montado en el `docker-compose.yml`
3. Haz commit y push de los cambios al repositorio

### Error: `Database connection failure: could not translate host name "db"`

**Causa:** El contenedor de Odoo no puede encontrar el contenedor de PostgreSQL.

**Solución:**
1. Verifica que ambos servicios estén configurados en el mismo `docker-compose.yml`
2. Asegúrate de que estén en la misma red Docker (ya configurado en este proyecto)
3. Espera a que PostgreSQL esté completamente iniciado (healthcheck configurado)

## 📋 Pasos para Desplegar en Dokploy

### 1. Preparar el Repositorio

Asegúrate de que tu repositorio tenga estos archivos:

```
├── docker-compose.yml
├── .env.example
├── config/
│   └── odoo.conf
├── addons/
│   └── .gitkeep
└── README.md
```

### 2. Configurar Variables de Entorno en Dokploy

En el panel de Dokploy, configura estas variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `ODOO_HOST` | `db` | Nombre del servicio de PostgreSQL |
| `ODOO_USER` | `odoo` | Usuario de la base de datos |
| `ODOO_PASSWORD` | `tu_contraseña_segura` | Contraseña de la base de datos |

⚠️ **IMPORTANTE:** En producción, usa contraseñas seguras y diferentes a las del ejemplo.

### 3. Configurar el Proyecto en Dokploy

1. **Crear un nuevo proyecto:**
   - Tipo: `Docker Compose`
   - Fuente: Tu repositorio de GitHub

2. **Configuración del Build:**
   - Build Path: `/`
   - Compose File: `docker-compose.yml`

3. **Puertos:**
   - Mapea el puerto `8090` (o el que prefieras) al puerto interno `8069`

4. **Volúmenes (opcional en Dokploy, ya configurados en docker-compose.yml):**
   - `odoo-data:/var/lib/odoo`
   - `db-data:/var/lib/postgresql/data`

### 4. Verificar el Despliegue

Después del despliegue:

1. **Verifica los logs:**
   ```
   [OK] Database: Conectado a PostgreSQL
   [OK] HTTP service: Escuchando en el puerto 8069
   ```

2. **Accede a Odoo:**
   - Abre la URL proporcionada por Dokploy
   - Deberías ver la página de inicio de Odoo

3. **Primera vez:**
   - Crea una nueva base de datos
   - Usuario master password: `admin` (configurable en `odoo.conf`)
   - Crea tu cuenta de administrador

## 🔒 Seguridad para Producción

1. **Cambia la contraseña del admin_passwd en `config/odoo.conf`**
2. **Usa contraseñas fuertes para PostgreSQL**
3. **Configura HTTPS con un proxy reverso**
4. **Limita el acceso a puertos sensibles**
5. **Habilita backups automáticos de la base de datos**

## 🐛 Debug

Si algo falla:

1. **Revisa los logs del contenedor de Odoo:**
   ```bash
   docker logs odoo
   ```

2. **Revisa los logs del contenedor de PostgreSQL:**
   ```bash
   docker logs db
   ```

3. **Verifica la conectividad entre contenedores:**
   ```bash
   docker exec odoo ping db
   ```

4. **Verifica que PostgreSQL esté listo:**
   ```bash
   docker exec db pg_isready -U odoo
   ```

## 📞 Soporte

Si continúas teniendo problemas:
1. Verifica que todos los archivos estén commiteados al repositorio
2. Asegúrate de que las variables de entorno estén correctamente configuradas en Dokploy
3. Revisa los logs completos en Dokploy

## ✅ Checklist Pre-Despliegue

- [ ] Archivo `config/odoo.conf` existe y está commiteado
- [ ] Carpeta `addons/` existe (aunque esté vacía)
- [ ] Variables de entorno configuradas en Dokploy
- [ ] `docker-compose.yml` tiene la configuración de red
- [ ] Healthcheck configurado para PostgreSQL
- [ ] Puerto 8090 mapeado correctamente

