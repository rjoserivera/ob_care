-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 13-12-2025 a las 04:00:01
-- Versión del servidor: 8.0.17
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `legacy_obstetric`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `controles_previos`
--

CREATE TABLE `controles_previos` (
  `id` bigint(20) NOT NULL,
  `paciente_rut` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_control` date NOT NULL,
  `numero_control` int(10) UNSIGNED DEFAULT NULL,
  `tipo_control` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `consultorio_origen` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profesional_nombre` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profesional_tipo` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `semanas_gestacion` int(10) UNSIGNED DEFAULT NULL,
  `dias_gestacion` int(10) UNSIGNED DEFAULT NULL,
  `fur` date DEFAULT NULL,
  `fpp` date DEFAULT NULL,
  `peso_kg` decimal(5,2) DEFAULT NULL,
  `talla_cm` decimal(5,2) DEFAULT NULL,
  `imc` decimal(5,2) DEFAULT NULL,
  `altura_uterina_cm` decimal(5,2) DEFAULT NULL,
  `ganancia_peso_total_kg` decimal(5,2) DEFAULT NULL,
  `presion_sistolica` int(11) DEFAULT NULL,
  `presion_diastolica` int(11) DEFAULT NULL,
  `frecuencia_cardiaca_materna` smallint(6) DEFAULT NULL,
  `temperatura_c` decimal(4,1) DEFAULT NULL,
  `saturacion_o2` int(11) DEFAULT NULL,
  `fcf_lpm` int(11) DEFAULT NULL,
  `movimientos_fetales` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `presentacion_fetal` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situacion_fetal` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `glucosa_mg_dl` decimal(6,2) DEFAULT NULL,
  `hemoglobina_g_dl` decimal(4,1) DEFAULT NULL,
  `hematocrito_pct` decimal(5,2) DEFAULT NULL,
  `grupo_sanguineo` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `factor_rh` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `proteinuria` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `leucocitos_orina` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vih_resultado` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vih_fecha_toma` date DEFAULT NULL,
  `vih_orden` int(10) UNSIGNED DEFAULT NULL,
  `vdrl_resultado` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vdrl_fecha` date DEFAULT NULL,
  `sgb_resultado` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sgb_fecha_cultivo` date DEFAULT NULL,
  `sgb_profilaxis` tinyint(1) DEFAULT NULL,
  `toxoplasma_resultado` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `toxoplasma_fecha` date DEFAULT NULL,
  `hepatitis_b_resultado` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hepatitis_b_fecha` date DEFAULT NULL,
  `diabetes_gestacional` tinyint(1) DEFAULT NULL,
  `hipertension_arterial` tinyint(1) DEFAULT NULL,
  `preeclampsia_leve` tinyint(1) DEFAULT NULL,
  `preeclampsia_severa` tinyint(1) DEFAULT NULL,
  `eclampsia` tinyint(1) DEFAULT NULL,
  `anemia` tinyint(1) DEFAULT NULL,
  `infeccion_urinaria` tinyint(1) DEFAULT NULL,
  `corioamnionitis` tinyint(1) DEFAULT NULL,
  `amenaza_parto_prematuro` tinyint(1) DEFAULT NULL,
  `rotura_prematura_membranas` tinyint(1) DEFAULT NULL,
  `otras_patologias` text COLLATE utf8mb4_unicode_ci,
  `numero_aro` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nivel_riesgo` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `medicamentos_activos` text COLLATE utf8mb4_unicode_ci,
  `acido_folico` tinyint(1) DEFAULT NULL,
  `sulfato_ferroso` tinyint(1) DEFAULT NULL,
  `aspirina_profilactica` tinyint(1) DEFAULT NULL,
  `otros_tratamientos` text COLLATE utf8mb4_unicode_ci,
  `numero_gestas` int(10) UNSIGNED DEFAULT NULL,
  `numero_partos` int(10) UNSIGNED DEFAULT NULL,
  `partos_vaginales_previos` int(10) UNSIGNED DEFAULT NULL,
  `cesareas_previas` int(10) UNSIGNED DEFAULT NULL,
  `numero_abortos` int(10) UNSIGNED DEFAULT NULL,
  `hijos_vivos` int(10) UNSIGNED DEFAULT NULL,
  `paridad_formato` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `edema_grado` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `edema_localizacion` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `varices` tinyint(1) DEFAULT NULL,
  `reflejos_osteotendinosos` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tiene_plan_parto` tinyint(1) DEFAULT NULL,
  `realizo_visita_guiada` tinyint(1) DEFAULT NULL,
  `fecha_proximo_control` date DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `indicaciones_medicas` text COLLATE utf8mb4_unicode_ci,
  `motivo_consulta` text COLLATE utf8mb4_unicode_ci,
  `turno` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_hora_registro` datetime DEFAULT NULL,
  `sistema_origen` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `controles_previos`
--

INSERT INTO `controles_previos` (`id`, `paciente_rut`, `fecha_control`, `numero_control`, `tipo_control`, `consultorio_origen`, `profesional_nombre`, `profesional_tipo`, `semanas_gestacion`, `dias_gestacion`, `fur`, `fpp`, `peso_kg`, `talla_cm`, `imc`, `altura_uterina_cm`, `ganancia_peso_total_kg`, `presion_sistolica`, `presion_diastolica`, `frecuencia_cardiaca_materna`, `temperatura_c`, `saturacion_o2`, `fcf_lpm`, `movimientos_fetales`, `presentacion_fetal`, `situacion_fetal`, `glucosa_mg_dl`, `hemoglobina_g_dl`, `hematocrito_pct`, `grupo_sanguineo`, `factor_rh`, `proteinuria`, `leucocitos_orina`, `vih_resultado`, `vih_fecha_toma`, `vih_orden`, `vdrl_resultado`, `vdrl_fecha`, `sgb_resultado`, `sgb_fecha_cultivo`, `sgb_profilaxis`, `toxoplasma_resultado`, `toxoplasma_fecha`, `hepatitis_b_resultado`, `hepatitis_b_fecha`, `diabetes_gestacional`, `hipertension_arterial`, `preeclampsia_leve`, `preeclampsia_severa`, `eclampsia`, `anemia`, `infeccion_urinaria`, `corioamnionitis`, `amenaza_parto_prematuro`, `rotura_prematura_membranas`, `otras_patologias`, `numero_aro`, `nivel_riesgo`, `medicamentos_activos`, `acido_folico`, `sulfato_ferroso`, `aspirina_profilactica`, `otros_tratamientos`, `numero_gestas`, `numero_partos`, `partos_vaginales_previos`, `cesareas_previas`, `numero_abortos`, `hijos_vivos`, `paridad_formato`, `edema_grado`, `edema_localizacion`, `varices`, `reflejos_osteotendinosos`, `tiene_plan_parto`, `realizo_visita_guiada`, `fecha_proximo_control`, `observaciones`, `indicaciones_medicas`, `motivo_consulta`, `turno`, `fecha_hora_registro`, `sistema_origen`) VALUES
(1, '16293109-1', '2023-01-15', 1, 'PRENATAL', 'CESFAM Coronel', 'Dra. María González', 'MEDICO', 8, 3, '2022-11-20', '2023-08-27', '62.50', '162.00', '23.80', '10.00', '3.50', 110, 70, 72, '36.5', 98, 145, 'PRESENTES', 'CEFALICA', 'LONGITUDINAL', '85.00', '12.5', '38.00', 'O', '+', 'NEGATIVO', '0-5 por campo', 'NEGATIVO', '2023-01-10', 1, 'NO REACTIVO', '2023-01-10', 'NEGATIVO', NULL, 0, 'NEGATIVO', '2023-01-15', 'NEGATIVO', '2023-01-15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 'ARO-2023-0001', 'BAJO', 'Acido folico 1mg/dia, Sulfato ferroso 300mg/dia', 1, 1, 0, NULL, 2, 1, 1, 0, 0, 1, 'G2P1A0', 'AUSENTE', 'N/A', 0, 'Normales', 1, 0, '2023-02-15', 'Embarazo de curso normal. Paciente sin antecedentes mórbidos.', 'Continuar con ácido fólico y sulfato ferroso. Control en 4 semanas.', 'Control prenatal de rutina', 'MANANA', '2023-01-15 13:30:00', 'Legacy'),
(2, '16293109-1', '2023-02-20', 2, 'PRENATAL', 'CESFAM Coronel', 'Matrona Carmen Rojas', 'MATRONA', 13, 2, '2022-11-20', '2023-08-27', '64.00', '162.00', '24.40', '12.00', '1.50', 115, 72, 75, '36.6', 98, 150, 'PRESENTES', 'CEFALICA', 'LONGITUDINAL', '88.00', '12.2', '37.50', NULL, NULL, 'NEGATIVO', '0-5 por campo', NULL, NULL, 1, NULL, NULL, 'NEGATIVO', NULL, 0, 'NEGATIVO', '2023-02-20', 'NEGATIVO', '2023-02-20', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 'ARO-2023-0002', 'BAJO', 'Acido folico 1mg/dia, Sulfato ferroso 300mg/dia', 1, 1, 0, NULL, 2, 1, 1, 0, 0, 1, 'G2P1A0', 'AUSENTE', 'N/A', 0, 'Normales', 1, 0, '2023-03-20', 'Embarazo evolucionando favorablemente. Ecografía de 12 semanas normal.', 'Continuar suplementación. Control mensual.', 'Control prenatal de rutina', 'MANANA', '2023-02-20 13:30:00', 'Legacy'),
(3, '16293109-1', '2023-04-10', 3, 'PRENATAL', 'CESFAM Coronel', 'Matrona Carmen Rojas', 'MATRONA', 20, 5, '2022-11-20', '2023-08-27', '67.50', '162.00', '25.70', '18.00', '5.00', 118, 75, 78, '36.7', 98, 148, 'PRESENTES', 'CEFALICA', 'LONGITUDINAL', '90.00', '11.8', '36.80', NULL, NULL, 'NEGATIVO', '0-5 por campo', NULL, NULL, 1, NULL, NULL, 'PENDIENTE', NULL, 0, 'NEGATIVO', '2023-04-10', 'NEGATIVO', '2023-04-10', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 'ARO-2023-0003', 'BAJO', 'Acido folico 1mg/dia, Sulfato ferroso 300mg/dia', 1, 1, 0, NULL, 2, 1, 1, 0, 0, 1, 'G2P1A0', 'LEVE', 'Tobillos', 0, 'Normales', 1, 0, '2023-05-10', 'Ecografía morfológica normal. Feto único, sexo femenino. Movimientos fetales activos.', 'Continuar suplementación. Elevar piernas para edema leve. Control en 4 semanas.', 'Control prenatal de rutina', 'MANANA', '2023-04-10 14:30:00', 'Legacy'),
(4, '16293109-1', '2023-06-15', 4, 'PRENATAL', 'CESFAM Coronel', 'Dra. María González', 'MEDICO', 29, 1, '2022-11-20', '2023-08-27', '72.00', '162.00', '27.40', '27.00', '9.50', 120, 78, 80, '36.6', 98, 142, 'PRESENTES', 'CEFALICA', 'LONGITUDINAL', '92.00', '11.5', '36.00', NULL, NULL, 'NEGATIVO', '0-5 por campo', NULL, NULL, 1, NULL, NULL, 'NEGATIVO', '2023-06-10', 0, 'NEGATIVO', '2023-06-15', 'NEGATIVO', '2023-06-15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 'ARO-2023-0004', 'BAJO', 'Acido folico 1mg/dia, Sulfato ferroso 300mg/dia', 1, 1, 0, NULL, 2, 1, 1, 0, 0, 1, 'G2P1A0', 'LEVE', 'Tobillos y pies', 1, 'Normales', 1, 1, '2023-07-15', 'Tercer trimestre. Cultivo SGB negativo. Visita guiada al servicio de maternidad realizada.', 'Continuar suplementación. Uso de medias de compresión para varices. Control en 4 semanas.', 'Control prenatal de rutina', 'MANANA', '2023-06-15 14:30:00', 'Legacy'),
(5, '16293109-1', '2023-07-25', 5, 'PRENATAL', 'CESFAM Coronel', 'Matrona Carmen Rojas', 'MATRONA', 34, 4, '2022-11-20', '2023-08-27', '75.00', '162.00', '28.60', '32.00', '12.50', 122, 80, 82, '36.8', 98, 140, 'PRESENTES', 'CEFALICA', 'LONGITUDINAL', '95.00', '11.2', '35.50', NULL, NULL, 'NEGATIVO', '0-5 por campo', NULL, NULL, 1, NULL, NULL, 'NEGATIVO', NULL, 0, 'NEGATIVO', '2023-07-25', 'NEGATIVO', '2023-07-25', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, 'ARO-2023-0005', 'BAJO', 'Acido folico 1mg/dia, Sulfato ferroso 300mg/dia', 1, 1, 0, NULL, 2, 1, 1, 0, 0, 1, 'G2P1A0', 'MODERADO', 'Tobillos, pies y manos', 1, 'Normales', 1, 1, '2023-08-08', 'Embarazo de término cercano. Feto en presentación cefálica. Edema moderado fisiológico.', 'Continuar suplementación. Reposo relativo. Signos de alarma explicados. Control semanal hasta el parto.', 'Control prenatal de rutina', 'MANANA', '2023-07-25 14:30:00', 'Legacy');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `controles_previos`
--
ALTER TABLE `controles_previos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_paciente_rut` (`paciente_rut`),
  ADD KEY `idx_fecha_control` (`fecha_control`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `controles_previos`
--
ALTER TABLE `controles_previos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
