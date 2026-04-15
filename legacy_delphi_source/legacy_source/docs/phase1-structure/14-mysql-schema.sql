-- Schema export (no data) for `chul_09_db`SET NAMES utf8mb4;

-- Table `G0_Gbun`
CREATE TABLE `G0_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `hcode` (`hcode`),
  KEY `gcode` (`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `G1_Gbun`
CREATE TABLE `G1_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G1_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=513 DEFAULT CHARSET=euckr;

-- Table `G1_Ggeo`
CREATE TABLE `G1_Ggeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `jubun` varchar(10) DEFAULT NULL,
  `pubun` char(2) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gnumb` varchar(12) DEFAULT NULL,
  `guper` varchar(30) DEFAULT NULL,
  `gjomo` varchar(30) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gadd1` varchar(90) DEFAULT NULL,
  `gadd2` varchar(90) DEFAULT NULL,
  `gtel1` varchar(4) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gfax1` varchar(4) DEFAULT NULL,
  `gfax2` varchar(20) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `grat2` int(11) DEFAULT NULL,
  `grat3` int(11) DEFAULT NULL,
  `grat4` int(11) DEFAULT NULL,
  `grat5` int(11) DEFAULT NULL,
  `grat6` int(11) DEFAULT NULL,
  `grat7` int(11) DEFAULT NULL,
  `grat8` int(11) DEFAULT NULL,
  `grat9` int(11) DEFAULT NULL,
  `gqut1` float DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `gpper` varchar(20) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gphon` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `bigo1` varchar(8) DEFAULT NULL,
  `bigo2` varchar(4) DEFAULT NULL,
  `bigo3` varchar(8) DEFAULT NULL,
  `bigo4` varchar(4) DEFAULT NULL,
  `gnum1` varchar(10) DEFAULT NULL,
  `gnum2` varchar(10) DEFAULT NULL,
  `memos` longblob,
  `gssum` float DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G1_Ggeo_index` (`hcode`,`gcode`,`gname`,`gposa`)
) ENGINE=MyISAM AUTO_INCREMENT=78520 DEFAULT CHARSET=euckr;

-- Table `G1_Ggeo_1`
CREATE TABLE `G1_Ggeo_1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `jubun` varchar(10) DEFAULT NULL,
  `pubun` char(2) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gnumb` varchar(12) DEFAULT NULL,
  `guper` varchar(30) DEFAULT NULL,
  `gjomo` varchar(30) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gadd1` varchar(90) DEFAULT NULL,
  `gadd2` varchar(90) DEFAULT NULL,
  `gtel1` varchar(4) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gfax1` varchar(4) DEFAULT NULL,
  `gfax2` varchar(20) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `grat2` int(11) DEFAULT NULL,
  `grat3` int(11) DEFAULT NULL,
  `grat4` int(11) DEFAULT NULL,
  `grat5` int(11) DEFAULT NULL,
  `grat6` int(11) DEFAULT NULL,
  `grat7` int(11) DEFAULT NULL,
  `grat8` int(11) DEFAULT NULL,
  `grat9` int(11) DEFAULT NULL,
  `gqut1` float DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `gpper` varchar(20) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gphon` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `bigo1` varchar(8) DEFAULT NULL,
  `bigo2` varchar(4) DEFAULT NULL,
  `bigo3` varchar(8) DEFAULT NULL,
  `bigo4` varchar(4) DEFAULT NULL,
  `gnum1` varchar(10) DEFAULT NULL,
  `gnum2` varchar(10) DEFAULT NULL,
  `memos` longblob,
  `gssum` float DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G1_Ggeo_index` (`hcode`,`gcode`,`gname`,`gposa`)
) ENGINE=MyISAM AUTO_INCREMENT=54523 DEFAULT CHARSET=euckr;

-- Table `G1_Logn`
CREATE TABLE `G1_Logn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `hname` varchar(50) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ghost` varchar(30) DEFAULT NULL,
  `gpass` varchar(30) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `f11` char(1) DEFAULT NULL,
  `f12` char(1) DEFAULT NULL,
  `f13` char(1) DEFAULT NULL,
  `f14` char(1) DEFAULT NULL,
  `f15` char(1) DEFAULT NULL,
  `f16` char(1) DEFAULT NULL,
  `f17` char(1) DEFAULT NULL,
  `f18` char(1) DEFAULT NULL,
  `f19` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G1_Logn_index` (`hcode`,`gcode`,`ghost`,`gpass`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=euckr;

-- Table `G2_Gbun`
CREATE TABLE `G2_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G2_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=129 DEFAULT CHARSET=euckr;

-- Table `G2_Ggwo`
CREATE TABLE `G2_Ggwo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `jubun` varchar(10) DEFAULT NULL,
  `pubun` char(2) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gnumb` varchar(12) DEFAULT NULL,
  `guper` varchar(30) DEFAULT NULL,
  `gjomo` varchar(30) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gadd1` varchar(90) DEFAULT NULL,
  `gadd2` varchar(90) DEFAULT NULL,
  `gtel1` varchar(4) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gfax1` varchar(4) DEFAULT NULL,
  `gfax2` varchar(20) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `grat2` int(11) DEFAULT NULL,
  `grat3` int(11) DEFAULT NULL,
  `grat4` int(11) DEFAULT NULL,
  `grat5` int(11) DEFAULT NULL,
  `grat6` int(11) DEFAULT NULL,
  `grat7` int(11) DEFAULT NULL,
  `grat8` int(11) DEFAULT NULL,
  `grat9` int(11) DEFAULT NULL,
  `gqut1` float DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `gpper` varchar(20) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gphon` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `bigo1` varchar(8) DEFAULT NULL,
  `bigo2` varchar(4) DEFAULT NULL,
  `bigo3` varchar(8) DEFAULT NULL,
  `bigo4` varchar(4) DEFAULT NULL,
  `gnum1` varchar(10) DEFAULT NULL,
  `gnum2` varchar(10) DEFAULT NULL,
  `memos` longblob,
  `gssum` float DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G2_Ggwo_index` (`hcode`,`gcode`,`gname`,`gposa`)
) ENGINE=MyISAM AUTO_INCREMENT=2275 DEFAULT CHARSET=euckr;

-- Table `G3_Gbun`
CREATE TABLE `G3_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G3_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=91 DEFAULT CHARSET=euckr;

-- Table `G3_Gjeo`
CREATE TABLE `G3_Gjeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `date1` varchar(10) DEFAULT NULL,
  `date2` varchar(10) DEFAULT NULL,
  `gjice` varchar(20) DEFAULT NULL,
  `gscho` varchar(20) DEFAULT NULL,
  `gnumb` varchar(20) DEFAULT NULL,
  `gnum1` varchar(20) DEFAULT NULL,
  `gnum2` varchar(20) DEFAULT NULL,
  `gtel1` varchar(4) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gfax1` varchar(4) DEFAULT NULL,
  `gfax2` varchar(20) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gadd1` varchar(90) DEFAULT NULL,
  `gadd2` varchar(90) DEFAULT NULL,
  `opost` varchar(7) DEFAULT NULL,
  `oadd1` varchar(90) DEFAULT NULL,
  `oadd2` varchar(90) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `ghost` varchar(30) DEFAULT NULL,
  `gpass` varchar(30) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `memos` longblob,
  `f11` char(1) DEFAULT NULL,
  `f12` char(1) DEFAULT NULL,
  `f13` char(1) DEFAULT NULL,
  `f14` char(1) DEFAULT NULL,
  `f15` char(1) DEFAULT NULL,
  `f16` char(1) DEFAULT NULL,
  `f17` char(1) DEFAULT NULL,
  `f18` char(1) DEFAULT NULL,
  `f19` char(1) DEFAULT NULL,
  `f21` char(1) DEFAULT NULL,
  `f22` char(1) DEFAULT NULL,
  `f23` char(1) DEFAULT NULL,
  `f24` char(1) DEFAULT NULL,
  `f25` char(1) DEFAULT NULL,
  `f26` char(1) DEFAULT NULL,
  `f27` char(1) DEFAULT NULL,
  `f28` char(1) DEFAULT NULL,
  `f29` char(1) DEFAULT NULL,
  `f31` char(1) DEFAULT NULL,
  `f32` char(1) DEFAULT NULL,
  `f33` char(1) DEFAULT NULL,
  `f34` char(1) DEFAULT NULL,
  `f35` char(1) DEFAULT NULL,
  `f36` char(1) DEFAULT NULL,
  `f37` char(1) DEFAULT NULL,
  `f38` char(1) DEFAULT NULL,
  `f39` char(1) DEFAULT NULL,
  `f41` char(1) DEFAULT NULL,
  `f42` char(1) DEFAULT NULL,
  `f43` char(1) DEFAULT NULL,
  `f44` char(1) DEFAULT NULL,
  `f45` char(1) DEFAULT NULL,
  `f46` char(1) DEFAULT NULL,
  `f47` char(1) DEFAULT NULL,
  `f48` char(1) DEFAULT NULL,
  `f49` char(1) DEFAULT NULL,
  `f51` char(1) DEFAULT NULL,
  `f52` char(1) DEFAULT NULL,
  `f53` char(1) DEFAULT NULL,
  `f54` char(1) DEFAULT NULL,
  `f55` char(1) DEFAULT NULL,
  `f56` char(1) DEFAULT NULL,
  `f57` char(1) DEFAULT NULL,
  `f58` char(1) DEFAULT NULL,
  `f59` char(1) DEFAULT NULL,
  `f61` char(1) DEFAULT NULL,
  `f62` char(1) DEFAULT NULL,
  `f63` char(1) DEFAULT NULL,
  `f64` char(1) DEFAULT NULL,
  `f65` char(1) DEFAULT NULL,
  `f66` char(1) DEFAULT NULL,
  `f67` char(1) DEFAULT NULL,
  `f68` char(1) DEFAULT NULL,
  `f69` char(1) DEFAULT NULL,
  `f71` char(1) DEFAULT NULL,
  `f72` char(1) DEFAULT NULL,
  `f73` char(1) DEFAULT NULL,
  `f74` char(1) DEFAULT NULL,
  `f75` char(1) DEFAULT NULL,
  `f76` char(1) DEFAULT NULL,
  `f77` char(1) DEFAULT NULL,
  `f78` char(1) DEFAULT NULL,
  `f79` char(1) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G3_Gjeo_index` (`hcode`,`gcode`,`gname`,`gposa`)
) ENGINE=MyISAM AUTO_INCREMENT=2803 DEFAULT CHARSET=euckr;

