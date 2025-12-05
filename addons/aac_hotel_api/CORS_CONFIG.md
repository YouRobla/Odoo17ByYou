# 🌐 Configuración de CORS para la API de Hotel

## ¿Qué es CORS?

**CORS** (Cross-Origin Resource Sharing) es un mecanismo de seguridad que permite que un navegador web solicite recursos de un dominio diferente al que sirve la página web.

## 🔧 Problema Resuelto

### Error Original:
```
Access to XMLHttpRequest at 'https://odoo-docker-hotel.manager.consulting-sac.com.pe/api/hotel/hoteles' 
from origin 'https://hotel.calendar.consulting-sac.consulting-sac.com.pe' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

### Solución Implementada:

Hemos agregado soporte completo de CORS a todos los endpoints de la API mediante:

1. **Nuevo archivo `cors_handler.py`** con:
   - Decorador `@cors_enabled` para endpoints
   - Función `add_cors_headers()` para agregar headers CORS
   - Manejo de peticiones OPTIONS (preflight)

2. **Headers CORS configurados:**
   ```python
   'Access-Control-Allow-Origin': '*'
   'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
   'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key, x-api-key'
   'Access-Control-Max-Age': '86400'  # 24 horas
   'Access-Control-Allow-Credentials': 'true'
   ```

## 📦 Endpoints Actualizados con CORS

### ✅ Endpoints de Hoteles (`lista_hoteles.py`):
- `GET /api/hotel/hoteles` - Lista todos los hoteles
- `GET /api/hotel/hoteles/<id>` - Obtiene un hotel por ID
- `GET /api/hotel/hoteles/search` - Búsqueda de hoteles
- `GET /api/hotel/debug/data` - Información de debug
- `GET /api/hotel/hoteles/<id>/cuartos` - Habitaciones de un hotel
- `GET /api/hotel/cuartos` - Lista todas las habitaciones
- `GET /api/hotel/cuartos/<id>` - Obtiene una habitación por ID

### ✅ Endpoints de Autenticación (`api_auth.py`):
- `POST /api/auth/generate_key` - Generar API key
- `GET /api/auth/my_keys` - Obtener mis API keys
- `POST /api/auth/revoke_key/<id>` - Revocar API key
- `POST /api/auth/validate` - Validar API key
- `GET /api/auth/test_key` - Probar API key

### 🔄 Todos los endpoints ahora soportan:
- Método `OPTIONS` (preflight request)
- Headers CORS automáticos en todas las respuestas

## 🚀 Cómo Usar desde React/Frontend

### Ejemplo con Axios:

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://odoo-docker-hotel.manager.consulting-sac.com.pe',
  headers: {
    'X-API-Key': 'tu_api_key_aqui',
    'Content-Type': 'application/json',
  }
});

// GET request
const getHoteles = async () => {
  try {
    const response = await api.get('/api/hotel/hoteles');
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};

// POST request
const validateApiKey = async (apiKey) => {
  try {
    const response = await api.post('/api/auth/validate', {
      api_key: apiKey
    });
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### Ejemplo con Fetch:

```javascript
// GET request
fetch('https://odoo-docker-hotel.manager.consulting-sac.com.pe/api/hotel/hoteles', {
  method: 'GET',
  headers: {
    'X-API-Key': 'tu_api_key_aqui',
    'Content-Type': 'application/json',
  }
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// POST request
fetch('https://odoo-docker-hotel.manager.consulting-sac.com.pe/api/auth/validate', {
  method: 'POST',
  headers: {
    'X-API-Key': 'tu_api_key_aqui',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    api_key: 'key_a_validar'
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

## 🔐 Configuración de Seguridad (Producción)

Por defecto, CORS está configurado con `'Access-Control-Allow-Origin': '*'` para permitir cualquier origen. 

### Para restringir a dominios específicos en producción:

Puedes configurar CORS dinámicamente desde la interfaz de Odoo:

1. Ve a **Configuración → Parámetros del Sistema**
2. Agrega estos parámetros:

| Clave | Valor |
|-------|-------|
| `aac_hotel_api.cors_allowed_origins` | `https://hotel.calendar.consulting-sac.com.pe` |
| `aac_hotel_api.cors_allowed_methods` | `GET, POST, PUT, DELETE, OPTIONS` |
| `aac_hotel_api.cors_allowed_headers` | `Content-Type, Authorization, X-API-Key` |

### Múltiples dominios:

Para permitir múltiples dominios, necesitarás modificar `cors_handler.py` para validar el origen:

```python
allowed_origins = [
    'https://hotel.calendar.consulting-sac.com.pe',
    'https://app.example.com',
    'http://localhost:3000'  # Para desarrollo
]

origin = request.httprequest.headers.get('Origin')
if origin in allowed_origins:
    response.headers['Access-Control-Allow-Origin'] = origin
```

## ✅ Verificación

Para verificar que CORS está funcionando correctamente:

### 1. Desde el navegador (Console):

```javascript
// Prueba rápida
fetch('https://odoo-docker-hotel.manager.consulting-sac.com.pe/api/hotel/hoteles', {
  headers: {'X-API-Key': 'tu_api_key'}
})
.then(r => r.json())
.then(console.log);
```

### 2. Inspeccionar Headers en DevTools:

1. Abre las DevTools (F12)
2. Ve a la pestaña **Network**
3. Haz una petición a la API
4. Revisa los Response Headers, deberías ver:
   ```
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
   Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key, x-api-key
   ```

### 3. Test de preflight (OPTIONS):

```bash
curl -X OPTIONS https://odoo-docker-hotel.manager.consulting-sac.com.pe/api/hotel/hoteles \
  -H "Origin: https://hotel.calendar.consulting-sac.com.pe" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: X-API-Key" \
  -v
```

Deberías ver una respuesta `200 OK` con los headers CORS.

## 🐛 Troubleshooting

### Problema: Todavía recibo error CORS

**Soluciones:**

1. **Verifica que el módulo esté actualizado:**
   ```bash
   docker exec -it odoo odoo --config=/etc/odoo/odoo.conf -d odoo --update=aac_hotel_api --stop-after-init
   docker restart odoo
   ```

2. **Limpia la caché del navegador:**
   - Chrome: Ctrl + Shift + Delete
   - Firefox: Ctrl + Shift + Delete
   - Safari: Command + Option + E

3. **Verifica los logs de Odoo:**
   ```bash
   docker logs -f odoo | grep -i cors
   ```

4. **Prueba con un endpoint simple primero:**
   ```javascript
   fetch('https://tu-odoo.com/api/auth/validate', {
     method: 'OPTIONS'
   }).then(r => console.log(r.headers));
   ```

### Problema: API key no funciona

- Verifica que estés enviando el header correcto: `X-API-Key` o `Authorization: Bearer <key>`
- Genera una nueva API key desde Odoo: **Preferencias → Seguridad → Claves API**
- Verifica que la API key esté activa y no haya expirado

## 📚 Referencias

- [MDN: CORS](https://developer.mozilla.org/es/docs/Web/HTTP/CORS)
- [Odoo Documentation: Controllers](https://www.odoo.com/documentation/17.0/developer/reference/backend/http.html)
- [API Authentication in Odoo](https://www.odoo.com/documentation/17.0/developer/reference/backend/security.html)

## ✅ Checklist Post-Despliegue

- [ ] Módulo `aac_hotel_api` actualizado en Odoo
- [ ] Contenedor de Odoo reiniciado
- [ ] Frontend configurado con la API key correcta
- [ ] Headers CORS verificados en Network DevTools
- [ ] Peticiones GET funcionando desde el frontend
- [ ] Peticiones POST funcionando desde el frontend
- [ ] API key validada correctamente
- [ ] Sin errores CORS en la consola del navegador

---

**Última actualización:** Diciembre 2025  
**Versión de Odoo:** 17.0  
**Autor:** Alania Poma Nick - Consulting SAC

