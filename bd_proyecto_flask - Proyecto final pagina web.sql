-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-09-2025 a las 02:42:36
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_proyecto_flask`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `email`) VALUES
(1, 'Brayan Camacho', 'juguitod295@gmail.com'),
(2, 'Alisson Damaris', 'alisson@gmail.com'),
(3, 'Mayra', 'mayra12@gmail.com'),
(4, 'Cesar', 'cesar@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventarios`
--

CREATE TABLE `inventarios` (
  `id_inventario` int(11) NOT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventarios`
--

INSERT INTO `inventarios` (`id_inventario`, `id_producto`, `cantidad`) VALUES
(1, 2, 0),
(2, 3, 4),
(3, 4, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `precio`, `cantidad`) VALUES
(2, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 'Nuestras barras son el impulso saludable que buscas. Hechas con ingredientes locales y orgánicos de la Amazonía ecuatoriana (semillas, frutas, superalimentos).\r\n\r\n100% Natural: Sin conservantes ni azúcares añadidos.', 1.00, 0),
(3, 'Guayusa Amazónica Pura: El Café de la Selva Embotellado  ', 'la Guayusa. Más que un té, es la bebida energética y funcional de los Kichwa, cultivada en los campos fértiles de Lago Agrio. A diferencia del café, la Guayusa ofrece una energía limpia y prolongada, sin los nervios o el bajón.', 1.50, 4),
(4, 'Mix de Frutas Deshidratadas', '¡El sabor concentrado de la Amazonía en tu mano! Nuestro Mix de Frutas Deshidratadas es la manera más deliciosa y cómoda de disfrutar los beneficios de las frutas locales, sin conservantes ni azúcares añadidos', 1.50, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idusuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idusuario`, `nombre`, `email`, `password`, `rol`) VALUES
(1, 'Brayan Camacho', 'brayancamacho@gmail.com', 'scrypt:32768:8:1$UtAyguicg4mLIc9A$5e65174548c7fe7eb584ab0514716d0eb8b896179766a588f22abd3d251e736e7bf8bd078ff8bab5e5623e3fe4b29cfc5885ec8f9959541fc752dd90b918f24b', 'usuario'),
(3, 'Brayan', 'brayan2004@gmail.com', 'scrypt:32768:8:1$TH2QVIJa8Hzbci3Z$4136b11b2a71b714d11efe3116e3668e0c78491086af9788a2957d1c157e94c63f3f5fb955fb7397304481c72215e535aa3426c83a1163e5ca762c477ffbbfb1', 'admin'),
(5, 'Alisson Damaris', 'alisson@gmail.com', 'scrypt:32768:8:1$BjvuJUhKf3zGF0VW$507046d64c85c65d96b59989c03788959aaa6697d4c387f36c8c7967ba01af670078482363a25915dd4a0702d71573905321607953d098864ed1c07c25e451a0', 'usuario'),
(6, 'Mayra', 'mayra12@gmail.com', 'scrypt:32768:8:1$Q834wLlWYOdTYwxb$4d300c9cf45f074bc2f116f069487995c6b05522cbda4e2759eaa7c9335992c6d4ebe632e5befa816a73f135323d3a43092e6e875645c1893ec62b72f0e82c13', 'usuario'),
(7, 'Cesar', 'cesar@gmail.com', 'scrypt:32768:8:1$r3JDNPEusB8vD9JR$99b14241644341f8740a4965ff913edfa13a2cf293090fab181f96ee9f8a05507a62a81ecfed07bc772c63ebcc9dd7b3114803de07eba5ef870f05311c2d38d8', 'usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` int(11) NOT NULL,
  `producto` varchar(255) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `producto`, `cantidad`, `fecha`, `id_usuario`) VALUES
(1, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 6, '2025-09-28 06:26:20', 5),
(2, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 3, '2025-09-28 06:34:52', 1),
(3, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 2, '2025-09-28 06:53:54', 1),
(4, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 2, '2025-09-28 06:59:16', 1),
(5, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 4, '2025-09-28 07:02:21', 5),
(6, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 2, '2025-09-28 07:06:01', 5),
(7, 'Guayusa Amazónica Pura: El Café de la Selva Embotellado  ', 2, '2025-09-28 07:06:09', 5),
(8, 'Guayusa Amazónica Pura: El Café de la Selva Embotellado  ', 1, '2025-09-28 07:06:12', 5),
(9, 'Mix de Frutas Deshidratadas', 1, '2025-09-28 07:09:34', 5),
(10, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 1, '2025-09-28 18:36:25', 1),
(11, 'Guayusa Amazónica Pura: El Café de la Selva Embotellado  ', 1, '2025-09-28 18:37:46', 1),
(12, 'Guayusa Amazónica Pura: El Café de la Selva Embotellado  ', 1, '2025-09-28 18:37:55', 1),
(13, 'Guayusa Amazónica Pura: El Café de la Selva Embotellado  ', 1, '2025-09-28 18:38:46', 1),
(14, 'Mix de Frutas Deshidratadas', 1, '2025-09-28 18:38:52', 1),
(15, 'Mix de Frutas Deshidratadas', 1, '2025-09-28 18:38:59', 1),
(16, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 1, '2025-09-28 18:50:30', 5),
(17, 'Guayusa Amazónica Pura: El Café de la Selva Embotellado  ', 1, '2025-09-28 18:50:30', 5),
(18, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 1, '2025-09-28 18:56:17', 5),
(19, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 1, '2025-09-28 18:57:45', 7),
(20, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 1, '2025-09-28 19:03:16', 5),
(21, 'Barras Energéticas EcoSnacks: El Poder de la Amazonía', 1, '2025-09-28 19:32:54', 5);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `inventarios`
--
ALTER TABLE `inventarios`
  ADD PRIMARY KEY (`id_inventario`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idusuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `inventarios`
--
ALTER TABLE `inventarios`
  MODIFY `id_inventario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idusuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `inventarios`
--
ALTER TABLE `inventarios`
  ADD CONSTRAINT `inventarios_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
