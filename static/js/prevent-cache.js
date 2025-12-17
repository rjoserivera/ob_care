/**
 * prevent-cache.js
 * Script para prevenir el acceso a páginas sensibles desde el caché del navegador
 * Esto asegura que siempre se validen los permisos del usuario al retroceder
 */

(function() {
    'use strict';

    // ═══════════════════════════════════════════════════════════════
    // PREVENIR ACCESO A PÁGINA CACHEADA AL RETROCEDER
    // ═══════════════════════════════════════════════════════════════
    
    /**
     * Detectar si la página se cargó desde el caché del navegador (botón retroceder)
     * El evento 'pageshow' se dispara cuando la página se muestra, incluso desde caché
     */
    window.addEventListener('pageshow', function(event) {
        // Si la página viene del caché (persisted = true), recargar
        if (event.persisted) {
            console.log('[Security] Página cargada desde caché - Recargando para validar permisos...');
            window.location.reload();
        }
    });

    /**
     * Detectar navegación desde caché usando Performance API
     * type 2 = página cargada desde caché (botón retroceder/adelantar)
     */
    if (window.performance && performance.navigation.type === 2) {
        console.log('[Security] Navegación desde caché detectada - Recargando...');
        window.location.reload();
    }

    /**
     * Prevenir que la página se guarde en el caché del navegador
     * Esto ayuda a que el navegador no cachee la página al salir
     */
    window.addEventListener('beforeunload', function() {
        // Ocultar el contenido antes de salir para evitar que se cachee visualmente
        document.body.style.display = 'none';
    });

    /**
     * Detectar cuando el usuario vuelve a esta página usando el historial
     * El evento 'popstate' se dispara cuando se navega por el historial
     */
    window.addEventListener('popstate', function(event) {
        console.log('[Security] Navegación con botón retroceder detectada - Recargando...');
        window.location.reload();
    });

    /**
     * Prevenir el uso de la tecla de retroceso (Backspace) fuera de inputs
     * Esto evita navegación accidental
     */
    document.addEventListener('keydown', function(event) {
        // Si presiona Backspace y NO está en un input/textarea
        if (event.key === 'Backspace' && 
            !['INPUT', 'TEXTAREA'].includes(event.target.tagName) &&
            !event.target.isContentEditable) {
            
            // Prevenir la navegación hacia atrás
            event.preventDefault();
            console.log('[Security] Navegación con Backspace bloqueada');
        }
    });

    console.log('[Security] Sistema de prevención de caché activado');
})();
