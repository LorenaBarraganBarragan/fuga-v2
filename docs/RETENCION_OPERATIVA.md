# Retención del prototipo: procedimiento revisable

Decisiones D-06/D-14; ACT-14 del plan autorizado el 2026-11-18. Este documento no
ejecuta ni autoriza limpiezas. La validación de la entrega se realiza con datos ficticios.

## Estado implementado

Desactivar marca disabled_at, bloquea API, solicita bloqueo al proveedor y programa
tarea_retencion.suprimir_desde a disabled_at + 30 días. Reactivar cancela esa tarea.
Auditoría registra actor/acción/resultado sin gastos o tokens. No existe ejecutor automático.
La prueba local test_retention_queue_reactivation_and_restrictive_audit_foreign_key
comprueba esos estados y que una eliminación directa de perfil falla ante dependencias.

## Revisión antes de cualquier operación real

1. Identificar responsable, entorno y autorización concreta; preservar respaldo revisado.
2. Verificar desactivación, tarea pendiente y vencimiento de 30 días. Una tarea cancelada
   o una cuenta reactivada no es elegible. Revisar obligaciones y ciclo de respaldos con el responsable.
3. Preparar un informe de conteos, sin exportar correos, descripciones, montos ni tokens.
4. Simular el procedimiento completo en copia desechable, con los mismos constraints,
   y acordar explícitamente datos a suprimir, anonimizar o conservar y forma de recuperación.
5. Revisar el SQL exacto y la lista de afectados antes de autorizar su ejecución. No usar
   CASCADE global, borrar todas las tablas o conceder permisos nuevos al cliente.

Consulta informativa de conteo (solo SELECT; no ejecutada contra Supabase por el agente):

```sql
SELECT count(*) AS tareas_elegibles
FROM public.tarea_retencion t
JOIN public.perfil p ON p.id=t.usuario_id
WHERE t.estado='pendiente' AND p.disabled_at IS NOT NULL
  AND t.suprimir_desde <= statement_timestamp();
```

## Dependencias que impiden una eliminación ingenua

| Recurso | Relación / tratamiento a diseñar y revisar |
|---|---|
| fuga y fuga_evidencia | Eliminar snapshots objetivo y sus relaciones antes de gastos/perfil; no tocar evidencias ajenas |
| gasto | Borrado lógico actual no es supresión física; FK a perfil es restrictiva |
| actividad_mensual, tarea_retencion | Referencian perfil; conservar solo si la política lo justifica, o retirar en operación revisada |
| auditoria.actor_id | FK restrictiva a perfil; no permite borrar perfil conservando su auditoría sin una decisión explícita |
| auth.users | Su eliminación intenta cascada a perfil; no saltarse las FK de public ni borrar Auth primero |

Al día 30 se **programa y revisa** la supresión. Si la auditoría del actor debe conservarse
hasta 90 días, no se debe borrar el perfil técnico que exige su FK. El responsable debe
aprobar una supresión por etapas: minimizar datos personales/financieros elegibles y
conservar temporalmente la referencia técnica necesaria, o aprobar una evolución de
esquema para desacoplar auditoría. Ninguna de esas mutaciones está automatizada aquí.
El tratamiento de identidad en Auth también requiere revisión del operador.

Para auditoría, revisar eventos con antigüedad mayor a 90 días según created_at UTC,
retener excepciones justificadas y simular su depuración antes de liberar referencias.
Después de resolver dependencias podrá evaluarse eliminación física de perfil/Auth.
La recuperación de una cuenta ya suprimida no se promete; antes de supresión, reactivar
debe cancelar la tarea y restaurar acceso mediante la gestión existente.

## Aceptación

El prototipo cumple el alcance documental de ACT-14 cuando cola, cancelación y límites
de FK estén comprobados localmente y el procedimiento esté revisado. No debe anunciar
supresión automática ni conformidad operativa de usuarios reales por existir esta guía.
Para usar datos reales debe cerrarse la decisión de tratamiento por etapas, validar
respaldos y autorizar por separado cualquier operación. Las muestras actuales de Supabase
permanecen intactas.
