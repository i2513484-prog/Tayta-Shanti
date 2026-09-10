-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mysql-taytashanti.alwaysdata.net
-- Generation Time: Apr 29, 2026 at 08:01 AM
-- Server version: 11.4.9-MariaDB
-- PHP Version: 8.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `taytashanti_admin`
--

-- --------------------------------------------------------

--
-- Table structure for table `calificaciones`
--

CREATE TABLE `calificaciones` (
  `id` int(11) NOT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `estrellas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id` int(11) NOT NULL,
  `venta_id` int(11) DEFAULT NULL,
  `producto` varchar(100) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detalle_venta`
--

INSERT INTO `detalle_venta` (`id`, `venta_id`, `producto`, `cantidad`, `precio`) VALUES
(1, 3, 'Ron Cartavio', 1, 25),
(24, 17, 'Vodka Premium', 1, 50),
(25, 19, 'Whisky Blue Label', 1, 80),
(26, 19, 'Vodka Premium', 1, 50),
(27, 19, 'Vino Tinto Reserva', 1, 45),
(28, 19, 'Tequila Gold', 1, 60),
(35, 25, 'Vodka Premium', 1, 50),
(36, 25, 'Vino Tinto Reserva', 1, 45),
(37, 26, 'Hoja de coca', 1, 3),
(38, 26, 'Vino Tinto Reserva', 1, 45),
(39, 26, 'Tequila Gold', 1, 60),
(40, 27, 'Hoja de coca', 1, 3),
(41, 27, 'Vino Tinto Reserva', 1, 45),
(42, 28, 'Hoja de coca', 1, 3),
(43, 28, 'Vino Tinto Reserva', 1, 45),
(44, 29, 'Ron Cartavio', 1, 25),
(45, 29, 'Whisky Blue Label', 2, 80),
(46, 29, 'Vino Tinto Reserva', 1, 45),
(47, 30, 'Whisky Blue Label', 1, 80),
(48, 30, 'Vino Tinto Reserva', 2, 45),
(49, 31, 'Whisky Blue Label', 3, 80),
(50, 31, 'Vodka Premium', 1, 50),
(51, 32, 'Hoja de coca', 1, 3),
(52, 32, 'Tequila Gold', 1, 60),
(53, 33, 'Whisky Blue Label', 2, 80),
(54, 33, 'Vino Tinto Reserva', 2, 45),
(55, 33, 'Tequila Gold', 2, 60),
(56, 34, 'Vodka Premium', 1, 50),
(57, 34, 'Hoja de coca', 2, 3),
(58, 35, 'Vino Tinto Reserva', 2, 45),
(59, 36, 'Vodka Premium', 1, 50),
(60, 36, 'Hoja de coca', 1, 3),
(61, 37, 'Hoja de coca', 1, 3),
(62, 37, 'Vino Tinto Reserva', 2, 45),
(63, 38, 'Hoja de coca', 1, 3),
(64, 38, 'Vino Tinto Reserva', 1, 45),
(65, 39, 'Vodka Premium', 1, 50),
(66, 39, 'Hoja de coca', 2, 3),
(67, 40, 'Ron Cartavio', 1, 25),
(68, 40, 'Whisky Blue Label', 1, 80),
(69, 40, 'Vodka Premium', 3, 50),
(70, 40, 'Hoja de coca', 1, 3),
(71, 40, 'Vino Tinto Reserva', 1, 45),
(72, 40, 'Tequila Gold', 1, 60);

-- --------------------------------------------------------

--
-- Table structure for table `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` float NOT NULL,
  `stock` int(11) DEFAULT NULL,
  `imagen` varchar(200) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `precio`, `stock`, `imagen`, `descripcion`, `categoria`) VALUES
(2, 'Ron Cartavio', 25, 0, 'ron.jpg', NULL, 'ron'),
(3, 'Whisky Blue Label', 80, 0, 'whisky.jpg', NULL, 'whisky'),
(4, 'Vodka Premium', 50, 0, 'vodka.png', NULL, 'vodka'),
(5, 'Hoja de coca', 3, 0, 'coca.jpg', NULL, 'otros'),
(6, 'Vino Tinto Reserva', 45, 0, 'vino.jpg', NULL, 'vino'),
(7, 'Tequila Gold', 60, 0, 'tequila.jpg', NULL, 'tequila');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `password` varchar(200) NOT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `usuario` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password`, `apellidos`, `usuario`) VALUES
(1, 'JOHN', 'admin@mail.com', '$2a$12$M1BqNrMsUp4.0JGrt4g8fOXuo9gul0REEcA6tUE92YrBSqmoracrO', NULL, NULL),
(2, 'JOHN', 'johntc@gmail.com', 'scrypt:32768:8:1$fAb4K2c0LQfSybib$044583eb185c9ef8ad3f95cea6009caee55cc792727219abd0e70d5d835be47ce56b446e4224a8b4f4bb345e8f6da4b7676d344f886d846b1b2de10224bd675c', 'PÉREZ', 'johnTc'),
(3, 'John', 'john345@gmail.com', 'scrypt:32768:8:1$5epqgrLMN4D71ZA6$e80d124d04505ee22f67a7d372f5c229dcd1e219f0666516076eff987436885ccab15f2b320070901bb0d3e564cbec32f1cc1a57cf5ed6ef20f8066073dd8251', 'Suasnabar', 'johnTc');