-- Table `G4_Book`
CREATE TABLE `G4_Book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `tcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `jubun` varchar(6) DEFAULT NULL,
  `pubun` char(2) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `ocode` varchar(10) DEFAULT NULL,
  `gname` varchar(80) DEFAULT NULL,
  `gjeja` varchar(30) DEFAULT NULL,
  `gdabi` varchar(5) DEFAULT NULL,
  `gdang` float DEFAULT NULL,
  `odang` float DEFAULT NULL,
  `price` float DEFAULT NULL,
  `gisbn` varchar(20) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `grat2` int(11) DEFAULT NULL,
  `grat3` int(11) DEFAULT NULL,
  `grat4` int(11) DEFAULT NULL,
  `grat5` int(11) DEFAULT NULL,
  `grat6` int(11) DEFAULT NULL,
  `grat7` int(11) DEFAULT NULL,
  `grat8` int(11) DEFAULT NULL,
  `grat9` int(11) DEFAULT NULL,
  `gbjil` varchar(6) DEFAULT NULL,
  `date1` varchar(10) DEFAULT NULL,
  `date2` varchar(10) DEFAULT NULL,
  `gnumb` varchar(20) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `gpage` float DEFAULT NULL,
  `gpan1` float DEFAULT NULL,
  `gpan2` float DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `jeja1` varchar(20) DEFAULT NULL,
  `jeja2` varchar(20) DEFAULT NULL,
  `gpost` varchar(20) DEFAULT NULL,
  `opost` varchar(20) DEFAULT NULL,
  `bcode` varchar(13) DEFAULT NULL,
  `bigo1` char(2) DEFAULT NULL,
  `bigo2` char(2) DEFAULT NULL,
  `bigo3` char(2) DEFAULT NULL,
  `bigo4` char(2) DEFAULT NULL,
  `memos` longblob,
  `gqut1` float DEFAULT NULL,
  `gqut2` float DEFAULT NULL,
  `gssum` float DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G4_Book_index` (`hcode`,`gcode`,`gname`,`gjeja`)
) ENGINE=MyISAM AUTO_INCREMENT=134545 DEFAULT CHARSET=euckr;

-- Table `G4_Gbun`
CREATE TABLE `G4_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `grat2` int(11) DEFAULT NULL,
  `grat3` int(11) DEFAULT NULL,
  `grat4` int(11) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G4_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=1141 DEFAULT CHARSET=euckr;

