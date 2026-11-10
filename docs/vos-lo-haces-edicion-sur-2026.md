# Vos Lo Hacés · Edición Sur 2026
## Dossier estratégico de competencia — Digital South

**Proyecto:** Digital South  
**Empresa:** EmergentSoft Corporation  
**Fundador:** Alejandro Lamas  
**Territorio inicial:** sur de la Ciudad de Buenos Aires y conurbano sur  
**Vertical inicial:** PyMEs metalmecánicas  
**Estado declarado:** prototipo funcional con datos sintéticos; etapa precomercial; sin clientes ni ingresos recurrentes al momento de esta versión.

> **Tesis:** Digital South ayuda a las PyMEs industriales a entender dónde pierden capacidad productiva y a probar mejoras mediante un gemelo digital antes de invertir o modificar la operación real.

## 1. El problema

Muchas PyMEs metalmecánicas coordinan producción, inventario, personal, mantenimiento y entregas con información fragmentada: planillas, registros manuales y sistemas que no reflejan en conjunto el estado operativo.

Esto dificulta responder preguntas cotidianas:
- ¿Dónde se acumula el trabajo en proceso?
- ¿Qué estación limita el flujo de producción?
- ¿Qué ocurre si aumenta la demanda o falta personal?
- ¿Conviene cambiar turnos, secuencias o capacidad antes de comprar una máquina?
- ¿Qué impacto tienen las demoras y los retrabajos sobre las entregas?

El problema no es la falta de dashboards: es la falta de una representación operativa integrada que permita experimentar con decisiones.

## 2. La solución

Digital South es una plataforma de inteligencia operativa industrial basada en gemelos digitales, simulación y analítica asistida por IA.

La propuesta de valor se organiza en cinco capacidades:
1. **Observar:** representar máquinas, estaciones, recursos y flujo de materiales.
2. **Modelar:** construir una línea base con datos disponibles de la empresa.
3. **Simular:** probar cambios de demanda, turnos, disponibilidad, mantenimiento y capacidad.
4. **Comparar:** medir diferencias entre línea base y escenarios alternativos.
5. **Decidir:** entregar evidencia e hipótesis de mejora para revisión humana.

La primera aplicación se concentra en procesos metalmecánicos: corte, plegado, soldadura, mecanizado, terminación y despacho.

## 3. Qué existe hoy y qué falta

La demo industrial del repositorio GitHub alejandro lamas-netizen / MeDigtwin-, rama feat/industrial-digital-twin-demo, incorpora una interfaz autónoma con siete vistas: panorama, topología, simulación, What-if, escenarios, cuellos de botella y arquitectura.

**Capacidad demostrada en el prototipo**
- Interfaz interactiva y modo de presentación.
- Modelo de topología y dependencias operativas.
- Escenarios reproducibles calculados localmente.
- Comparación contra una línea base sintética.
- Inspección de nodos y análisis de restricciones.
- Declaración explícita de límites y uso de datos sintéticos.

**No debe presentarse como capacidad ya implementada**
- Conexión a ERP, MES, sensores o datos de una fábrica.
- Predicción validada con históricos industriales.
- Optimización productiva validada en una planta.
- Integración operativa con NVIDIA Omniverse, Isaac Sim, Metropolis, cuOpt, Cosmos o servicios NVIDIA.
- Despliegue industrial o resultados medidos de clientes.

Estas capacidades pertenecen al roadmap y requieren ingeniería, datos, validación y acuerdos de integración.

## 4. Cliente inicial y validación

**Segmento inicial:** PyMEs metalmecánicas de aproximadamente 10–50 empleados en el sur de Buenos Aires y conurbano sur.

**Comprador/decisor:** dueño, gerente de planta o responsable de producción.

**Primer caso de uso:** diagnosticar y simular un cuello de botella en una línea o familia de productos.

