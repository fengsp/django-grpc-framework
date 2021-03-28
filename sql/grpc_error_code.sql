-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  Dim 28 mars 2021 à 23:09
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
-- Structure de la table `django_grpc_framework_grcpdatabases`
--

DROP TABLE IF EXISTS `django_grpc_framework_grcpdatabases`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_grcpdatabases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `database` varchar(40) NOT NULL,
  `description` longtext,
  `django` varchar(40) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grcpdatabases_database_63208879` (`database`),
  KEY `django_grpc_framework_grcpdatabases_django_34d456fd` (`django`),
  KEY `django_grpc_framework_grcpdatabases_service_id_56b5b4bd` (`service_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grcpdatabases`
--

INSERT INTO `django_grpc_framework_grcpdatabases` (`id`, `created`, `modified`, `is_active`, `is_delete`, `database`, `description`, `django`, `service_id`) VALUES
(1, '2021-03-27 22:25:32.000000', '2021-03-28 14:22:36.515007', 1, 0, 'Car', '', 'carcheck', 1),
(2, '2021-03-28 21:01:39.000000', '2021-03-28 21:15:29.234007', 1, 0, 'Notification', '', 'notification', 2);

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
  `category` int(11) NOT NULL,
  `reason` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grcperrorcode_status_ca49a1b3` (`status`),
  KEY `django_grpc_framework_grcperrorcode_reason_22238c87` (`reason`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grcperrorcode`
--

INSERT INTO `django_grpc_framework_grcperrorcode` (`id`, `created`, `modified`, `code`, `status`, `notes`, `is_active`, `is_delete`, `count`, `category`, `reason`) VALUES
(1, '2021-03-26 00:45:50.685001', '2021-03-26 00:45:50.685001', 0, 'OK', 'Return on Success', 1, 0, 1, 1, ''),
(2, '2021-03-26 00:46:05.084001', '2021-03-26 00:46:05.084001', 1, 'CANCELLED', 'The operation was cancelled, typically by the caller.', 1, 0, 1, 1, ''),
(3, '2021-03-26 00:46:19.780001', '2021-03-26 00:46:19.780001', 2, 'UNKNOWN', 'For example, this error may be returned when a Status value received from another address space belongs to an error-space that isn\'t known in this address space. Also errors raised by APIs that don\'t return enough error information may be converted to this error.', 1, 0, 1, 1, ''),
(4, '2021-03-26 00:46:39.361001', '2021-03-26 00:46:39.361001', 3, 'INVALID_ARGUMENT', 'The client specified an invalid argument.', 1, 0, 1, 1, ''),
(5, '2021-03-26 00:46:58.978001', '2021-03-26 00:46:58.978001', 4, 'DEADLINE_EXCEEDED', 'The deadline expired before the operation was complete. For operations that change the state of the system, this error may be returned even if the operation is completed successfully. For example, a successful response from a server which was delayed long enough for the deadline to expire.', 1, 0, 1, 1, ''),
(6, '2021-03-26 00:47:14.393001', '2021-03-26 00:47:14.393001', 5, 'The deadline expired before the operatio', 'Some requested entity wasn\'t found.', 1, 0, 1, 1, ''),
(7, '2021-03-26 00:47:27.487001', '2021-03-26 00:47:27.487001', 6, 'ALREADY_EXISTS', 'The entity that a client attempted to create already exists.', 1, 0, 1, 1, ''),
(8, '2021-03-26 00:47:42.633001', '2021-03-26 00:47:42.633001', 7, 'PERMISSION_DENIED', 'The caller doesn\'t have permission to execute the specified operation. Don\'t use PERMISSION_DENIED for rejections caused by exhausting some resource; use RESOURCE_EXHAUSTED instead for those errors. Don\'t use PERMISSION_DENIED if the caller can\'t be identified (use UNAUTHENTICATED instead for those errors). To receive a PERMISSION_DENIED error code doesn\'t imply the request is valid or the requested entity exists or satisfies other pre-conditions.', 1, 0, 1, 1, ''),
(9, '2021-03-26 00:48:02.369001', '2021-03-26 00:48:02.369001', 8, 'RESOURCE_EXHAUSTED', 'Some resource has been exhausted, perhaps a per-user quota, or perhaps the entire file system is out of space.', 1, 0, 1, 1, ''),
(10, '2021-03-26 00:48:20.561001', '2021-03-26 00:48:20.561001', 9, 'FAILED_PRECONDITION', 'The operation was rejected because the system is not in a state required for the operation\'s execution. For example, the directory to be deleted is non-empty or an rmdir operation is applied to a non-directory.', 1, 0, 1, 1, ''),
(11, '2021-03-26 00:48:33.465001', '2021-03-26 00:48:33.465001', 10, 'ABORTED', 'The operation was aborted, typically due to a concurrency issue such as a sequencer check failure or transaction abort.', 1, 0, 1, 1, ''),
(12, '2021-03-26 00:48:51.037001', '2021-03-26 00:48:51.037001', 11, 'OUT_OF_RANGE', 'The operation was attempted past the valid range.', 1, 0, 1, 1, ''),
(13, '2021-03-26 00:49:03.000000', '2021-03-26 01:03:37.062001', 12, 'UNIMPLEMENTED', 'The operation isn\'t implemented or isn\'t supported/enabled in this service.', 1, 0, 1, 1, ''),
(14, '2021-03-26 00:49:18.060001', '2021-03-26 00:49:18.060001', 13, 'INTERNAL', 'Internal errors. This means that some invariants expected by the underlying system have been broken. This error code is reserved for serious errors.', 1, 0, 1, 1, ''),
(15, '2021-03-26 00:49:31.443001', '2021-03-26 00:49:31.443001', 14, 'UNAVAILABLE', 'The service is currently unavailable. This is most likely a transient condition that can be corrected if retried with a backoff.', 1, 0, 1, 1, ''),
(16, '2021-03-26 00:49:49.768001', '2021-03-26 00:49:49.768001', 15, 'DATA_LOSS', 'Unrecoverable data loss or corruption.', 1, 0, 1, 1, ''),
(17, '2021-03-26 00:50:08.415001', '2021-03-26 00:50:08.415001', 16, 'UNAUTHENTICATED', 'The request doesn\'t have valid authentication credentials for the operation.', 1, 0, 1, 1, ''),
(18, '2021-03-28 18:24:51.476007', '2021-03-28 18:24:51.476007', 900, 'SERVICE NOT FOUND', 'Socotoec MicroService Not found', 1, 0, 0, 1, ''),
(19, '2021-03-28 23:07:04.911007', '2021-03-28 23:07:04.911007', 901, 'INVALID METHOD', 'Accepted method are (List, Retrieve, Update or Destroy)', 1, 0, 0, 1, ''),
(20, '2021-03-29 00:38:43.801007', '2021-03-29 00:38:43.801007', 902, 'INVALID SERVICE', 'INVALID SOCIO SERVICE', 1, 0, 0, 1, ''),
(21, '2021-03-29 00:47:25.514007', '2021-03-29 00:47:25.514007', 903, 'NO DATABASE DEFINED FOR THIS SERVICE', 'No DataBase defined for the requested Service, please see Addmin tool to update the following Database : grpcDatabase', 1, 0, 0, 1, ''),
(22, '2021-03-29 00:50:17.499007', '2021-03-29 00:50:17.499007', 904, 'NO METHOD FOUND', 'The required method has not been defined for the requested Service, please Update the admin tool : update the Table   gRPCMethod', 1, 0, 0, 1, ''),
(23, '2021-03-29 00:52:38.685007', '2021-03-29 00:52:38.685007', 905, 'MISS PROTOBUF FIELDS', 'Please add protobuf fields to the gRPC admin tool : please update the following table :grpcProtocolBufFields', 1, 0, 0, 1, ''),
(24, '2021-03-29 00:57:25.900007', '2021-03-29 00:57:25.900007', 906, 'MISSING PB2 GRPC FILE', 'the related pb2 grpc python file is missing, please execute the command :  python -m grpc_tools.protoc', 1, 0, 0, 1, ''),
(25, '2021-03-29 00:59:45.398007', '2021-03-29 00:59:45.398007', 907, 'NO GRPC SERVER FOUND', 'No grpc server found or Invalid Port\r\n\r\nPlease start as followed : python manage.py grpcrunserver --dev', 1, 0, 0, 1, ''),
(26, '2021-03-29 01:05:11.658007', '2021-03-29 01:05:11.658007', 908, 'INVALID STUD REQUEST', 'The Stud request has failed, please review the xxx_pb2.py module and verify if the related Database Request method is present and valid : NNNDDDRequest', 1, 0, 0, 1, '');

-- --------------------------------------------------------

--
-- Structure de la table `django_grpc_framework_grcpmicroservices`
--

DROP TABLE IF EXISTS `django_grpc_framework_grcpmicroservices`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_grcpmicroservices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `service` varchar(40) NOT NULL,
  `category` int(11) NOT NULL,
  `description` longtext,
  `count` bigint(20) NOT NULL,
  `directory` varchar(60) NOT NULL,
  `isInput` tinyint(1) NOT NULL,
  `result` int(11) NOT NULL,
  `error` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grcpmicroservices_service_02ac832f` (`service`),
  KEY `django_grpc_framework_grcpmicroservices_directory_741529b2` (`directory`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grcpmicroservices`
--

INSERT INTO `django_grpc_framework_grcpmicroservices` (`id`, `created`, `modified`, `is_active`, `is_delete`, `service`, `category`, `description`, `count`, `directory`, `isInput`, `result`, `error`) VALUES
(1, '2021-03-26 15:00:52.000000', '2021-03-28 15:01:55.841007', 1, 0, 'carcheck', 1, 'Car Check  Back Microservices', 0, 'carcheck', 0, 1, 0),
(2, '2021-03-28 21:14:54.519007', '2021-03-28 21:14:54.519007', 1, 0, 'notification', 1, 'notification email', 0, 'notification', 1, 2, 0);

-- --------------------------------------------------------

--
-- Structure de la table `django_grpc_framework_grcpprotobuf`
--

DROP TABLE IF EXISTS `django_grpc_framework_grcpprotobuf`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_grcpprotobuf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `protobuf` varchar(50) NOT NULL,
  `file` varchar(50) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grcpprotobuf_protobuf_797a86f1` (`protobuf`),
  KEY `django_grpc_framework_grcpprotobuf_file_4be55168` (`file`),
  KEY `django_grpc_framework_grcpprotobuf_service_id_d7f65dd9` (`service_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grcpprotobuf`
--

INSERT INTO `django_grpc_framework_grcpprotobuf` (`id`, `created`, `modified`, `is_active`, `is_delete`, `protobuf`, `file`, `service_id`) VALUES
(1, '2021-03-27 22:25:46.144600', '2021-03-27 22:25:46.144600', 1, 0, 'carcheck.proto', '', 1),
(2, '2021-03-28 21:01:39.638007', '2021-03-28 21:01:39.638007', 1, 0, 'notification.proto', 'notification.proto', 2);

-- --------------------------------------------------------

--
-- Structure de la table `django_grpc_framework_grcpprotobuffields`
--

DROP TABLE IF EXISTS `django_grpc_framework_grcpprotobuffields`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_grcpprotobuffields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `field` varchar(50) NOT NULL,
  `is_query` tinyint(1) NOT NULL,
  `field_sequence` int(11) NOT NULL,
  `query_sequence` int(11) NOT NULL,
  `database_id` int(11) DEFAULT NULL,
  `protobuf_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grcpprotobuffields_field_10b5709e` (`field`),
  KEY `django_grpc_framework_grcpprotobuffields_database_id_187e91e7` (`database_id`),
  KEY `django_grpc_framework_grcpprotobuffields_protobuf_id_a9908976` (`protobuf_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grcpprotobuffields`
--

INSERT INTO `django_grpc_framework_grcpprotobuffields` (`id`, `created`, `modified`, `is_active`, `is_delete`, `field`, `is_query`, `field_sequence`, `query_sequence`, `database_id`, `protobuf_id`) VALUES
(1, '2021-03-27 22:37:28.000000', '2021-03-28 22:07:33.862007', 1, 0, 'brand', 1, 1, 1, 1, 1),
(2, '2021-03-27 22:37:30.702600', '2021-03-27 22:37:30.702600', 1, 0, 'model', 0, 2, 1, 1, 1),
(3, '2021-03-27 22:37:32.290600', '2021-03-27 22:37:32.290600', 1, 0, 'version', 0, 3, 1, 1, 1),
(4, '2021-03-28 21:01:39.643007', '2021-03-28 21:01:39.643007', 1, 0, 'recipient_email', 0, 1, 1, 2, 2),
(5, '2021-03-28 21:01:39.645007', '2021-03-28 21:01:39.645007', 1, 0, 'read', 0, 2, 1, 2, 2),
(6, '2021-03-28 21:01:39.647007', '2021-03-28 21:01:39.647007', 1, 0, 'sender_email', 0, 3, 1, 2, 2),
(7, '2021-03-28 21:01:39.649007', '2021-03-28 21:01:39.649007', 1, 0, 'application', 0, 4, 1, 2, 2),
(8, '2021-03-28 21:01:39.650007', '2021-03-28 21:01:39.650007', 1, 0, 'code', 0, 5, 1, 2, 2),
(9, '2021-03-28 21:01:39.652007', '2021-03-28 21:01:39.652007', 1, 0, 'data', 0, 6, 1, 2, 2),
(10, '2021-03-28 21:01:39.656007', '2021-03-28 21:01:39.656007', 1, 0, 'is_email', 0, 7, 1, 2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `django_grpc_framework_grpclogging`
--

DROP TABLE IF EXISTS `django_grpc_framework_grpclogging`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_grpclogging` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `method` int(11) NOT NULL,
  `query` longtext,
  `elapse` double NOT NULL,
  `database_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `result` longtext NOT NULL,
  `CQRS` tinyint(1) NOT NULL,
  `EventStore` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grpclogging_database_id_539d8dd6` (`database_id`),
  KEY `django_grpc_framework_grpclogging_service_id_0af8e429` (`service_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grpclogging`
--

INSERT INTO `django_grpc_framework_grpclogging` (`id`, `created`, `modified`, `is_active`, `is_delete`, `method`, `query`, `elapse`, `database_id`, `service_id`, `result`, `CQRS`, `EventStore`) VALUES
(1, '2021-03-28 20:04:01.050007', '2021-03-28 20:04:01.050007', 1, 0, 1, '', 4.96, 1, 1, '[brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n, brand: \"volkswagen\"\nmodel: \"touran\"\nversion: \"gti\"\n]', 0, 0),
(2, '2021-03-28 21:30:02.129007', '2021-03-28 21:30:02.129007', 1, 0, 1, '', 4.43, 1, 1, '[brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n, brand: \"volkswagen\"\nmodel: \"touran\"\nversion: \"gti\"\n]', 0, 0),
(3, '2021-03-29 00:03:51.408007', '2021-03-29 00:03:51.408007', 1, 0, 3, '', 13.91, 1, 1, 'brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n', 0, 0),
(4, '2021-03-29 00:06:32.094007', '2021-03-29 00:06:32.094007', 1, 0, 3, '', 3.8, 1, 1, 'brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n', 0, 0),
(5, '2021-03-29 00:07:41.228007', '2021-03-29 00:07:41.228007', 1, 0, 3, '', 5.58, 1, 1, 'brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n', 0, 0),
(6, '2021-03-29 00:09:23.968007', '2021-03-29 00:09:23.968007', 1, 0, 3, '', 0.11, 1, 1, 'brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n', 0, 0),
(7, '2021-03-29 00:09:43.567007', '2021-03-29 00:09:43.567007', 1, 0, 3, '', 0.11, 1, 1, 'brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n', 0, 0),
(8, '2021-03-29 01:07:38.240007', '2021-03-29 01:07:38.240007', 1, 0, 3, '', 0.25, 1, 1, 'brand: \"renault\"\nmodel: \"clio\"\nversion: \"gti\"\n', 0, 0);

-- --------------------------------------------------------

--
-- Structure de la table `django_grpc_framework_grpcmethod`
--

DROP TABLE IF EXISTS `django_grpc_framework_grpcmethod`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_grpcmethod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `method` varchar(40) NOT NULL,
  `database_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `result` varchar(40) NOT NULL,
  `is_update` tinyint(1) NOT NULL,
  `input` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_grpcmethod_database_id_a2460b7c` (`database_id`),
  KEY `django_grpc_framework_grpcmethod_service_id_03694929` (`service_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_grpcmethod`
--

INSERT INTO `django_grpc_framework_grpcmethod` (`id`, `created`, `modified`, `is_active`, `is_delete`, `method`, `database_id`, `service_id`, `result`, `is_update`, `input`) VALUES
(1, '2021-03-28 23:45:59.164007', '2021-03-28 23:50:00.795007', 1, 0, 'list', 1, 1, 'array', 0, 'array'),
(2, '2021-03-28 23:50:12.070007', '2021-03-29 00:01:37.567007', 1, 0, 'retrieve', 1, 1, 'get', 0, 'arg');

-- --------------------------------------------------------

--
-- Structure de la table `django_grpc_framework_sociogrpcerrors`
--

DROP TABLE IF EXISTS `django_grpc_framework_sociogrpcerrors`;
CREATE TABLE IF NOT EXISTS `django_grpc_framework_sociogrpcerrors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `method` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `aborted` tinyint(1) NOT NULL,
  `database_id` int(11) DEFAULT NULL,
  `error_id` int(11) DEFAULT NULL,
  `query` longtext,
  `service_id` int(11) DEFAULT NULL,
  `custom` tinyint(1) NOT NULL,
  `reason` varchar(250) NOT NULL,
  `elapse` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_grpc_framework_sociogrpcerrors_database_id_d099299f` (`database_id`),
  KEY `django_grpc_framework_sociogrpcerrors_error_id_b1055feb` (`error_id`),
  KEY `django_grpc_framework_sociogrpcerrors_service_id_35b2e896` (`service_id`),
  KEY `django_grpc_framework_sociogrpcerrors_reason_5d4c9aa0` (`reason`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_grpc_framework_sociogrpcerrors`
--

INSERT INTO `django_grpc_framework_sociogrpcerrors` (`id`, `created`, `modified`, `method`, `is_active`, `is_delete`, `aborted`, `database_id`, `error_id`, `query`, `service_id`, `custom`, `reason`, `elapse`) VALUES
(1, '2021-03-28 19:05:36.708007', '2021-03-28 19:05:36.708007', 0, 1, 0, 1, 1, 18, '', 1, 1, '', 0),
(2, '2021-03-28 19:07:14.923007', '2021-03-28 19:07:14.923007', 0, 1, 0, 1, 1, 18, '', 1, 1, '', 0),
(3, '2021-03-28 19:24:19.889007', '2021-03-28 19:24:19.889007', 0, 1, 0, 1, 1, 18, '', 1, 1, '', 0.04700016975402832),
(4, '2021-03-28 19:25:44.960007', '2021-03-28 19:25:44.960007', 0, 1, 0, 1, 1, 18, '', 1, 1, '', 0.05),
(5, '2021-03-28 19:26:47.385007', '2021-03-28 19:26:47.385007', 0, 1, 0, 1, 1, 18, '', 1, 1, 'Invalid Method or Service [CarList2Request]', 0.05),
(6, '2021-03-29 00:17:45.645007', '2021-03-29 00:17:45.645007', 3, 1, 0, 1, 1, 6, '', 1, 0, '', 0.11),
(7, '2021-03-29 00:18:06.449007', '2021-03-29 00:18:06.449007', 3, 1, 0, 1, 1, 6, '', 1, 0, '', 0.11),
(8, '2021-03-29 01:06:08.243007', '2021-03-29 01:06:08.243007', 3, 1, 0, 1, 1, 15, '', 1, 0, '', 4.38),
(9, '2021-03-29 01:07:05.022007', '2021-03-29 01:07:05.022007', 3, 1, 0, 1, 1, 15, '', 1, 0, '', 5.67),
(10, '2021-03-29 01:07:48.495007', '2021-03-29 01:07:48.495007', 3, 1, 0, 1, 1, 6, '', 1, 0, '', 0.11);
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
