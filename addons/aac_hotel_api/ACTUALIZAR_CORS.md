# 🚀 Guía Rápida: Actualizar Módulo con CORS

## ✅ Cambios Realizados

He agregado soporte completo de CORS a tu módulo `aac_hotel_api`. Ahora tu frontend de React podrá conectarse sin problemas de CORS.

## 📋 Pasos para Aplicar los Cambios

### 1️⃣ Sube los cambios a Git

```bash
cd C:\Users\libra\OneDrive\Desktop\ProyectoConDocker\Coparador\odoo-17You

# Ver cambios
git status

# Agregar todo
git add addons/aac_hotel_api/

# Commit
git commit -m "Fix: Agregar soporte CORS completo a API de Hotel"

# Push
git push
```

### 2️⃣ En Dokploy: Redesplegar

1. Entra a tu proyecto en Dokploy
2. Haz clic en **"Redeploy"** o **"Pull & Restart"**
3. Espera a que termine el despliegue

### 3️⃣ Actualizar el Módulo en Odoo

Una vez que Dokploy haya desplegado:

#### Opción A: Desde la Interfaz de Odoo (Recomendado)

1. Entra a Odoo: `https://odoo-docker-hotel.manager.consulting-sac.com.pe`
2. Ve a **Aplicaciones** (icono de cuadrados)
3. Activa el **Modo Desarrollador**:
   - Configuración → Ajustes → Scroll abajo → "Activar el modo de desarrollador"
4. Busca el módulo **"aac_hotel_api"**
5. Haz clic en **"Actualizar"** (icono de refresh)

#### Opción B: Desde SSH/Terminal de Dokploy

```bash
# Entrar al contenedor de Odoo
docker exec -it odoo bash

# Actualizar el módulo
odoo --config=/etc/odoo/odoo.conf -d odoo --update=aac_hotel_api --stop-after-init

# Salir
exit

# Reiniciar Odoo
docker restart odoo
```

### 4️⃣ Verificar que CORS Funciona

#### Desde el navegador (DevTools Console):

```javascript
// Test rápido de CORS
fetch('https://odoo-docker-hotel.manager.consulting-sac.com.pe/api/hotel/hoteles', {
  headers: {
    'X-API-Key': 'TU_API_KEY_AQUI'
  }
})
.then(r => {
  console.log('✅ CORS funcionando!');
  return r.json();
})
.then(data => console.log(data))
.catch(error => console.error('❌ Error:', error));
```

#### Verificar Headers CORS:

1. Abre DevTools (F12)
2. Ve a la pestaña **Network**
3. Haz una petición a la API desde tu React app
4. Haz clic en la petición
5. Ve a **"Headers"** → **"Response Headers"**
6. Deberías ver:
   ```
   access-control-allow-origin: *
   access-control-allow-methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
   access-control-allow-headers: Content-Type, Authorization, X-API-Key, x-api-key
   ```

### 5️⃣ Probar desde tu React App

Tu código de React ahora debería funcionar sin errores CORS:

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://odoo-docker-hotel.manager.consulting-sac.com.pe',
  headers: {
    'X-API-Key': 'TU_API_KEY',
  }
});

// Probar
api.get('/api/hotel/hoteles')
  .then(response => {
    console.log('✅ Hoteles obtenidos:', response.data);
  })
  .catch(error => {
    console.error('❌ Error:', error);
  });
```

## 🔧 Troubleshooting

### ❌ Todavía veo error CORS

**Solución 1: Forzar actualización del módulo**

```bash
docker exec -it odoo bash
odoo --config=/etc/odoo/odoo.conf -d odoo --update=aac_hotel_api --stop-after-init
exit
docker restart odoo
```

**Solución 2: Limpiar caché del navegador**

- Chrome: Ctrl + Shift + Delete
- Firefox: Ctrl + Shift + Delete  
- Safari: Command + Option + E

**Solución 3: Hard refresh en la página**

- Windows: Ctrl + Shift + R
- Mac: Command + Shift + R

### ❌ El módulo no se actualiza

**Ver logs de Odoo:**

```bash
docker logs -f odoo
```

Busca errores como:
- `SyntaxError` en Python
- `ImportError` 
- `ModuleNotFoundError`

### ❌ API Key no funciona

**Genera una nueva API key:**

1. Entra a Odoo
2. Click en tu nombre (esquina superior derecha)
3. **Preferencias**
4. **Seguridad de la cuenta**
5. **Claves API** → **Nueva clave API**
6. Dale un nombre: "React Frontend"
7. Copia la clave (solo se muestra una vez)
8. Úsala en tu frontend

## ✅ Checklist de Verificación

Marca cada paso conforme lo completes:

- [ ] Cambios subidos a Git (`git push`)
- [ ] Proyecto redesplegado en Dokploy
- [ ] Módulo `aac_hotel_api` actualizado en Odoo
- [ ] Contenedor Odoo reiniciado
- [ ] Headers CORS verificados en DevTools
- [ ] Test desde console del navegador exitoso
- [ ] Frontend React conectándose correctamente
- [ ] Sin errores CORS en la consola
- [ ] Datos de hoteles cargando en tu app

## 📁 Archivos Modificados

```
addons/aac_hotel_api/
├── controllers/
│   ├── __init__.py              ← Actualizado (importa cors_handler)
│   ├── cors_handler.py          ← NUEVO (maneja CORS)
│   ├── lista_hoteles.py         ← Actualizado (decorador @cors_enabled)
│   └── api_auth.py              ← Actualizado (decorador @cors_enabled)
├── CORS_CONFIG.md               ← NUEVO (documentación completa)
└── ACTUALIZAR_CORS.md           ← ESTE ARCHIVO
```

## 🎯 Resultado Esperado

**ANTES:**
```
❌ Access to XMLHttpRequest blocked by CORS policy
❌ No 'Access-Control-Allow-Origin' header
```

**DESPUÉS:**
```
✅ Status: 200 OK
✅ access-control-allow-origin: *
✅ Datos cargados en React correctamente
```

## 📞 Si Necesitas Ayuda

1. **Revisa los logs:**
   ```bash
   docker logs -f odoo | grep -i "cors\|error"
   ```

2. **Verifica que el archivo existe:**
   ```bash
   docker exec -it odoo ls -la /mnt/extra-addons/aac_hotel_api/controllers/
   ```
   Debes ver `cors_handler.py` en la lista

3. **Verifica imports:**
   ```bash
   docker exec -it odoo python3 -c "from odoo.addons.aac_hotel_api.controllers import cors_handler; print('✅ CORS handler importado correctamente')"
   ```

---

**¡Listo! Tu API ahora tiene soporte completo de CORS.** 🎉

Tu frontend de React en `https://hotel.calendar.consulting-sac.consulting-sac.com.pe` ahora podrá consumir la API en `https://odoo-docker-hotel.manager.consulting-sac.com.pe` sin problemas.