-- Table `G5_Gbun`
CREATE TABLE `G5_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G5_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=139 DEFAULT CHARSET=euckr;

-- Table `G5_Ggeo`
CREATE TABLE `G5_Ggeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `jubun` varchar(10) DEFAULT NULL,
  `pubun` char(2) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gnumb` varchar(12) DEFAULT NULL,
  `guper` varchar(30) DEFAULT NULL,
  `gjomo` varchar(30) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gadd1` varchar(90) DEFAULT NULL,
  `gadd2` varchar(90) DEFAULT NULL,
  `gtel1` varchar(4) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gfax1` varchar(4) DEFAULT NULL,
  `gfax2` varchar(20) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `grat2` int(11) DEFAULT NULL,
  `grat3` int(11) DEFAULT NULL,
  `grat4` int(11) DEFAULT NULL,
  `grat5` int(11) DEFAULT NULL,
  `grat6` int(11) DEFAULT NULL,
  `grat7` int(11) DEFAULT NULL,
  `grat8` int(11) DEFAULT NULL,
  `grat9` int(11) DEFAULT NULL,
  `gqut1` float DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `gpper` varchar(20) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gphon` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `bigo1` varchar(8) DEFAULT NULL,
  `bigo2` varchar(4) DEFAULT NULL,
  `bigo3` varchar(8) DEFAULT NULL,
  `bigo4` varchar(4) DEFAULT NULL,
  `gnum1` varchar(10) DEFAULT NULL,
  `gnum2` varchar(10) DEFAULT NULL,
  `memos` longblob,
  `gssum` float DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G5_Ggeo_index` (`hcode`,`gcode`,`gname`,`gposa`)
) ENGINE=MyISAM AUTO_INCREMENT=55444 DEFAULT CHARSET=euckr;

-- Table `G6_Ggeo`
CREATE TABLE `G6_Ggeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `gubun` varchar(20) DEFAULT NULL,
  `jubun` varchar(20) DEFAULT NULL,
  `gpper` varchar(20) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `grat2` int(11) DEFAULT NULL,
  `grat3` int(11) DEFAULT NULL,
  `grat4` int(11) DEFAULT NULL,
  `grat5` int(11) DEFAULT NULL,
  `grat6` int(11) DEFAULT NULL,
  `grat7` int(11) DEFAULT NULL,
  `grat8` int(11) DEFAULT NULL,
  `grat9` int(11) DEFAULT NULL,
  `gssum` float DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G6_Ggeo_index` (`hcode`,`gcode`,`bcode`)
) ENGINE=MyISAM AUTO_INCREMENT=215851 DEFAULT CHARSET=euckr;

-- Table `G7_Gbun`
CREATE TABLE `G7_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G7_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `G7_Ggeo`
CREATE TABLE `G7_Ggeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chek1` varchar(5) DEFAULT NULL,
  `chek2` varchar(5) DEFAULT NULL,
  `chek3` varchar(5) DEFAULT NULL,
  `chek4` varchar(5) DEFAULT NULL,
  `chek5` varchar(5) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `jubun` varchar(6) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gnumb` varchar(12) DEFAULT NULL,
  `guper` varchar(30) DEFAULT NULL,
  `gjomo` varchar(30) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `jumin` varchar(14) DEFAULT NULL,
  `gpper` varchar(20) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gadd1` varchar(90) DEFAULT NULL,
  `gadd2` varchar(90) DEFAULT NULL,
  `gtel1` varchar(4) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gfax1` varchar(4) DEFAULT NULL,
  `gfax2` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `bigo1` varchar(80) DEFAULT NULL,
  `bigo2` varchar(80) DEFAULT NULL,
  `gnum1` varchar(10) DEFAULT NULL,
  `giqut` float DEFAULT NULL,
  `gisum` float DEFAULT NULL,
  `gosum` float DEFAULT NULL,
  `gssum` float DEFAULT NULL,
  `sum02` float DEFAULT NULL,
  `sum04` float DEFAULT NULL,
  `sum06` float DEFAULT NULL,
  `sum09` float DEFAULT NULL,
  `sum12` float DEFAULT NULL,
  `sum15` float DEFAULT NULL,
  `sum18` float DEFAULT NULL,
  `sum19` float DEFAULT NULL,
  `sum21` float DEFAULT NULL,
  `sum22` float DEFAULT NULL,
  `sum25` float DEFAULT NULL,
  `sum32` float DEFAULT NULL,
  `sum33` float DEFAULT NULL,
  `sum34` float DEFAULT NULL,
  `sum36` float DEFAULT NULL,
  `sum38` float DEFAULT NULL,
  `sum39` float DEFAULT NULL,
  `sum40` float DEFAULT NULL,
  `sum41` float DEFAULT NULL,
  `sum42` float DEFAULT NULL,
  `sum43` float DEFAULT NULL,
  `sum44` float DEFAULT NULL,
  `sum45` float DEFAULT NULL,
  `sum46` float DEFAULT NULL,
  `sum47` float(2,1) DEFAULT NULL,
  `sum61` float DEFAULT NULL,
  `sum62` float DEFAULT NULL,
  `sum63` float DEFAULT NULL,
  `sum64` float DEFAULT NULL,
  `sum68` float DEFAULT NULL,
  `sum69` float DEFAULT NULL,
  `yes33` char(1) DEFAULT NULL,
  `yes34` char(1) DEFAULT NULL,
  `yes35` char(1) DEFAULT NULL,
  `yes41` char(1) DEFAULT NULL,
  `yes42` char(1) DEFAULT NULL,
  `yes43` char(1) DEFAULT NULL,
  `yes44` char(1) DEFAULT NULL,
  `yes45` char(1) DEFAULT NULL,
  `yes48` char(1) DEFAULT NULL,
  `yes49` char(1) DEFAULT NULL,
  `yes51` char(1) DEFAULT NULL,
  `yes52` char(1) DEFAULT NULL,
  `yes53` char(1) DEFAULT NULL,
  `yes54` char(1) DEFAULT NULL,
  `yes55` char(1) DEFAULT NULL,
  `yes56` char(1) DEFAULT NULL,
  `yes57` char(1) DEFAULT NULL,
  `yes58` char(1) DEFAULT NULL,
  `yes59` char(1) DEFAULT NULL,
  `yes61` char(1) DEFAULT NULL,
  `yes62` char(1) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `date1` char(2) DEFAULT NULL,
  `date2` char(2) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `memos` longblob,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G7_Ggeo_index` (`hcode`,`gcode`,`gname`,`gposa`)
) ENGINE=MyISAM AUTO_INCREMENT=198 DEFAULT CHARSET=euckr;