-- --------------------------------------------------------

--
-- Table structure for table `venta`
--

CREATE TABLE `venta` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `total` float DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `tipo_documento` varchar(10) DEFAULT NULL,
  `numero_documento` varchar(15) DEFAULT NULL,
  `nombre_completo` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `venta`
--

INSERT INTO `venta` (`id`, `usuario_id`, `nombre`, `telefono`, `direccion`, `total`, `fecha`, `tipo_documento`, `numero_documento`, `nombre_completo`) VALUES
(25, NULL, 'JOHN', '904434996', 'av los heroes', 95, '2026-04-23 06:47:00', 'dni', '75181842', ''),
(26, NULL, 'JOHN', '904434996', 'av los heroes', 108, '2026-04-23 07:23:01', 'dni', '75181842', ''),
(27, NULL, 'JOHN', '904434996', 'av los heroes', 48, '2026-04-23 07:35:20', 'dni', '75181842', ''),
(28, NULL, 'JOHN', '904434996', 'av los heroes', 48, '2026-04-23 07:44:07', 'dni', '75181842', ''),
(29, NULL, 'JOHN', '904434996', 'av los heroes', 230, '2026-04-23 07:47:14', 'dni', '75181842', ''),
(30, NULL, '', '904434996', 'av los heroes', 170, '2026-04-23 07:54:13', 'dni', '75181842', ''),
(31, NULL, '', '904434996', 'av los heroes', 290, '2026-04-23 08:01:07', 'dni', '75181842', ''),
(32, NULL, 'John Paul Suasnabar Perez', '904434996', 'av los heroes', 63, '2026-04-23 08:03:07', 'dni', '75181842', ''),
(33, NULL, 'JOHN', '904434996', 'av los heroes', 370, '2026-04-23 08:04:03', 'dni', '75181842', ''),
(34, NULL, '', '904434996', 'av los heroes', 56, '2026-04-23 08:23:03', 'dni', '75181842', ''),
(35, NULL, '', '904434996', 'av los heroes', 90, '2026-04-23 08:41:39', 'dni', '75181842', ''),
(36, NULL, 'JOHN PAUL SUASNABAR PEREZ', '904434996', 'av los heroes', 53, '2026-04-23 08:45:12', 'dni', '75181842', 'JOHN PAUL SUASNABAR PEREZ'),
(37, NULL, 'ENTEL PERU S.A.', '904434996', 'av los heroes', 93, '2026-04-23 09:07:14', 'ruc', '20106897914', 'ENTEL PERU S.A.'),
(38, NULL, 'ENTEL PERU S.A.', '904434996', 'av los heroes', 48, '2026-04-23 09:08:35', 'ruc', '20106897914', 'ENTEL PERU S.A.'),
(39, NULL, 'JOHN PAUL SUASNABAR PEREZ', '904434996', 'av los heroes', 56, '2026-04-25 05:17:57', 'dni', '75181842', 'JOHN PAUL SUASNABAR PEREZ'),
(40, NULL, 'JOHN PAUL SUASNABAR PEREZ', '904434996', 'av los heroes', 363, '2026-04-29 05:31:37', 'dni', '75181842', 'JOHN PAUL SUASNABAR PEREZ');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indexes for table `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indexes for table `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `calificaciones`
--
ALTER TABLE `calificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `venta`
--
ALTER TABLE `venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