**Validación comercial propuesta**
1. Entrevista de descubrimiento con dueño o responsable de planta.
2. Relevamiento de un proceso y sus fuentes de datos.
3. Selección conjunta de un indicador operativo prioritario.
4. Construcción de una línea base con datos autorizados.
5. Simulación de dos o tres intervenciones posibles.
6. Presentación de resultados, supuestos, limitaciones y siguiente decisión.

No se deben anunciar ahorros, aumentos de productividad ni reducciones de desperdicio hasta medirlos y validarlos con el cliente.

## 5. Modelo de negocio

**Entrada:** diagnóstico y piloto de alcance acotado, con precio y entregables acordados con cada empresa.

**Continuidad:** suscripción por planta o unidad operativa, con módulos de simulación, seguimiento de indicadores y soporte.

**Expansión:** conectores de datos, más líneas productivas, modelos especializados y analítica avanzada.

La estrategia es comenzar con un problema específico y un piloto verificable; evitar vender una transformación integral antes de demostrar valor.

## 6. Impacto territorial

Digital South busca acercar capacidades de industria 4.0 a PyMEs que no suelen disponer de equipos propios de simulación avanzada.

Impactos que se medirán en cada piloto:
- Tiempo requerido para identificar restricciones operativas.
- Tiempo de ciclo y producción por período.
- Trabajo en proceso y tiempos de espera.
- Utilización de máquinas y disponibilidad.
- Entregas a tiempo.
- Retrabajos, desperdicio y consumo energético, cuando existan datos fiables.

**Impacto ambiental:** la reducción de desperdicios, movimientos improductivos y consumo energético es una hipótesis de impacto que deberá comprobarse mediante mediciones comparables antes/después.

**Impacto laboral:** la plataforma se plantea como herramienta de apoyo a trabajadores y responsables de planta, no como sustituto automático de su criterio. La adopción incluirá transferencia de conocimiento y capacitación.

## 7. Diferenciación

- Foco inicial en un vertical productivo concreto, no en un gemelo genérico.
- Entrada gradual: aprovechar datos que la PyME ya posee antes de exigir sensores nuevos.
- Simulación de decisiones operativas, no solo visualización 3D.
- Arquitectura modular, con evolución hacia estándares y herramientas industriales como OpenUSD y tecnologías NVIDIA cuando el caso de uso lo justifique.
- Diseño de pilotos con métricas acordadas y revisión humana.

## 8. Equipo y ejecución

EmergentSoft está en etapa temprana y actualmente es impulsada por su fundador, Alejandro Lamas. El fundador aporta experiencia docente de 26 años y lidera la definición de producto, arquitectura y desarrollo.

La ejecución debe ser realista: validar un primer proceso con una PyME, documentar resultados y sumar capacidades técnicas/comerciales según los hitos de tracción. No presentar un equipo ampliado ni alianzas operativas que no estén formalizadas.

## 9. Hoja de ruta

| Etapa | Entregable | Evidencia de avance |
|---|---|---|
| 1. Producto demostrable | Demo industrial estable y guion de presentación | Prueba funcional y checklist |
| 2. Descubrimiento | Entrevistas con PyMEs y mapa de procesos | Problemas priorizados y cartas de interés si se obtienen |
| 3. Primer piloto | Gemelo de un proceso con datos autorizados | Línea base acordada |
| 4. Validación | Comparación de escenarios y medición de resultados | Informe revisado por cliente |
| 5. Producto repetible | Plantillas por proceso y conectores reutilizables | Menor tiempo de implementación |
| 6. Escala | Integraciones y aceleración según demanda | Casos de uso y clientes activos |

## 10. Estructura recomendada para un pitch de 10 diapositivas

