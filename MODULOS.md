# 📦 Gestión de Módulos en Odoo

## ¿Por qué Odoo no reconoce mis módulos?

Para que Odoo reconozca y muestre tus módulos personalizados, necesitas:

1. ✅ Los módulos en la carpeta `addons/` (YA LO TIENES)
2. ✅ El `addons_path` correctamente configurado en `odoo.conf` (YA CORREGIDO)
3. 🔄 **Actualizar la lista de aplicaciones en Odoo**

---

## 🚀 Cómo hacer que Odoo reconozca tus módulos

### Opción 1: Activar el Modo Desarrollador y Actualizar Lista de Aplicaciones

1. **Accede a Odoo** (http://localhost:8090 o tu URL de Dokploy)

2. **Activa el Modo Desarrollador:**
   - Ve a: `Configuración` → `Ajustes`
   - Baja hasta el final de la página
   - Haz clic en **"Activar el modo de desarrollador"**

3. **Actualiza la lista de aplicaciones:**
   - Ve a: `Aplicaciones`
   - Haz clic en el menú de los tres puntos (⋮) en la parte superior
   - Selecciona **"Actualizar lista de aplicaciones"**
   - Confirma la acción

4. **Busca tus módulos:**
   - En el buscador de aplicaciones, escribe el nombre de tu módulo
   - Ejemplo: busca "hotel" o "aac_hotel_api"
   - Deberías ver tus módulos listados

5. **Instala el módulo:**
   - Haz clic en **"Instalar"** en el módulo que desees

---

### Opción 2: Reiniciar con actualización automática (Ya configurado)

El `docker-compose.yml` ya está configurado con:
```yaml
command: ["odoo", "--config=/etc/odoo/odoo.conf", "--update=all"]
```

Esto significa que al reiniciar los contenedores, Odoo automáticamente:
- Cargará la configuración de `odoo.conf`
- Actualizará la lista de módulos

**Para aplicar los cambios:**

```bash
# Detén los contenedores
docker compose down

# Inicia de nuevo
docker compose up -d

# Ver los logs para verificar
docker logs -f odoo
```

---

### Opción 3: Comando manual para actualizar módulos

Si prefieres actualizar manualmente:

```bash
# Opción A: Actualizar lista de módulos
docker exec -it odoo odoo --config=/etc/odoo/odoo.conf --update=all --stop-after-init

# Opción B: Solo actualizar la lista sin instalar
docker exec -it odoo odoo --config=/etc/odoo/odoo.conf --update=base --stop-after-init

# Después reinicia el contenedor
docker restart odoo
```

---

## 📋 Verificar que los módulos estén disponibles

### 1. Verifica que la carpeta está montada:
```bash
docker exec -it odoo ls -la /mnt/extra-addons
```

Deberías ver tus módulos:
- aac_hotel_api
- hotel_management_system
- hotel_management_system_extension
- etc.

### 2. Verifica el addons_path:
```bash
docker exec -it odoo cat /etc/odoo/odoo.conf
```

Deberías ver:
```
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
```

### 3. Verifica los logs de Odoo:
```bash
docker logs odoo
```

Busca líneas como:
```
INFO ? odoo.modules.loading: loading 1 modules...
INFO ? odoo.modules.loading: Module aac_hotel_api loaded
```

---

## ⚠️ Problemas Comunes

### ❌ "El módulo no aparece en la lista"

**Solución:**
1. Verifica que el módulo tenga `__manifest__.py` o `__openerp__.py`
2. Verifica que el `__manifest__.py` tenga la estructura correcta
3. Activa el modo desarrollador y actualiza la lista de aplicaciones
4. Reinicia Odoo: `docker restart odoo`

### ❌ "Error al instalar: dependencia no encontrada"

Tu módulo `aac_hotel_api` depende de:
- `hotel_management_system`
- `hotel_management_system_extension`

**Solución:**
1. Instala primero los módulos base
2. Luego instala `aac_hotel_api`

**Orden de instalación:**
```
1. hotel_management_system
2. hotel_management_system_extension
3. wk_hotel_pos_extension (si es necesario)
4. hotel_qloapps_channel_manager (si es necesario)
5. aac_hotel_api
```

### ❌ "ModuleNotFoundError: No module named 'xyz'"

Si falta alguna librería de Python:

```bash
# Entra al contenedor
docker exec -it odoo bash

# Instala la librería faltante
pip3 install nombre-libreria

# Reinicia Odoo
exit
docker restart odoo
```

---

## 🎯 Checklist para módulos nuevos

Cuando agregues un módulo nuevo:

- [ ] El módulo está en la carpeta `addons/`
- [ ] Tiene archivo `__manifest__.py` válido
- [ ] Tiene archivo `__init__.py` en la raíz del módulo
- [ ] Reiniciaste Odoo o actualizaste la lista de aplicaciones
- [ ] Activaste el modo desarrollador
- [ ] Buscaste el módulo en Aplicaciones

---

## 📚 Comandos útiles

```bash
# Ver logs en tiempo real
docker logs -f odoo

# Reiniciar solo Odoo
docker restart odoo

# Reiniciar todo
docker compose restart

# Entrar al contenedor de Odoo
docker exec -it odoo bash

# Ver módulos instalados
docker exec -it odoo odoo shell --config=/etc/odoo/odoo.conf
# Dentro del shell:
>>> self.env['ir.module.module'].search([('state','=','installed')])
```

---

## ✅ Resumen para Dokploy

Después de subir tus módulos a Git y desplegar en Dokploy:

1. **Los módulos se desplegarán automáticamente** (están en `addons/`)
2. **Accede a tu Odoo en Dokploy**
3. **Activa el modo desarrollador**
4. **Actualiza la lista de aplicaciones**
5. **Instala tus módulos en el orden correcto**

¡Listo! 🚀

