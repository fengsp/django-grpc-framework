-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  ven. 26 mars 2021 à 00:31
-- Version du serveur :  5.7.24
-- Version de PHP :  7.2.14

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `carcheck`
--

-- --------------------------------------------------------

--
-- Structure de la table `django_grpc_framework_grcperrorcode`
--

DROP TABLE IF EXISTS `django_grpc_framework_grcperrorcode`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_grcperrorcode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `code` int(11) NOT NULL,
  `status` varchar(40) NOT NULL,
  `notes` longtext,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grcperrorcode_status_ca49a1b3` (`status`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grcperrorcode`
--

INSERT INTO `django_grpc_framework_grcperrorcode` (`id`, `created`, `modified`, `code`, `status`, `notes`, `is_active`, `is_delete`, `count`) VALUES
(1, '2021-03-26 00:45:50.685001', '2021-03-26 00:45:50.685001', 0, 'OK', 'Return on Success', 1, 0, 1),
(2, '2021-03-26 00:46:05.084001', '2021-03-26 00:46:05.084001', 1, 'CANCELLED', 'The operation was cancelled, typically by the caller.', 1, 0, 1),
(3, '2021-03-26 00:46:19.780001', '2021-03-26 00:46:19.780001', 2, 'UNKNOWN', 'For example, this error may be returned when a Status value received from another address space belongs to an error-space that isn\'t known in this address space. Also errors raised by APIs that don\'t return enough error information may be converted to this error.', 1, 0, 1),
(4, '2021-03-26 00:46:39.361001', '2021-03-26 00:46:39.361001', 3, 'INVALID_ARGUMENT', 'The client specified an invalid argument.', 1, 0, 1),
(5, '2021-03-26 00:46:58.978001', '2021-03-26 00:46:58.978001', 4, 'DEADLINE_EXCEEDED', 'The deadline expired before the operation was complete. For operations that change the state of the system, this error may be returned even if the operation is completed successfully. For example, a successful response from a server which was delayed long enough for the deadline to expire.', 1, 0, 1),
(6, '2021-03-26 00:47:14.393001', '2021-03-26 00:47:14.393001', 5, 'The deadline expired before the operatio', 'Some requested entity wasn\'t found.', 1, 0, 1),
(7, '2021-03-26 00:47:27.487001', '2021-03-26 00:47:27.487001', 6, 'ALREADY_EXISTS', 'The entity that a client attempted to create already exists.', 1, 0, 1),
(8, '2021-03-26 00:47:42.633001', '2021-03-26 00:47:42.633001', 7, 'PERMISSION_DENIED', 'The caller doesn\'t have permission to execute the specified operation. Don\'t use PERMISSION_DENIED for rejections caused by exhausting some resource; use RESOURCE_EXHAUSTED instead for those errors. Don\'t use PERMISSION_DENIED if the caller can\'t be identified (use UNAUTHENTICATED instead for those errors). To receive a PERMISSION_DENIED error code doesn\'t imply the request is valid or the requested entity exists or satisfies other pre-conditions.', 1, 0, 1),
(9, '2021-03-26 00:48:02.369001', '2021-03-26 00:48:02.369001', 8, 'RESOURCE_EXHAUSTED', 'Some resource has been exhausted, perhaps a per-user quota, or perhaps the entire file system is out of space.', 1, 0, 1),
(10, '2021-03-26 00:48:20.561001', '2021-03-26 00:48:20.561001', 9, 'FAILED_PRECONDITION', 'The operation was rejected because the system is not in a state required for the operation\'s execution. For example, the directory to be deleted is non-empty or an rmdir operation is applied to a non-directory.', 1, 0, 1),
(11, '2021-03-26 00:48:33.465001', '2021-03-26 00:48:33.465001', 10, 'ABORTED', 'The operation was aborted, typically due to a concurrency issue such as a sequencer check failure or transaction abort.', 1, 0, 1),
(12, '2021-03-26 00:48:51.037001', '2021-03-26 00:48:51.037001', 11, 'OUT_OF_RANGE', 'The operation was attempted past the valid range.', 1, 0, 1),
(13, '2021-03-26 00:49:03.000000', '2021-03-26 01:03:37.062001', 12, 'UNIMPLEMENTED', 'The operation isn\'t implemented or isn\'t supported/enabled in this service.', 1, 0, 1),
(14, '2021-03-26 00:49:18.060001', '2021-03-26 00:49:18.060001', 13, 'INTERNAL', 'Internal errors. This means that some invariants expected by the underlying system have been broken. This error code is reserved for serious errors.', 1, 0, 1),
(15, '2021-03-26 00:49:31.443001', '2021-03-26 00:49:31.443001', 14, 'UNAVAILABLE', 'The service is currently unavailable. This is most likely a transient condition that can be corrected if retried with a backoff.', 1, 0, 1),
(16, '2021-03-26 00:49:49.768001', '2021-03-26 00:49:49.768001', 15, 'DATA_LOSS', 'Unrecoverable data loss or corruption.', 1, 0, 1),
(17, '2021-03-26 00:50:08.415001', '2021-03-26 00:50:08.415001', 16, 'UNAUTHENTICATED', 'The request doesn\'t have valid authentication credentials for the operation.', 1, 0, 1);
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