1. **Digital South:** inteligencia operativa para la industria del sur de Buenos Aires.
2. **El problema:** información fragmentada y decisiones productivas a ciegas.
3. **El cliente:** PyMEs metalmecánicas y sus decisores.
4. **La solución:** observar, modelar, simular, comparar y decidir.
5. **Demostración:** recorrido breve por topología, cuello de botella y What-if.
6. **Innovación:** gemelo digital vertical, simulación y arquitectura escalable.
7. **Modelo de negocio:** diagnóstico, piloto y suscripción.
8. **Impacto:** productividad, competitividad, capacidades locales y medición ambiental.
9. **Equipo y estado:** fundador, prototipo existente, etapa precomercial y brechas abiertas.
10. **Próximo hito:** conseguir una PyME anfitriona para validar el primer piloto.

## 11. Guion oral sugerido (aprox. 2 minutos)

En el sur de Buenos Aires hay PyMEs industriales que producen, emplean personas y sostienen cadenas de valor. Pero muchas todavía toman decisiones con información fragmentada. Cuando se acumulan pedidos, falta un insumo o una máquina se convierte en cuello de botella, conocer el problema tarde cuesta tiempo y competitividad.

Soy Alejandro Lamas, fundador de EmergentSoft, y estoy desarrollando Digital South: una plataforma de inteligencia operativa que permite representar una planta, modelar sus procesos y simular alternativas antes de cambiar la operación real.

Nuestra primera vertical es la industria metalmecánica. Empezamos por empresas que realizan corte, plegado, soldadura, mecanizado y despacho. La propuesta es concreta: tomar un proceso, construir una línea base con los datos disponibles y comparar escenarios para identificar oportunidades de mejora.

Hoy contamos con un prototipo interactivo que demuestra la topología, la simulación de escenarios y el análisis de restricciones con datos sintéticos. Todavía no afirmamos resultados de una fábrica ni integraciones que no están implementadas. El siguiente paso es validar el modelo con una PyME anfitriona y medir indicadores acordados con ella.

El modelo de negocio comienza con un diagnóstico y un piloto acotado, y evoluciona hacia una suscripción por planta. Queremos que las PyMEs del sur accedan a herramientas de industria 4.0 de forma gradual, medible y útil.

Digital South busca transformar datos operativos en mejores decisiones productivas. Construido en Buenos Aires, diseñado para escalar.

## 12. Preguntas difíciles del jurado

**¿Ya tienen clientes o ventas?**  
Todavía no. El proyecto está en etapa precomercial. Tenemos un prototipo y buscamos una PyME anfitriona para validar el primer piloto.

**¿La demo está conectada a una fábrica?**  
No. Utiliza datos sintéticos. La conexión a datos reales se realizará con autorización, relevamiento y controles de seguridad.

**¿Qué tiene de innovador frente a un dashboard?**  
No se limita a mostrar indicadores: representa relaciones entre recursos y procesos y permite comparar escenarios operativos antes de tomar decisiones.

**¿Por qué empezar por metalmecánica?**  
Porque permite acotar el problema a procesos identificables —corte, plegado, soldadura y despacho— y construir una metodología replicable.

**¿Qué papel tiene NVIDIA?**  
La arquitectura contempla tecnologías del ecosistema NVIDIA como opciones de evolución. No afirmamos una integración técnica o patrocinio específico hasta contar con implementación y evidencia.

**¿Cómo van a demostrar impacto?**  
Acordando con cada empresa una línea base, indicadores, período de observación y método de comparación. Los resultados se reportarán con sus supuestos y límites.

**¿Qué necesitan del programa?**  
Acceso a PyMEs anfitrionas, mentoría comercial e industrial, validación del modelo de negocio y acompañamiento para convertir el prototipo en un piloto medible.

## Regla de comunicación para la competencia

Usar siempre tres etiquetas claras:
- **Implementado:** visible y comprobable en el prototipo.
- **En desarrollo:** trabajo técnico iniciado, todavía no validado como capacidad terminada.
- **Propuesto:** arquitectura o integración futura.

La credibilidad es parte de la innovación. No atribuir a clientes, aliados, NVIDIA, AWS ni al programa resultados o avales que no estén documentados.