-- Table `G7_Logn`
CREATE TABLE `G7_Logn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `hname` varchar(30) DEFAULT NULL,
  `ghost` varchar(30) DEFAULT NULL,
  `gpass` varchar(30) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT '0',
  `check` char(1) DEFAULT NULL,
  `f11` char(1) DEFAULT NULL,
  `f12` char(1) DEFAULT NULL,
  `f13` char(1) DEFAULT NULL,
  `f14` char(1) DEFAULT NULL,
  `f15` char(1) DEFAULT NULL,
  `f16` char(1) DEFAULT NULL,
  `f17` char(1) DEFAULT NULL,
  `f18` char(1) DEFAULT NULL,
  `f19` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G7_Logn_index` (`hcode`)
) ENGINE=MyISAM AUTO_INCREMENT=74 DEFAULT CHARSET=euckr;

-- Table `G8_Gbun`
CREATE TABLE `G8_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G8_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `G8_Ggeo`
CREATE TABLE `G8_Ggeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(5) DEFAULT NULL,
  `jubun` varchar(6) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gadd1` varchar(90) DEFAULT NULL,
  `gadd2` varchar(90) DEFAULT NULL,
  `gtel1` varchar(4) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gfax1` varchar(4) DEFAULT NULL,
  `gfax2` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `G8_Ggeo_index` (`hcode`,`gcode`,`gname`,`gposa`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Gg_Book`
CREATE TABLE `Gg_Book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `gpper` varchar(20) DEFAULT NULL,
  `giqut` double(10,0) DEFAULT NULL,
  `gisum` double(10,0) DEFAULT NULL,
  `gpqut` double(10,0) DEFAULT NULL,
  `gpsum` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Gg_Book_index` (`gcode`,`hcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Gg_Magn`
CREATE TABLE `Gg_Magn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gu` char(2) DEFAULT NULL,
  `top` int(11) DEFAULT NULL,
  `l11` int(11) DEFAULT NULL,
  `l12` int(11) DEFAULT NULL,
  `l13` int(11) DEFAULT NULL,
  `l14` int(11) DEFAULT NULL,
  `f11` varchar(15) DEFAULT NULL,
  `f12` varchar(20) DEFAULT NULL,
  `f21` varchar(15) DEFAULT NULL,
  `f22` varchar(20) DEFAULT NULL,
  `f31` varchar(15) DEFAULT NULL,
  `f32` varchar(20) DEFAULT NULL,
  `f41` varchar(15) DEFAULT NULL,
  `f42` varchar(20) DEFAULT NULL,
  `f51` varchar(15) DEFAULT NULL,
  `f52` varchar(20) DEFAULT NULL,
  `f61` varchar(15) DEFAULT NULL,
  `f62` varchar(20) DEFAULT NULL,
  `f71` varchar(15) DEFAULT NULL,
  `f72` varchar(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `posa` varchar(15) DEFAULT NULL,
  `memo1` varchar(200) DEFAULT NULL,
  `memo2` varchar(200) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Gg_Magn_index` (`gu`,`hcode`)
) ENGINE=MyISAM AUTO_INCREMENT=303 DEFAULT CHARSET=euckr;

