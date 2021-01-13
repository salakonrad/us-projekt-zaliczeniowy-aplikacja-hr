-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Jan 16, 2021 at 09:49 AM
-- Server version: 8.0.22
-- PHP Version: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hr`
--
CREATE DATABASE hr;
USE hr;

-- --------------------------------------------------------

--
-- Table structure for table `holidays_balance`
--

CREATE TABLE `holidays_balance` (
  `id` int NOT NULL,
  `id_users` int NOT NULL,
  `holiday_type` varchar(20) NOT NULL,
  `amount_left` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `holidays_balance`
--

INSERT INTO `holidays_balance` (`id`, `id_users`, `holiday_type`, `amount_left`) VALUES
(1, 2, 'urlop-macierzynski', 10),
(2, 3, 'urlop-macierzynski', 10),
(3, 4, 'urlop-macierzynski', 10),
(4, 2, 'urlop-na-zadanie', 4),
(5, 3, 'urlop-na-zadanie', 4),
(6, 4, 'urlop-na-zadanie', 4),
(7, 2, 'urlop-wypoczynkowy', 26),
(8, 3, 'urlop-wypoczynkowy', 26),
(9, 4, 'urlop-wypoczynkowy', 26);

-- --------------------------------------------------------

--
-- Table structure for table `holidays_requests`
--

CREATE TABLE `holidays_requests` (
  `id` int NOT NULL,
  `id_users` int NOT NULL,
  `holiday_type` varchar(20) NOT NULL,
  `date_from` date NOT NULL,
  `date_to` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `salaries`
--

CREATE TABLE `salaries` (
  `id` int NOT NULL,
  `id_users` int NOT NULL,
  `amount_gross` float NOT NULL,
  `amount_net` float NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `salaries`
--

INSERT INTO `salaries` (`id`, `id_users`, `amount_gross`, `amount_net`, `date`) VALUES
(1, 2, 5000, 3000, '2020-01-10'),
(2, 3, 7000, 4900, '2020-01-10'),
(3, 4, 11000, 8500, '2020-01-10');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `role`) VALUES
(1, 'boss@salins.pl', 'password', 'admin'),
(2, 'milox@salins.pl', 'password', 'user'),
(3, 'stefan@salins.pl', 'password', 'user'),
(4, 'mariusz@salins.pl', 'password', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `holidays_balance`
--
ALTER TABLE `holidays_balance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `holidays_requests`
--
ALTER TABLE `holidays_requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `salaries`
--
ALTER TABLE `salaries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `holidays_balance`
--
ALTER TABLE `holidays_balance`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `holidays_requests`
--
ALTER TABLE `holidays_requests`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `salaries`
--
ALTER TABLE `salaries`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
