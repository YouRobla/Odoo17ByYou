# -*- coding: utf-8 -*-
"""
Manejador de CORS (Cross-Origin Resource Sharing) para la API de Hotel
Permite que frontends externos (React, Vue, etc.) puedan consumir la API
"""
import logging
from functools import wraps
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


def cors_preflight_response():
    """
    Crea una respuesta para peticiones OPTIONS (preflight) de CORS
    """
    headers = {
        'Access-Control-Allow-Origin': '*',  # Permite todos los orígenes
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key, x-api-key',
        'Access-Control-Max-Age': '86400',  # 24 horas
        'Access-Control-Allow-Credentials': 'true',
    }
    
    return Response(
        '',
        status=200,
        headers=headers
    )


def add_cors_headers(response):
    """
    Agrega headers de CORS a una respuesta existente
    
    Args:
        response: Objeto Response de Odoo
        
    Returns:
        Response con headers de CORS agregados
    """
    # Headers CORS permisivos para desarrollo y producción
    cors_headers = {
        'Access-Control-Allow-Origin': '*',  # Permite todos los orígenes
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key, x-api-key',
        'Access-Control-Max-Age': '86400',
        'Access-Control-Allow-Credentials': 'true',
    }
    
    # Agregar headers a la respuesta
    if hasattr(response, 'headers'):
        for key, value in cors_headers.items():
            response.headers[key] = value
    
    return response


def cors_enabled(func):
    """
    Decorador que habilita CORS en un endpoint.
    
    Usage:
        @http.route('/api/endpoint', auth='public', type='http', methods=['GET'], csrf=False)
        @cors_enabled
        def my_endpoint(self, **kw):
            return self._prepare_response({'data': 'value'})
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Manejar peticiones OPTIONS (preflight)
        if request.httprequest.method == 'OPTIONS':
            _logger.debug(f"CORS preflight request para {request.httprequest.path}")
            return cors_preflight_response()
        
        # Ejecutar la función original
        response = func(self, *args, **kwargs)
        
        # Si la respuesta es un Response object, agregar headers CORS
        if isinstance(response, Response):
            response = add_cors_headers(response)
        else:
            # Si no es un Response, crear uno nuevo con CORS
            _logger.warning(f"Respuesta no es un Response object en {func.__name__}")
            response = Response(
                response,
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key, x-api-key',
                }
            )
        
        return response
    
    return wrapper


def get_cors_config():
    """
    Obtiene la configuración de CORS desde parámetros del sistema.
    Permite configurar CORS dinámicamente desde Odoo.
    
    Returns:
        dict: Configuración de CORS
    """
    try:
        IrConfigParameter = request.env['ir.config_parameter'].sudo()
        
        allowed_origins = IrConfigParameter.get_param(
            'aac_hotel_api.cors_allowed_origins', 
            '*'
        )
        
        allowed_methods = IrConfigParameter.get_param(
            'aac_hotel_api.cors_allowed_methods',
            'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        )
        
        allowed_headers = IrConfigParameter.get_param(
            'aac_hotel_api.cors_allowed_headers',
            'Content-Type, Authorization, X-API-Key, x-api-key'
        )
        
        return {
            'allowed_origins': allowed_origins,
            'allowed_methods': allowed_methods,
            'allowed_headers': allowed_headers,
        }
    except Exception as e:
        _logger.error(f"Error obteniendo configuración de CORS: {e}")
        return {
            'allowed_origins': '*',
            'allowed_methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
            'allowed_headers': 'Content-Type, Authorization, X-API-Key, x-api-key',
        }