-- Table `Gg_Megn`
CREATE TABLE `Gg_Megn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` char(2) DEFAULT NULL,
  `gname` varchar(15) DEFAULT NULL,
  `gnumb` float DEFAULT NULL,
  `gfild` varchar(10) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Gg_Megn_index` (`hcode`)
) ENGINE=MyISAM AUTO_INCREMENT=414 DEFAULT CHARSET=euckr;

-- Table `Gg_Memo`
CREATE TABLE `Gg_Memo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `memos` longblob,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Gg_Memo_index` (`hcode`,`scode`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Gg_Post`
CREATE TABLE `Gg_Post` (
  `post` varchar(7) DEFAULT NULL,
  `addr` varchar(55) DEFAULT NULL,
  `dddd` varchar(4) DEFAULT NULL,
  `dong` varchar(20) DEFAULT NULL,
  `city` varchar(8) DEFAULT NULL,
  KEY `Gg_Post_index` (`post`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Gg_Prnt`
CREATE TABLE `Gg_Prnt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `ocode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `line1` float DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Gg_Prnt_index` (`hcode`,`scode`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Gs_Csum`
CREATE TABLE `Gs_Csum` (
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `giqut` double(10,0) DEFAULT NULL,
  `goqut` double(10,0) DEFAULT NULL,
  `gjqut` double(10,0) DEFAULT NULL,
  `gbqut` double(10,0) DEFAULT NULL,
  `gpqut` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `gsumx` double(10,0) DEFAULT NULL,
  `gsumy` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `Gs_Csum_index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Gs_Gsum`
CREATE TABLE `Gs_Gsum` (
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `goqut` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gjqut` double(10,0) DEFAULT NULL,
  `gjsum` double(10,0) DEFAULT NULL,
  `gbqut` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  `gsumx` double(10,0) DEFAULT NULL,
  `gsumy` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `Gs_Gsum_index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `H1_Gbun`
CREATE TABLE `H1_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `oname` varchar(50) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `clas1` double(10,0) DEFAULT NULL,
  `clas2` double(10,0) DEFAULT NULL,
  `clas3` double(10,0) DEFAULT NULL,
  `gsum1` double(10,0) DEFAULT NULL,
  `gsum2` double(10,0) DEFAULT NULL,
  `gsum3` double(10,0) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `H1_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=755 DEFAULT CHARSET=euckr;

-- Table `H1_Ssub`
CREATE TABLE `H1_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idnum` int(11) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `tcode` char(1) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `oname` varchar(50) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gsumx` double(10,0) DEFAULT NULL,
  `gsumy` double(10,0) DEFAULT NULL,
  `pubun` varchar(4) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `H1_Ssub_index` (`hcode`,`gdate`,`gcode`,`ocode`),
  KEY `H1_Ssub_hcode` (`hcode`),
  KEY `H1_Ssub_gdate` (`gdate`),
  KEY `H1_Ssub_gcode` (`gcode`),
  KEY `H1_Ssub_ocode` (`ocode`)
) ENGINE=MyISAM AUTO_INCREMENT=1181437 DEFAULT CHARSET=euckr;

-- Table `H2_Gbun`
CREATE TABLE `H2_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `oname` varchar(40) DEFAULT NULL,
  `jubun` varchar(30) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gphon` varchar(10) DEFAULT NULL,
  `gnum1` varchar(10) DEFAULT NULL,
  `clas1` double(10,0) DEFAULT NULL,
  `clas2` double(10,0) DEFAULT NULL,
  `clas3` double(10,0) DEFAULT NULL,
  `gsum1` double(10,0) DEFAULT NULL,
  `gsum2` double(10,0) DEFAULT NULL,
  `gsum3` double(10,0) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `memos` longblob,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `H2_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=12547 DEFAULT CHARSET=euckr;

-- Table `H4_Iyeo`
CREATE TABLE `H4_Iyeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idnum` int(11) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gnumb` varchar(30) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `date1` varchar(10) DEFAULT NULL,
  `date2` varchar(10) DEFAULT NULL,
  `date3` varchar(10) DEFAULT NULL,
  `date4` varchar(10) DEFAULT NULL,
  `gbang` varchar(50) DEFAULT NULL,
  `name1` varchar(50) DEFAULT NULL,
  `name2` varchar(50) DEFAULT NULL,
  `scode` varchar(8) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `H4_Iyeo_index` (`hcode`,`gnumb`)
) ENGINE=MyISAM AUTO_INCREMENT=16212 DEFAULT CHARSET=euckr;

-- Table `H5_Bang`
CREATE TABLE `H5_Bang` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(8) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gposa` varchar(30) DEFAULT NULL,
  `gnumb` varchar(24) DEFAULT NULL,
  `gubun` varchar(20) DEFAULT NULL,
  `gtels` varchar(15) DEFAULT NULL,
  `name1` varchar(20) DEFAULT NULL,
  `name2` varchar(20) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `class` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `H5_Bang_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=88 DEFAULT CHARSET=euckr;

-- Table `Id_Logn`
CREATE TABLE `Id_Logn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `hname` varchar(50) DEFAULT NULL,
  `gcode` varchar(50) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `f11` char(1) DEFAULT NULL,
  `f12` char(1) DEFAULT NULL,
  `f13` char(1) DEFAULT NULL,
  `f14` char(1) DEFAULT NULL,
  `f15` char(1) DEFAULT NULL,
  `f16` char(1) DEFAULT NULL,
  `f17` char(1) DEFAULT NULL,
  `f18` char(1) DEFAULT NULL,
  `f19` char(1) DEFAULT NULL,
  `f21` char(1) DEFAULT NULL,
  `f22` char(1) DEFAULT NULL,
  `f23` char(1) DEFAULT NULL,
  `f24` char(1) DEFAULT NULL,
  `f25` char(1) DEFAULT NULL,
  `f26` char(1) DEFAULT NULL,
  `f27` char(1) DEFAULT NULL,
  `f28` char(1) DEFAULT NULL,
  `f29` char(1) DEFAULT NULL,
  `f31` char(1) DEFAULT NULL,
  `f32` char(1) DEFAULT NULL,
  `f33` char(1) DEFAULT NULL,
  `f34` char(1) DEFAULT NULL,
  `f35` char(1) DEFAULT NULL,
  `f36` char(1) DEFAULT NULL,
  `f37` char(1) DEFAULT NULL,
  `f38` char(1) DEFAULT NULL,
  `f39` char(1) DEFAULT NULL,
  `f41` char(1) DEFAULT NULL,
  `f42` char(1) DEFAULT NULL,
  `f43` char(1) DEFAULT NULL,
  `f44` char(1) DEFAULT NULL,
  `f45` char(1) DEFAULT NULL,
  `f46` char(1) DEFAULT NULL,
  `f47` char(1) DEFAULT NULL,
  `f48` char(1) DEFAULT NULL,
  `f49` char(1) DEFAULT NULL,
  `f51` char(1) DEFAULT NULL,
  `f52` char(1) DEFAULT NULL,
  `f53` char(1) DEFAULT NULL,
  `f54` char(1) DEFAULT NULL,
  `f55` char(1) DEFAULT NULL,
  `f56` char(1) DEFAULT NULL,
  `f57` char(1) DEFAULT NULL,
  `f58` char(1) DEFAULT NULL,
  `f59` char(1) DEFAULT NULL,
  `f61` char(1) DEFAULT NULL,
  `f62` char(1) DEFAULT NULL,
  `f63` char(1) DEFAULT NULL,
  `f64` char(1) DEFAULT NULL,
  `f65` char(1) DEFAULT NULL,
  `f66` char(1) DEFAULT NULL,
  `f67` char(1) DEFAULT NULL,
  `f68` char(1) DEFAULT NULL,
  `f69` char(1) DEFAULT NULL,
  `f71` char(1) DEFAULT NULL,
  `f72` char(1) DEFAULT NULL,
  `f73` char(1) DEFAULT NULL,
  `f74` char(1) DEFAULT NULL,
  `f75` char(1) DEFAULT NULL,
  `f76` char(1) DEFAULT NULL,
  `f77` char(1) DEFAULT NULL,
  `f78` char(1) DEFAULT NULL,
  `f79` char(1) DEFAULT NULL,
  `f81` char(1) DEFAULT NULL,
  `f82` char(1) DEFAULT NULL,
  `f83` char(1) DEFAULT NULL,
  `f84` char(1) DEFAULT NULL,
  `f85` char(1) DEFAULT NULL,
  `f86` char(1) DEFAULT NULL,
  `f87` char(1) DEFAULT NULL,
  `f88` char(1) DEFAULT NULL,
  `f89` char(1) DEFAULT NULL,
  `gpass` varchar(20) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Id_Logn_index` (`gcode`,`gname`)
) ENGINE=MyISAM AUTO_INCREMENT=219 DEFAULT CHARSET=euckr;

-- Table `Id_Memo`
CREATE TABLE `Id_Memo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gnumb` float DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Id_Memo_index` (`hcode`,`gdate`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Ie_Logn`
CREATE TABLE `Ie_Logn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Ie_Logn_index` (`hcode`,`gcode`,`bcode`)
) ENGINE=MyISAM AUTO_INCREMENT=675 DEFAULT CHARSET=euckr;

