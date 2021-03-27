-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2020-11-27 08:53:04
-- 伺服器版本： 10.4.14-MariaDB
-- PHP 版本： 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `db`
--

-- --------------------------------------------------------

--
-- 資料表結構 `comment`
--

CREATE TABLE `comment` (
  `commentid` int(255) NOT NULL,
  `wid` int(255) NOT NULL,
  `postuser` varchar(255) NOT NULL,
  `usericon` varchar(255) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 傾印資料表的資料 `comment`
--

INSERT INTO `comment` (`commentid`, `wid`, `postuser`, `usericon`, `content`, `time`) VALUES
(17, 2, '1234', '65330068a5404385b908059680a9ccdf_l.png', 'hgfhgfh', '2019-03-20 08:12:48'),
(18, 28, '1234', 'b7254a0764144e5e9121fbc3868667a6_l.png', 'hi', '2020-11-23 06:38:50'),
(20, 26, '1234', 'd333ed48fdc44eb0b6de98f98f646c59_l.png', 'It\'s good', '2020-11-24 10:01:17'),
(21, 25, '1234', 'd333ed48fdc44eb0b6de98f98f646c59_l.png', '1234', '2020-11-24 10:08:29'),
(23, 24, '1234', 'd333ed48fdc44eb0b6de98f98f646c59_l.png', '1245', '2020-11-24 10:13:21'),
(25, 32, '1234', 'https://i.imgur.com/TeiJJKq.png', '1234', '2020-11-26 12:33:31'),
(26, 33, '1111', 'https://i.imgur.com/ecc2q63.png', 'hi', '2020-11-26 12:36:53'),
(27, 35, '1111', 'https://i.imgur.com/ecc2q63.png', '1234', '2020-11-26 12:58:50'),
(28, 35, '1234', 'https://i.imgur.com/TeiJJKq.png', 'good', '2020-11-26 12:59:26'),
(29, 36, '1111', 'https://i.imgur.com/IABYllq.png', '1234', '2020-11-26 13:04:17');

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `Userid` int(8) NOT NULL,
  `Username` varchar(20) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Register_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `icon` varchar(255) NOT NULL DEFAULT 'https://i.imgur.com/ecc2q63.png',
  `Description` varchar(1000) DEFAULT NULL,
  `Admin` varchar(5) NOT NULL DEFAULT 'false'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`Userid`, `Username`, `Password`, `Email`, `Register_date`, `icon`, `Description`, `Admin`) VALUES
(10, '1234', '$5$rounds=535000$rxvuolxmhYh0spXI$aAJQjJX1bSeuCxT2BuX27e6nHMbs2PHTb6ZmuTt6GN1', '123@123', '2019-04-02 12:51:37', 'https://i.imgur.com/TeiJJKq.png', 'Hi everybody', 'True'),
(14, '1111', '$5$rounds=535000$UTwHBtTIKT3kdKkP$mIfnRh9kRTNq4Mh9UZ21asyN2YsV8Je5c0T0OJbQVu/', '1111@gmail.com', '2020-11-26 12:34:54', 'https://i.imgur.com/IABYllq.png', 'A samll potato', 'false'),
(15, '2222', '$5$rounds=535000$LpQV2V4j2h/3JgWf$cJ0.9qL37.oN8qvcuH4cWdMRqvaDrwpwhzLjajwNAdC', '2222@gmail.com', '2020-11-27 06:55:27', 'https://i.imgur.com/Ko62l9s.png', 'happy every day', 'false');

-- --------------------------------------------------------

--
-- 資料表結構 `works`
--

CREATE TABLE `works` (
  `id` int(255) NOT NULL,
  `Author` varchar(255) NOT NULL,
  `Wname` varchar(100) NOT NULL,
  `iname` varchar(255) NOT NULL,
  `aname` varchar(255) NOT NULL,
  `Description` varchar(1000) NOT NULL,
  `ulike` int(255) DEFAULT NULL,
  `UploadDate` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 傾印資料表的資料 `works`
--

INSERT INTO `works` (`id`, `Author`, `Wname`, `iname`, `aname`, `Description`, `ulike`, `UploadDate`) VALUES
(32, '1234', '123', 'https://i.imgur.com/6O1HMKl.jpg', 'temp', '123', NULL, '2020-11-25 21:25:33'),
(33, '1234', '1', 'https://i.imgur.com/YQIt5vK.jpg', 'temp', '1', NULL, '2020-11-25 21:29:56'),
(34, '1234', '3', 'https://i.imgur.com/tqldGrH.jpg', 'temp', '3', NULL, '2020-11-25 21:35:00'),
(35, '1111', 'pokemon', 'https://i.imgur.com/U2hsYJB.gif', 'temp', 'pokemon', NULL, '2020-11-26 20:58:38'),
(36, '1111', 'sky cat', 'https://i.imgur.com/tsyJzzY.jpeg', 'temp', 'catcat', NULL, '2020-11-26 21:03:18'),
(37, '2222', 'meme', 'https://i.imgur.com/6EZhV8r.jpeg', 'temp', 'meme', NULL, '2020-11-27 14:56:35');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`commentid`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`Userid`);

--
-- 資料表索引 `works`
--
ALTER TABLE `works`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `comment`
--
ALTER TABLE `comment`
  MODIFY `commentid` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `Userid` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `works`
--
ALTER TABLE `works`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
