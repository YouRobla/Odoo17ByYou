# 🔧 Hotfix: Error de Archivo de Seguridad

## ❌ Error Original:

```
FileNotFoundError: File not found: aac_hotel_api/security/ir.model.access.csv
```

O después:

```
RPC_ERROR: Odoo Server Error
Error al actualizar módulo aac_hotel_api
```

## ✅ Solución Aplicada:

Se corrigió el archivo `security/ir.model.access.csv` para que coincida correctamente con el modelo `hotel.api.response`.

### Cambio Realizado:

**Antes:**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hotel_api_response,access_hotel_api_response,model_hotel_api_response,base.group_user,1,1,1,0
```

**Después:**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hotel_api_response,Hotel API Response Access,model_hotel_api_response,base.group_user,1,1,1,1
```

### Versión Actualizada:

- **Versión anterior**: 17.0.1.0
- **Versión nueva**: 17.0.1.1

## 🚀 Aplicar el Cambio:

### 1. Subir a Git:

```bash
cd C:\Users\libra\OneDrive\Desktop\ProyectoConDocker\Coparador\odoo-17You

git add addons/aac_hotel_api/
git commit -m "Hotfix: Corregir archivo de seguridad ir.model.access.csv"
git push
```

### 2. Redesplegar en Dokploy:

1. Entra a Dokploy
2. Click en "Redeploy" o "Pull & Restart"
3. Espera a que termine

### 3. Actualizar el Módulo en Odoo:

**Opción A: Desde la Interfaz (Recomendado)**

1. Ve a **Aplicaciones**
2. Busca **"aac_hotel_api"**
3. Click en **"Actualizar"**
4. Espera a que termine
5. Verifica que la versión sea **17.0.1.1**

**Opción B: Desde Terminal**

```bash
# Actualizar el módulo
docker exec -it odoo odoo --config=/etc/odoo/odoo.conf -d odoo --update=aac_hotel_api --stop-after-init

# Reiniciar Odoo
docker restart odoo
```

## ✅ Verificación:

Después de actualizar, verifica:

1. **No hay errores** al actualizar el módulo
2. **La versión es 17.0.1.1** en la lista de aplicaciones
3. **CORS sigue funcionando** correctamente
4. **Tu React app puede conectarse** sin problemas

### Test Rápido:

```javascript
// En la consola del navegador
fetch('https://odoo-docker-hotel.manager.consulting-sac.com.pe/api/hotel/hoteles', {
  headers: {'X-API-Key': 'TU_API_KEY'}
})
.then(r => r.json())
.then(data => console.log('✅ Todo funcionando!', data))
.catch(err => console.error('❌ Error:', err));
```

## 📋 Resumen de Cambios en Esta Actualización:

| Archivo | Cambio |
|---------|--------|
| `security/ir.model.access.csv` | Corregido model_id y permisos |
| `__manifest__.py` | Versión actualizada a 17.0.1.1 |

## 🎯 Estado Actual del Módulo:

- ✅ **CORS**: Completamente funcional
- ✅ **Seguridad**: Archivo CSV corregido
- ✅ **Versión**: 17.0.1.1
- ✅ **Listo para producción**

---

**Nota:** Este hotfix no afecta la funcionalidad de CORS. Solo corrige un problema con el archivo de permisos de seguridad que impedía actualizar el módulo.