-- Table `Ie_Memo`
CREATE TABLE `Ie_Memo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gnumb` float DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Ie_Memo_index` (`hcode`,`gcode`,`gdate`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `In_Csum`
CREATE TABLE `In_Csum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `In_Csum_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=14786 DEFAULT CHARSET=euckr;

-- Table `In_Gsum`
CREATE TABLE `In_Gsum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `In_Gsum_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=5486 DEFAULT CHARSET=euckr;

-- Table `J1_Sub1`
CREATE TABLE `J1_Sub1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `gpan1` varchar(5) DEFAULT NULL,
  `gpan2` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gdang` double(10,0) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `gsum1` double(10,0) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gbigo` blob,
  `gfile` varchar(200) DEFAULT NULL,
  `gfold` varchar(200) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `J1_Sub1_hcode` (`hcode`),
  KEY `J1_Sub1_bcode` (`bcode`),
  KEY `J1_Sub1_gdate` (`gdate`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J2_Sub1`
CREATE TABLE `J2_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J2_Sub2`
CREATE TABLE `J2_Sub2` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J3_Sub1`
CREATE TABLE `J3_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J4_Sub1`
CREATE TABLE `J4_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J5_Sub1`
CREATE TABLE `J5_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J6_Sub1`
CREATE TABLE `J6_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J6_Sub2`
CREATE TABLE `J6_Sub2` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J6_Sub3`
CREATE TABLE `J6_Sub3` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J7_Sub1`
CREATE TABLE `J7_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J8_Sub1`
CREATE TABLE `J8_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J9_Sub1`
CREATE TABLE `J9_Sub1` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `J9_Sub2`
CREATE TABLE `J9_Sub2` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Me_Sage`
CREATE TABLE `Me_Sage` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `gdate` varchar(10) DEFAULT NULL,
  `date1` varchar(10) DEFAULT NULL,
  `date2` varchar(10) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gbigo` longblob,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=58 DEFAULT CHARSET=euckr;

-- Table `S1_Chek`
CREATE TABLE `S1_Chek` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` char(1) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `gposa` varchar(50) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `gbigo` varchar(100) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `gnumb` char(2) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `S1_Chek_index` (`hcode`,`gdate`,`gcode`),
  KEY `S1_Chek_hcode` (`hcode`),
  KEY `S1_Chek_gdate` (`gdate`),
  KEY `S1_Chek_gcode` (`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=591601 DEFAULT CHARSET=euckr;

-- Table `S1_Memo`
CREATE TABLE `S1_Memo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `ocode` char(1) DEFAULT NULL,
  `pubun` varchar(4) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gbigo` varchar(90) DEFAULT NULL,
  `sbigo` varchar(90) DEFAULT NULL,
  `gtel1` varchar(20) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gname` varchar(30) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `S1_Memo_index` (`hcode`,`gdate`,`gcode`),
  KEY `S1_Memo_hcode` (`hcode`),
  KEY `S1_Memo_gdate` (`gdate`),
  KEY `S1_Memo_gcode` (`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=613718 DEFAULT CHARSET=euckr;

-- Table `S1_Ssub`
CREATE TABLE `S1_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `icode` int(11) DEFAULT NULL,
  `idnum` int(11) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `bdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` char(1) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `pubun` varchar(4) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `qsqut` double(10,0) DEFAULT NULL,
  `gdang` double(10,0) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `jeago` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `time4` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `S1_Ssub_index` (`hcode`,`gdate`,`gcode`,`bcode`),
  KEY `S1_Ssub_hcode` (`hcode`),
  KEY `S1_Ssub_gdate` (`gdate`),
  KEY `S1_Ssub_gcode` (`gcode`),
  KEY `S1_Ssub_bcode` (`bcode`),
  KEY `S1_Ssub_bdate` (`bdate`),
  KEY `S1_Ssub_icode` (`icode`)
) ENGINE=MyISAM AUTO_INCREMENT=24500709 DEFAULT CHARSET=euckr;

-- Table `S2_Ssub`
CREATE TABLE `S2_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ycode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gubun` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `hcode` char(1) DEFAULT NULL,
  `ocode` varchar(5) DEFAULT NULL,
  `oname` varchar(50) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `jubun` varchar(20) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gdang` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `S2_Ssub_index` (`ycode`,`gdate`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=139 DEFAULT CHARSET=euckr;

-- Table `S3_Ssub`
CREATE TABLE `S3_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `bcode` varchar(50) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `grat1` double(10,0) DEFAULT NULL,
  `gisum` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `S3_Ssub_index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=euckr;

-- Table `S7_Memo`
CREATE TABLE `S7_Memo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `ocode` char(1) DEFAULT NULL,
  `pubun` varchar(4) DEFAULT NULL,
  `gpost` varchar(7) DEFAULT NULL,
  `gbigo` varchar(90) DEFAULT NULL,
  `sbigo` varchar(90) DEFAULT NULL,
  `gtel1` varchar(20) DEFAULT NULL,
  `gtel2` varchar(20) DEFAULT NULL,
  `gname` varchar(30) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `S7_Memo_index` (`hcode`,`gdate`,`gcode`),
  KEY `S7_Memo_hcode` (`hcode`),
  KEY `S7_Memo_gdate` (`gdate`),
  KEY `S7_Memo_gcode` (`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=euckr;

-- Table `S7_Ssub`
CREATE TABLE `S7_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `icode` int(11) DEFAULT NULL,
  `idnum` int(11) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `bdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `ocode` char(1) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `pubun` varchar(4) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `qsqut` double(10,0) DEFAULT NULL,
  `gdang` double(10,0) DEFAULT NULL,
  `grat1` int(11) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `jeago` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `time1` datetime DEFAULT NULL,
  `time2` datetime DEFAULT NULL,
  `time3` datetime DEFAULT NULL,
  `time4` datetime DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `S7_Ssub_index` (`hcode`,`gdate`,`gcode`,`bcode`),
  KEY `S7_Ssub_hcode` (`hcode`),
  KEY `S7_Ssub_gdate` (`gdate`),
  KEY `S7_Ssub_gcode` (`gcode`),
  KEY `S7_Ssub_bcode` (`bcode`),
  KEY `S7_Ssub_bdate` (`bdate`),
  KEY `S7_Ssub_icode` (`icode`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=euckr;

-- Table `Sb_Csum`
CREATE TABLE `Sb_Csum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Sb_Csum_index` (`hcode`,`gdate`,`gcode`,`scode`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=euckr;

-- Table `Sg_Csum`
CREATE TABLE `Sg_Csum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Sg_Csum_index` (`hcode`,`gdate`,`gcode`,`scode`)
) ENGINE=MyISAM AUTO_INCREMENT=133570 DEFAULT CHARSET=euckr;

-- Table `Sg_Gsum`
CREATE TABLE `Sg_Gsum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Sg_Gsum_index` (`hcode`,`gdate`,`gcode`,`scode`)
) ENGINE=MyISAM AUTO_INCREMENT=95552 DEFAULT CHARSET=euckr;

-- Table `Sm_Ggeo`
CREATE TABLE `Sm_Ggeo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `name0` varchar(80) DEFAULT NULL,
  `name1` varchar(80) DEFAULT NULL,
  `name2` varchar(80) DEFAULT NULL,
  `name3` varchar(80) DEFAULT NULL,
  `name4` varchar(80) DEFAULT NULL,
  `gtel0` varchar(15) DEFAULT NULL,
  `gtel1` varchar(15) DEFAULT NULL,
  `gtel2` varchar(15) DEFAULT NULL,
  `gtel3` varchar(15) DEFAULT NULL,
  `gtel4` varchar(15) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Sm_Ggeo_hcode` (`hcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sm_Ssub`
CREATE TABLE `Sm_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gname` varchar(100) DEFAULT NULL,
  `gtel1` varchar(15) DEFAULT NULL,
  `gtel2` varchar(15) DEFAULT NULL,
  `memo0` varchar(50) DEFAULT NULL,
  `memo1` longblob,
  `sdate` datetime DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gcnts` double(10,0) DEFAULT NULL,
  `gleft` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `Sm_Ssub_hcode` (`hcode`),
  KEY `Sm_Ssub_gubun` (`gubun`),
  KEY `Sm_Ssub_gdate` (`gdate`),
  KEY `Sm_Ssub_gname` (`gname`),
  KEY `Sm_Ssub_gtel1` (`gtel1`),
  KEY `Sm_Ssub_gtel2` (`gtel2`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sv_Chng`
CREATE TABLE `Sv_Chng` (
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `goqut` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gjqut` double(10,0) DEFAULT NULL,
  `gjsum` double(10,0) DEFAULT NULL,
  `gbqut` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `Sv_Chng_index` (`hcode`,`gdate`,`gcode`,`scode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sv_Csum`
CREATE TABLE `Sv_Csum` (
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `giqut` double(10,0) DEFAULT NULL,
  `goqut` double(10,0) DEFAULT NULL,
  `gjqut` double(10,0) DEFAULT NULL,
  `gbqut` double(10,0) DEFAULT NULL,
  `gpqut` double(10,0) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `Sv_Csum_index` (`hcode`,`gdate`,`gcode`,`scode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sv_Ghng`
CREATE TABLE `Sv_Ghng` (
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(10) DEFAULT NULL,
  `giqut` double(10,0) DEFAULT NULL,
  `goqut` double(10,0) DEFAULT NULL,
  `gjqut` double(10,0) DEFAULT NULL,
  `gbqut` double(10,0) DEFAULT NULL,
  `gpqut` double(10,0) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `obqut` double(10,0) DEFAULT NULL,
  `obsum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `Sv_Ghng_index` (`hcode`,`gdate`,`gcode`,`scode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sv_Gsum`
CREATE TABLE `Sv_Gsum` (
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gubun` char(2) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `goqut` double(10,0) DEFAULT NULL,
  `gosum` double(10,0) DEFAULT NULL,
  `gjqut` double(10,0) DEFAULT NULL,
  `gjsum` double(10,0) DEFAULT NULL,
  `gbqut` double(10,0) DEFAULT NULL,
  `gbsum` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `Sv_Gsum_index` (`hcode`,`gdate`,`gcode`,`scode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sx_Chek`
CREATE TABLE `Sx_Chek` (
  `code1` char(1) DEFAULT NULL,
  `code2` varchar(5) DEFAULT NULL,
  KEY `Sx_Chek_code1` (`code1`),
  KEY `Sx_Chek_code2` (`code2`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sx_Host`
CREATE TABLE `Sx_Host` (
  `code1` char(1) DEFAULT NULL,
  `code2` varchar(5) DEFAULT NULL,
  `idkey` int(11) NOT NULL AUTO_INCREMENT,
  `id` float DEFAULT NULL,
  `idnum` float DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `bcode` varchar(10) DEFAULT NULL,
  `bname` varchar(80) DEFAULT NULL,
  `gjeja` varchar(30) DEFAULT NULL,
  `ocode` varchar(4) DEFAULT NULL,
  `pubun` varchar(4) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gdang` double(10,0) DEFAULT NULL,
  `grat1` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `gsumx` double(10,0) DEFAULT NULL,
  `gsumy` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gtels` varchar(20) DEFAULT NULL,
  `gfaxs` varchar(20) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idkey`),
  KEY `Sx_Host_code1` (`code1`),
  KEY `Sx_Host_code2` (`code2`),
  KEY `Sx_Host_id` (`id`),
  KEY `Sx_Host_hcode` (`hcode`),
  KEY `Sx_Host_gdate` (`gdate`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `Sx_Memo`
CREATE TABLE `Sx_Memo` (
  `code1` char(1) DEFAULT NULL,
  `code2` varchar(5) DEFAULT NULL,
  `scode` char(1) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gubun` varchar(4) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `Sx_Memo_index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `T1_Gbun`
CREATE TABLE `T1_Gbun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(20) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `jubun` varchar(15) DEFAULT NULL,
  `bebon` varchar(10) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T1_Gbun_index` (`hcode`,`gcode`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=euckr;

-- Table `T1_Ssub`
CREATE TABLE `T1_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `name1` varchar(30) DEFAULT NULL,
  `name2` varchar(30) DEFAULT NULL,
  `gnumb` varchar(30) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T1_Ssub_index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `T2_Ssub`
CREATE TABLE `T2_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gdate` varchar(10) DEFAULT NULL,
  `sdate` varchar(10) DEFAULT NULL,
  `hcode` varchar(5) DEFAULT NULL,
  `sum01` double(10,0) DEFAULT NULL,
  `sum02` double(10,0) DEFAULT NULL,
  `sum03` double(10,0) DEFAULT NULL,
  `sum04` double(10,0) DEFAULT NULL,
  `sum05` double(10,0) DEFAULT NULL,
  `sum06` double(10,0) DEFAULT NULL,
  `sum07` double(10,0) DEFAULT NULL,
  `sum08` double(10,0) DEFAULT NULL,
  `sum09` double(10,0) DEFAULT NULL,
  `sum10` double(10,0) DEFAULT NULL,
  `sum11` double(10,0) DEFAULT NULL,
  `sum12` double(10,0) DEFAULT NULL,
  `sum13` double(10,0) DEFAULT NULL,
  `sum14` double(10,0) DEFAULT NULL,
  `sum15` double(10,0) DEFAULT NULL,
  `sum16` double(10,0) DEFAULT NULL,
  `sum17` double(10,0) DEFAULT NULL,
  `sum18` double(10,0) DEFAULT NULL,
  `sum19` double(10,0) DEFAULT NULL,
  `sum20` double(10,0) DEFAULT NULL,
  `sum21` double(10,0) DEFAULT NULL,
  `sum22` double(10,0) DEFAULT NULL,
  `sum23` double(10,0) DEFAULT NULL,
  `sum24` double(10,0) DEFAULT NULL,
  `sum25` double(10,0) DEFAULT NULL,
  `sum26` double(10,0) DEFAULT NULL,
  `sum27` double(10,0) DEFAULT NULL,
  `sum28` double(10,0) DEFAULT NULL,
  `sum29` double(10,0) DEFAULT NULL,
  `sum30` double(10,0) DEFAULT NULL,
  `sum31` double(10,0) DEFAULT NULL,
  `sum32` double(10,0) DEFAULT NULL,
  `sum33` double(10,0) DEFAULT NULL,
  `sum34` double(10,0) DEFAULT NULL,
  `sum35` double(10,0) DEFAULT NULL,
  `sum36` double(10,0) DEFAULT NULL,
  `sum37` double(10,0) DEFAULT NULL,
  `sum40` double(10,0) DEFAULT NULL,
  `sum41` double(10,0) DEFAULT NULL,
  `sum42` double(10,0) DEFAULT NULL,
  `sum43` double(10,0) DEFAULT NULL,
  `sum44` double(10,0) DEFAULT NULL,
  `sum45` double(10,0) DEFAULT NULL,
  `sum46` double(10,0) DEFAULT NULL,
  `sum47` double(10,0) DEFAULT NULL,
  `sum48` double(10,0) DEFAULT NULL,
  `sum50` double(10,0) DEFAULT NULL,
  `sum51` double(10,0) DEFAULT NULL,
  `sum52` double(10,0) DEFAULT NULL,
  `sum53` double(10,0) DEFAULT NULL,
  `sum54` double(10,0) DEFAULT NULL,
  `sum55` double(10,0) DEFAULT NULL,
  `sum56` double(10,0) DEFAULT NULL,
  `sum57` double(10,0) DEFAULT NULL,
  `sum58` double(10,0) DEFAULT NULL,
  `sum59` double(10,0) DEFAULT NULL,
  `sum61` double(10,0) DEFAULT NULL,
  `sum62` double(10,0) DEFAULT NULL,
  `sum63` double(10,0) DEFAULT NULL,
  `sum64` double(10,0) DEFAULT NULL,
  `sum65` double(10,0) DEFAULT NULL,
  `sum66` double(10,0) DEFAULT NULL,
  `sum67` double(10,0) DEFAULT NULL,
  `sum68` double(10,0) DEFAULT NULL,
  `sum69` double(10,0) DEFAULT NULL,
  `sum70` double(10,0) DEFAULT NULL,
  `sum71` double(10,0) DEFAULT NULL,
  `sum72` double(10,0) DEFAULT NULL,
  `gsusu` double(10,0) DEFAULT NULL,
  `vdate` varchar(10) DEFAULT NULL,
  `bigo1` varchar(50) DEFAULT NULL,
  `bigo2` varchar(50) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `chek1` varchar(5) DEFAULT NULL,
  `chek2` datetime DEFAULT NULL,
  `chek3` varchar(5) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T2_Ssub_index` (`gdate`,`hcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `T3_Ssub`
CREATE TABLE `T3_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `name1` varchar(30) DEFAULT NULL,
  `name2` varchar(30) DEFAULT NULL,
  `gqut1` double(10,0) DEFAULT NULL,
  `gqut2` double(10,0) DEFAULT NULL,
  `gqut3` double(10,0) DEFAULT NULL,
  `gqut4` double(10,0) DEFAULT NULL,
  `gqut5` double(10,0) DEFAULT NULL,
  `gqut6` double(10,0) DEFAULT NULL,
  `gqut7` double(10,0) DEFAULT NULL,
  `gqut8` double(10,0) DEFAULT NULL,
  `gqut9` double(10,0) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gsum1` double(10,0) DEFAULT NULL,
  `gsum2` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T3_Ssub_index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `T4_Ssub`
CREATE TABLE `T4_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gjisa` varchar(30) DEFAULT NULL,
  `jubun` char(2) DEFAULT NULL,
  `pubun` char(2) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gqut1` double(10,0) DEFAULT NULL,
  `gqut2` double(10,0) DEFAULT NULL,
  `gqut3` double(10,0) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `yesno` varchar(5) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T4_Ssub_index` (`hcode`,`gcode`,`gdate`)
) ENGINE=MyISAM AUTO_INCREMENT=109990 DEFAULT CHARSET=euckr;

-- Table `T5_Ssub`
CREATE TABLE `T5_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `pubun` varchar(4) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T5_Ssub_Index` (`hcode`,`gdate`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `T6_Ssub`
CREATE TABLE `T6_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `name1` varchar(30) DEFAULT NULL,
  `name2` varchar(30) DEFAULT NULL,
  `gnumb` varchar(30) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gqut1` double(10,0) DEFAULT NULL,
  `gqut2` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T6_Ssub_Index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;

-- Table `T7_Ssub`
CREATE TABLE `T7_Ssub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hcode` varchar(5) DEFAULT NULL,
  `gdate` varchar(10) DEFAULT NULL,
  `gcode` varchar(5) DEFAULT NULL,
  `gname` varchar(50) DEFAULT NULL,
  `name1` varchar(30) DEFAULT NULL,
  `name2` varchar(30) DEFAULT NULL,
  `gnumb` varchar(30) DEFAULT NULL,
  `gbigo` varchar(50) DEFAULT NULL,
  `gsqut` double(10,0) DEFAULT NULL,
  `gdang` double(10,0) DEFAULT NULL,
  `gssum` double(10,0) DEFAULT NULL,
  `check` char(1) DEFAULT NULL,
  `gmemo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `T7_Ssub_index` (`hcode`,`gdate`,`gcode`)
) ENGINE=MyISAM DEFAULT CHARSET=euckr;
