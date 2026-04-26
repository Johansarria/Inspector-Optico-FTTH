# Glosario Técnico de Redes FTTH (Fiber-To-The-Home) 📖

Este documento centraliza la terminología técnica estándar utilizada en la industria de las telecomunicaciones para despliegues de fibra óptica, sirviendo como base de conocimiento para **FiberMind Analytics**.

---

## 1. ODF (Optical Distribution Frame)
*   **Nombre en Español:** Distribuidor Óptico / Cabecera.
*   **Definición:** Es el bastidor o panel central ubicado en la oficina central (CO) o cuarto de equipos. Integra el empalme, la terminación y el enrutamiento de las fibras.
*   **Rol en la Red:** Es el punto de partida (Origen). Aquí es donde las "trazas" (feeder cables) se conectan a los equipos activos (OLT). En nuestro diseño, usan módulos Clase C++ (potencia de +3 dBm a +5 dBm).

## 2. Mufa (Splice Closure)
*   **Nombre en Español:** Caja de Empalme / Manga de Empalme.
*   **Definición:** Carcasa protectora utilizada en campo para alojar y proteger los empalmes (uniones) de fibra óptica contra la humedad, el polvo y daños físicos.
*   **Rol en la Red:** Se instalan en cámaras subterráneas, postes o enterradas directamente. Permiten unir bobinas de cable o "sangrar" un cable principal (extraer algunos hilos) para crear ramificaciones.

## 3. Splitter (Optical Splitter)
*   **Nombre en Español:** Divisor Óptico.
*   **Definición:** Componente pasivo (no requiere electricidad) esencial en redes PON. Divide una señal óptica entrante en múltiples señales de salida (ej. 1x8, 1x16).
*   **Rol en la Red:** Permite que un solo hilo de fibra alimente a múltiples clientes. En nuestra arquitectura, usamos una doble cascada de splitters 1x8 (generando una atenuación natural de ~10.5 dB por nivel).

## 4. CTO (Caja Terminal Óptica)
*   **Nombre en Español:** Caja Terminal Óptica / Caja de Dispersión.
*   **Definición:** Es el punto de distribución final en la calle o edificio antes de llegar al cliente final. Es el destino donde el "hilo" se convierte en "servicio".
*   **Rol en la Red:** Aquí termina la red de distribución. Desde la CTO se lanzan las "acometidas" (drop cables) hacia las casas de los usuarios (ONT). Nuestro presupuesto objetivo en este punto debe estar entre -18 dBm y -22 dBm.

## 5. CA (Cable de Fibra Óptica)
*   **Definición:** El medio de transporte principal. La nomenclatura **CA** (seguida de un número, ej. CA08) identifica a un cable específico de la red.
*   **Capacidades Típicas:** Pueden ser cables de 288, 144, 48 o 24 hilos.
*   **Rol en la Red:** Es la infraestructura que contiene los hilos que FiberMind audita. Un plano que referencia un "CA08" está describiendo la ruta y los elementos asociados a ese cable de distribución.

## 6. OTDR (Optical Time-Domain Reflectometer)
*   **Nombre en Español:** Reflectómetro Óptico en el Dominio del Tiempo.
*   **Definición:** Instrumento optoelectrónico usado para caracterizar una fibra óptica.
*   **Rol en la Red:** Envía pulsos de luz y mide las reflexiones para crear una "radiografía" del enlace (`.sor`). Detecta distancias, empalmes (pérdidas por fusión) y roturas. Un empalme > 0.5 dB se considera una falla crítica en esta red.

---
*Glosario indexado por FiberMind Analytics para estandarizar la comunicación técnica de Operaciones y Mantenimiento.*
