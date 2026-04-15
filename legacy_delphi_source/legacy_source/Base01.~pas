unit Base01;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ComCtrls, DBGrids, Db, Grids, DBClient, ScktComp, SConnect, MConnect,
  DBClientSocket, IBDatabase, DBClientTable, ZTransact, ZMySqlTr, ZConnect,
  ZMySqlCon, MySqlClientTable, DBGridEh, ZQuery, ZMySqlQuery, ComObj;

const
  E_Ggeo  : String = '출판사명을 입력해 주세요.';
  E_Open  : String = '오픈시 에러가 발생했습니다.'+#13+'다시 시도해 주십시오.';
  E_Insert: String = '입력시 에러가 발생했습니다.'+#13+'다시 시도해 주십시오.';
  E_Update: String = '수정시 에러가 발생했습니다.'+#13+'다시 시도해 주십시오.';
  E_Delete: String = '삭제시 에러가 발생했습니다.'+#13+'다시 시도해 주십시오.';
  E_Connect:String = '사용관한이 없습니다.'+#13+'관리자에게 문의하십시오.';

  //D_Select: String = '('+'Check is null '+' or '+'Check'+'<>'+#39+'D'+#39+')'+' and ';
  //D_Open:   String = '('+'Check is null '+' or '+'Check'+'<>'+#39+'D'+#39+')';
  D_Open:   String = '('+' `Check` is null '+' or '+' `Check` '+'<>'+#39+'D'+#39+')';
  D_Select: String = '';

  //-손수레-//
  S_Where0: String = '';
  S_Where1: String = '';
  S_Where2: String = '';
{ S_Where0: String = '('+'S.Hcode = 029'+' or '+'S.Hcode = 122'+')';
  S_Where1: String = '('+'Hcode = 029'+' or '+'Hcode = 122'+')';
  S_Where2: String = '('+'Gcode = 029'+' or '+'Gcode = 122'+')'; }

type
  TBase10 = class(TDataModule)
    T1_Sub11: TClientDataSet;
    T1_Sub12: TClientDataSet;
    T1_Sub21: TClientDataSet;
    T1_Sub22: TClientDataSet;
    T1_Sub31: TClientDataSet;
    T1_Sub32: TClientDataSet;
    T1_Sub41: TClientDataSet;
    T1_Sub42: TClientDataSet;
    T1_Sub51: TClientDataSet;
    T1_Sub52: TClientDataSet;
    T1_Sub61: TClientDataSet;
    T1_Sub62: TClientDataSet;
    T1_Sub71: TClientDataSet;
    T1_Sub72: TClientDataSet;
    T1_Sub81: TClientDataSet;
    T1_Sub82: TClientDataSet;
    T1_Sub91: TClientDataSet;
    T1_Sub92: TClientDataSet;
    T1_Sub01: TClientDataSet;
    T1_Sub02: TClientDataSet;
    T2_Sub11: TClientDataSet;
    T2_Sub12: TClientDataSet;
    T2_Sub21: TClientDataSet;
    T2_Sub22: TClientDataSet;
    T2_Sub31: TClientDataSet;
    T2_Sub32: TClientDataSet;
    T2_Sub41: TClientDataSet;
    T2_Sub42: TClientDataSet;
    T2_Sub51: TClientDataSet;
    T2_Sub52: TClientDataSet;
    T2_Sub61: TClientDataSet;
    T2_Sub62: TClientDataSet;
    T2_Sub71: TClientDataSet;
    T2_Sub72: TClientDataSet;
    T2_Sub81: TClientDataSet;
    T2_Sub82: TClientDataSet;
    T2_Sub91: TClientDataSet;
    T2_Sub92: TClientDataSet;
    T2_Sub01: TClientDataSet;
    T2_Sub02: TClientDataSet;
    T3_Sub11: TClientDataSet;
    T3_Sub12: TClientDataSet;
    T3_Sub21: TClientDataSet;
    T3_Sub22: TClientDataSet;
    T3_Sub31: TClientDataSet;
    T3_Sub32: TClientDataSet;
    T3_Sub41: TClientDataSet;
    T3_Sub42: TClientDataSet;
    T3_Sub51: TClientDataSet;
    T3_Sub52: TClientDataSet;
    T3_Sub61: TClientDataSet;
    T3_Sub62: TClientDataSet;
    T3_Sub71: TClientDataSet;
    T3_Sub72: TClientDataSet;
    T3_Sub81: TClientDataSet;
    T3_Sub82: TClientDataSet;
    T3_Sub91: TClientDataSet;
    T3_Sub92: TClientDataSet;
    T3_Sub01: TClientDataSet;
    T3_Sub02: TClientDataSet;
    T4_Sub11: TClientDataSet;
    T4_Sub12: TClientDataSet;
    T4_Sub21: TClientDataSet;
    T4_Sub22: TClientDataSet;
    T4_Sub31: TClientDataSet;
    T4_Sub32: TClientDataSet;
    T4_Sub41: TClientDataSet;
    T4_Sub42: TClientDataSet;
    T4_Sub51: TClientDataSet;
    T4_Sub52: TClientDataSet;
    T4_Sub61: TClientDataSet;
    T4_Sub62: TClientDataSet;
    T4_Sub71: TClientDataSet;
    T4_Sub72: TClientDataSet;
    T4_Sub81: TClientDataSet;
    T4_Sub82: TClientDataSet;
    T4_Sub91: TClientDataSet;
    T4_Sub92: TClientDataSet;
    T4_Sub01: TClientDataSet;
    T4_Sub02: TClientDataSet;
    T5_Sub11: TClientDataSet;
    T5_Sub12: TClientDataSet;
    T5_Sub21: TClientDataSet;
    T5_Sub22: TClientDataSet;
    T5_Sub31: TClientDataSet;
    T5_Sub32: TClientDataSet;
    T5_Sub41: TClientDataSet;
    T5_Sub42: TClientDataSet;
    T5_Sub51: TClientDataSet;
    T5_Sub52: TClientDataSet;
    T5_Sub61: TClientDataSet;
    T5_Sub62: TClientDataSet;
    T5_Sub71: TClientDataSet;
    T5_Sub72: TClientDataSet;
    T5_Sub81: TClientDataSet;
    T5_Sub82: TClientDataSet;
    T5_Sub91: TClientDataSet;
    T5_Sub92: TClientDataSet;
    T0_Sub01: TClientDataSet;
    T0_Sub02: TClientDataSet;
    T6_Sub11: TClientDataSet;
    T6_Sub12: TClientDataSet;
    T6_Sub21: TClientDataSet;
    T6_Sub22: TClientDataSet;
    T6_Sub31: TClientDataSet;
    T6_Sub32: TClientDataSet;
    T6_Sub41: TClientDataSet;
    T6_Sub42: TClientDataSet;
    T6_Sub51: TClientDataSet;
    T6_Sub52: TClientDataSet;
    T6_Sub61: TClientDataSet;
    T6_Sub62: TClientDataSet;
    T6_Sub71: TClientDataSet;
    T6_Sub72: TClientDataSet;
    T6_Sub81: TClientDataSet;
    T6_Sub82: TClientDataSet;
    T6_Sub91: TClientDataSet;
    T6_Sub92: TClientDataSet;
    T0_Sub11: TClientDataSet;
    T0_Sub12: TClientDataSet;
    T1_Sub11ID: TFloatField;
    T1_Sub11SNAME: TStringField;
    T1_Sub11GUBUN: TStringField;
    T1_Sub11JUBUN: TStringField;
    T1_Sub11PUBUN: TStringField;
    T1_Sub11SCODE: TStringField;
    T1_Sub11GCODE: TStringField;
    T1_Sub11GNAME: TStringField;
    T1_Sub11OCODE: TStringField;
    T1_Sub11GPOSA: TStringField;
    T1_Sub11GNUMB: TStringField;
    T1_Sub11GUPER: TStringField;
    T1_Sub11GJOMO: TStringField;
    T1_Sub11GPOST: TStringField;
    T1_Sub11GADD1: TStringField;
    T1_Sub11GADD2: TStringField;
    T1_Sub11GADDS: TStringField;
    T1_Sub11GTEL1: TStringField;
    T1_Sub11GTEL2: TStringField;
    T1_Sub11GFAX1: TStringField;
    T1_Sub11GFAX2: TStringField;
    T1_Sub11GTELS: TStringField;
    T1_Sub11GFAXS: TStringField;
    T1_Sub11GPPER: TStringField;
    T1_Sub11GBIGO: TStringField;
    T1_Sub11GRAT1: TSmallintField;
    T1_Sub11GRAT2: TSmallintField;
    T1_Sub11GRAT3: TSmallintField;
    T1_Sub11GRAT4: TSmallintField;
    T1_Sub11GRAT5: TSmallintField;
    T1_Sub11GRAT6: TSmallintField;
    T1_Sub11GRAT7: TSmallintField;
    T1_Sub11GRAT8: TSmallintField;
    T1_Sub11GRAT9: TSmallintField;
    T1_Sub11GQUT1: TFloatField;
    T1_Sub12ID: TFloatField;
    T1_Sub12GCODE: TStringField;
    T1_Sub12GNAME: TStringField;
    T1_Sub21ID: TFloatField;
    T1_Sub21SCODE: TStringField;
    T1_Sub21SNAME: TStringField;
    T1_Sub21GUBUN: TStringField;
    T1_Sub21JUBUN: TStringField;
    T1_Sub21PUBUN: TStringField;
    T1_Sub21GCODE: TStringField;
    T1_Sub21OCODE: TStringField;
    T1_Sub21GNAME: TStringField;
    T1_Sub21GPOSA: TStringField;
    T1_Sub21GNUMB: TStringField;
    T1_Sub21GUPER: TStringField;
    T1_Sub21GJOMO: TStringField;
    T1_Sub21GPPER: TStringField;
    T1_Sub21GTEL1: TStringField;
    T1_Sub21GTEL2: TStringField;
    T1_Sub21GTELS: TStringField;
    T1_Sub21GFAX1: TStringField;
    T1_Sub21GFAX2: TStringField;
    T1_Sub21GFAXS: TStringField;
    T1_Sub21GPOST: TStringField;
    T1_Sub21GADD1: TStringField;
    T1_Sub21GADD2: TStringField;
    T1_Sub21GADDS: TStringField;
    T1_Sub21GBIGO: TStringField;
    T1_Sub21GRAT1: TSmallintField;
    T1_Sub21GRAT2: TSmallintField;
    T1_Sub21GRAT3: TSmallintField;
    T1_Sub21GRAT4: TSmallintField;
    T1_Sub21GRAT5: TSmallintField;
    T1_Sub21GRAT6: TSmallintField;
    T1_Sub21GRAT7: TSmallintField;
    T1_Sub21GRAT8: TSmallintField;
    T1_Sub21GRAT9: TSmallintField;
    T1_Sub21GQUT1: TFloatField;
    T1_Sub22ID: TFloatField;
    T1_Sub22GCODE: TStringField;
    T1_Sub22GNAME: TStringField;
    T1_Sub31ID: TFloatField;
    T1_Sub31SNAME: TStringField;
    T1_Sub31GUBUN: TStringField;
    T1_Sub31SCODE: TStringField;
    T1_Sub31GCODE: TStringField;
    T1_Sub31GPOSA: TStringField;
    T1_Sub31GNAME: TStringField;
    T1_Sub31DATE1: TStringField;
    T1_Sub31DATE2: TStringField;
    T1_Sub31GJICE: TStringField;
    T1_Sub31GSCHO: TStringField;
    T1_Sub31GNUMB: TStringField;
    T1_Sub31GNUM1: TStringField;
    T1_Sub31GNUM2: TStringField;
    T1_Sub31GTEL1: TStringField;
    T1_Sub31GTEL2: TStringField;
    T1_Sub31GTELS: TStringField;
    T1_Sub31GFAX1: TStringField;
    T1_Sub31GFAX2: TStringField;
    T1_Sub31GFAXS: TStringField;
    T1_Sub31GPOST: TStringField;
    T1_Sub31GADD1: TStringField;
    T1_Sub31GADD2: TStringField;
    T1_Sub31GADDS: TStringField;
    T1_Sub31OPOST: TStringField;
    T1_Sub31OADD1: TStringField;
    T1_Sub31OADD2: TStringField;
    T1_Sub31OADDS: TStringField;
    T1_Sub31GBIGO: TStringField;
    T1_Sub32ID: TFloatField;
    T1_Sub32GCODE: TStringField;
    T1_Sub32GNAME: TStringField;
    T1_Sub41ID: TFloatField;
    T1_Sub41SNAME: TStringField;
    T1_Sub41GUBUN: TStringField;
    T1_Sub41JUBUN: TStringField;
    T1_Sub41SCODE: TStringField;
    T1_Sub41GCODE: TStringField;
    T1_Sub41OCODE: TStringField;
    T1_Sub41GNAME: TStringField;
    T1_Sub41GJEJA: TStringField;
    T1_Sub41GDABI: TStringField;
    T1_Sub41GDANG: TFloatField;
    T1_Sub41GISBN: TStringField;
    T1_Sub41GRAT1: TSmallintField;
    T1_Sub41GRAT2: TSmallintField;
    T1_Sub41GRAT3: TSmallintField;
    T1_Sub41GRAT4: TSmallintField;
    T1_Sub41GRAT5: TSmallintField;
    T1_Sub41GRAT6: TSmallintField;
    T1_Sub41GRAT7: TSmallintField;
    T1_Sub41GRAT9: TSmallintField;
    T1_Sub41GBJIL: TStringField;
    T1_Sub41GBIGO: TStringField;
    T1_Sub41GSQUT: TFloatField;
    T1_Sub41GSSUM: TFloatField;
    T1_Sub41GQUT1: TFloatField;
    T1_Sub41GQUT2: TFloatField;
    T1_Sub42ID: TFloatField;
    T1_Sub42GCODE: TStringField;
    T1_Sub42GNAME: TStringField;
    T1_Sub51ID: TFloatField;
    T1_Sub51SCODE: TStringField;
    T1_Sub51SNAME: TStringField;
    T1_Sub51GUBUN: TStringField;
    T1_Sub51JUBUN: TStringField;
    T1_Sub51PUBUN: TStringField;
    T1_Sub51GCODE: TStringField;
    T1_Sub51OCODE: TStringField;
    T1_Sub51GNAME: TStringField;
    T1_Sub51GPOSA: TStringField;
    T1_Sub51GNUMB: TStringField;
    T1_Sub51GUPER: TStringField;
    T1_Sub51GJOMO: TStringField;
    T1_Sub51GPPER: TStringField;
    T1_Sub51GTEL1: TStringField;
    T1_Sub51GTEL2: TStringField;
    T1_Sub51GTELS: TStringField;
    T1_Sub51GFAX1: TStringField;
    T1_Sub51GFAX2: TStringField;
    T1_Sub51GFAXS: TStringField;
    T1_Sub51GPOST: TStringField;
    T1_Sub51GADD1: TStringField;
    T1_Sub51GADD2: TStringField;
    T1_Sub51GADDS: TStringField;
    T1_Sub51GBIGO: TStringField;
    T1_Sub51GRAT1: TSmallintField;
    T1_Sub51GRAT2: TSmallintField;
    T1_Sub51GRAT3: TSmallintField;
    T1_Sub51GRAT4: TSmallintField;
    T1_Sub51GRAT5: TSmallintField;
    T1_Sub51GRAT6: TSmallintField;
    T1_Sub51GRAT7: TSmallintField;
    T1_Sub51GRAT8: TSmallintField;
    T1_Sub51GRAT9: TSmallintField;
    T1_Sub51GQUT1: TFloatField;
    T1_Sub52ID: TFloatField;
    T1_Sub52GCODE: TStringField;
    T1_Sub52GNAME: TStringField;
    T1_Sub61ID: TFloatField;
    T1_Sub61GCODE: TStringField;
    T1_Sub61GNAME: TStringField;
    T1_Sub61BCODE: TStringField;
    T1_Sub61BNAME: TStringField;
    T1_Sub61GRAT1: TSmallintField;
    T1_Sub61GRAT2: TSmallintField;
    T1_Sub61GRAT3: TSmallintField;
    T1_Sub61GRAT4: TSmallintField;
    T1_Sub61GRAT5: TSmallintField;
    T1_Sub61GRAT6: TSmallintField;
    T1_Sub61GRAT7: TSmallintField;
    T1_Sub61GRAT8: TSmallintField;
    T1_Sub61GRAT9: TSmallintField;
    T1_Sub61GSSUM: TFloatField;
    T1_Sub62ID: TFloatField;
    T1_Sub62GCODE: TStringField;
    T1_Sub62GNAME: TStringField;
    T1_Sub62BCODE: TStringField;
    T1_Sub62BNAME: TStringField;
    T1_Sub62GRAT1: TSmallintField;
    T1_Sub62GRAT2: TSmallintField;
    T1_Sub62GRAT3: TSmallintField;
    T1_Sub62GRAT4: TSmallintField;
    T1_Sub62GRAT5: TSmallintField;
    T1_Sub62GRAT6: TSmallintField;
    T1_Sub62GRAT7: TSmallintField;
    T1_Sub62GRAT8: TSmallintField;
    T1_Sub62GRAT9: TSmallintField;
    T1_Sub62GSSUM: TFloatField;
    T1_Sub71ID: TFloatField;
    T1_Sub71SCODE: TStringField;
    T1_Sub71SNAME: TStringField;
    T1_Sub71GUBUN: TStringField;
    T1_Sub71JUBUN: TStringField;
    T1_Sub71GCODE: TStringField;
    T1_Sub71GNAME: TStringField;
    T1_Sub71OCODE: TStringField;
    T1_Sub71ONAME: TStringField;
    T1_Sub71NAME1: TStringField;
    T1_Sub71NAME2: TStringField;
    T1_Sub71JUMIN: TStringField;
    T1_Sub71GPPER: TStringField;
    T1_Sub71GPOST: TStringField;
    T1_Sub71GADD1: TStringField;
    T1_Sub71GADD2: TStringField;
    T1_Sub71GADDS: TStringField;
    T1_Sub71GTEL1: TStringField;
    T1_Sub71GTEL2: TStringField;
    T1_Sub71GTELS: TStringField;
    T1_Sub71GFAX1: TStringField;
    T1_Sub71GFAX2: TStringField;
    T1_Sub71GFAXS: TStringField;
    T1_Sub71BIGO2: TStringField;
    T1_Sub71GBIGO: TStringField;
    T1_Sub72ID: TFloatField;
    T1_Sub72GCODE: TStringField;
    T1_Sub72GNAME: TStringField;
    T1_Sub81ID: TFloatField;
    T1_Sub81SCODE: TStringField;
    T1_Sub81SNAME: TStringField;
    T1_Sub81GUBUN: TStringField;
    T1_Sub81JUBUN: TStringField;
    T1_Sub81GCODE: TStringField;
    T1_Sub81OCODE: TStringField;
    T1_Sub81GNAME: TStringField;
    T1_Sub81GPOSA: TStringField;
    T1_Sub81GNUMB: TStringField;
    T1_Sub81GDATE: TStringField;
    T1_Sub81GUPER: TStringField;
    T1_Sub81GJOMO: TStringField;
    T1_Sub81GPOST: TStringField;
    T1_Sub81GADD1: TStringField;
    T1_Sub81GADD2: TStringField;
    T1_Sub81GADDS: TStringField;
    T1_Sub81GTEL1: TStringField;
    T1_Sub81GTEL2: TStringField;
    T1_Sub81GTELS: TStringField;
    T1_Sub81GFAX1: TStringField;
    T1_Sub81GFAX2: TStringField;
    T1_Sub81GFAXS: TStringField;
    T1_Sub81EMAIL: TStringField;
    T1_Sub81GBIGO: TStringField;
    T1_Sub82ID: TFloatField;
    T1_Sub82GCODE: TStringField;
    T1_Sub82GNAME: TStringField;
    T1_Sub91GUBUN: TStringField;
    T1_Sub91GNAME: TStringField;
    T1_Sub91GNUMB: TFloatField;
    T1_Sub91GFILD: TStringField;
    T1_Sub92GU: TStringField;
    T1_Sub92TOP: TSmallintField;
    T1_Sub92L11: TSmallintField;
    T1_Sub92L12: TSmallintField;
    T1_Sub92L13: TSmallintField;
    T1_Sub92L14: TSmallintField;
    T1_Sub92L15: TSmallintField;
    T1_Sub92L16: TSmallintField;
    T1_Sub92L17: TSmallintField;
    T1_Sub92L18: TSmallintField;
    T1_Sub92L19: TSmallintField;
    T1_Sub92L21: TSmallintField;
    T1_Sub92L22: TSmallintField;
    T1_Sub92L23: TSmallintField;
    T1_Sub92L24: TSmallintField;
    T1_Sub92L25: TSmallintField;
    T1_Sub92L26: TSmallintField;
    T1_Sub92L27: TSmallintField;
    T1_Sub92L28: TSmallintField;
    T1_Sub92L29: TSmallintField;
    T1_Sub92L31: TSmallintField;
    T1_Sub92L32: TSmallintField;
    T1_Sub92L33: TSmallintField;
    T1_Sub92L34: TSmallintField;
    T1_Sub92L35: TSmallintField;
    T1_Sub92L36: TSmallintField;
    T1_Sub92L37: TSmallintField;
    T1_Sub92L38: TSmallintField;
    T1_Sub92L39: TSmallintField;
    T1_Sub92L41: TSmallintField;
    T1_Sub92L42: TSmallintField;
    T1_Sub92L43: TSmallintField;
    T1_Sub92L44: TSmallintField;
    T1_Sub92L45: TSmallintField;
    T1_Sub92L46: TSmallintField;
    T1_Sub92L47: TSmallintField;
    T1_Sub92L48: TSmallintField;
    T1_Sub92L49: TSmallintField;
    T1_Sub92L51: TSmallintField;
    T1_Sub92L52: TSmallintField;
    T1_Sub92L53: TSmallintField;
    T1_Sub92L54: TSmallintField;
    T1_Sub92L55: TSmallintField;
    T1_Sub92L56: TSmallintField;
    T1_Sub92L57: TSmallintField;
    T1_Sub92L58: TSmallintField;
    T1_Sub92L59: TSmallintField;
    T1_Sub92L61: TSmallintField;
    T1_Sub92L62: TSmallintField;
    T1_Sub92L63: TSmallintField;
    T1_Sub92L64: TSmallintField;
    T1_Sub92L65: TSmallintField;
    T1_Sub92L66: TSmallintField;
    T1_Sub92L67: TSmallintField;
    T1_Sub92L68: TSmallintField;
    T1_Sub92L69: TSmallintField;
    T1_Sub92L71: TSmallintField;
    T1_Sub92L72: TSmallintField;
    T1_Sub92L73: TSmallintField;
    T1_Sub92L74: TSmallintField;
    T1_Sub92L75: TSmallintField;
    T1_Sub92L76: TSmallintField;
    T1_Sub92L77: TSmallintField;
    T1_Sub92L78: TSmallintField;
    T1_Sub92L79: TSmallintField;
    T1_Sub92L91: TSmallintField;
    T1_Sub92L92: TSmallintField;
    T1_Sub92L93: TSmallintField;
    T1_Sub92L94: TSmallintField;
    T1_Sub92L95: TSmallintField;
    T1_Sub92L96: TSmallintField;
    T1_Sub92L97: TSmallintField;
    T1_Sub92L98: TSmallintField;
    T1_Sub92L99: TSmallintField;
    T1_Sub92F11: TStringField;
    T1_Sub92F12: TStringField;
    T1_Sub92F21: TStringField;
    T1_Sub92F22: TStringField;
    T1_Sub92F31: TStringField;
    T1_Sub92F32: TStringField;
    T1_Sub92F41: TStringField;
    T1_Sub92F42: TStringField;
    T1_Sub92F51: TStringField;
    T1_Sub92F52: TStringField;
    T1_Sub92F61: TStringField;
    T1_Sub92F62: TStringField;
    T1_Sub92F71: TStringField;
    T1_Sub92F72: TStringField;
    T1_Sub92NAME: TStringField;
    T1_Sub92POSA: TStringField;
    T1_Sub01ID: TFloatField;
    T1_Sub01SUBUN: TStringField;
    T1_Sub01GUBUN: TStringField;
    T1_Sub01JUBUN: TStringField;
    T1_Sub01PUBUN: TStringField;
    T1_Sub01SCODE: TStringField;
    T1_Sub01GCODE: TStringField;
    T1_Sub01GNAME: TStringField;
    T1_Sub01OCODE: TStringField;
    T1_Sub01ONAME: TStringField;
    T1_Sub01NAME1: TStringField;
    T1_Sub01NAME2: TStringField;
    T1_Sub01GBANG: TStringField;
    T1_Sub01GPOSA: TStringField;
    T1_Sub01GNUMB: TStringField;
    T1_Sub01GNUM1: TStringField;
    T1_Sub01GNUM2: TStringField;
    T1_Sub01GUPER: TStringField;
    T1_Sub01GJOMO: TStringField;
    T1_Sub01GPOST: TStringField;
    T1_Sub01GADD1: TStringField;
    T1_Sub01GADD2: TStringField;
    T1_Sub01OPOST: TStringField;
    T1_Sub01OADD1: TStringField;
    T1_Sub01OADD2: TStringField;
    T1_Sub01GTEL1: TStringField;
    T1_Sub01GTEL2: TStringField;
    T1_Sub01GFAX1: TStringField;
    T1_Sub01GFAX2: TStringField;
    T1_Sub01DATE1: TStringField;
    T1_Sub01DATE2: TStringField;
    T1_Sub01DATE3: TStringField;
    T1_Sub01DATE4: TStringField;
    T1_Sub01GJEJA: TStringField;
    T1_Sub01GISBN: TStringField;
    T1_Sub01GDABI: TStringField;
    T1_Sub01GBJIL: TStringField;
    T1_Sub01GJICE: TStringField;
    T1_Sub01GSCHO: TStringField;
    T1_Sub01GPPER: TStringField;
    T1_Sub01GBIGO: TStringField;
    T1_Sub01GRAT1: TSmallintField;
    T1_Sub01GRAT2: TSmallintField;
    T1_Sub01GRAT3: TSmallintField;
    T1_Sub01GRAT4: TSmallintField;
    T1_Sub01GRAT5: TSmallintField;
    T1_Sub01GRAT6: TSmallintField;
    T1_Sub01GRAT7: TSmallintField;
    T1_Sub01GRAT8: TSmallintField;
    T1_Sub01GRAT9: TSmallintField;
    T1_Sub01GDANG: TFloatField;
    T1_Sub01GQUT1: TFloatField;
    T1_Sub01GOSUM: TFloatField;
    T1_Sub01GBSUM: TFloatField;
    T2_Sub11ID: TFloatField;
    T2_Sub11IDNUM: TFloatField;
    T2_Sub11GDATE: TStringField;
    T2_Sub11SCODE: TStringField;
    T2_Sub11GCODE: TStringField;
    T2_Sub11GNAME: TStringField;
    T2_Sub11HCODE: TStringField;
    T2_Sub11OCODE: TStringField;
    T2_Sub11BCODE: TStringField;
    T2_Sub11BNAME: TStringField;
    T2_Sub11GJEJA: TStringField;
    T2_Sub11GUBUN: TStringField;
    T2_Sub11JUBUN: TStringField;
    T2_Sub11PUBUN: TStringField;
    T2_Sub11GSQUT: TFloatField;
    T2_Sub11GDANG: TFloatField;
    T2_Sub11GRAT1: TSmallintField;
    T2_Sub11GSSUM: TFloatField;
    T2_Sub11GBIGO: TStringField;
    T2_Sub12ID: TFloatField;
    T2_Sub12IDNUM: TFloatField;
    T2_Sub12GDATE: TStringField;
    T2_Sub12SCODE: TStringField;
    T2_Sub12GCODE: TStringField;
    T2_Sub12GNAME: TStringField;
    T2_Sub12HCODE: TStringField;
    T2_Sub12OCODE: TStringField;
    T2_Sub12BCODE: TStringField;
    T2_Sub12BNAME: TStringField;
    T2_Sub12GJEJA: TStringField;
    T2_Sub12GUBUN: TStringField;
    T2_Sub12JUBUN: TStringField;
    T2_Sub12PUBUN: TStringField;
    T2_Sub12GSQUT: TFloatField;
    T2_Sub12GDANG: TFloatField;
    T2_Sub12GRAT1: TSmallintField;
    T2_Sub12GSSUM: TFloatField;
    T2_Sub12GBIGO: TStringField;
    T2_Sub21ID: TFloatField;
    T2_Sub21IDNUM: TFloatField;
    T2_Sub21GDATE: TStringField;
    T2_Sub21SCODE: TStringField;
    T2_Sub21GCODE: TStringField;
    T2_Sub21GNAME: TStringField;
    T2_Sub21HCODE: TStringField;
    T2_Sub21OCODE: TStringField;
    T2_Sub21BCODE: TStringField;
    T2_Sub21BNAME: TStringField;
    T2_Sub21GJEJA: TStringField;
    T2_Sub21GUBUN: TStringField;
    T2_Sub21JUBUN: TStringField;
    T2_Sub21PUBUN: TStringField;
    T2_Sub21GSQUT: TFloatField;
    T2_Sub21GDANG: TFloatField;
    T2_Sub21GRAT1: TSmallintField;
    T2_Sub21GSSUM: TFloatField;
    T2_Sub21GBIGO: TStringField;
    T2_Sub22ID: TFloatField;
    T2_Sub22IDNUM: TFloatField;
    T2_Sub22GDATE: TStringField;
    T2_Sub22SCODE: TStringField;
    T2_Sub22GCODE: TStringField;
    T2_Sub22GNAME: TStringField;
    T2_Sub22HCODE: TStringField;
    T2_Sub22OCODE: TStringField;
    T2_Sub22BCODE: TStringField;
    T2_Sub22BNAME: TStringField;
    T2_Sub22GJEJA: TStringField;
    T2_Sub22GUBUN: TStringField;
    T2_Sub22JUBUN: TStringField;
    T2_Sub22PUBUN: TStringField;
    T2_Sub22GSQUT: TFloatField;
    T2_Sub22GDANG: TFloatField;
    T2_Sub22GRAT1: TSmallintField;
    T2_Sub22GSSUM: TFloatField;
    T2_Sub22GBIGO: TStringField;
    T2_Sub31ID: TFloatField;
    T2_Sub31IDNUM: TFloatField;
    T2_Sub31GDATE: TStringField;
    T2_Sub31SCODE: TStringField;
    T2_Sub31GCODE: TStringField;
    T2_Sub31GNAME: TStringField;
    T2_Sub31HCODE: TStringField;
    T2_Sub31OCODE: TStringField;
    T2_Sub31BCODE: TStringField;
    T2_Sub31BNAME: TStringField;
    T2_Sub31GJEJA: TStringField;
    T2_Sub31GUBUN: TStringField;
    T2_Sub31JUBUN: TStringField;
    T2_Sub31PUBUN: TStringField;
    T2_Sub31GSQUT: TFloatField;
    T2_Sub31GDANG: TFloatField;
    T2_Sub31GRAT1: TSmallintField;
    T2_Sub31GSSUM: TFloatField;
    T2_Sub31GBIGO: TStringField;
    T2_Sub51ID: TFloatField;
    T2_Sub51IDNUM: TFloatField;
    T2_Sub51GDATE: TStringField;
    T2_Sub51SCODE: TStringField;
    T2_Sub51GCODE: TStringField;
    T2_Sub51GNAME: TStringField;
    T2_Sub51HCODE: TStringField;
    T2_Sub51OCODE: TStringField;
    T2_Sub51BCODE: TStringField;
    T2_Sub51BNAME: TStringField;
    T2_Sub51GJEJA: TStringField;
    T2_Sub51GUBUN: TStringField;
    T2_Sub51JUBUN: TStringField;
    T2_Sub51PUBUN: TStringField;
    T2_Sub51GSQUT: TFloatField;
    T2_Sub51GDANG: TFloatField;
    T2_Sub51GRAT1: TSmallintField;
    T2_Sub51GSSUM: TFloatField;
    T2_Sub51GBIGO: TStringField;
    T2_Sub52GUBUN: TStringField;
    T2_Sub52GCODE: TStringField;
    T2_Sub52GNAME: TStringField;
    T2_Sub52GIQUT: TFloatField;
    T2_Sub52GISUM: TFloatField;
    T2_Sub52GOQUT: TFloatField;
    T2_Sub52GOSUM: TFloatField;
    T2_Sub52GJQUT: TFloatField;
    T2_Sub52GJSUM: TFloatField;
    T2_Sub52GBQUT: TFloatField;
    T2_Sub52GBSUM: TFloatField;
    T2_Sub52GPQUT: TFloatField;
    T2_Sub52GPSUM: TFloatField;
    T2_Sub52GSUSU: TFloatField;
    T2_Sub52GSQUT: TFloatField;
    T2_Sub52GSSUM: TFloatField;
    T2_Sub52GSUMX: TFloatField;
    T2_Sub52GSUMY: TFloatField;
    T2_Sub91ID: TFloatField;
    T2_Sub91IDNUM: TFloatField;
    T2_Sub91GDATE: TStringField;
    T2_Sub91SCODE: TStringField;
    T2_Sub91GCODE: TStringField;
    T2_Sub91GNAME: TStringField;
    T2_Sub91HCODE: TStringField;
    T2_Sub91OCODE: TStringField;
    T2_Sub91BCODE: TStringField;
    T2_Sub91BNAME: TStringField;
    T2_Sub91GJEJA: TStringField;
    T2_Sub91GUBUN: TStringField;
    T2_Sub91JUBUN: TStringField;
    T2_Sub91PUBUN: TStringField;
    T2_Sub91GSQUT: TFloatField;
    T2_Sub91GDANG: TFloatField;
    T2_Sub91GRAT1: TSmallintField;
    T2_Sub91GSSUM: TFloatField;
    T2_Sub91GBIGO: TStringField;
    T2_Sub92ID: TFloatField;
    T2_Sub92SCODE: TStringField;
    T2_Sub92SNAME: TStringField;
    T2_Sub92GUBUN: TStringField;
    T2_Sub92JUBUN: TStringField;
    T2_Sub92PUBUN: TStringField;
    T2_Sub92GCODE: TStringField;
    T2_Sub92OCODE: TStringField;
    T2_Sub92GNAME: TStringField;
    T2_Sub92GPOSA: TStringField;
    T2_Sub92GNUMB: TStringField;
    T2_Sub92GUPER: TStringField;
    T2_Sub92GJOMO: TStringField;
    T2_Sub92GPPER: TStringField;
    T2_Sub92GTEL1: TStringField;
    T2_Sub92GTEL2: TStringField;
    T2_Sub92GTELS: TStringField;
    T2_Sub92GFAX1: TStringField;
    T2_Sub92GFAX2: TStringField;
    T2_Sub92GFAXS: TStringField;
    T2_Sub92GPOST: TStringField;
    T2_Sub92GADD1: TStringField;
    T2_Sub92GADD2: TStringField;
    T2_Sub92GADDS: TStringField;
    T2_Sub92GBIGO: TStringField;
    T2_Sub92GRAT1: TSmallintField;
    T2_Sub92GRAT2: TSmallintField;
    T2_Sub92GRAT3: TSmallintField;
    T2_Sub92GRAT4: TSmallintField;
    T2_Sub92GRAT5: TSmallintField;
    T2_Sub92GRAT6: TSmallintField;
    T2_Sub92GRAT7: TSmallintField;
    T2_Sub92GRAT8: TSmallintField;
    T2_Sub92GRAT9: TSmallintField;
    T2_Sub92GQUT1: TFloatField;
    T2_Sub01ID: TFloatField;
    T2_Sub01GCODE: TStringField;
    T2_Sub01GNAME: TStringField;
    T2_Sub01GDATE: TStringField;
    T2_Sub01BCODE: TStringField;
    T2_Sub01BNAME: TStringField;
    T2_Sub01GSSUM: TFloatField;
    T2_Sub01GRAT1: TFloatField;
    T2_Sub01GISUM: TFloatField;
    T2_Sub01GOSUM: TFloatField;
    T2_Sub01GBSUM: TFloatField;
    T2_Sub01GSUMX: TFloatField;
    T2_Sub01GSUMY: TFloatField;
    T3_Sub11GDATE: TStringField;
    T3_Sub11GCODE: TStringField;
    T3_Sub11GNAME: TStringField;
    T3_Sub11JUBUN: TStringField;
    T3_Sub11GIQUT: TFloatField;
    T3_Sub11GISUM: TFloatField;
    T3_Sub11GOQUT: TFloatField;
    T3_Sub11GOSUM: TFloatField;
    T3_Sub11GJQUT: TFloatField;
    T3_Sub11GJSUM: TFloatField;
    T3_Sub11GBQUT: TFloatField;
    T3_Sub11GBSUM: TFloatField;
    T3_Sub11GPQUT: TFloatField;
    T3_Sub11GPSUM: TFloatField;
    T3_Sub11GSUSU: TFloatField;
    T3_Sub11GSQUT: TFloatField;
    T3_Sub11GSSUM: TFloatField;
    T3_Sub11GSUMX: TFloatField;
    T3_Sub11GSUMY: TFloatField;
    T3_Sub12GDATE: TStringField;
    T3_Sub12GCODE: TStringField;
    T3_Sub12GNAME: TStringField;
    T3_Sub12JUBUN: TStringField;
    T3_Sub12GIQUT: TFloatField;
    T3_Sub12GISUM: TFloatField;
    T3_Sub12GOQUT: TFloatField;
    T3_Sub12GOSUM: TFloatField;
    T3_Sub12GJQUT: TFloatField;
    T3_Sub12GJSUM: TFloatField;
    T3_Sub12GBQUT: TFloatField;
    T3_Sub12GBSUM: TFloatField;
    T3_Sub12GPQUT: TFloatField;
    T3_Sub12GPSUM: TFloatField;
    T3_Sub12GSUSU: TFloatField;
    T3_Sub12GSQUT: TFloatField;
    T3_Sub12GSSUM: TFloatField;
    T3_Sub12GSUMX: TFloatField;
    T3_Sub12GSUMY: TFloatField;
    T3_Sub21GDATE: TStringField;
    T3_Sub21GCODE: TStringField;
    T3_Sub21GNAME: TStringField;
    T3_Sub21JUBUN: TStringField;
    T3_Sub21GIQUT: TFloatField;
    T3_Sub21GISUM: TFloatField;
    T3_Sub21GOQUT: TFloatField;
    T3_Sub21GOSUM: TFloatField;
    T3_Sub21GJQUT: TFloatField;
    T3_Sub21GJSUM: TFloatField;
    T3_Sub21GBQUT: TFloatField;
    T3_Sub21GBSUM: TFloatField;
    T3_Sub21GPQUT: TFloatField;
    T3_Sub21GPSUM: TFloatField;
    T3_Sub21GSUSU: TFloatField;
    T3_Sub21GSQUT: TFloatField;
    T3_Sub21GSSUM: TFloatField;
    T3_Sub21GSUMX: TFloatField;
    T3_Sub21GSUMY: TFloatField;
    T3_Sub22GDATE: TStringField;
    T3_Sub22GCODE: TStringField;
    T3_Sub22GNAME: TStringField;
    T3_Sub22JUBUN: TStringField;
    T3_Sub22GIQUT: TFloatField;
    T3_Sub22GISUM: TFloatField;
    T3_Sub22GOQUT: TFloatField;
    T3_Sub22GOSUM: TFloatField;
    T3_Sub22GJQUT: TFloatField;
    T3_Sub22GJSUM: TFloatField;
    T3_Sub22GBQUT: TFloatField;
    T3_Sub22GBSUM: TFloatField;
    T3_Sub22GPQUT: TFloatField;
    T3_Sub22GPSUM: TFloatField;
    T3_Sub22GSUSU: TFloatField;
    T3_Sub22GSQUT: TFloatField;
    T3_Sub22GSSUM: TFloatField;
    T3_Sub22GSUMX: TFloatField;
    T3_Sub22GSUMY: TFloatField;
    T3_Sub31GDATE: TStringField;
    T3_Sub31GUBUN: TStringField;
    T3_Sub31GCODE: TStringField;
    T3_Sub31GNAME: TStringField;
    T3_Sub31GDANG: TFloatField;
    T3_Sub31GIQUT: TFloatField;
    T3_Sub31GISUM: TFloatField;
    T3_Sub31GOQUT: TFloatField;
    T3_Sub31GOSUM: TFloatField;
    T3_Sub31GJQUT: TFloatField;
    T3_Sub31GJSUM: TFloatField;
    T3_Sub31GBQUT: TFloatField;
    T3_Sub31GBSUM: TFloatField;
    T3_Sub31GPQUT: TFloatField;
    T3_Sub31GPSUM: TFloatField;
    T3_Sub31GSUSU: TFloatField;
    T3_Sub31GSQUT: TFloatField;
    T3_Sub31GSSUM: TFloatField;
    T3_Sub31GSUMX: TFloatField;
    T3_Sub31GSUMY: TFloatField;
    T3_Sub32GDATE: TStringField;
    T3_Sub32GUBUN: TStringField;
    T3_Sub32GCODE: TStringField;
    T3_Sub32GNAME: TStringField;
    T3_Sub32GDANG: TFloatField;
    T3_Sub32GIQUT: TFloatField;
    T3_Sub32GISUM: TFloatField;
    T3_Sub32GOQUT: TFloatField;
    T3_Sub32GOSUM: TFloatField;
    T3_Sub32GJQUT: TFloatField;
    T3_Sub32GJSUM: TFloatField;
    T3_Sub32GBQUT: TFloatField;
    T3_Sub32GBSUM: TFloatField;
    T3_Sub32GPQUT: TFloatField;
    T3_Sub32GPSUM: TFloatField;
    T3_Sub32GSUSU: TFloatField;
    T3_Sub32GSQUT: TFloatField;
    T3_Sub32GSSUM: TFloatField;
    T3_Sub32GSUMX: TFloatField;
    T3_Sub32GSUMY: TFloatField;
    T3_Sub41GDATE: TStringField;
    T3_Sub41GUBUN: TStringField;
    T3_Sub41GCODE: TStringField;
    T3_Sub41GNAME: TStringField;
    T3_Sub41GIQUT: TFloatField;
    T3_Sub41GISUM: TFloatField;
    T3_Sub41GOQUT: TFloatField;
    T3_Sub41GOSUM: TFloatField;
    T3_Sub41GJQUT: TFloatField;
    T3_Sub41GJSUM: TFloatField;
    T3_Sub41GBQUT: TFloatField;
    T3_Sub41GBSUM: TFloatField;
    T3_Sub41GPQUT: TFloatField;
    T3_Sub41GPSUM: TFloatField;
    T3_Sub41GSUSU: TFloatField;
    T3_Sub41GSQUT: TFloatField;
    T3_Sub41GSSUM: TFloatField;
    T3_Sub41GSUMX: TFloatField;
    T3_Sub41GSUMY: TFloatField;
    T3_Sub42GDATE: TStringField;
    T3_Sub42GUBUN: TStringField;
    T3_Sub42GCODE: TStringField;
    T3_Sub42GNAME: TStringField;
    T3_Sub42GIQUT: TFloatField;
    T3_Sub42GISUM: TFloatField;
    T3_Sub42GOQUT: TFloatField;
    T3_Sub42GOSUM: TFloatField;
    T3_Sub42GJQUT: TFloatField;
    T3_Sub42GJSUM: TFloatField;
    T3_Sub42GBQUT: TFloatField;
    T3_Sub42GBSUM: TFloatField;
    T3_Sub42GPQUT: TFloatField;
    T3_Sub42GPSUM: TFloatField;
    T3_Sub42GSUSU: TFloatField;
    T3_Sub42GSQUT: TFloatField;
    T3_Sub42GSSUM: TFloatField;
    T3_Sub42GSUMX: TFloatField;
    T3_Sub42GSUMY: TFloatField;
    T3_Sub51GDATE: TStringField;
    T3_Sub51GUBUN: TStringField;
    T3_Sub51GCODE: TStringField;
    T3_Sub51GNAME: TStringField;
    T3_Sub51GIQUT: TFloatField;
    T3_Sub51GISUM: TFloatField;
    T3_Sub51GOQUT: TFloatField;
    T3_Sub51GOSUM: TFloatField;
    T3_Sub51GJQUT: TFloatField;
    T3_Sub51GJSUM: TFloatField;
    T3_Sub51GBQUT: TFloatField;
    T3_Sub51GBSUM: TFloatField;
    T3_Sub51GPQUT: TFloatField;
    T3_Sub51GPSUM: TFloatField;
    T3_Sub51GSUSU: TFloatField;
    T3_Sub51GSQUT: TFloatField;
    T3_Sub51GSSUM: TFloatField;
    T3_Sub51GSUMX: TFloatField;
    T3_Sub51GSUMY: TFloatField;
    T3_Sub52GDATE: TStringField;
    T3_Sub52GUBUN: TStringField;
    T3_Sub52GCODE: TStringField;
    T3_Sub52GNAME: TStringField;
    T3_Sub52GIQUT: TFloatField;
    T3_Sub52GISUM: TFloatField;
    T3_Sub52GOQUT: TFloatField;
    T3_Sub52GOSUM: TFloatField;
    T3_Sub52GJQUT: TFloatField;
    T3_Sub52GJSUM: TFloatField;
    T3_Sub52GBQUT: TFloatField;
    T3_Sub52GBSUM: TFloatField;
    T3_Sub52GPQUT: TFloatField;
    T3_Sub52GPSUM: TFloatField;
    T3_Sub52GSUSU: TFloatField;
    T3_Sub52GSQUT: TFloatField;
    T3_Sub52GSSUM: TFloatField;
    T3_Sub52GSUMX: TFloatField;
    T3_Sub52GSUMY: TFloatField;
    T3_Sub61GDATE: TStringField;
    T3_Sub61GUBUN: TStringField;
    T3_Sub61GCODE: TStringField;
    T3_Sub61GNAME: TStringField;
    T3_Sub61GIQUT: TFloatField;
    T3_Sub61GISUM: TFloatField;
    T3_Sub61GOQUT: TFloatField;
    T3_Sub61GOSUM: TFloatField;
    T3_Sub61GJQUT: TFloatField;
    T3_Sub61GJSUM: TFloatField;
    T3_Sub61GBQUT: TFloatField;
    T3_Sub61GBSUM: TFloatField;
    T3_Sub61GPQUT: TFloatField;
    T3_Sub61GPSUM: TFloatField;
    T3_Sub61GSUSU: TFloatField;
    T3_Sub61GSQUT: TFloatField;
    T3_Sub61GSSUM: TFloatField;
    T3_Sub61GSUMX: TFloatField;
    T3_Sub61GSUMY: TFloatField;
    T3_Sub62GDATE: TStringField;
    T3_Sub62GUBUN: TStringField;
    T3_Sub62GCODE: TStringField;
    T3_Sub62GNAME: TStringField;
    T3_Sub62GIQUT: TFloatField;
    T3_Sub62GISUM: TFloatField;
    T3_Sub62GOQUT: TFloatField;
    T3_Sub62GOSUM: TFloatField;
    T3_Sub62GJQUT: TFloatField;
    T3_Sub62GJSUM: TFloatField;
    T3_Sub62GBQUT: TFloatField;
    T3_Sub62GBSUM: TFloatField;
    T3_Sub62GPQUT: TFloatField;
    T3_Sub62GPSUM: TFloatField;
    T3_Sub62GSUSU: TFloatField;
    T3_Sub62GSQUT: TFloatField;
    T3_Sub62GSSUM: TFloatField;
    T3_Sub62GSUMX: TFloatField;
    T3_Sub62GSUMY: TFloatField;
    T3_Sub71GDATE: TStringField;
    T3_Sub71GUBUN: TStringField;
    T3_Sub71GCODE: TStringField;
    T3_Sub71GNAME: TStringField;
    T3_Sub71GIQUT: TFloatField;
    T3_Sub71GISUM: TFloatField;
    T3_Sub71GOQUT: TFloatField;
    T3_Sub71GOSUM: TFloatField;
    T3_Sub71GJQUT: TFloatField;
    T3_Sub71GJSUM: TFloatField;
    T3_Sub71GBQUT: TFloatField;
    T3_Sub71GBSUM: TFloatField;
    T3_Sub71GPQUT: TFloatField;
    T3_Sub71GPSUM: TFloatField;
    T3_Sub71GSUSU: TFloatField;
    T3_Sub71GSQUT: TFloatField;
    T3_Sub71GSSUM: TFloatField;
    T3_Sub71GSUMX: TFloatField;
    T3_Sub71GSUMY: TFloatField;
    T3_Sub72GDATE: TStringField;
    T3_Sub72GUBUN: TStringField;
    T3_Sub72GCODE: TStringField;
    T3_Sub72GNAME: TStringField;
    T3_Sub72GIQUT: TFloatField;
    T3_Sub72GISUM: TFloatField;
    T3_Sub72GOQUT: TFloatField;
    T3_Sub72GOSUM: TFloatField;
    T3_Sub72GJQUT: TFloatField;
    T3_Sub72GJSUM: TFloatField;
    T3_Sub72GBQUT: TFloatField;
    T3_Sub72GBSUM: TFloatField;
    T3_Sub72GPQUT: TFloatField;
    T3_Sub72GPSUM: TFloatField;
    T3_Sub72GSUSU: TFloatField;
    T3_Sub72GSQUT: TFloatField;
    T3_Sub72GSSUM: TFloatField;
    T3_Sub72GSUMX: TFloatField;
    T3_Sub72GSUMY: TFloatField;
    T3_Sub91GDATE: TStringField;
    T3_Sub91GCODE: TStringField;
    T3_Sub91GNAME: TStringField;
    T3_Sub91JUBUN: TStringField;
    T3_Sub91GIQUT: TFloatField;
    T3_Sub91GISUM: TFloatField;
    T3_Sub91GOQUT: TFloatField;
    T3_Sub91GOSUM: TFloatField;
    T3_Sub91GJQUT: TFloatField;
    T3_Sub91GJSUM: TFloatField;
    T3_Sub91GBQUT: TFloatField;
    T3_Sub91GBSUM: TFloatField;
    T3_Sub91GPQUT: TFloatField;
    T3_Sub91GPSUM: TFloatField;
    T3_Sub91GSUSU: TFloatField;
    T3_Sub91GSQUT: TFloatField;
    T3_Sub91GSSUM: TFloatField;
    T3_Sub91GSUMX: TFloatField;
    T3_Sub91GSUMY: TFloatField;
    T3_Sub92GDATE: TStringField;
    T3_Sub92GCODE: TStringField;
    T3_Sub92GNAME: TStringField;
    T3_Sub92JUBUN: TStringField;
    T3_Sub92GIQUT: TFloatField;
    T3_Sub92GISUM: TFloatField;
    T3_Sub92GOQUT: TFloatField;
    T3_Sub92GOSUM: TFloatField;
    T3_Sub92GJQUT: TFloatField;
    T3_Sub92GJSUM: TFloatField;
    T3_Sub92GBQUT: TFloatField;
    T3_Sub92GBSUM: TFloatField;
    T3_Sub92GPQUT: TFloatField;
    T3_Sub92GPSUM: TFloatField;
    T3_Sub92GSUSU: TFloatField;
    T3_Sub92GSQUT: TFloatField;
    T3_Sub92GSSUM: TFloatField;
    T3_Sub92GSUMX: TFloatField;
    T3_Sub92GSUMY: TFloatField;
    T4_Sub11ID: TFloatField;
    T4_Sub11IDNUM: TFloatField;
    T4_Sub11GDATE: TStringField;
    T4_Sub11SDATE: TStringField;
    T4_Sub11HCODE: TStringField;
    T4_Sub11SCODE: TStringField;
    T4_Sub11GCODE: TStringField;
    T4_Sub11GNAME: TStringField;
    T4_Sub11TCODE: TStringField;
    T4_Sub11OCODE: TStringField;
    T4_Sub11ONAME: TStringField;
    T4_Sub11GSSUM: TFloatField;
    T4_Sub11PUBUN: TStringField;
    T4_Sub11GBIGO: TStringField;
    T4_Sub11SNAME: TStringField;
    T4_Sub12ID: TFloatField;
    T4_Sub12IDNUM: TFloatField;
    T4_Sub12GDATE: TStringField;
    T4_Sub12GUBUN: TStringField;
    T4_Sub12HCODE: TStringField;
    T4_Sub12SCODE: TStringField;
    T4_Sub12GCODE: TStringField;
    T4_Sub12GNAME: TStringField;
    T4_Sub12TCODE: TStringField;
    T4_Sub12OCODE: TStringField;
    T4_Sub12ONAME: TStringField;
    T4_Sub12GSSUM: TFloatField;
    T4_Sub12PUBUN: TStringField;
    T4_Sub12GBIGO: TStringField;
    T4_Sub12SNAME: TStringField;
    T4_Sub21ID: TFloatField;
    T4_Sub21GDATE: TStringField;
    T4_Sub21GUBUN: TStringField;
    T4_Sub21HCODE: TStringField;
    T4_Sub22ID: TFloatField;
    T4_Sub22IDNUM: TFloatField;
    T4_Sub22GDATE: TStringField;
    T4_Sub22GUBUN: TStringField;
    T4_Sub22HCODE: TStringField;
    T4_Sub22SCODE: TStringField;
    T4_Sub22GCODE: TStringField;
    T4_Sub22GNAME: TStringField;
    T4_Sub22TCODE: TStringField;
    T4_Sub22OCODE: TStringField;
    T4_Sub22ONAME: TStringField;
    T4_Sub22GSSUM: TFloatField;
    T4_Sub22PUBUN: TStringField;
    T4_Sub22GBIGO: TStringField;
    T4_Sub22SNAME: TStringField;
    T4_Sub61ID: TFloatField;
    T4_Sub61GNUMB: TStringField;
    T4_Sub61GNAME: TStringField;
    T4_Sub61GPOSA: TStringField;
    T4_Sub61DATE1: TStringField;
    T4_Sub61DATE2: TStringField;
    T4_Sub61DATE3: TStringField;
    T4_Sub61DATE4: TStringField;
    T4_Sub61GBANG: TStringField;
    T4_Sub61NAME1: TStringField;
    T4_Sub61NAME2: TStringField;
    T4_Sub61SCODE: TStringField;
    T4_Sub61GRAT1: TSmallintField;
    T4_Sub61GOSUM: TFloatField;
    T4_Sub61GSSUM: TFloatField;
    T4_Sub61GBIGO: TStringField;
    T4_Sub62ID: TFloatField;
    T4_Sub62GCODE: TStringField;
    T4_Sub62GNAME: TStringField;
    T4_Sub62GPOSA: TStringField;
    T4_Sub62GNUMB: TStringField;
    T4_Sub62GUBUN: TStringField;
    T4_Sub62GTELS: TStringField;
    T4_Sub62NAME1: TStringField;
    T4_Sub62NAME2: TStringField;
    T4_Sub62GDATE: TStringField;
    T4_Sub62CLASS: TFloatField;
    T4_Sub62GSUSU: TFloatField;
    T4_Sub62GSSUM: TFloatField;
    T4_Sub72GDATE: TStringField;
    T4_Sub72GCODE: TStringField;
    T4_Sub72GNAME: TStringField;
    T4_Sub72OCODE: TStringField;
    T4_Sub72ONAME: TStringField;
    T4_Sub72GISUM: TFloatField;
    T4_Sub72GOSUM: TFloatField;
    T4_Sub72GJSUM: TFloatField;
    T4_Sub72GBSUM: TFloatField;
    T4_Sub72GSSUM: TFloatField;
    T4_Sub72GSUMX: TFloatField;
    T4_Sub72GSUMY: TFloatField;
    T4_Sub82GDATE: TStringField;
    T4_Sub82GCODE: TStringField;
    T4_Sub82GNAME: TStringField;
    T4_Sub82OCODE: TStringField;
    T4_Sub82ONAME: TStringField;
    T4_Sub82GISUM: TFloatField;
    T4_Sub82GOSUM: TFloatField;
    T4_Sub82GJSUM: TFloatField;
    T4_Sub82GBSUM: TFloatField;
    T4_Sub82GSSUM: TFloatField;
    T4_Sub82GSUMX: TFloatField;
    T4_Sub82GSUMY: TFloatField;
    T4_Sub91SCODE: TStringField;
    T4_Sub91GDATE: TStringField;
    T4_Sub91GUBUN: TStringField;
    T4_Sub91GCODE: TStringField;
    T4_Sub91GNAME: TStringField;
    T4_Sub91GIQUT: TFloatField;
    T4_Sub91GISUM: TFloatField;
    T4_Sub91GOQUT: TFloatField;
    T4_Sub91GOSUM: TFloatField;
    T4_Sub91GJQUT: TFloatField;
    T4_Sub91GJSUM: TFloatField;
    T4_Sub91GBQUT: TFloatField;
    T4_Sub91GBSUM: TFloatField;
    T4_Sub91GPQUT: TFloatField;
    T4_Sub91GPSUM: TFloatField;
    T4_Sub91GSUSU: TFloatField;
    T4_Sub91GSQUT: TFloatField;
    T4_Sub91GSSUM: TFloatField;
    T4_Sub91GSUMX: TFloatField;
    T4_Sub91GSUMY: TFloatField;
    T4_Sub92SCODE: TStringField;
    T4_Sub92GDATE: TStringField;
    T4_Sub92GUBUN: TStringField;
    T4_Sub92GCODE: TStringField;
    T4_Sub92GNAME: TStringField;
    T4_Sub92GIQUT: TFloatField;
    T4_Sub92GISUM: TFloatField;
    T4_Sub92GOQUT: TFloatField;
    T4_Sub92GOSUM: TFloatField;
    T4_Sub92GJQUT: TFloatField;
    T4_Sub92GJSUM: TFloatField;
    T4_Sub92GBQUT: TFloatField;
    T4_Sub92GBSUM: TFloatField;
    T4_Sub92GPQUT: TFloatField;
    T4_Sub92GPSUM: TFloatField;
    T4_Sub92GSUSU: TFloatField;
    T4_Sub92GSQUT: TFloatField;
    T4_Sub92GSSUM: TFloatField;
    T4_Sub92GSUMX: TFloatField;
    T4_Sub92GSUMY: TFloatField;
    T5_Sub11ID: TFloatField;
    T5_Sub11GDATE: TStringField;
    T5_Sub11SCODE: TStringField;
    T5_Sub11GCODE: TStringField;
    T5_Sub11HCODE: TStringField;
    T5_Sub11GNAME: TStringField;
    T5_Sub11GSSUM: TFloatField;
    T5_Sub11GOSUM: TFloatField;
    T5_Sub11GBSUM: TFloatField;
    T5_Sub11GBIGO: TStringField;
    T5_Sub12ID: TFloatField;
    T5_Sub12GDATE: TStringField;
    T5_Sub12SCODE: TStringField;
    T5_Sub12GCODE: TStringField;
    T5_Sub12HCODE: TStringField;
    T5_Sub12GNAME: TStringField;
    T5_Sub12GSSUM: TFloatField;
    T5_Sub12GOSUM: TFloatField;
    T5_Sub12GBSUM: TFloatField;
    T5_Sub12GBIGO: TStringField;
    T5_Sub21ID: TFloatField;
    T5_Sub21GDATE: TStringField;
    T5_Sub21SCODE: TStringField;
    T5_Sub21GCODE: TStringField;
    T5_Sub21HCODE: TStringField;
    T5_Sub21GNAME: TStringField;
    T5_Sub21GSSUM: TFloatField;
    T5_Sub21GOSUM: TFloatField;
    T5_Sub21GBSUM: TFloatField;
    T5_Sub21GBIGO: TStringField;
    T5_Sub22ID: TFloatField;
    T5_Sub22GDATE: TStringField;
    T5_Sub22SCODE: TStringField;
    T5_Sub22GCODE: TStringField;
    T5_Sub22HCODE: TStringField;
    T5_Sub22GNAME: TStringField;
    T5_Sub22GSSUM: TFloatField;
    T5_Sub22GOSUM: TFloatField;
    T5_Sub22GBSUM: TFloatField;
    T5_Sub22GBIGO: TStringField;
    T6_Sub11GCODE: TStringField;
    T6_Sub11GNAME: TStringField;
    T6_Sub11GIQUT: TFloatField;
    T6_Sub11GISUM: TFloatField;
    T6_Sub11GOQUT: TFloatField;
    T6_Sub11GOSUM: TFloatField;
    T6_Sub11GJQUT: TFloatField;
    T6_Sub11GJSUM: TFloatField;
    T6_Sub11GBQUT: TFloatField;
    T6_Sub11GBSUM: TFloatField;
    T6_Sub11GPQUT: TFloatField;
    T6_Sub11GPSUM: TFloatField;
    T6_Sub11GSUSU: TFloatField;
    T6_Sub11GSQUT: TFloatField;
    T6_Sub11GSSUM: TFloatField;
    T6_Sub11GSUMX: TFloatField;
    T6_Sub11GSUMY: TFloatField;
    T6_Sub12GCODE: TStringField;
    T6_Sub12GNAME: TStringField;
    T6_Sub12GIQUT: TFloatField;
    T6_Sub12GISUM: TFloatField;
    T6_Sub12GOQUT: TFloatField;
    T6_Sub12GOSUM: TFloatField;
    T6_Sub12GJQUT: TFloatField;
    T6_Sub12GJSUM: TFloatField;
    T6_Sub12GBQUT: TFloatField;
    T6_Sub12GBSUM: TFloatField;
    T6_Sub12GPQUT: TFloatField;
    T6_Sub12GPSUM: TFloatField;
    T6_Sub12GSUSU: TFloatField;
    T6_Sub12GSQUT: TFloatField;
    T6_Sub12GSSUM: TFloatField;
    T6_Sub12GSUMX: TFloatField;
    T6_Sub12GSUMY: TFloatField;
    T6_Sub21GCODE: TStringField;
    T6_Sub21GNAME: TStringField;
    T6_Sub21GIQUT: TFloatField;
    T6_Sub21GISUM: TFloatField;
    T6_Sub21GOQUT: TFloatField;
    T6_Sub21GOSUM: TFloatField;
    T6_Sub21GJQUT: TFloatField;
    T6_Sub21GJSUM: TFloatField;
    T6_Sub21GBQUT: TFloatField;
    T6_Sub21GBSUM: TFloatField;
    T6_Sub21GPQUT: TFloatField;
    T6_Sub21GPSUM: TFloatField;
    T6_Sub21GSUSU: TFloatField;
    T6_Sub21GSQUT: TFloatField;
    T6_Sub21GSSUM: TFloatField;
    T6_Sub21GSUMX: TFloatField;
    T6_Sub21GSUMY: TFloatField;
    T6_Sub22GCODE: TStringField;
    T6_Sub22GNAME: TStringField;
    T6_Sub22GIQUT: TFloatField;
    T6_Sub22GISUM: TFloatField;
    T6_Sub22GOQUT: TFloatField;
    T6_Sub22GOSUM: TFloatField;
    T6_Sub22GJQUT: TFloatField;
    T6_Sub22GJSUM: TFloatField;
    T6_Sub22GBQUT: TFloatField;
    T6_Sub22GBSUM: TFloatField;
    T6_Sub22GPQUT: TFloatField;
    T6_Sub22GPSUM: TFloatField;
    T6_Sub22GSUSU: TFloatField;
    T6_Sub22GSQUT: TFloatField;
    T6_Sub22GSSUM: TFloatField;
    T6_Sub22GSUMX: TFloatField;
    T6_Sub22GSUMY: TFloatField;
    T6_Sub31GCODE: TStringField;
    T6_Sub31GNAME: TStringField;
    T6_Sub31GIQUT: TFloatField;
    T6_Sub31GISUM: TFloatField;
    T6_Sub31GOQUT: TFloatField;
    T6_Sub31GOSUM: TFloatField;
    T6_Sub31GJQUT: TFloatField;
    T6_Sub31GJSUM: TFloatField;
    T6_Sub31GBQUT: TFloatField;
    T6_Sub31GBSUM: TFloatField;
    T6_Sub31GPQUT: TFloatField;
    T6_Sub31GPSUM: TFloatField;
    T6_Sub31GSUSU: TFloatField;
    T6_Sub31GSQUT: TFloatField;
    T6_Sub31GSSUM: TFloatField;
    T6_Sub31GSUMX: TFloatField;
    T6_Sub31GSUMY: TFloatField;
    T6_Sub32GCODE: TStringField;
    T6_Sub32GNAME: TStringField;
    T6_Sub32GIQUT: TFloatField;
    T6_Sub32GISUM: TFloatField;
    T6_Sub32GOQUT: TFloatField;
    T6_Sub32GOSUM: TFloatField;
    T6_Sub32GJQUT: TFloatField;
    T6_Sub32GJSUM: TFloatField;
    T6_Sub32GBQUT: TFloatField;
    T6_Sub32GBSUM: TFloatField;
    T6_Sub32GPQUT: TFloatField;
    T6_Sub32GPSUM: TFloatField;
    T6_Sub32GSUSU: TFloatField;
    T6_Sub32GSQUT: TFloatField;
    T6_Sub32GSSUM: TFloatField;
    T6_Sub32GSUMX: TFloatField;
    T6_Sub32GSUMY: TFloatField;
    T6_Sub41GCODE: TStringField;
    T6_Sub41GNAME: TStringField;
    T6_Sub41GIQUT: TFloatField;
    T6_Sub41GISUM: TFloatField;
    T6_Sub41GOQUT: TFloatField;
    T6_Sub41GOSUM: TFloatField;
    T6_Sub41GJQUT: TFloatField;
    T6_Sub41GJSUM: TFloatField;
    T6_Sub41GBQUT: TFloatField;
    T6_Sub41GBSUM: TFloatField;
    T6_Sub41GPQUT: TFloatField;
    T6_Sub41GPSUM: TFloatField;
    T6_Sub41GSUSU: TFloatField;
    T6_Sub41GSQUT: TFloatField;
    T6_Sub41GSSUM: TFloatField;
    T6_Sub41GSUMX: TFloatField;
    T6_Sub41GSUMY: TFloatField;
    T6_Sub42GCODE: TStringField;
    T6_Sub42GNAME: TStringField;
    T6_Sub42GIQUT: TFloatField;
    T6_Sub42GISUM: TFloatField;
    T6_Sub42GOQUT: TFloatField;
    T6_Sub42GOSUM: TFloatField;
    T6_Sub42GJQUT: TFloatField;
    T6_Sub42GJSUM: TFloatField;
    T6_Sub42GBQUT: TFloatField;
    T6_Sub42GBSUM: TFloatField;
    T6_Sub42GPQUT: TFloatField;
    T6_Sub42GPSUM: TFloatField;
    T6_Sub42GSUSU: TFloatField;
    T6_Sub42GSQUT: TFloatField;
    T6_Sub42GSSUM: TFloatField;
    T6_Sub42GSUMX: TFloatField;
    T6_Sub42GSUMY: TFloatField;
    T6_Sub51GUBUN: TStringField;
    T6_Sub51GCODE: TStringField;
    T6_Sub51GNAME: TStringField;
    T6_Sub51GIQUT: TFloatField;
    T6_Sub51GISUM: TFloatField;
    T6_Sub51GOQUT: TFloatField;
    T6_Sub51GOSUM: TFloatField;
    T6_Sub51GJQUT: TFloatField;
    T6_Sub51GJSUM: TFloatField;
    T6_Sub51GBQUT: TFloatField;
    T6_Sub51GBSUM: TFloatField;
    T6_Sub51GPQUT: TFloatField;
    T6_Sub51GPSUM: TFloatField;
    T6_Sub51GSUSU: TFloatField;
    T6_Sub51GSQUT: TFloatField;
    T6_Sub51GSSUM: TFloatField;
    T6_Sub51GSUMX: TFloatField;
    T6_Sub51GSUMY: TFloatField;
    T6_Sub52GUBUN: TStringField;
    T6_Sub52GCODE: TStringField;
    T6_Sub52GNAME: TStringField;
    T6_Sub52GIQUT: TFloatField;
    T6_Sub52GISUM: TFloatField;
    T6_Sub52GOQUT: TFloatField;
    T6_Sub52GOSUM: TFloatField;
    T6_Sub52GJQUT: TFloatField;
    T6_Sub52GJSUM: TFloatField;
    T6_Sub52GBQUT: TFloatField;
    T6_Sub52GBSUM: TFloatField;
    T6_Sub52GPQUT: TFloatField;
    T6_Sub52GPSUM: TFloatField;
    T6_Sub52GSUSU: TFloatField;
    T6_Sub52GSQUT: TFloatField;
    T6_Sub52GSSUM: TFloatField;
    T6_Sub52GSUMX: TFloatField;
    T6_Sub52GSUMY: TFloatField;
    T6_Sub61GUBUN: TStringField;
    T6_Sub61GCODE: TStringField;
    T6_Sub61GNAME: TStringField;
    T6_Sub61GIQUT: TFloatField;
    T6_Sub61GISUM: TFloatField;
    T6_Sub61GOQUT: TFloatField;
    T6_Sub61GOSUM: TFloatField;
    T6_Sub61GJQUT: TFloatField;
    T6_Sub61GJSUM: TFloatField;
    T6_Sub61GBQUT: TFloatField;
    T6_Sub61GBSUM: TFloatField;
    T6_Sub61GPQUT: TFloatField;
    T6_Sub61GPSUM: TFloatField;
    T6_Sub61GSUSU: TFloatField;
    T6_Sub61GSQUT: TFloatField;
    T6_Sub61GSSUM: TFloatField;
    T6_Sub61GSUMX: TFloatField;
    T6_Sub61GSUMY: TFloatField;
    T6_Sub62GUBUN: TStringField;
    T6_Sub62GCODE: TStringField;
    T6_Sub62GNAME: TStringField;
    T6_Sub62GIQUT: TFloatField;
    T6_Sub62GISUM: TFloatField;
    T6_Sub62GOQUT: TFloatField;
    T6_Sub62GOSUM: TFloatField;
    T6_Sub62GJQUT: TFloatField;
    T6_Sub62GJSUM: TFloatField;
    T6_Sub62GBQUT: TFloatField;
    T6_Sub62GBSUM: TFloatField;
    T6_Sub62GPQUT: TFloatField;
    T6_Sub62GPSUM: TFloatField;
    T6_Sub62GSUSU: TFloatField;
    T6_Sub62GSQUT: TFloatField;
    T6_Sub62GSSUM: TFloatField;
    T6_Sub62GSUMX: TFloatField;
    T6_Sub62GSUMY: TFloatField;
    T6_Sub71GDATE: TStringField;
    T6_Sub71GCODE: TStringField;
    T6_Sub71GNAME: TStringField;
    T6_Sub71GIQUT: TFloatField;
    T6_Sub71GISUM: TFloatField;
    T6_Sub71GOQUT: TFloatField;
    T6_Sub71GOSUM: TFloatField;
    T6_Sub71GJQUT: TFloatField;
    T6_Sub71GJSUM: TFloatField;
    T6_Sub71GBQUT: TFloatField;
    T6_Sub71GBSUM: TFloatField;
    T6_Sub71GPQUT: TFloatField;
    T6_Sub71GPSUM: TFloatField;
    T6_Sub71GSUSU: TFloatField;
    T6_Sub71GSQUT: TFloatField;
    T6_Sub71GSSUM: TFloatField;
    T6_Sub71GSUMX: TFloatField;
    T6_Sub71GSUMY: TFloatField;
    T6_Sub72GDATE: TStringField;
    T6_Sub72GCODE: TStringField;
    T6_Sub72GNAME: TStringField;
    T6_Sub72GIQUT: TFloatField;
    T6_Sub72GISUM: TFloatField;
    T6_Sub72GOQUT: TFloatField;
    T6_Sub72GOSUM: TFloatField;
    T6_Sub72GJQUT: TFloatField;
    T6_Sub72GJSUM: TFloatField;
    T6_Sub72GBQUT: TFloatField;
    T6_Sub72GBSUM: TFloatField;
    T6_Sub72GPQUT: TFloatField;
    T6_Sub72GPSUM: TFloatField;
    T6_Sub72GSUSU: TFloatField;
    T6_Sub72GSQUT: TFloatField;
    T6_Sub72GSSUM: TFloatField;
    T6_Sub72GSUMX: TFloatField;
    T6_Sub72GSUMY: TFloatField;
    T6_Sub81GDATE: TStringField;
    T6_Sub81GCODE: TStringField;
    T6_Sub81GNAME: TStringField;
    T6_Sub81GIQUT: TFloatField;
    T6_Sub81GISUM: TFloatField;
    T6_Sub81GOQUT: TFloatField;
    T6_Sub81GOSUM: TFloatField;
    T6_Sub81GJQUT: TFloatField;
    T6_Sub81GJSUM: TFloatField;
    T6_Sub81GBQUT: TFloatField;
    T6_Sub81GBSUM: TFloatField;
    T6_Sub81GPQUT: TFloatField;
    T6_Sub81GPSUM: TFloatField;
    T6_Sub81GSUSU: TFloatField;
    T6_Sub81GSQUT: TFloatField;
    T6_Sub81GSSUM: TFloatField;
    T6_Sub81GSUMX: TFloatField;
    T6_Sub81GSUMY: TFloatField;
    T6_Sub82GDATE: TStringField;
    T6_Sub82GCODE: TStringField;
    T6_Sub82GNAME: TStringField;
    T6_Sub82GIQUT: TFloatField;
    T6_Sub82GISUM: TFloatField;
    T6_Sub82GOQUT: TFloatField;
    T6_Sub82GOSUM: TFloatField;
    T6_Sub82GJQUT: TFloatField;
    T6_Sub82GJSUM: TFloatField;
    T6_Sub82GBQUT: TFloatField;
    T6_Sub82GBSUM: TFloatField;
    T6_Sub82GPQUT: TFloatField;
    T6_Sub82GPSUM: TFloatField;
    T6_Sub82GSUSU: TFloatField;
    T6_Sub82GSQUT: TFloatField;
    T6_Sub82GSSUM: TFloatField;
    T6_Sub82GSUMX: TFloatField;
    T6_Sub82GSUMY: TFloatField;
    T3_Sub81ID: TFloatField;
    T3_Sub81SCODE: TStringField;
    T3_Sub81GCODE: TStringField;
    T3_Sub81OCODE: TStringField;
    T3_Sub81GNAME: TStringField;
    T3_Sub82ID: TFloatField;
    T3_Sub82SCODE: TStringField;
    T3_Sub82GCODE: TStringField;
    T3_Sub82OCODE: TStringField;
    T3_Sub82GNAME: TStringField;
    T2_Sub32ID: TFloatField;
    T2_Sub32GDATE: TStringField;
    T2_Sub32SCODE: TStringField;
    T2_Sub32BCODE: TStringField;
    T2_Sub32BNAME: TStringField;
    T2_Sub32JUBUN: TStringField;
    T1_Sub71GPOSA: TStringField;
    T1_Sub71GNUMB: TStringField;
    T1_Sub71GUPER: TStringField;
    T1_Sub71GJOMO: TStringField;
    T1_Sub11HCODE: TStringField;
    T1_Sub12HCODE: TStringField;
    T1_Sub21HCODE: TStringField;
    T1_Sub22HCODE: TStringField;
    T1_Sub31HCODE: TStringField;
    T1_Sub32HCODE: TStringField;
    T1_Sub41HCODE: TStringField;
    T1_Sub42HCODE: TStringField;
    T1_Sub51HCODE: TStringField;
    T1_Sub52HCODE: TStringField;
    T1_Sub61HCODE: TStringField;
    T1_Sub62HCODE: TStringField;
    T1_Sub71HCODE: TStringField;
    T1_Sub72HCODE: TStringField;
    T1_Sub81HCODE: TStringField;
    T1_Sub82HCODE: TStringField;
    T4_Sub61HCODE: TStringField;
    T4_Sub62HCODE: TStringField;
    T1_Sub91HCODE: TStringField;
    Database: TZMySqlDatabase;
    Transact: TZMySqlTransact;
    Socket: TMySqlClientTable;
    T2_Sub92HCODE: TStringField;
    T1_Sub11YESNO: TStringField;
    T1_Sub11NAME1: TStringField;
    T1_Sub11NAME2: TStringField;
    T1_Sub21YESNO: TStringField;
    T1_Sub21NAME1: TStringField;
    T1_Sub21NAME2: TStringField;
    T1_Sub41YESNO: TStringField;
    T1_Sub41GNUMB: TStringField;
    T1_Sub41DATE1: TStringField;
    T1_Sub41DATE2: TStringField;
    T1_Sub41NAME1: TStringField;
    T1_Sub41NAME2: TStringField;
    T1_Sub41GPAGE: TFloatField;
    T1_Sub41GPAN1: TFloatField;
    T1_Sub41GPAN2: TFloatField;
    T1_Sub51YESNO: TStringField;
    T1_Sub51NAME1: TStringField;
    T1_Sub51NAME2: TStringField;
    T2_Sub61ID: TFloatField;
    T2_Sub61IDNUM: TFloatField;
    T2_Sub61GDATE: TStringField;
    T2_Sub61SCODE: TStringField;
    T2_Sub61GCODE: TStringField;
    T2_Sub61GNAME: TStringField;
    T2_Sub61HCODE: TStringField;
    T2_Sub61OCODE: TStringField;
    T2_Sub61BCODE: TStringField;
    T2_Sub61BNAME: TStringField;
    T2_Sub61GJEJA: TStringField;
    T2_Sub61GUBUN: TStringField;
    T2_Sub61JUBUN: TStringField;
    T2_Sub61PUBUN: TStringField;
    T2_Sub61GSQUT: TFloatField;
    T2_Sub61GDANG: TFloatField;
    T2_Sub61GRAT1: TSmallintField;
    T2_Sub61GSSUM: TFloatField;
    T2_Sub61GBIGO: TStringField;
    T2_Sub62ID: TFloatField;
    T2_Sub62IDNUM: TFloatField;
    T2_Sub62GDATE: TStringField;
    T2_Sub62SCODE: TStringField;
    T2_Sub62GCODE: TStringField;
    T2_Sub62GNAME: TStringField;
    T2_Sub62HCODE: TStringField;
    T2_Sub62OCODE: TStringField;
    T2_Sub62BCODE: TStringField;
    T2_Sub62BNAME: TStringField;
    T2_Sub62GJEJA: TStringField;
    T2_Sub62GUBUN: TStringField;
    T2_Sub62JUBUN: TStringField;
    T2_Sub62PUBUN: TStringField;
    T2_Sub62GSQUT: TFloatField;
    T2_Sub62GDANG: TFloatField;
    T2_Sub62GRAT1: TSmallintField;
    T2_Sub62GSSUM: TFloatField;
    T2_Sub62GBIGO: TStringField;
    T2_Sub61HNAME: TStringField;
    T2_Sub62HNAME: TStringField;
    T2_Sub11QSQUT: TFloatField;
    T2_Sub11JEAGO: TFloatField;
    T2_Sub12QSQUT: TFloatField;
    T2_Sub12JEAGO: TFloatField;
    T2_Sub21QSQUT: TFloatField;
    T2_Sub21JEAGO: TFloatField;
    T2_Sub22QSQUT: TFloatField;
    T2_Sub22JEAGO: TFloatField;
    T2_Sub31QSQUT: TFloatField;
    T2_Sub31JEAGO: TFloatField;
    T2_Sub51QSQUT: TFloatField;
    T2_Sub51JEAGO: TFloatField;
    T2_Sub91QSQUT: TFloatField;
    T2_Sub91JEAGO: TFloatField;
    T2_Sub61QSQUT: TFloatField;
    T2_Sub61JEAGO: TFloatField;
    T2_Sub62QSQUT: TFloatField;
    T2_Sub62JEAGO: TFloatField;
    T2_Sub41ID: TFloatField;
    T2_Sub41IDNUM: TFloatField;
    T2_Sub41GDATE: TStringField;
    T2_Sub41SCODE: TStringField;
    T2_Sub41GCODE: TStringField;
    T2_Sub41GNAME: TStringField;
    T2_Sub41HCODE: TStringField;
    T2_Sub41HNAME: TStringField;
    T2_Sub41OCODE: TStringField;
    T2_Sub41BCODE: TStringField;
    T2_Sub41BNAME: TStringField;
    T2_Sub41GJEJA: TStringField;
    T2_Sub41GUBUN: TStringField;
    T2_Sub41JUBUN: TStringField;
    T2_Sub41PUBUN: TStringField;
    T2_Sub41GSQUT: TFloatField;
    T2_Sub41QSQUT: TFloatField;
    T2_Sub41GDANG: TFloatField;
    T2_Sub41GRAT1: TSmallintField;
    T2_Sub41GSSUM: TFloatField;
    T2_Sub41JEAGO: TFloatField;
    T2_Sub41GBIGO: TStringField;
    T2_Sub42ID: TFloatField;
    T2_Sub42IDNUM: TFloatField;
    T2_Sub42GDATE: TStringField;
    T2_Sub42SCODE: TStringField;
    T2_Sub42GCODE: TStringField;
    T2_Sub42GNAME: TStringField;
    T2_Sub42HCODE: TStringField;
    T2_Sub42HNAME: TStringField;
    T2_Sub42OCODE: TStringField;
    T2_Sub42BCODE: TStringField;
    T2_Sub42BNAME: TStringField;
    T2_Sub42GJEJA: TStringField;
    T2_Sub42GUBUN: TStringField;
    T2_Sub42JUBUN: TStringField;
    T2_Sub42PUBUN: TStringField;
    T2_Sub42GSQUT: TFloatField;
    T2_Sub42QSQUT: TFloatField;
    T2_Sub42GDANG: TFloatField;
    T2_Sub42GRAT1: TSmallintField;
    T2_Sub42GSSUM: TFloatField;
    T2_Sub42JEAGO: TFloatField;
    T2_Sub42GBIGO: TStringField;
    T4_Sub31ID: TFloatField;
    T4_Sub31GDATE: TStringField;
    T4_Sub31SCODE: TStringField;
    T4_Sub31GCODE: TStringField;
    T4_Sub31GNAME: TStringField;
    T4_Sub31HCODE: TStringField;
    T4_Sub31HNAME: TStringField;
    T4_Sub31NAME1: TStringField;
    T4_Sub31NAME2: TStringField;
    T4_Sub31GSSUM: TFloatField;
    T4_Sub32ID: TFloatField;
    T4_Sub32GDATE: TStringField;
    T4_Sub32SCODE: TStringField;
    T4_Sub32GCODE: TStringField;
    T4_Sub32GNAME: TStringField;
    T4_Sub32HCODE: TStringField;
    T4_Sub32HNAME: TStringField;
    T4_Sub32NAME1: TStringField;
    T4_Sub32NAME2: TStringField;
    T4_Sub32GSSUM: TFloatField;
    T4_Sub41ID: TFloatField;
    T4_Sub41GDATE: TStringField;
    T4_Sub41SCODE: TStringField;
    T4_Sub41GCODE: TStringField;
    T4_Sub41GNAME: TStringField;
    T4_Sub41HCODE: TStringField;
    T4_Sub41HNAME: TStringField;
    T4_Sub41NAME1: TStringField;
    T4_Sub41NAME2: TStringField;
    T4_Sub41GSSUM: TFloatField;
    T4_Sub42ID: TFloatField;
    T4_Sub42GDATE: TStringField;
    T4_Sub42SCODE: TStringField;
    T4_Sub42GCODE: TStringField;
    T4_Sub42GNAME: TStringField;
    T4_Sub42HCODE: TStringField;
    T4_Sub42HNAME: TStringField;
    T4_Sub42NAME1: TStringField;
    T4_Sub42NAME2: TStringField;
    T4_Sub42GSSUM: TFloatField;
    T2_Sub11YESNO: TStringField;
    T2_Sub12YESNO: TStringField;
    T2_Sub21YESNO: TStringField;
    T2_Sub22YESNO: TStringField;
    T2_Sub31YESNO: TStringField;
    T2_Sub41YESNO: TStringField;
    T2_Sub42YESNO: TStringField;
    T2_Sub51YESNO: TStringField;
    T2_Sub61YESNO: TStringField;
    T2_Sub62YESNO: TStringField;
    T2_Sub91YESNO: TStringField;
    T5_Sub31ID: TFloatField;
    T5_Sub31IDNUM: TFloatField;
    T5_Sub31GDATE: TStringField;
    T5_Sub31SCODE: TStringField;
    T5_Sub31GCODE: TStringField;
    T5_Sub31GNAME: TStringField;
    T5_Sub31HCODE: TStringField;
    T5_Sub31HNAME: TStringField;
    T5_Sub31OCODE: TStringField;
    T5_Sub31BCODE: TStringField;
    T5_Sub31BNAME: TStringField;
    T5_Sub31GJEJA: TStringField;
    T5_Sub31GUBUN: TStringField;
    T5_Sub31JUBUN: TStringField;
    T5_Sub31PUBUN: TStringField;
    T5_Sub31TCODE: TStringField;
    T5_Sub31GSQUT: TFloatField;
    T5_Sub31QSQUT: TFloatField;
    T5_Sub31GDANG: TFloatField;
    T5_Sub31GRAT1: TSmallintField;
    T5_Sub31GSSUM: TFloatField;
    T5_Sub31JEAGO: TFloatField;
    T5_Sub31GBIGO: TStringField;
    T5_Sub31YESNO: TStringField;
    T5_Sub32ID: TFloatField;
    T5_Sub32IDNUM: TFloatField;
    T5_Sub32GDATE: TStringField;
    T5_Sub32SCODE: TStringField;
    T5_Sub32GCODE: TStringField;
    T5_Sub32GNAME: TStringField;
    T5_Sub32HCODE: TStringField;
    T5_Sub32HNAME: TStringField;
    T5_Sub32OCODE: TStringField;
    T5_Sub32BCODE: TStringField;
    T5_Sub32BNAME: TStringField;
    T5_Sub32GJEJA: TStringField;
    T5_Sub32GUBUN: TStringField;
    T5_Sub32JUBUN: TStringField;
    T5_Sub32PUBUN: TStringField;
    T5_Sub32TCODE: TStringField;
    T5_Sub32GSQUT: TFloatField;
    T5_Sub32QSQUT: TFloatField;
    T5_Sub32GDANG: TFloatField;
    T5_Sub32GRAT1: TSmallintField;
    T5_Sub32GSSUM: TFloatField;
    T5_Sub32JEAGO: TFloatField;
    T5_Sub32GBIGO: TStringField;
    T5_Sub32YESNO: TStringField;
    T5_Sub61ID: TFloatField;
    T5_Sub61IDNUM: TFloatField;
    T5_Sub61GDATE: TStringField;
    T5_Sub61SCODE: TStringField;
    T5_Sub61GCODE: TStringField;
    T5_Sub61GNAME: TStringField;
    T5_Sub61HCODE: TStringField;
    T5_Sub61HNAME: TStringField;
    T5_Sub61OCODE: TStringField;
    T5_Sub61BCODE: TStringField;
    T5_Sub61BNAME: TStringField;
    T5_Sub61GJEJA: TStringField;
    T5_Sub61GUBUN: TStringField;
    T5_Sub61JUBUN: TStringField;
    T5_Sub61PUBUN: TStringField;
    T5_Sub61TCODE: TStringField;
    T5_Sub61GSQUT: TFloatField;
    T5_Sub61QSQUT: TFloatField;
    T5_Sub61GDANG: TFloatField;
    T5_Sub61GRAT1: TSmallintField;
    T5_Sub61GSSUM: TFloatField;
    T5_Sub61JEAGO: TFloatField;
    T5_Sub61GBIGO: TStringField;
    T5_Sub61YESNO: TStringField;
    T5_Sub62ID: TFloatField;
    T5_Sub62IDNUM: TFloatField;
    T5_Sub62GDATE: TStringField;
    T5_Sub62SCODE: TStringField;
    T5_Sub62GCODE: TStringField;
    T5_Sub62GNAME: TStringField;
    T5_Sub62HCODE: TStringField;
    T5_Sub62HNAME: TStringField;
    T5_Sub62OCODE: TStringField;
    T5_Sub62BCODE: TStringField;
    T5_Sub62BNAME: TStringField;
    T5_Sub62GJEJA: TStringField;
    T5_Sub62GUBUN: TStringField;
    T5_Sub62JUBUN: TStringField;
    T5_Sub62PUBUN: TStringField;
    T5_Sub62TCODE: TStringField;
    T5_Sub62GSQUT: TFloatField;
    T5_Sub62QSQUT: TFloatField;
    T5_Sub62GDANG: TFloatField;
    T5_Sub62GRAT1: TSmallintField;
    T5_Sub62GSSUM: TFloatField;
    T5_Sub62JEAGO: TFloatField;
    T5_Sub62GBIGO: TStringField;
    T5_Sub62YESNO: TStringField;
    T5_Sub41ID: TFloatField;
    T5_Sub41IDNUM: TFloatField;
    T5_Sub41GDATE: TStringField;
    T5_Sub41SCODE: TStringField;
    T5_Sub41GCODE: TStringField;
    T5_Sub41GNAME: TStringField;
    T5_Sub41HCODE: TStringField;
    T5_Sub41HNAME: TStringField;
    T5_Sub41OCODE: TStringField;
    T5_Sub41BCODE: TStringField;
    T5_Sub41BNAME: TStringField;
    T5_Sub41GJEJA: TStringField;
    T5_Sub41GUBUN: TStringField;
    T5_Sub41JUBUN: TStringField;
    T5_Sub41PUBUN: TStringField;
    T5_Sub41TCODE: TStringField;
    T5_Sub41GSQUT: TFloatField;
    T5_Sub41QSQUT: TFloatField;
    T5_Sub41GDANG: TFloatField;
    T5_Sub41GRAT1: TSmallintField;
    T5_Sub41GSSUM: TFloatField;
    T5_Sub41JEAGO: TFloatField;
    T5_Sub41GBIGO: TStringField;
    T5_Sub41YESNO: TStringField;
    T5_Sub42ID: TFloatField;
    T5_Sub42IDNUM: TFloatField;
    T5_Sub42GDATE: TStringField;
    T5_Sub42SCODE: TStringField;
    T5_Sub42GCODE: TStringField;
    T5_Sub42GNAME: TStringField;
    T5_Sub42HCODE: TStringField;
    T5_Sub42HNAME: TStringField;
    T5_Sub42OCODE: TStringField;
    T5_Sub42BCODE: TStringField;
    T5_Sub42BNAME: TStringField;
    T5_Sub42GJEJA: TStringField;
    T5_Sub42GUBUN: TStringField;
    T5_Sub42JUBUN: TStringField;
    T5_Sub42PUBUN: TStringField;
    T5_Sub42TCODE: TStringField;
    T5_Sub42GSQUT: TFloatField;
    T5_Sub42QSQUT: TFloatField;
    T5_Sub42GDANG: TFloatField;
    T5_Sub42GRAT1: TSmallintField;
    T5_Sub42GSSUM: TFloatField;
    T5_Sub42JEAGO: TFloatField;
    T5_Sub42GBIGO: TStringField;
    T5_Sub42YESNO: TStringField;
    T5_Sub51ID: TFloatField;
    T5_Sub51IDNUM: TFloatField;
    T5_Sub51GDATE: TStringField;
    T5_Sub51SCODE: TStringField;
    T5_Sub51GCODE: TStringField;
    T5_Sub51GNAME: TStringField;
    T5_Sub51HCODE: TStringField;
    T5_Sub51HNAME: TStringField;
    T5_Sub51OCODE: TStringField;
    T5_Sub51BCODE: TStringField;
    T5_Sub51BNAME: TStringField;
    T5_Sub51GJEJA: TStringField;
    T5_Sub51GUBUN: TStringField;
    T5_Sub51JUBUN: TStringField;
    T5_Sub51PUBUN: TStringField;
    T5_Sub51TCODE: TStringField;
    T5_Sub51GSQUT: TFloatField;
    T5_Sub51QSQUT: TFloatField;
    T5_Sub51GDANG: TFloatField;
    T5_Sub51GRAT1: TSmallintField;
    T5_Sub51GSSUM: TFloatField;
    T5_Sub51JEAGO: TFloatField;
    T5_Sub51GBIGO: TStringField;
    T5_Sub51YESNO: TStringField;
    T5_Sub52ID: TFloatField;
    T5_Sub52IDNUM: TFloatField;
    T5_Sub52GDATE: TStringField;
    T5_Sub52SCODE: TStringField;
    T5_Sub52GCODE: TStringField;
    T5_Sub52GNAME: TStringField;
    T5_Sub52HCODE: TStringField;
    T5_Sub52HNAME: TStringField;
    T5_Sub52OCODE: TStringField;
    T5_Sub52BCODE: TStringField;
    T5_Sub52BNAME: TStringField;
    T5_Sub52GJEJA: TStringField;
    T5_Sub52GUBUN: TStringField;
    T5_Sub52JUBUN: TStringField;
    T5_Sub52PUBUN: TStringField;
    T5_Sub52TCODE: TStringField;
    T5_Sub52GSQUT: TFloatField;
    T5_Sub52QSQUT: TFloatField;
    T5_Sub52GDANG: TFloatField;
    T5_Sub52GRAT1: TSmallintField;
    T5_Sub52GSSUM: TFloatField;
    T5_Sub52JEAGO: TFloatField;
    T5_Sub52GBIGO: TStringField;
    T5_Sub52YESNO: TStringField;
    T5_Sub71ID: TFloatField;
    T5_Sub71IDNUM: TFloatField;
    T5_Sub71GDATE: TStringField;
    T5_Sub71SCODE: TStringField;
    T5_Sub71GCODE: TStringField;
    T5_Sub71GNAME: TStringField;
    T5_Sub71HCODE: TStringField;
    T5_Sub71HNAME: TStringField;
    T5_Sub71OCODE: TStringField;
    T5_Sub71BCODE: TStringField;
    T5_Sub71BNAME: TStringField;
    T5_Sub71GJEJA: TStringField;
    T5_Sub71GUBUN: TStringField;
    T5_Sub71JUBUN: TStringField;
    T5_Sub71PUBUN: TStringField;
    T5_Sub71TCODE: TStringField;
    T5_Sub71GSQUT: TFloatField;
    T5_Sub71QSQUT: TFloatField;
    T5_Sub71GDANG: TFloatField;
    T5_Sub71GRAT1: TSmallintField;
    T5_Sub71GSSUM: TFloatField;
    T5_Sub71JEAGO: TFloatField;
    T5_Sub71GBIGO: TStringField;
    T5_Sub71YESNO: TStringField;
    T5_Sub72ID: TFloatField;
    T5_Sub72IDNUM: TFloatField;
    T5_Sub72GDATE: TStringField;
    T5_Sub72SCODE: TStringField;
    T5_Sub72GCODE: TStringField;
    T5_Sub72GNAME: TStringField;
    T5_Sub72HCODE: TStringField;
    T5_Sub72HNAME: TStringField;
    T5_Sub72OCODE: TStringField;
    T5_Sub72BCODE: TStringField;
    T5_Sub72BNAME: TStringField;
    T5_Sub72GJEJA: TStringField;
    T5_Sub72GUBUN: TStringField;
    T5_Sub72JUBUN: TStringField;
    T5_Sub72PUBUN: TStringField;
    T5_Sub72TCODE: TStringField;
    T5_Sub72GSQUT: TFloatField;
    T5_Sub72QSQUT: TFloatField;
    T5_Sub72GDANG: TFloatField;
    T5_Sub72GRAT1: TSmallintField;
    T5_Sub72GSSUM: TFloatField;
    T5_Sub72JEAGO: TFloatField;
    T5_Sub72GBIGO: TStringField;
    T5_Sub72YESNO: TStringField;
    T5_Sub81ID: TFloatField;
    T5_Sub81IDNUM: TFloatField;
    T5_Sub81GDATE: TStringField;
    T5_Sub81SCODE: TStringField;
    T5_Sub81GCODE: TStringField;
    T5_Sub81GNAME: TStringField;
    T5_Sub81HCODE: TStringField;
    T5_Sub81HNAME: TStringField;
    T5_Sub81OCODE: TStringField;
    T5_Sub81BCODE: TStringField;
    T5_Sub81BNAME: TStringField;
    T5_Sub81GJEJA: TStringField;
    T5_Sub81GUBUN: TStringField;
    T5_Sub81JUBUN: TStringField;
    T5_Sub81PUBUN: TStringField;
    T5_Sub81TCODE: TStringField;
    T5_Sub81GSQUT: TFloatField;
    T5_Sub81QSQUT: TFloatField;
    T5_Sub81GDANG: TFloatField;
    T5_Sub81GRAT1: TSmallintField;
    T5_Sub81GSSUM: TFloatField;
    T5_Sub81JEAGO: TFloatField;
    T5_Sub81GBIGO: TStringField;
    T5_Sub81YESNO: TStringField;
    T5_Sub82ID: TFloatField;
    T5_Sub82IDNUM: TFloatField;
    T5_Sub82GDATE: TStringField;
    T5_Sub82SCODE: TStringField;
    T5_Sub82GCODE: TStringField;
    T5_Sub82GNAME: TStringField;
    T5_Sub82HCODE: TStringField;
    T5_Sub82HNAME: TStringField;
    T5_Sub82OCODE: TStringField;
    T5_Sub82BCODE: TStringField;
    T5_Sub82BNAME: TStringField;
    T5_Sub82GJEJA: TStringField;
    T5_Sub82GUBUN: TStringField;
    T5_Sub82JUBUN: TStringField;
    T5_Sub82PUBUN: TStringField;
    T5_Sub82TCODE: TStringField;
    T5_Sub82GSQUT: TFloatField;
    T5_Sub82QSQUT: TFloatField;
    T5_Sub82GDANG: TFloatField;
    T5_Sub82GRAT1: TSmallintField;
    T5_Sub82GSSUM: TFloatField;
    T5_Sub82JEAGO: TFloatField;
    T5_Sub82GBIGO: TStringField;
    T5_Sub82YESNO: TStringField;
    T4_Sub11HNAME: TStringField;
    T4_Sub12HNAME: TStringField;
    T4_Sub21HNAME: TStringField;
    T4_Sub22HNAME: TStringField;
    T2_Sub61GMEMO: TDateTimeField;
    T2_Sub62GMEMO: TDateTimeField;
    T4_Sub51ID: TFloatField;
    T4_Sub51IDNUM: TFloatField;
    T4_Sub51GDATE: TStringField;
    T4_Sub51GCODE: TStringField;
    T4_Sub51GNAME: TStringField;
    T4_Sub51HCODE: TStringField;
    T4_Sub51HNAME: TStringField;
    T4_Sub51NAME1: TStringField;
    T4_Sub51NAME2: TStringField;
    T4_Sub51GQUT1: TFloatField;
    T4_Sub51GQUT2: TFloatField;
    T4_Sub51GQUT3: TFloatField;
    T4_Sub51GSSUM: TFloatField;
    T4_Sub51GQUT4: TFloatField;
    T4_Sub52ID: TFloatField;
    T4_Sub52IDNUM: TFloatField;
    T4_Sub52GDATE: TStringField;
    T4_Sub52SCODE: TStringField;
    T4_Sub52GCODE: TStringField;
    T4_Sub52GNAME: TStringField;
    T4_Sub52HCODE: TStringField;
    T4_Sub52HNAME: TStringField;
    T4_Sub52OCODE: TStringField;
    T4_Sub52BCODE: TStringField;
    T4_Sub52BNAME: TStringField;
    T4_Sub52GJEJA: TStringField;
    T4_Sub52GUBUN: TStringField;
    T4_Sub52JUBUN: TStringField;
    T4_Sub52PUBUN: TStringField;
    T4_Sub52TCODE: TStringField;
    T4_Sub52GSQUT: TFloatField;
    T4_Sub52QSQUT: TFloatField;
    T4_Sub52GDANG: TFloatField;
    T4_Sub52GRAT1: TSmallintField;
    T4_Sub52GSSUM: TFloatField;
    T4_Sub52JEAGO: TFloatField;
    T4_Sub52GBIGO: TStringField;
    T4_Sub52YESNO: TStringField;
    T4_Sub52GMEMO: TDateTimeField;
    T4_Sub71ID: TFloatField;
    T4_Sub71GDATE: TStringField;
    T4_Sub71SCODE: TStringField;
    T4_Sub71GCODE: TStringField;
    T4_Sub71GNAME: TStringField;
    T4_Sub71HCODE: TStringField;
    T4_Sub71HNAME: TStringField;
    T4_Sub71NAME1: TStringField;
    T4_Sub71NAME2: TStringField;
    T4_Sub71GSSUM: TFloatField;
    T1_Sub71GIQUT: TFloatField;
    T1_Sub71GISUM: TFloatField;
    T1_Sub71GOSUM: TFloatField;
    T1_Sub71GSSUM: TFloatField;
    T1_Sub71GDATE: TStringField;
    T2_Sub81ID: TFloatField;
    T2_Sub81HCODE: TStringField;
    T2_Sub81GCODE: TStringField;
    T2_Sub81GNAME: TStringField;
    T2_Sub81ONAME: TStringField;
    T2_Sub82ID: TFloatField;
    T2_Sub82GDATE: TStringField;
    T2_Sub82GCODE: TStringField;
    T2_Sub82GNAME: TStringField;
    T2_Sub82GTELS: TStringField;
    T2_Sub82OCODE: TStringField;
    T2_Sub82ONAME: TStringField;
    T2_Sub82CODE1: TStringField;
    T2_Sub82CODE2: TStringField;
    T2_Sub82CODE3: TStringField;
    T2_Sub82GOQUT: TFloatField;
    T2_Sub82GSQUT: TFloatField;
    T2_Sub82GSSUM: TFloatField;
    T2_Sub71ID: TFloatField;
    T2_Sub71IDNUM: TFloatField;
    T2_Sub71GDATE: TStringField;
    T2_Sub71SCODE: TStringField;
    T2_Sub71GCODE: TStringField;
    T2_Sub71GNAME: TStringField;
    T2_Sub71HCODE: TStringField;
    T2_Sub71HNAME: TStringField;
    T2_Sub71OCODE: TStringField;
    T2_Sub71BCODE: TStringField;
    T2_Sub71BNAME: TStringField;
    T2_Sub71GJEJA: TStringField;
    T2_Sub71GUBUN: TStringField;
    T2_Sub71JUBUN: TStringField;
    T2_Sub71PUBUN: TStringField;
    T2_Sub71GSQUT: TFloatField;
    T2_Sub71QSQUT: TFloatField;
    T2_Sub71GDANG: TFloatField;
    T2_Sub71GRAT1: TSmallintField;
    T2_Sub71GSSUM: TFloatField;
    T2_Sub71JEAGO: TFloatField;
    T2_Sub71GBIGO: TStringField;
    T2_Sub71YESNO: TStringField;
    T2_Sub71GMEMO: TDateTimeField;
    T2_Sub72ID: TFloatField;
    T2_Sub72GDATE: TStringField;
    T2_Sub72GCODE: TStringField;
    T2_Sub72GNAME: TStringField;
    T2_Sub72GTELS: TStringField;
    T2_Sub72CODE4: TStringField;
    T2_Sub72CODE5: TStringField;
    T2_Sub72CODE1: TStringField;
    T2_Sub72CODE2: TStringField;
    T2_Sub72CODE3: TStringField;
    T2_Sub72GOQUT: TFloatField;
    T2_Sub72GSQUT: TFloatField;
    T2_Sub72GSSUM: TFloatField;
    T4_Sub51GSQUT: TFloatField;
    T4_Sub71GSUMX: TFloatField;
    T4_Sub71GSUMY: TFloatField;
    T4_Sub81ID: TFloatField;
    T4_Sub81GDATE: TStringField;
    T4_Sub81SCODE: TStringField;
    T4_Sub81GCODE: TStringField;
    T4_Sub81GNAME: TStringField;
    T4_Sub81HCODE: TStringField;
    T4_Sub81HNAME: TStringField;
    T4_Sub81NAME1: TStringField;
    T4_Sub81NAME2: TStringField;
    T4_Sub81GSSUM: TFloatField;
    T4_Sub81GSUMX: TFloatField;
    T4_Sub81GSUMY: TFloatField;
    T2_Sub11GJISA: TStringField;
    T2_Sub12GJISA: TStringField;
    T2_Sub21GJISA: TStringField;
    T2_Sub22GJISA: TStringField;
    T2_Sub31GJISA: TStringField;
    T2_Sub32GJISA: TStringField;
    T2_Sub41GJISA: TStringField;
    T2_Sub51GJISA: TStringField;
    T2_Sub91GJISA: TStringField;
    T2_Sub81GJISA: TStringField;
    T2_Sub61GJISA: TStringField;
    T2_Sub62GJISA: TStringField;
    T5_Sub31GJISA: TStringField;
    T5_Sub32GJISA: TStringField;
    T5_Sub41GJISA: TStringField;
    T5_Sub42GJISA: TStringField;
    T5_Sub51GJISA: TStringField;
    T5_Sub52GJISA: TStringField;
    T5_Sub61GJISA: TStringField;
    T5_Sub62GJISA: TStringField;
    T5_Sub71GJISA: TStringField;
    T5_Sub72GJISA: TStringField;
    T5_Sub81GJISA: TStringField;
    T5_Sub82GJISA: TStringField;
    T2_Sub71GJISA: TStringField;
    T4_Sub81GQUT1: TFloatField;
    T4_Sub81GQUT2: TFloatField;
    T6_Sub11GJISA: TStringField;
    T6_Sub12GJISA: TStringField;
    T6_Sub21GJISA: TStringField;
    T6_Sub22GJISA: TStringField;
    T6_Sub31GJISA: TStringField;
    T6_Sub32GJISA: TStringField;
    T6_Sub41GJISA: TStringField;
    T6_Sub42GJISA: TStringField;
    T6_Sub51GJISA: TStringField;
    T6_Sub52GJISA: TStringField;
    T6_Sub61GJISA: TStringField;
    T6_Sub62GJISA: TStringField;
    T6_Sub71GJISA: TStringField;
    T6_Sub72GJISA: TStringField;
    T6_Sub81GJISA: TStringField;
    T6_Sub82GJISA: TStringField;
    G1_Ggeo: TClientDataSet;
    G1_GgeoHCODE: TStringField;
    G1_GgeoGCODE: TStringField;
    G1_GgeoGNAME: TStringField;
    G1_GgeoOCODE: TStringField;
    G1_GgeoGUBUN: TStringField;
    G2_Ggwo: TClientDataSet;
    G4_Book: TClientDataSet;
    G7_Ggeo: TClientDataSet;
    G2_GgwoHCODE: TStringField;
    G2_GgwoGCODE: TStringField;
    G2_GgwoGNAME: TStringField;
    G2_GgwoOCODE: TStringField;
    G2_GgwoGUBUN: TStringField;
    G4_BookHCODE: TStringField;
    G4_BookGCODE: TStringField;
    G4_BookGNAME: TStringField;
    G4_BookOCODE: TStringField;
    G4_BookGUBUN: TStringField;
    G4_BookGDANG: TFloatField;
    G7_GgeoHCODE: TStringField;
    G7_GgeoGCODE: TStringField;
    G7_GgeoGNAME: TStringField;
    T2_Sub81JUBUN: TStringField;
    T1_Sub11EMAIL: TStringField;
    T1_Sub21EMAIL: TStringField;
    T1_Sub51EMAIL: TStringField;
    T2_Sub81BEBON: TStringField;
    G1_GgeoPUBUN: TStringField;
    G2_GgwoPUBUN: TStringField;
    H2_Gbun: TClientDataSet;
    H2_GbunHCODE: TStringField;
    H2_GbunSCODE: TStringField;
    H2_GbunGCODE: TStringField;
    H2_GbunGNAME: TStringField;
    H2_GbunJUBUN: TStringField;
    H2_GbunGDATE: TStringField;
    T1_Gbun: TClientDataSet;
    T1_GbunHCODE: TStringField;
    T1_GbunGCODE: TStringField;
    T1_GbunGNAME: TStringField;
    T1_GbunGJISA: TStringField;
    T1_GbunJUBUN: TStringField;
    T1_Ssub: TClientDataSet;
    T2_Ssub: TClientDataSet;
    T3_Ssub: TClientDataSet;
    T4_Ssub: TClientDataSet;
    T4_SsubHCODE: TStringField;
    T4_SsubGCODE: TStringField;
    T4_SsubGDATE: TStringField;
    T4_SsubGJISA: TStringField;
    T4_SsubGQUT1: TFloatField;
    T4_SsubGQUT2: TFloatField;
    T4_SsubGQUT3: TFloatField;
    T4_SsubJUBUN: TStringField;
    T4_Sub31GNUMB: TStringField;
    T4_Sub31GBIGO: TStringField;
    T4_Sub32GNUMB: TStringField;
    T4_Sub32GBIGO: TStringField;
    T4_Sub41GNUMB: TStringField;
    T4_Sub41GBIGO: TStringField;
    T4_Sub42GNUMB: TStringField;
    T4_Sub42GBIGO: TStringField;
    G6_Ggeo: TClientDataSet;
    G6_GgeoID: TFloatField;
    G6_GgeoHCODE: TStringField;
    G6_GgeoGCODE: TStringField;
    G6_GgeoBCODE: TStringField;
    G6_GgeoGRAT1: TSmallintField;
    G6_GgeoGRAT2: TSmallintField;
    G6_GgeoGRAT3: TSmallintField;
    G6_GgeoGRAT4: TSmallintField;
    G6_GgeoGRAT5: TSmallintField;
    G6_GgeoGRAT6: TSmallintField;
    G6_GgeoGRAT7: TSmallintField;
    G6_GgeoGRAT8: TSmallintField;
    G6_GgeoGRAT9: TSmallintField;
    G6_GgeoGSSUM: TFloatField;
    T4_Sub21GSUMX: TFloatField;
    T4_Sub21GOSUM: TFloatField;
    T4_Sub21GSSUM: TFloatField;
    T4_Sub21GSUSU: TFloatField;
    T4_Sub21GSUMY: TFloatField;
    T4_Sub21GBSUM: TFloatField;
    T1_Sub71CHEK1: TStringField;
    T1_Sub71CHEK2: TStringField;
    G7_GgeoCHEK1: TStringField;
    G7_GgeoCHEK2: TStringField;
    T4_Sub81GNUM1: TFloatField;
    T4_Sub81GNUM2: TFloatField;
    T4_Sub81GQUT3: TFloatField;
    T4_Sub81GQUT4: TFloatField;
    T1_Sub11GPHON: TStringField;
    T1_Sub21GPHON: TStringField;
    T1_Sub51GPHON: TStringField;
    T4_Sub51YESNO: TStringField;
    T1_Sub81GPPER: TStringField;
    T1_Sub81BIGO1: TStringField;
    T1_Sub81BIGO2: TStringField;
    T1_Sub81GPHON: TStringField;
    T1_Sub11TCODE: TStringField;
    T1_Sub11TNAME: TStringField;
    T1_Sub21TCODE: TStringField;
    T1_Sub21TNAME: TStringField;
    T1_Sub41TCODE: TStringField;
    T1_Sub41TNAME: TStringField;
    T1_Sub51TCODE: TStringField;
    T1_Sub51TNAME: TStringField;
    G7_GgeoYES35: TStringField;
    T5_Sub31BDATE: TStringField;
    T5_Sub41BDATE: TStringField;
    T5_Sub51BDATE: TStringField;
    T5_Sub61BDATE: TStringField;
    T5_Sub71BDATE: TStringField;
    T5_Sub81BDATE: TStringField;
    T4_Sub51GQUT5: TFloatField;
    T4_Sub51GQUT6: TFloatField;
    T4_Sub51GQUT7: TFloatField;
    T4_Sub51AQUT1: TFloatField;
    T4_Sub51AQUT2: TFloatField;
    T4_Sub51BQUT1: TFloatField;
    T4_Sub51BQUT2: TFloatField;
    T1_Sub41GPOST: TStringField;
    T4_SsubGSQUT: TFloatField;
    T4_Sub51GQUT8: TFloatField;
    T4_Sub51GQUT9: TFloatField;
    T4_Sub31GSQUT: TFloatField;
    T4_Sub31GDANG: TFloatField;
    T4_Sub32GSQUT: TFloatField;
    T4_Sub32GDANG: TFloatField;
    T4_SsubPUBUN: TStringField;
    T2_Sub61TIME1: TDateTimeField;
    T2_Sub61TIME2: TDateTimeField;
    T2_Sub61TIME3: TDateTimeField;
    T2_Sub61TIME4: TDateTimeField;
    T2_Sub11GPOST: TStringField;
    T2_Sub61GPOST: TStringField;
    T2_Sub71GPOST: TStringField;
    T2_Sub71QPOST: TStringField;
    T2_Sub61QPOST: TStringField;
    T2_Sub11QPOST: TStringField;
    T3_Sub31GPOST: TStringField;
    T3_Sub32GPOST: TStringField;
    T4_SsubGBIGO: TStringField;
    T1_GbunBEBON: TStringField;
    G5_Ggeo: TClientDataSet;
    G5_GgeoHCODE: TStringField;
    G5_GgeoGCODE: TStringField;
    G5_GgeoGNAME: TStringField;
    G5_GgeoOCODE: TStringField;
    G5_GgeoGUBUN: TStringField;
    G5_GgeoPUBUN: TStringField;
    T1_Sub11GNUM1: TStringField;
    T1_Sub21GNUM1: TStringField;
    T1_Sub51GNUM1: TStringField;
    T4_Sub51GSUM1: TFloatField;
    T4_Sub51GSUM2: TFloatField;
    T6_Sub21HCODE: TStringField;
    T6_Sub22HCODE: TStringField;
    T2_Sub11ICODE: TFloatField;
    T2_Sub12ICODE: TFloatField;
    T2_Sub21ICODE: TFloatField;
    T2_Sub22ICODE: TFloatField;
    T2_Sub31ICODE: TFloatField;
    T2_Sub91ICODE: TFloatField;
    T2_Sub41ICODE: TFloatField;
    T2_Sub42ICODE: TFloatField;
    T2_Sub51ICODE: TFloatField;
    T2_Sub61ICODE: TFloatField;
    T2_Sub62ICODE: TFloatField;
    T2_Sub71ICODE: TFloatField;
    G4_BookGRAT8: TFloatField;
    G4_BookBIGO4: TStringField;
    T1_Sub41BIGO4: TStringField;
    T1_Sub71GNUM1: TStringField;
    T3_Sub21OQUT1: TFloatField;
    T3_Sub21OQUT2: TFloatField;
    T3_Sub21OQUT3: TFloatField;
    T3_Sub21OQUT4: TFloatField;
    H2_GbunONAME: TStringField;
    T1_Sub71CHEK4: TStringField;
    T4_SsubYESNO: TStringField;
    T1_Sub41GRAT8: TFloatField;
    ZMySqlQuery1: TZMySqlQuery;
    function LockPass01(nStr:String):String;
    function LockPass02(nStr:String):String;
    function LockCheck1(nStr:String):String;
    function LockCheck2(nStr:String):String;

    procedure T2_Sub11OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub11OCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub11TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub11TCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub12OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub12OCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub12TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub12TCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub21OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub21OCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub21TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub21TCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub22OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub22OCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub22TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub22TCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub31OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub31OCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub31TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub31TCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub41TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub41TCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub51TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub51TCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub91OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub91OCODESetText(Sender: TField; const Text: String);
    procedure T2_Sub91TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
    procedure T2_Sub91TCODESetText(Sender: TField; const Text: String);

    procedure T1_Sub11AfterScroll(DataSet: TDataSet);
    procedure T1_Sub12AfterScroll(DataSet: TDataSet);
    procedure T1_Sub21AfterScroll(DataSet: TDataSet);
    procedure T1_Sub22AfterScroll(DataSet: TDataSet);
    procedure T1_Sub31AfterScroll(DataSet: TDataSet);
    procedure T1_Sub32AfterScroll(DataSet: TDataSet);
    procedure T1_Sub41AfterScroll(DataSet: TDataSet);
    procedure T1_Sub42AfterScroll(DataSet: TDataSet);
    procedure T1_Sub51AfterScroll(DataSet: TDataSet);
    procedure T1_Sub52AfterScroll(DataSet: TDataSet);
    procedure T1_Sub71AfterScroll(DataSet: TDataSet);
    procedure T1_Sub72AfterScroll(DataSet: TDataSet);
    procedure T1_Sub81AfterScroll(DataSet: TDataSet);
    procedure T1_Sub82AfterScroll(DataSet: TDataSet);
    procedure T4_Sub61AfterScroll(DataSet: TDataSet);
    procedure T4_Sub62AfterScroll(DataSet: TDataSet);

    procedure T1_Sub61AfterCancel(DataSet: TDataSet);
    procedure T1_Sub61AfterPost(DataSet: TDataSet);
    procedure T1_Sub61AfterDelete(DataSet: TDataSet);
    procedure T1_Sub61BeforePost(DataSet: TDataSet);
    procedure T1_Sub61AfterScroll(DataSet: TDataSet);
    procedure T1_Sub61BeforeClose(DataSet: TDataSet);

    procedure T1_Sub62AfterCancel(DataSet: TDataSet);
    procedure T1_Sub62AfterScroll(DataSet: TDataSet);
    procedure T1_Sub62AfterPost(DataSet: TDataSet);
    procedure T1_Sub62AfterDelete(DataSet: TDataSet);
    procedure T1_Sub62BeforePost(DataSet: TDataSet);
    procedure T1_Sub62BeforeClose(DataSet: TDataSet);

    procedure T2_Sub11AfterCancel(DataSet: TDataSet);
    procedure T2_Sub11AfterScroll(DataSet: TDataSet);
    procedure T2_Sub11AfterPost(DataSet: TDataSet);
    procedure T2_Sub11AfterDelete(DataSet: TDataSet);
    procedure T2_Sub11BeforePost(DataSet: TDataSet);
    procedure T2_Sub11BeforeClose(DataSet: TDataSet);

    procedure T2_Sub21AfterCancel(DataSet: TDataSet);
    procedure T2_Sub21AfterScroll(DataSet: TDataSet);
    procedure T2_Sub21AfterPost(DataSet: TDataSet);
    procedure T2_Sub21AfterDelete(DataSet: TDataSet);
    procedure T2_Sub21BeforePost(DataSet: TDataSet);
    procedure T2_Sub21BeforeClose(DataSet: TDataSet);

    procedure T2_Sub31AfterCancel(DataSet: TDataSet);
    procedure T2_Sub31AfterScroll(DataSet: TDataSet);
    procedure T2_Sub31AfterPost(DataSet: TDataSet);
    procedure T2_Sub31AfterDelete(DataSet: TDataSet);
    procedure T2_Sub31BeforePost(DataSet: TDataSet);
    procedure T2_Sub31BeforeClose(DataSet: TDataSet);

    procedure T2_Sub41AfterCancel(DataSet: TDataSet);
    procedure T2_Sub41AfterScroll(DataSet: TDataSet);
    procedure T2_Sub41AfterPost(DataSet: TDataSet);
    procedure T2_Sub41AfterDelete(DataSet: TDataSet);
    procedure T2_Sub41BeforePost(DataSet: TDataSet);
    procedure T2_Sub41BeforeClose(DataSet: TDataSet);

    procedure T2_Sub51AfterCancel(DataSet: TDataSet);
    procedure T2_Sub51AfterScroll(DataSet: TDataSet);
    procedure T2_Sub51AfterPost(DataSet: TDataSet);
    procedure T2_Sub51AfterDelete(DataSet: TDataSet);
    procedure T2_Sub51BeforePost(DataSet: TDataSet);
    procedure T2_Sub51BeforeClose(DataSet: TDataSet);

    procedure T2_Sub61AfterCancel(DataSet: TDataSet);
    procedure T2_Sub61AfterScroll(DataSet: TDataSet);
    procedure T2_Sub61AfterPost(DataSet: TDataSet);
    procedure T2_Sub61AfterDelete(DataSet: TDataSet);
    procedure T2_Sub61BeforePost(DataSet: TDataSet);
    procedure T2_Sub61BeforeClose(DataSet: TDataSet);

    procedure T2_Sub62AfterCancel(DataSet: TDataSet);
    procedure T2_Sub62AfterScroll(DataSet: TDataSet);
    procedure T2_Sub62AfterPost(DataSet: TDataSet);
    procedure T2_Sub62AfterDelete(DataSet: TDataSet);
    procedure T2_Sub62BeforePost(DataSet: TDataSet);
    procedure T2_Sub62BeforeClose(DataSet: TDataSet);

    procedure T2_Sub81AfterCancel(DataSet: TDataSet);
    procedure T2_Sub81AfterScroll(DataSet: TDataSet);
    procedure T2_Sub81AfterPost(DataSet: TDataSet);
    procedure T2_Sub81AfterDelete(DataSet: TDataSet);
    procedure T2_Sub81BeforePost(DataSet: TDataSet);
    procedure T2_Sub81BeforeClose(DataSet: TDataSet);

    procedure T2_Sub91AfterCancel(DataSet: TDataSet);
    procedure T2_Sub91AfterScroll(DataSet: TDataSet);
    procedure T2_Sub91AfterPost(DataSet: TDataSet);
    procedure T2_Sub91AfterDelete(DataSet: TDataSet);
    procedure T2_Sub91BeforePost(DataSet: TDataSet);
    procedure T2_Sub91BeforeClose(DataSet: TDataSet);

    procedure T3_Sub81AfterCancel(DataSet: TDataSet);
    procedure T3_Sub81AfterPost(DataSet: TDataSet);
    procedure T3_Sub81AfterDelete(DataSet: TDataSet);
    procedure T3_Sub81BeforePost(DataSet: TDataSet);
    procedure T3_Sub81AfterScroll(DataSet: TDataSet);
    procedure T3_Sub81BeforeClose(DataSet: TDataSet);

    procedure T3_Sub82AfterCancel(DataSet: TDataSet);
    procedure T3_Sub82AfterScroll(DataSet: TDataSet);
    procedure T3_Sub82AfterPost(DataSet: TDataSet);
    procedure T3_Sub82AfterDelete(DataSet: TDataSet);
    procedure T3_Sub82BeforePost(DataSet: TDataSet);
    procedure T3_Sub82BeforeClose(DataSet: TDataSet);

    procedure T4_Sub11AfterCancel(DataSet: TDataSet);
    procedure T4_Sub11AfterScroll(DataSet: TDataSet);
    procedure T4_Sub11AfterPost(DataSet: TDataSet);
    procedure T4_Sub11AfterDelete(DataSet: TDataSet);
    procedure T4_Sub11BeforePost(DataSet: TDataSet);
    procedure T4_Sub11BeforeClose(DataSet: TDataSet);

    procedure T4_Sub12AfterCancel(DataSet: TDataSet);
    procedure T4_Sub12AfterScroll(DataSet: TDataSet);
    procedure T4_Sub12AfterPost(DataSet: TDataSet);
    procedure T4_Sub12AfterDelete(DataSet: TDataSet);
    procedure T4_Sub12BeforePost(DataSet: TDataSet);
    procedure T4_Sub12BeforeClose(DataSet: TDataSet);

    procedure T4_Sub21AfterCancel(DataSet: TDataSet);
    procedure T4_Sub21AfterScroll(DataSet: TDataSet);
    procedure T4_Sub21AfterPost(DataSet: TDataSet);
    procedure T4_Sub21AfterDelete(DataSet: TDataSet);
    procedure T4_Sub21BeforePost(DataSet: TDataSet);
    procedure T4_Sub21BeforeClose(DataSet: TDataSet);

    procedure T4_Sub22AfterCancel(DataSet: TDataSet);
    procedure T4_Sub22AfterScroll(DataSet: TDataSet);
    procedure T4_Sub22AfterPost(DataSet: TDataSet);
    procedure T4_Sub22AfterDelete(DataSet: TDataSet);
    procedure T4_Sub22BeforePost(DataSet: TDataSet);
    procedure T4_Sub22BeforeClose(DataSet: TDataSet);

    procedure T4_Sub31AfterCancel(DataSet: TDataSet);
    procedure T4_Sub31AfterScroll(DataSet: TDataSet);
    procedure T4_Sub31AfterPost(DataSet: TDataSet);
    procedure T4_Sub31AfterDelete(DataSet: TDataSet);
    procedure T4_Sub31BeforePost(DataSet: TDataSet);
    procedure T4_Sub31BeforeClose(DataSet: TDataSet);

    procedure T4_Sub51AfterCancel(DataSet: TDataSet);
    procedure T4_Sub51AfterScroll(DataSet: TDataSet);
    procedure T4_Sub51AfterPost(DataSet: TDataSet);
    procedure T4_Sub51AfterDelete(DataSet: TDataSet);
    procedure T4_Sub51BeforePost(DataSet: TDataSet);
    procedure T4_Sub51BeforeClose(DataSet: TDataSet);

    procedure T5_Sub11AfterCancel(DataSet: TDataSet);
    procedure T5_Sub11AfterScroll(DataSet: TDataSet);
    procedure T5_Sub11AfterPost(DataSet: TDataSet);
    procedure T5_Sub11AfterDelete(DataSet: TDataSet);
    procedure T5_Sub11BeforePost(DataSet: TDataSet);
    procedure T5_Sub11BeforeClose(DataSet: TDataSet);

    procedure T5_Sub12AfterCancel(DataSet: TDataSet);
    procedure T5_Sub12AfterScroll(DataSet: TDataSet);
    procedure T5_Sub12AfterPost(DataSet: TDataSet);
    procedure T5_Sub12AfterDelete(DataSet: TDataSet);
    procedure T5_Sub12BeforePost(DataSet: TDataSet);
    procedure T5_Sub12BeforeClose(DataSet: TDataSet);

    procedure T5_Sub21AfterCancel(DataSet: TDataSet);
    procedure T5_Sub21AfterScroll(DataSet: TDataSet);
    procedure T5_Sub21AfterPost(DataSet: TDataSet);
    procedure T5_Sub21AfterDelete(DataSet: TDataSet);
    procedure T5_Sub21BeforePost(DataSet: TDataSet);
    procedure T5_Sub21BeforeClose(DataSet: TDataSet);

    procedure T5_Sub22AfterCancel(DataSet: TDataSet);
    procedure T5_Sub22AfterScroll(DataSet: TDataSet);
    procedure T5_Sub22AfterPost(DataSet: TDataSet);
    procedure T5_Sub22AfterDelete(DataSet: TDataSet);
    procedure T5_Sub22BeforePost(DataSet: TDataSet);
    procedure T5_Sub22BeforeClose(DataSet: TDataSet);

    procedure T5_Sub31AfterCancel(DataSet: TDataSet);
    procedure T5_Sub31AfterScroll(DataSet: TDataSet);
    procedure T5_Sub31AfterPost(DataSet: TDataSet);
    procedure T5_Sub31AfterDelete(DataSet: TDataSet);
    procedure T5_Sub31BeforePost(DataSet: TDataSet);
    procedure T5_Sub31BeforeClose(DataSet: TDataSet);

    procedure T5_Sub32AfterCancel(DataSet: TDataSet);
    procedure T5_Sub32AfterScroll(DataSet: TDataSet);
    procedure T5_Sub32AfterPost(DataSet: TDataSet);
    procedure T5_Sub32AfterDelete(DataSet: TDataSet);
    procedure T5_Sub32BeforePost(DataSet: TDataSet);
    procedure T5_Sub32BeforeClose(DataSet: TDataSet);

    procedure T5_Sub41AfterCancel(DataSet: TDataSet);
    procedure T5_Sub41AfterScroll(DataSet: TDataSet);
    procedure T5_Sub41AfterPost(DataSet: TDataSet);
    procedure T5_Sub41AfterDelete(DataSet: TDataSet);
    procedure T5_Sub41BeforePost(DataSet: TDataSet);
    procedure T5_Sub41BeforeClose(DataSet: TDataSet);

    procedure T5_Sub42AfterCancel(DataSet: TDataSet);
    procedure T5_Sub42AfterScroll(DataSet: TDataSet);
    procedure T5_Sub42AfterPost(DataSet: TDataSet);
    procedure T5_Sub42AfterDelete(DataSet: TDataSet);
    procedure T5_Sub42BeforePost(DataSet: TDataSet);
    procedure T5_Sub42BeforeClose(DataSet: TDataSet);

    procedure T5_Sub51AfterCancel(DataSet: TDataSet);
    procedure T5_Sub51AfterScroll(DataSet: TDataSet);
    procedure T5_Sub51AfterPost(DataSet: TDataSet);
    procedure T5_Sub51AfterDelete(DataSet: TDataSet);
    procedure T5_Sub51BeforePost(DataSet: TDataSet);
    procedure T5_Sub51BeforeClose(DataSet: TDataSet);

    procedure T5_Sub52AfterCancel(DataSet: TDataSet);
    procedure T5_Sub52AfterScroll(DataSet: TDataSet);
    procedure T5_Sub52AfterPost(DataSet: TDataSet);
    procedure T5_Sub52AfterDelete(DataSet: TDataSet);
    procedure T5_Sub52BeforePost(DataSet: TDataSet);
    procedure T5_Sub52BeforeClose(DataSet: TDataSet);

    procedure T1_Sub11NewRecord(DataSet: TDataSet);
    procedure T1_Sub21NewRecord(DataSet: TDataSet);
    procedure T1_Sub31NewRecord(DataSet: TDataSet);
    procedure T1_Sub41NewRecord(DataSet: TDataSet);
    procedure T1_Sub51NewRecord(DataSet: TDataSet);
    procedure T1_Sub61NewRecord(DataSet: TDataSet);
    procedure T1_Sub62NewRecord(DataSet: TDataSet);
    procedure T1_Sub71NewRecord(DataSet: TDataSet);
    procedure T1_Sub72NewRecord(DataSet: TDataSet);
    procedure T1_Sub81NewRecord(DataSet: TDataSet);
    procedure T1_Sub82NewRecord(DataSet: TDataSet);
    procedure T2_Sub11NewRecord(DataSet: TDataSet);
    procedure T2_Sub21NewRecord(DataSet: TDataSet);
    procedure T2_Sub31NewRecord(DataSet: TDataSet);
    procedure T2_Sub41NewRecord(DataSet: TDataSet);
    procedure T2_Sub51NewRecord(DataSet: TDataSet);
    procedure T2_Sub61NewRecord(DataSet: TDataSet);
    procedure T2_Sub62NewRecord(DataSet: TDataSet);
    procedure T2_Sub81NewRecord(DataSet: TDataSet);
    procedure T2_Sub91NewRecord(DataSet: TDataSet);
    procedure T3_Sub81NewRecord(DataSet: TDataSet);
    procedure T3_Sub82NewRecord(DataSet: TDataSet);
    procedure T4_Sub11NewRecord(DataSet: TDataSet);
    procedure T4_Sub12NewRecord(DataSet: TDataSet);
    procedure T4_Sub21NewRecord(DataSet: TDataSet);
    procedure T4_Sub22NewRecord(DataSet: TDataSet);
    procedure T4_Sub31NewRecord(DataSet: TDataSet);
    procedure T4_Sub61NewRecord(DataSet: TDataSet);
    procedure T4_Sub62NewRecord(DataSet: TDataSet);
    procedure T5_Sub11NewRecord(DataSet: TDataSet);
    procedure T5_Sub12NewRecord(DataSet: TDataSet);
    procedure T5_Sub21NewRecord(DataSet: TDataSet);
    procedure T5_Sub22NewRecord(DataSet: TDataSet);
    procedure T5_Sub31NewRecord(DataSet: TDataSet);
    procedure T5_Sub32NewRecord(DataSet: TDataSet);
    procedure T5_Sub41NewRecord(DataSet: TDataSet);
    procedure T5_Sub42NewRecord(DataSet: TDataSet);
    procedure T5_Sub51NewRecord(DataSet: TDataSet);
    procedure T5_Sub52NewRecord(DataSet: TDataSet);

    procedure T1_Sub11CalcFields(DataSet: TDataSet);
    procedure T2_Sub82CalcFields(DataSet: TDataSet);

    procedure Socket3Error(Sender: TObject; Socket: TCustomWinSocket;
      ErrorEvent: TErrorEvent; var ErrorCode: Integer);
  private
    { Private declarations }
  public
    { Public declarations }
    procedure LoadData_G1_Ggeo(fStr: string);
    procedure LoadData_G4_Book(fStr: string);
    procedure ColumnM0(TableX: TClientDataSet; PBar: TProgressBar);

    procedure SpaceDel(TableX: TClientDataSet; _Gcode,_Gname: String);
    procedure OpenData(TableX: TClientDataSet);
    procedure OpenBase(TableX: TClientDataSet);
    procedure OpenShow(TableX: TClientDataSet);
    procedure OpenExit(TableX: TClientDataSet);
    procedure CreateSX(TableX: TClientDataSet);
    procedure DeleteSX(TableX: TClientDataSet);
    procedure ColumnSX(TableX: TClientDataSet; Column: TColumn);
    procedure ColumnS9(TableX: TClientDataSet; Column: TColumnEh);
    procedure ColumnX0(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
    procedure ColumnX1(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
    procedure ColumnX2(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
    procedure ColumnX3(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
    procedure ColumnX9(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);

    procedure ColumnY0(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
    procedure ColumnY1(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
    procedure ColumnY2(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
    procedure ColumnY3(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);

    procedure _Gs_Gsum_(St0,St1,St2,St3,Field1,Field2:String;Sq1,Sq2:Double);
    procedure _Gs_Csum_(St0,St1,St2,St3,Field1,Field2:String;Sq1,Sq2:Double);
    procedure _Sv_Gsum_(St0,St1,St2,St4,St5,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sv_Csum_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);

    procedure _Sv_Chng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sv_Chnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sv_Ghng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sv_Ghnb_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sv_Ghnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);

    procedure _Sg_Chng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sg_Chnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sg_Ghng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sg_Ghnb_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
    procedure _Sg_Ghnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);

    procedure _H1_Gbun_(St0,St1,St2,St3,Field1:String;Sq1:Double);
    procedure _H2_Gbun_(St0,St1,St2,St3,Field1:String;Sq1:Double);
    procedure _H5_Bang_(St0,St1,St2,Field1:String;Sq1:Double);

    procedure _S_Repla1(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
    procedure _B_Repla1(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
    procedure _H_Repla1(St0,St1,St2,St3,St4,St5:String;Sq1:Double);
    procedure _G_Repla1(St0,St1,St2,St3:String;Sq1:Double);
    procedure _J_Repla1(St0,St1,St2,St3:String;Sq1:Double);

    procedure _S_Repla2(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
    procedure _B_Repla2(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
    procedure _H_Repla2(St0,St1,St2,St3,St4,St5:String;Sq1:Double);
    procedure _G_Repla2(St0,St1,St2,St3:String;Sq1:Double);
    procedure _J_Repla2(St0,St1,St2,St3:String;Sq1:Double);

    procedure _Z_Repla1(St0,St1,St2,St3,St4,St5,St6:String;Sq1:Double);
    procedure _W_Repla1(St0,St1,St2,St3,St4:String;Sq1:Double);

    procedure Insert_ID(TableX: TClientDataSet; GENERATOR: String);
    procedure Update_ID(TableX: TClientDataSet; GENERATOR: String);
    procedure Insert_Idnum(TableX: TClientDataSet; GENERATOR: String);
    procedure Update_Idnum(TableX: TClientDataSet; GENERATOR: String);
    procedure Update_Icode(TableX: TClientDataSet; GENERATOR: String);
    function Seek_Name(_Gcode1:String) : String;
    function Seek_Code(_Gcode1,_Gcode2,_Gcode3:String) : String;
    function Seek_Bigo(_Gcode1,_Gcode2,_Gcode3:String) : String;
    function Seek_Uses(_Gcode1:String) : String;
    function Seek_Ggeo(_Gcode1:String) : String;
    function Seek_Hgeo(_Gcode1,_Gcode2,_Gcode3:String) : String;
    function Seek_Hname(_Gcode1,_Gcode2:String) : String;
    function Seek_Jisa(_Gcode1,_Gcode2:String) : String;
    procedure Init_Show(Sender: TObject);
  end;

var
  Base10: TBase10;
  Bmark: TBookMark;
  List1,Grat1,RBand: Integer;
  nSqry,mSqry,tSqry,oSqry,uSqry,lSqry,sSqry: TClientDataSet;
  nForm,Code1,Code2,nPrnt,mPrnt,ePrnt,Sqlen,Sqlon: String;
  Gdate,Scode,Gcode,Gubun,Jubun,Pubun,Ocode,Bcode: String;
  nList,Jeago,Lower,Hnnnn,Logn1,Logn2,Logn3: String;
  System_Data: String;
  Idnum,Giqut,Goqut,Gjqut,Gbqut,Gpqut,Gsqut,Gdang: Double;
  Gisum,Gosum,Gjsum,Gbsum,Gsusu,Gssum,GsumX,GsumY: Double;
  T01,T02,T03,T04,T05,T06,T07,T08,T09,T00: Double;
  SGrid,YGrid: TStringGrid;

implementation

{$R *.DFM}

uses Chul,TcpLib,Tong01,Tong04,
     Subu11,Subu12,Subu13,Subu14,Subu15,Subu16,Subu17,Subu18,Subu19,Subu10,
     Subu21,Subu22,Subu23,Subu24,Subu25,Subu26,Subu27,Subu28,Subu29,Subu20,
     Subu31,Subu32,Subu33,Subu34,Subu35,Subu36,Subu37,Subu38,Subu39,Subu30,
     Subu41,Subu42,Subu43,Subu44,Subu45,Subu46,Subu47,Subu48,Subu49,Subu40,
     Subu51,Subu52,Subu53,Subu54,Subu55,Subu56,Subu57,Subu58,Subu59,Subu50,
     Subu61,Subu62,Subu63,Subu64,Subu65,Subu66,Subu67,Subu68,Subu69,Subu60;

function TBase10.LockPass01(nStr:String):String;
begin
  Result := '';
  if nStr='A' Then Result := '본사';
  if nStr='B' Then Result := '창고';
end;

function TBase10.LockPass02(nStr:String):String;
begin
  Result := 'A';
  if nStr='본사' Then Result := 'A';
  if nStr='창고' Then Result := 'B';
end;

function TBase10.LockCheck1(nStr:String):String;
begin
  Result := '';
  if nStr='0' Then Result := '';
  if nStr='1' Then Result := '접수';
  if nStr='2' Then Result := '완료';
  if nStr='3' Then Result := '등록';
  if nStr='4' Then Result := '확인';
end;

function TBase10.LockCheck2(nStr:String):String;
begin
  Result := '0';
  if nStr=''     Then Result := '0';
  if nStr='접수' Then Result := '1';
  if nStr='완료' Then Result := '2';
  if nStr='등록' Then Result := '3';
  if nStr='확인' Then Result := '4';
end;

procedure TBase10.T2_Sub11OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockPass01(T2_Sub11.FieldByName('Ocode').AsString);
end;

procedure TBase10.T2_Sub11OCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub11.FieldByName('Ocode').AsString:=LockPass02(Text);
end;

procedure TBase10.T2_Sub11TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub11.FieldByName('Yesno').AsString);
end;

procedure TBase10.T2_Sub11TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub11.FieldByName('Yesno').AsString:=LockCheck2(Text);
end;

procedure TBase10.T2_Sub12OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockPass01(T2_Sub12.FieldByName('Ocode').AsString);
end;

procedure TBase10.T2_Sub12OCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub12.FieldByName('Ocode').AsString:=LockPass02(Text);
end;

procedure TBase10.T2_Sub12TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub12.FieldByName('Tcode').AsString);
end;

procedure TBase10.T2_Sub12TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub12.FieldByName('Tcode').AsString:=LockCheck2(Text);
end;

procedure TBase10.T2_Sub21OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockPass01(T2_Sub21.FieldByName('Ocode').AsString);
end;

procedure TBase10.T2_Sub21OCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub21.FieldByName('Ocode').AsString:=LockPass02(Text);
end;

procedure TBase10.T2_Sub21TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub21.FieldByName('Yesno').AsString);
end;

procedure TBase10.T2_Sub21TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub21.FieldByName('Yesno').AsString:=LockCheck2(Text);
end;

procedure TBase10.T2_Sub22OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockPass01(T2_Sub22.FieldByName('Ocode').AsString);
end;

procedure TBase10.T2_Sub22OCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub22.FieldByName('Ocode').AsString:=LockPass02(Text);
end;

procedure TBase10.T2_Sub22TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub22.FieldByName('Tcode').AsString);
end;

procedure TBase10.T2_Sub22TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub22.FieldByName('Tcode').AsString:=LockCheck2(Text);
end;

procedure TBase10.T2_Sub31OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockPass01(T2_Sub31.FieldByName('Ocode').AsString);
end;

procedure TBase10.T2_Sub31OCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub31.FieldByName('Ocode').AsString:=LockPass02(Text);
end;

procedure TBase10.T2_Sub31TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub31.FieldByName('Yesno').AsString);
end;

procedure TBase10.T2_Sub31TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub31.FieldByName('Yesno').AsString:=LockCheck2(Text);
end;

procedure TBase10.T2_Sub41TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub61.FieldByName('Yesno').AsString);
end;

procedure TBase10.T2_Sub41TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub61.FieldByName('Yesno').AsString:=LockCheck2(Text);
end;

procedure TBase10.T2_Sub51TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub62.FieldByName('Yesno').AsString);
end;

procedure TBase10.T2_Sub51TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub62.FieldByName('Yesno').AsString:=LockCheck2(Text);
end;

procedure TBase10.T2_Sub91OCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockPass01(T2_Sub91.FieldByName('Ocode').AsString);
end;

procedure TBase10.T2_Sub91OCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub91.FieldByName('Ocode').AsString:=LockPass02(Text);
end;

procedure TBase10.T2_Sub91TCODEGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=LockCheck1(T2_Sub91.FieldByName('Yesno').AsString);
end;

procedure TBase10.T2_Sub91TCODESetText(Sender: TField; const Text: String);
begin
  T2_Sub91.FieldByName('Yesno').AsString:=LockCheck2(Text);
end;

procedure TBase10.ColumnM0(TableX: TClientDataSet; PBar: TProgressBar);
var I: Integer;
  St1: Integer;
cFieldname: string;
  St8:array [0..35] of String;
  St9:array [0..35] of String;
  St0: Integer;
begin
  if Subu00.ActiveMDIChild.Name='Sobo63' then begin
     St0:=14;
     St8[00]:='Gname'; St9[00]:='출판사';
     St8[01]:='Aquts'; St9[01]:='01월';
     St8[02]:='Bquts'; St9[02]:='02월';
     St8[03]:='Cquts'; St9[03]:='03월';
     St8[04]:='Dquts'; St9[04]:='04월';
     St8[05]:='Equts'; St9[05]:='05월';
     St8[06]:='Fquts'; St9[06]:='06월';
     St8[07]:='Gquts'; St9[07]:='07월';
     St8[08]:='Hquts'; St9[08]:='08월';
     St8[09]:='Iquts'; St9[09]:='09월';
     St8[10]:='Jquts'; St9[10]:='10월';
     St8[11]:='Kquts'; St9[11]:='11월';
     St8[12]:='Lquts'; St9[12]:='12월';
     St8[13]:='Squts'; St9[13]:='합계';
  end;
  if Subu00.ActiveMDIChild.Name='Sobo64' then begin
     St0:=27;
     St8[00]:='Gname'; St9[00]:='출판사';
     St8[01]:='Aqut1'; St9[01]:='01월(시내)';
     St8[02]:='Aqut2'; St9[02]:='01월(지방)';
     St8[03]:='Bqut1'; St9[03]:='02월(시내)';
     St8[04]:='Bqut2'; St9[04]:='02월(지방)';
     St8[05]:='Cqut1'; St9[05]:='03월(시내)';
     St8[06]:='Cqut2'; St9[06]:='03월(지방)';
     St8[07]:='Dqut1'; St9[07]:='04월(시내)';
     St8[08]:='Dqut2'; St9[08]:='04월(지방)';
     St8[09]:='Equt1'; St9[09]:='05월(시내)';
     St8[10]:='Equt2'; St9[10]:='05월(지방)';
     St8[11]:='Fqut1'; St9[11]:='06월(시내)';
     St8[12]:='Fqut2'; St9[12]:='06월(지방)';
     St8[13]:='Gqut1'; St9[13]:='07월(시내)';
     St8[14]:='Gqut2'; St9[14]:='07월(지방)';
     St8[15]:='Hqut1'; St9[15]:='08월(시내)';
     St8[16]:='Hqut2'; St9[16]:='08월(지방)';
     St8[17]:='Iqut1'; St9[17]:='09월(시내)';
     St8[18]:='Iqut2'; St9[18]:='09월(지방)';
     St8[19]:='Jqut1'; St9[19]:='10월(시내)';
     St8[20]:='Jqut2'; St9[20]:='10월(지방)';
     St8[21]:='Kqut1'; St9[21]:='11월(시내)';
     St8[22]:='Kqut2'; St9[22]:='11월(지방)';
     St8[23]:='Lqut1'; St9[23]:='12월(시내)';
     St8[24]:='Lqut2'; St9[24]:='12월(지방)';
     St8[25]:='Squt1'; St9[25]:='합계(시내)';
     St8[26]:='Squt2'; St9[26]:='합계(지방)';
  end;
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     for I := 0 to St0 - 1 do begin
       cFieldname:=St9[I];
       Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       for I := 0 to St0 - 1 do begin
         cFieldname:=St8[I];
         if TableX.FieldByName(cFieldname).DataType=ftString Then
         Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
         Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.SpaceDel(TableX: TClientDataSet; _Gcode,_Gname: String);
begin
  if TableX.Active=True Then begin
     TableX.First;
     While TableX.EOF=False do begin
       if(TableX.FieldByName(_Gcode).AsString<>'')and
         (TableX.FieldByName(_Gname).AsString<>'')Then begin
          TableX.Next;
       end else
          TableX.Delete;
     end;
  end;
end;

procedure TBase10.OpenData(TableX: TClientDataSet);
begin
  if TableX.Active=True Then
  TableX.Close;
  TableX.CreateDataSet;
  TableX.Filtered:=False;
  TableX.Open;
end;

procedure TBase10.OpenBase(TableX: TClientDataSet);
begin
  if TableX.Active=True Then begin
  DeleteSX(TableX);
  TableX.Close; end;
  TableX.Open;
  CreateSX(TableX);
end;

procedure TBase10.OpenShow(TableX: TClientDataSet);
begin
  if TableX.Active=True Then begin
  DeleteSX(TableX);
  TableX.Close; end;
  TableX.CreateDataSet;
  TableX.Filtered:=False;
  TableX.Open;
  CreateSX(TableX);
end;

procedure TBase10.OpenExit(TableX: TClientDataSet);
begin
  if TableX.Active=True Then begin
  DeleteSX(TableX);
  TableX.Close; end;
end;

procedure TBase10.CreateSX(TableX: TClientDataSet);
var I: Integer;
cFieldname: string;
begin
  for I := 0 to TableX.FieldCount - 1 do begin
    cFieldname:=TableX.Fields[I].FieldName;
    if TableX.FieldByName(cFieldname).FieldKind=fkData Then
    if TableX.Fields[I].DataType in [ftString,ftSmallint,ftInteger,ftWord,ftFloat,ftCurrency,
       ftBCD,ftDate,ftTime,ftDateTime,ftFixedChar,ftWideString,ftLargeInt] then begin
       with TableX do begin
         IndexDefs.Update;
         AddIndex('IDX'+cFieldname+'DOWN', cFieldname, []);
         AddIndex('IDX'+cFieldname+'UP', cFieldname, [],cFieldname);
       end;
    end;
  end;
end;

procedure TBase10.DeleteSX(TableX: TClientDataSet);
var I: Integer;
begin
  TableX.IndexDefs.Update;
  for I := TableX.IndexDefs.Count - 1 downto 0 do begin
    if (TableX.IndexDefs.Items[I].options * [ixPrimary]) <> ([ixPrimary]) then
      if Pos('IDX',TableX.IndexDefs.Items[I].Name) > 0 then
        TableX.DeleteIndex(TableX.IndexDefs.Items[I].Name);
  end;
end;

procedure TBase10.ColumnSX(TableX: TClientDataSet; Column: TColumn);
var I: Integer;
begin
  TableX.IndexDefs.Update;
  if (TableX.IndexDefs.IndexOf('IDX'+Column.FieldName+'DOWN') > 0) or
     (TableX.IndexDefs.IndexOf('IDX'+Column.FieldName+'UP') > 0) then begin
    with TDBGrid(Column.Grid) do begin
      for I := 0 to Columns.Count - 1 do begin
        if Columns[I] = Column then begin
          if Pos('▼',Columns[I].Title.Caption) > 0 then begin
            Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▼','▲',[rfReplaceAll, rfIgnoreCase]);
            TableX.IndexName := 'IDX'+Column.Fieldname+'UP';
          end
          else if Pos('▲',Columns[I].Title.Caption) > 0 then begin
            Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▲','▼',[rfReplaceAll, rfIgnoreCase]);
            TableX.IndexName := 'IDX'+Column.Fieldname+'DOWN';
          end
          else begin
            Columns[I].Title.Caption := Columns[I].Title.Caption + '▼';
            TableX.IndexName := 'IDX'+Column.Fieldname+'DOWN';
          end;
        end
        else begin
          Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▼','',[rfReplaceAll, rfIgnoreCase]);
          Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▲','',[rfReplaceAll, rfIgnoreCase]);
        end;
      end;
    end;
  end;
end;

procedure TBase10.ColumnS9(TableX: TClientDataSet; Column: TColumnEh);
var I: Integer;
begin
  TableX.IndexDefs.Update;
  if (TableX.IndexDefs.IndexOf('IDX'+Column.FieldName+'DOWN') > 0) or
     (TableX.IndexDefs.IndexOf('IDX'+Column.FieldName+'UP') > 0) then begin
    with TDBGridEh(Column.Grid) do begin
      for I := 0 to Columns.Count - 1 do begin
        if Columns[I] = Column then begin
          if Pos('▼',Columns[I].Title.Caption) > 0 then begin
            Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▼','▲',[rfReplaceAll, rfIgnoreCase]);
            TableX.IndexName := 'IDX'+Column.Fieldname+'UP';
          end
          else if Pos('▲',Columns[I].Title.Caption) > 0 then begin
            Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▲','▼',[rfReplaceAll, rfIgnoreCase]);
            TableX.IndexName := 'IDX'+Column.Fieldname+'DOWN';
          end
          else begin
            Columns[I].Title.Caption := Columns[I].Title.Caption + '▼';
            TableX.IndexName := 'IDX'+Column.Fieldname+'DOWN';
          end;
        end
        else begin
          Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▼','',[rfReplaceAll, rfIgnoreCase]);
          Columns[I].Title.Caption := StringReplace(Columns[I].Title.Caption,'▲','',[rfReplaceAll, rfIgnoreCase]);
        end;
      end;
    end;
  end;
end;

procedure TBase10.ColumnX0(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
var I,K,St1,St0: Integer;
  St8:array [0..25] of String;
  St9:array [0..25] of String;
 cFieldname: string;
XL, XArr, XTitle: Variant;
begin
  if(oSqry=Base10.T1_Sub11)or(oSqry=Base10.T1_Sub21)or(oSqry=Base10.T1_Sub51)Then begin
     St0:=20;
     St8[00]:='Sname'; St9[00]:='구분';
     St8[01]:='Jubun'; St9[01]:='지역';
     St8[02]:='Gcode'; St9[02]:='코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업태';
     St8[07]:='Gjomo'; St9[07]:='종목';
     St8[08]:='Gtels'; St9[08]:='전화번호';
     St8[09]:='Gfaxs'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadds'; St9[11]:='주소';
     St8[12]:='Grat1'; St9[12]:='위탁';
     St8[13]:='Grat2'; St9[13]:='현매';
     St8[14]:='Grat3'; St9[14]:='매절';
     St8[15]:='Grat4'; St9[15]:='납품';
     St8[16]:='Grat5'; St9[16]:='특별';
     St8[17]:='Grat6'; St9[17]:='기타';
     St8[18]:='Gqut1'; St9[18]:='신간';
     St8[19]:='Gbigo'; St9[19]:='비고';
  end else
  if(oSqry=Base10.T1_Sub31)Then begin
     St0:=17;
     St8[00]:='Sname'; St9[00]:='구분';
     St8[01]:='Date1'; St9[01]:='등록일자';
     St8[02]:='Gcode'; St9[02]:='저자코드';
     St8[03]:='Gposa'; St9[03]:='저 자 명';
     St8[04]:='Gname'; St9[04]:='직 장 명';
     St8[05]:='Gjice'; St9[05]:='직    책';
     St8[06]:='Gscho'; St9[06]:='출신학교';
     St8[07]:='Gnumb'; St9[07]:='사업자번호';
     St8[08]:='Gnum1'; St9[08]:='주민등록';
     St8[09]:='Gnum2'; St9[09]:='계좌번호';
     St8[10]:='Gtels'; St9[10]:='전화번호';
     St8[11]:='Gfaxs'; St9[11]:='팩스번호';
     St8[12]:='Gpost'; St9[12]:='우편번호';
     St8[13]:='Gadds'; St9[13]:='집 주 소';
     St8[14]:='Opost'; St9[14]:='우편번호';
     St8[15]:='Oadds'; St9[15]:='직장주소';
     St8[16]:='Gbigo'; St9[16]:='비고';
  end else
  if(oSqry=Base10.T1_Sub41)Then begin
     St0:=19;
     St8[00]:='Sname'; St9[00]:='도서분류';
     St8[01]:='Jubun'; St9[01]:='도서처리';
     St8[02]:='Gcode'; St9[02]:='도서코드';
     St8[03]:='Gname'; St9[03]:='도서명';
     St8[04]:='Gjeja'; St9[04]:='저자명';
     St8[05]:='Gdabi'; St9[05]:='단위';
     St8[06]:='Gdang'; St9[06]:='단가';
     St8[07]:='Gisbn'; St9[07]:='ISBN번호';
     St8[08]:='Gbjil'; St9[08]:='도 서 질';
     St8[09]:='Grat1'; St9[09]:='위탁';
     St8[10]:='Grat2'; St9[10]:='현매';
     St8[11]:='Grat3'; St9[11]:='매절';
     St8[12]:='Grat4'; St9[12]:='납품';
     St8[13]:='Grat5'; St9[13]:='특별';
     St8[14]:='Grat6'; St9[14]:='기타';
     St8[15]:='Grat8'; St9[15]:='셋트';
     St8[16]:='Gbigo'; St9[16]:='비고';
     St8[17]:='Gsqut'; St9[17]:='재고';
     St8[18]:='Gssum'; St9[18]:='재고금액';
  // St8[19]:='Gpost'; St9[19]:='서가위치';
  end else
  if(oSqry=Base10.T1_Sub71)Then begin
     St0:=13;
     St8[00]:='Sname'; St9[00]:='구분';
     St8[01]:='Jubun'; St9[01]:='지역';
     St8[02]:='Gcode'; St9[02]:='코드';
     St8[03]:='Gname'; St9[03]:='출판사명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업태';
     St8[07]:='Gjomo'; St9[07]:='종목';
     St8[08]:='Gtels'; St9[08]:='전화번호';
     St8[09]:='Gfaxs'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadds'; St9[11]:='주소';
     St8[12]:='Gbigo'; St9[12]:='비고';
  end else
  if(oSqry=Base10.T1_Sub12)or(oSqry=Base10.T1_Sub22)or(oSqry=Base10.T1_Sub72)or
    (oSqry=Base10.T1_Sub32)or(oSqry=Base10.T1_Sub42)or(oSqry=Base10.T1_Sub52)Then begin
     St0:=02;
     St8[00]:='Gcode'; St9[00]:='코드';
     St8[01]:='Gname'; St9[01]:='구분명';
  end else
  if(oSqry=Base10.T2_Sub11)or(oSqry=Base10.T2_Sub21)or(oSqry=Base10.T2_Sub31)Then begin
     St0:=10;
     St8[00]:='Gubun'; St9[00]:='구분';
     St8[01]:='Bcode'; St9[01]:='도서코드';
     St8[02]:='Bname'; St9[02]:='도서명';
     St8[03]:='Ocode'; St9[03]:='처리';
     St8[04]:='Gjeja'; St9[04]:='저자';
     St8[05]:='Gsqut'; St9[05]:='수량';
     St8[06]:='Gdang'; St9[06]:='단가';
     St8[07]:='Grat1'; St9[07]:='비율';
     St8[08]:='Gssum'; St9[08]:='금액';
     St8[09]:='Gbigo'; St9[09]:='비고';
  end else
  if(oSqry=Base10.T2_Sub41)or(oSqry=Base10.T2_Sub51)Then begin
     St0:=12;
     St8[00]:='Gdate'; St9[00]:='거래일자';
     St8[01]:='Pubun'; St9[01]:='구분';
     St8[02]:='Gcode'; St9[02]:='코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Bcode'; St9[04]:='도서코드';
     St8[05]:='Bname'; St9[05]:='도서명';
     St8[06]:='Ocode'; St9[06]:='처리';
     St8[07]:='Gsqut'; St9[07]:='수량';
     St8[08]:='Gdang'; St9[08]:='단가';
     St8[09]:='Grat1'; St9[09]:='비율';
     St8[10]:='Gssum'; St9[10]:='금액';
     St8[11]:='Gbigo'; St9[11]:='비고';
  end else
  if(oSqry=Base10.T2_Sub91)Then begin
     St0:=10;
     St8[00]:='Gubun'; St9[00]:='구분';
     St8[01]:='Bcode'; St9[01]:='도서코드';
     St8[02]:='Bname'; St9[02]:='도서명';
     St8[03]:='Ocode'; St9[03]:='처리';
     St8[04]:='Gjeja'; St9[04]:='저자';
     St8[05]:='Gsqut'; St9[05]:='수량';
     St8[06]:='Gdang'; St9[06]:='단가';
     St8[07]:='Grat1'; St9[07]:='비율';
     St8[08]:='Gssum'; St9[08]:='금액';
     St8[09]:='Gbigo'; St9[09]:='비고';
  end else
  if(oSqry=Base10.T4_Sub61)Then begin
     St0:=15;
     St8[00]:='Gnumb'; St9[00]:='어음번호';
     St8[01]:='Scode'; St9[01]:='처리코드';
     St8[02]:='Gname'; St9[02]:='발 행 처';
     St8[03]:='Gposa'; St9[03]:='발 행 인';
     St8[04]:='Date1'; St9[04]:='발행일자';
     St8[05]:='Date2'; St9[05]:='받은일자';
     St8[06]:='Date3'; St9[06]:='지급일자';
     St8[07]:='Name1'; St9[07]:='지 급 처';
     St8[08]:='Gbang'; St9[08]:='지급은행';
     St8[09]:='Name2'; St9[09]:='지급지점';
     St8[10]:='Date4'; St9[10]:='만기일자';
     St8[11]:='Gosum'; St9[11]:='할인금액';
     St8[12]:='Grat1'; St9[12]:='할 인 율';
     St8[13]:='Gssum'; St9[13]:='금    액';
     St8[14]:='Gbigo'; St9[14]:='비    고';
  end else
  if(oSqry=Base10.T4_Sub62)Then begin
     St0:=10;
     St8[00]:='Gcode'; St9[00]:='은행코드';
     St8[01]:='Gname'; St9[01]:='은 행 명';
     St8[02]:='Gposa'; St9[02]:='예 금 주';
     St8[03]:='Gnumb'; St9[03]:='계좌번호';
     St8[04]:='Gubun'; St9[04]:='은행구분';
     St8[05]:='Gtels'; St9[05]:='전화번호';
     St8[06]:='Name1'; St9[06]:='고객번호';
     St8[07]:='Name2'; St9[07]:='거 래 점';
     St8[08]:='Gdate'; St9[08]:='초기일자';
     St8[09]:='Class'; St9[09]:='초기금액';
  end else
  if(oSqry=Sobo39.T3_Sub91)Then begin
     St0:=08;
     St8[00]:='Hcode'; St9[00]:='출판사코드';
     St8[01]:='Hname'; St9[01]:='출판사명';
     St8[02]:='Gcode'; St9[02]:='거래처코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Gjeja'; St9[04]:='지역';
     St8[05]:='Gsqut'; St9[05]:='수량';
     St8[06]:='Gqut1'; St9[06]:='덩이';
     St8[07]:='Gqut3'; St9[07]:='박스';
  end;

  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     for I := 0 to St0 - 1 do begin
       cFieldname:=St9[I];
       Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       for I := 0 to St0 - 1 do begin
         cFieldname:=St8[I];
         if TableX.FieldByName(cFieldname).DataType=ftString Then
         Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
         Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, St0], VarVariant);
     TableX.First;
     with Column do begin
       while I <= St0 do begin
         cFieldname:=St8[I-1];
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         XTitle[I] := St9[I-1];
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + St0) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, St0], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
         while I <= St0 do begin
           cFieldname:=St8[I-1];
           XArr[I]   :=TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + St0) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;
     //셀 크기 조정
     XL.Range['A1', CHR(64 + St0) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnX1(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
var I,K,St1: Integer;
 cFieldname: string;
XL, XArr, XTitle: Variant;
begin
  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     with Column do begin
       for I := 0 to Columns.Count - 1 do begin
         Tong10.F1Book1.TextRC[1,I+1]:=Columns.Items[I].Title.Caption;
       end;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       with Column do begin
         for I := 0 to Columns.Count - 1 do begin
           cFieldname:=Column.Fields[I].FieldName;
           if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
         end;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, Column.Columns.Count], VarVariant);
     TableX.First;
     with Column do begin
       while I <= Columns.Count do begin
         XTitle[I] := Columns.Items[I-1].Title.Caption;
         cFieldname:=Column.Fields[I-1].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + Column.Columns.Count) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, Column.Columns.Count], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
         while I <= Columns.Count do begin
           cFieldname:=Column.Fields[I-1].FieldName;
           XArr[I]   :=TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + Column.Columns.Count) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;
     //셀 크기 조정
     XL.Range['A1', CHR(64 + Column.Columns.Count) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnX2(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
var I,K,St1: Integer;
 cFieldname: string;
XL, XArr, XTitle: Variant;
begin
  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     with Column do begin
         Tong10.F1Book1.TextRC[1,  1]:='코드';
       for I := 1 to Columns.Count - 0 do begin
         Tong10.F1Book1.TextRC[1,I+1]:=Columns.Items[I-1].Title.Caption;
       end;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       with Column do begin
         Tong10.F1Book1.TextRC[St1,1]:=TableX.FieldByName('Gcode').AsString;
         for I := 1 to Columns.Count - 0 do begin
           cFieldname:=Column.Fields[I-1].FieldName;
           if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
         end;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, Column.Columns.Count+1], VarVariant);
     TableX.First;
     with Column do begin
         XTitle[I] := '코드';
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
       while I <= Columns.Count do begin
         XTitle[I+1] := Columns.Items[I-1].Title.Caption;
         cFieldname:=Column.Fields[I-1].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I+1].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + Column.Columns.Count+1) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, Column.Columns.Count+1], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
           XArr[I] := '''' + TableX.FieldByName('Gcode').AsString;
         while I <= Columns.Count do begin
           cFieldname:=Column.Fields[I-1].FieldName;
           XArr[I+1] :=TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + Column.Columns.Count+1) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;
     //셀 크기 조정
     XL.Range['A1', CHR(64 + Column.Columns.Count+1) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnX3(TableX: TClientDataSet; Column: TDBGrid; PBar: TProgressBar);
var I,K,St1: Integer;
 cFieldname: string;
XL, XArr, XTitle: Variant;
begin
  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     for I := 0 to TableX.FieldCount - 1 do begin
       cFieldname:=TableX.Fields[I].FieldName;
       Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       for I := 0 to TableX.FieldCount - 1 do begin
         cFieldname:=TableX.Fields[I].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then
         Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
         Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, TableX.FieldCount], VarVariant);
     TableX.First;
     with Column do begin
       while I <= TableX.FieldCount do begin
         XTitle[I] := TableX.Fields[I-1].FieldName;
         cFieldname:= TableX.Fields[I-1].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + TableX.FieldCount) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, TableX.FieldCount], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
         while I <= TableX.FieldCount do begin
           cFieldname:=TableX.Fields[I-1].FieldName;
           XArr[I]   :=TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + Column.Columns.Count) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;
     //셀 크기 조정
     XL.Range['A1', CHR(64 + Column.Columns.Count) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnX9(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
var I,K,St1: Integer;
 cFieldname: string;
XL, XArr, XTitle: Variant;
begin
  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     with Column do begin
       for I := 0 to Columns.Count - 1 do begin
         Tong10.F1Book1.TextRC[1,I+1]:=Columns.Items[I].Title.Caption;
       end;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       with Column do begin
         for I := 0 to Columns.Count - 1 do begin
           cFieldname:=Column.Fields[I].FieldName;
           if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
         end;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, Column.Columns.Count], VarVariant);
     TableX.First;
     with Column do begin
       while I <= Columns.Count do begin
         XTitle[I] := Columns.Items[I-1].Title.Caption;
         cFieldname:=Column.Fields[I-1].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + Column.Columns.Count) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, Column.Columns.Count], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
         while I <= Columns.Count do begin
           cFieldname:=Column.Fields[I-1].FieldName;
           XArr[I]   :=TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + Column.Columns.Count) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;
     //셀 크기 조정
     XL.Range['A1', CHR(64 + Column.Columns.Count) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnY0(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
var I,K,St1,St0: Integer;
  St8:array [0..21] of String;
  St9:array [0..21] of String;
 cFieldname: string;
XL, XArr, XTitle: Variant;
begin
  if(oSqry=Base10.T1_Sub11)or(oSqry=Base10.T1_Sub21)or(oSqry=Base10.T1_Sub51)Then begin
     St0:=20;
     St8[00]:='Sname'; St9[00]:='구분';
     St8[01]:='Jubun'; St9[01]:='지역';
     St8[02]:='Gcode'; St9[02]:='코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업태';
     St8[07]:='Gjomo'; St9[07]:='종목';
     St8[08]:='Gtels'; St9[08]:='전화번호';
     St8[09]:='Gfaxs'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadds'; St9[11]:='주소';
     St8[12]:='Grat1'; St9[12]:='위탁';
     St8[13]:='Grat2'; St9[13]:='현매';
     St8[14]:='Grat3'; St9[14]:='매절';
     St8[15]:='Grat4'; St9[15]:='납품';
     St8[16]:='Grat5'; St9[16]:='특별';
     St8[17]:='Grat6'; St9[17]:='기타';
     St8[18]:='Gqut1'; St9[18]:='신간';
     St8[19]:='Gbigo'; St9[19]:='비고';
  end else
  if(oSqry=Base10.T1_Sub31)Then begin
     St0:=17;
     St8[00]:='Sname'; St9[00]:='구분';
     St8[01]:='Date1'; St9[01]:='등록일자';
     St8[02]:='Gcode'; St9[02]:='저자코드';
     St8[03]:='Gposa'; St9[03]:='저 자 명';
     St8[04]:='Gname'; St9[04]:='직 장 명';
     St8[05]:='Gjice'; St9[05]:='직    책';
     St8[06]:='Gscho'; St9[06]:='출신학교';
     St8[07]:='Gnumb'; St9[07]:='사업자번호';
     St8[08]:='Gnum1'; St9[08]:='주민등록';
     St8[09]:='Gnum2'; St9[09]:='계좌번호';
     St8[10]:='Gtels'; St9[10]:='전화번호';
     St8[11]:='Gfaxs'; St9[11]:='팩스번호';
     St8[12]:='Gpost'; St9[12]:='우편번호';
     St8[13]:='Gadds'; St9[13]:='집 주 소';
     St8[14]:='Opost'; St9[14]:='우편번호';
     St8[15]:='Oadds'; St9[15]:='직장주소';
     St8[16]:='Gbigo'; St9[16]:='비고';
  end else
  if(oSqry=Base10.T1_Sub41)Then begin
     St0:=18;
     St8[00]:='Sname'; St9[00]:='도서분류';
     St8[01]:='Jubun'; St9[01]:='도서처리';
     St8[02]:='Gcode'; St9[02]:='도서코드';
     St8[03]:='Gname'; St9[03]:='도서명';
     St8[04]:='Gjeja'; St9[04]:='저자명';
     St8[05]:='Gdabi'; St9[05]:='단위';
     St8[06]:='Gdang'; St9[06]:='단가';
     St8[07]:='Gisbn'; St9[07]:='ISBN번호';
     St8[08]:='Gbjil'; St9[08]:='도 서 질';
     St8[09]:='Grat1'; St9[09]:='위탁';
     St8[10]:='Grat2'; St9[10]:='현매';
     St8[11]:='Grat3'; St9[11]:='매절';
     St8[12]:='Grat4'; St9[12]:='납품';
     St8[13]:='Grat5'; St9[13]:='특별';
     St8[14]:='Grat6'; St9[14]:='기타';
     St8[15]:='Gbigo'; St9[15]:='비고';
     St8[16]:='Gsqut'; St9[16]:='재고';
     St8[17]:='Gssum'; St9[17]:='재고금액';
  end else
  if(oSqry=Base10.T1_Sub71)Then begin
     St0:=13;
     St8[00]:='Sname'; St9[00]:='구분';
     St8[01]:='Jubun'; St9[01]:='지역';
     St8[02]:='Gcode'; St9[02]:='코드';
     St8[03]:='Gname'; St9[03]:='출판사명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업태';
     St8[07]:='Gjomo'; St9[07]:='종목';
     St8[08]:='Gtels'; St9[08]:='전화번호';
     St8[09]:='Gfaxs'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadds'; St9[11]:='주소';
     St8[12]:='Gbigo'; St9[12]:='비고';
  end else
  if(oSqry=Base10.T1_Sub12)or(oSqry=Base10.T1_Sub22)or(oSqry=Base10.T1_Sub72)or
    (oSqry=Base10.T1_Sub32)or(oSqry=Base10.T1_Sub42)or(oSqry=Base10.T1_Sub52)Then begin
     St0:=02;
     St8[00]:='Gcode'; St9[00]:='코드';
     St8[01]:='Gname'; St9[01]:='구분명';
  end else
  if(oSqry=Base10.T2_Sub11)or(oSqry=Base10.T2_Sub21)or(oSqry=Base10.T2_Sub31)Then begin
     St0:=10;
     St8[00]:='Gubun'; St9[00]:='구분';
     St8[01]:='Bcode'; St9[01]:='도서코드';
     St8[02]:='Bname'; St9[02]:='도서명';
     St8[03]:='Ocode'; St9[03]:='처리';
     St8[04]:='Gjeja'; St9[04]:='저자';
     St8[05]:='Gsqut'; St9[05]:='수량';
     St8[06]:='Gdang'; St9[06]:='단가';
     St8[07]:='Grat1'; St9[07]:='비율';
     St8[08]:='Gssum'; St9[08]:='금액';
     St8[09]:='Gbigo'; St9[09]:='비고';
  end else
  if(oSqry=Base10.T2_Sub41)or(oSqry=Base10.T2_Sub51)Then begin
     St0:=12;
     St8[00]:='Gdate'; St9[00]:='거래일자';
     St8[01]:='Pubun'; St9[01]:='구분';
     St8[02]:='Gcode'; St9[02]:='코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Bcode'; St9[04]:='도서코드';
     St8[05]:='Bname'; St9[05]:='도서명';
     St8[06]:='Ocode'; St9[06]:='처리';
     St8[07]:='Gsqut'; St9[07]:='수량';
     St8[08]:='Gdang'; St9[08]:='단가';
     St8[09]:='Grat1'; St9[09]:='비율';
     St8[10]:='Gssum'; St9[10]:='금액';
     St8[11]:='Gbigo'; St9[11]:='비고';
  end else
  if(oSqry=Base10.T2_Sub91)Then begin
     St0:=10;
     St8[00]:='Gubun'; St9[00]:='구분';
     St8[01]:='Bcode'; St9[01]:='도서코드';
     St8[02]:='Bname'; St9[02]:='도서명';
     St8[03]:='Ocode'; St9[03]:='처리';
     St8[04]:='Gjeja'; St9[04]:='저자';
     St8[05]:='Gsqut'; St9[05]:='수량';
     St8[06]:='Gdang'; St9[06]:='단가';
     St8[07]:='Grat1'; St9[07]:='비율';
     St8[08]:='Gssum'; St9[08]:='금액';
     St8[09]:='Gbigo'; St9[09]:='비고';
  end else
  if(oSqry=Base10.T4_Sub61)Then begin
     St0:=15;
     St8[00]:='Gnumb'; St9[00]:='어음번호';
     St8[01]:='Scode'; St9[01]:='처리코드';
     St8[02]:='Gname'; St9[02]:='발 행 처';
     St8[03]:='Gposa'; St9[03]:='발 행 인';
     St8[04]:='Date1'; St9[04]:='발행일자';
     St8[05]:='Date2'; St9[05]:='받은일자';
     St8[06]:='Date3'; St9[06]:='지급일자';
     St8[07]:='Name1'; St9[07]:='지 급 처';
     St8[08]:='Gbang'; St9[08]:='지급은행';
     St8[09]:='Name2'; St9[09]:='지급지점';
     St8[10]:='Date4'; St9[10]:='만기일자';
     St8[11]:='Gosum'; St9[11]:='할인금액';
     St8[12]:='Grat1'; St9[12]:='할 인 율';
     St8[13]:='Gssum'; St9[13]:='금    액';
     St8[14]:='Gbigo'; St9[14]:='비    고';
  end else
  if(oSqry=Base10.T4_Sub62)Then begin
     St0:=10;
     St8[00]:='Gcode'; St9[00]:='은행코드';
     St8[01]:='Gname'; St9[01]:='은 행 명';
     St8[02]:='Gposa'; St9[02]:='예 금 주';
     St8[03]:='Gnumb'; St9[03]:='계좌번호';
     St8[04]:='Gubun'; St9[04]:='은행구분';
     St8[05]:='Gtels'; St9[05]:='전화번호';
     St8[06]:='Name1'; St9[06]:='고객번호';
     St8[07]:='Name2'; St9[07]:='거 래 점';
     St8[08]:='Gdate'; St9[08]:='초기일자';
     St8[09]:='Class'; St9[09]:='초기금액';
  end else
  if(oSqry=Sobo39.T3_Sub91)Then begin
     St0:=08;
     St8[00]:='Hcode'; St9[00]:='출판사코드';
     St8[01]:='Hname'; St9[01]:='출판사명';
     St8[02]:='Gcode'; St9[02]:='거래처코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Gjeja'; St9[04]:='지역';
     St8[05]:='Gsqut'; St9[05]:='수량';
     St8[06]:='Gqut1'; St9[06]:='덩이';
     St8[07]:='Gqut3'; St9[07]:='박스';
  end;

  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     for I := 0 to St0 - 1 do begin
       cFieldname:=St9[I];
       Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       for I := 0 to St0 - 1 do begin
         cFieldname:=St8[I];
         if TableX.FieldByName(cFieldname).DataType=ftString Then
         Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
         Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, St0], VarVariant);
     TableX.First;
     with Column do begin
       while I <= St0 do begin
         cFieldname:=St8[I-1];
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         XTitle[I] := St9[I-1];
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + St0) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, St0], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
         while I <= St0 do begin
           cFieldname:=St8[I-1];
           XArr[I]   :=TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + St0) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;
     //셀 크기 조정
     XL.Range['A1', CHR(64 + St0) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnY1(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
var I,J,K,St1 : Integer;
  cFieldname: string;
  XL, XArr, XTitle: Variant;
  DBGridEh: TDBGridEH;
  FCol: Integer;
begin
  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     with Column do begin
       for I := 0 to Columns.Count - 1 do begin
         Tong10.F1Book1.TextRC[1,I+1]:=Columns.Items[I].Title.Caption;
       end;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       with Column do begin
         for I := 0 to Columns.Count - 1 do begin
           cFieldname:=Column.Fields[I].FieldName;
           if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
         end;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, Column.Columns.Count], VarVariant);
     TableX.First;
     with Column do begin
       while I <= Columns.Count do begin
         XTitle[I] := Columns.Items[I-1].Title.Caption;
         cFieldname:=Column.Fields[I-1].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + Column.Columns.Count) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, Column.Columns.Count], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
         while I <= Columns.Count do begin
           //if DBGridEh.Columns[I].Visible then
           cFieldname:=Column.Fields[I-1].FieldName;
           XArr[I] := TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + Column.Columns.Count) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;

     //Footer Start
     DBGridEh := Column;
     FCol := 0;
     if DBGridEh.FooterRowCount = 1 then
     begin
       for I := 0 to DBGridEh.Columns.Count - 1 do
       begin
         //if DBGridEh.Columns[I].Visible then
         begin
           XArr[I+1] := DBGridEh.GetFooterValue(0,DBGridEh.Columns[I]);//DBGridEh.Columns[i].Footer.Value;
         end;
       end;

       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + DBGridEh.Columns.Count) + IntToStr(K+1)].Value := XArr;
       Inc(K);
     end;
     //Footer

     //셀 크기 조정
     XL.Range['A1', CHR(64 + Column.Columns.Count) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnY2(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
var I,K,St1: Integer;
 cFieldname: string;
XL, XArr, XTitle: Variant;
  DBGridEh: TDBGridEH;
  FCol: Integer;
begin
  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     with Column do begin
         Tong10.F1Book1.TextRC[1,  1]:='코드';
       for I := 1 to Columns.Count - 0 do begin
         Tong10.F1Book1.TextRC[1,I+1]:=Columns.Items[I-1].Title.Caption;
       end;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       with Column do begin
         Tong10.F1Book1.TextRC[St1,1]:=TableX.FieldByName('Gcode').AsString;
         for I := 1 to Columns.Count - 0 do begin
           cFieldname:=Column.Fields[I-1].FieldName;
           if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
         end;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, Column.Columns.Count+1], VarVariant);
     TableX.First;
     with Column do begin
         XTitle[I] := '코드';
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
       while I <= Columns.Count do begin
         XTitle[I+1] := Columns.Items[I-1].Title.Caption;
         cFieldname:=Column.Fields[I-1].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I+1].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + Column.Columns.Count+1) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, Column.Columns.Count+1], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
           XArr[I] := '''' + TableX.FieldByName('Gcode').AsString;
         while I <= Columns.Count do begin
           cFieldname:=Column.Fields[I-1].FieldName;
           XArr[I+1] := TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + Column.Columns.Count+1) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;

     //Footer Start
     DBGridEh := Column;
     FCol := 0;
     if DBGridEh.FooterRowCount = 1 then
     begin
       for I := 0 to DBGridEh.Columns.Count - 1 do
       begin
         cFieldname := DBGridEh.Fields[I].FieldName;
         if DBGridEh.Columns[I].Field.FieldName = cFieldname then
         begin
           if DBGridEh.Columns[I].Visible then
           XArr[I+2] := DBGridEh.GetFooterValue(0,DBGridEh.Columns[I]);//DBGridEh.Columns[i].Footer.Value;
         end;    
         //if DBGridEh.Columns[I].Visible then
         //begin
         //  XArr[I+1] := DBGridEh.GetFooterValue(0,DBGridEh.Columns[I]);//DBGridEh.Columns[i].Footer.Value;
         //end;
       end;

       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + DBGridEh.Columns.Count) + IntToStr(K+1)].Value := XArr;
       Inc(K);
     end;
     //Footer

     //셀 크기 조정
     XL.Range['A1', CHR(64 + Column.Columns.Count+1) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.ColumnY3(TableX: TClientDataSet; Column: TDBGridEH; PBar: TProgressBar);
var I,K,St1: Integer;
 cFieldname: string;
XL, XArr, XTitle: Variant;
begin
  if nList<>'3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;
     Application.CreateForm(TTong10, Tong10);
     St1:=1;
     TableX.First;
     for I := 0 to TableX.FieldCount - 1 do begin
       cFieldname:=TableX.Fields[I].FieldName;
       Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
     end;
     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       St1:=St1+1;
       for I := 0 to TableX.FieldCount - 1 do begin
         cFieldname:=TableX.Fields[I].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then
         Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
         Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat;
       end;
       TableX.Next;
     end;
     PBar.Position:=0;
     Tong10.ShowModal;
     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;

  if nList='3' then
  if TableX.Active=True Then begin
     Bmark:=TableX.GetBookmark; TableX.DisableControls;

     try
       //엑셀을 실행
       XL := CreateOLEObject('Excel.Application');
     except
       MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
       Exit;
     end;

     XL.WorkBooks.Add; //새로운 페이지 생성
     XL.Visible := True;
     I := 1;
     K := 1;

     //타이틀 처리변수
     XTitle := VarArrayCreate([1, TableX.FieldCount], VarVariant);
     TableX.First;
     with Column do begin
       while I <= TableX.FieldCount do begin
         XTitle[I] := TableX.Fields[I-1].FieldName;
         cFieldname:= TableX.Fields[I-1].FieldName;
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         Inc(I);
       end;
     end;
     //타이틀처리
     XL.Range['A1', CHR(64 + TableX.FieldCount) + '1'].Value := XTitle;

     //데이타 처리변수
     XArr := VarArrayCreate([1, TableX.FieldCount], VarVariant);

     PBar.Max:=TableX.RecordCount;
     While TableX.EOF=False do begin
       PBar.Position:=PBar.Position+1;
       I := 1;
       with Column do begin
         while I <= TableX.FieldCount do begin
           cFieldname:=TableX.Fields[I-1].FieldName;
           XArr[I]   :=TableX.FieldByName(cFieldname).Value;
           Inc(I);
         end;
       end;
       //셀에 값을 넣는다.
       XL.Range['A' + IntToStr(K+1), CHR(64 + Column.Columns.Count) + IntToStr(K+1)].Value := XArr;
       TableX.Next;
       Inc(K);
     end;
     //셀 크기 조정
     XL.Range['A1', CHR(64 + Column.Columns.Count) + IntToStr(K)].Select;
     XL.Selection.Columns.AutoFit;
     XL.Range['A1', 'A1'].Select;
     PBar.Position:=0;

     TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
  end;
end;

procedure TBase10.T1_Sub11AfterScroll(DataSet: TDataSet);
begin
  Sobo11.Button023Click(Self);
end;

procedure TBase10.T1_Sub12AfterScroll(DataSet: TDataSet);
begin
  Sobo11.Button024Click(Self);
end;

procedure TBase10.T1_Sub21AfterScroll(DataSet: TDataSet);
begin
  Sobo12.Button023Click(Self);
end;

procedure TBase10.T1_Sub22AfterScroll(DataSet: TDataSet);
begin
  Sobo12.Button024Click(Self);
end;

procedure TBase10.T1_Sub31AfterScroll(DataSet: TDataSet);
begin
  Sobo13.Button023Click(Self);
end;

procedure TBase10.T1_Sub32AfterScroll(DataSet: TDataSet);
begin
  Sobo13.Button024Click(Self);
end;

procedure TBase10.T1_Sub41AfterScroll(DataSet: TDataSet);
begin
  Sobo14.Button023Click(Self);
end;

procedure TBase10.T1_Sub42AfterScroll(DataSet: TDataSet);
begin
  Sobo14.Button024Click(Self);
end;

procedure TBase10.T1_Sub51AfterScroll(DataSet: TDataSet);
begin
  Sobo15.Button023Click(Self);
end;

procedure TBase10.T1_Sub52AfterScroll(DataSet: TDataSet);
begin
  Sobo15.Button024Click(Self);
end;

procedure TBase10.T1_Sub71AfterScroll(DataSet: TDataSet);
begin
  Sobo17.Button023Click(Self);
end;

procedure TBase10.T1_Sub72AfterScroll(DataSet: TDataSet);
begin
  Sobo17.Button024Click(Self);
end;

procedure TBase10.T1_Sub81AfterScroll(DataSet: TDataSet);
begin
  Sobo18.Button023Click(Self);
end;

procedure TBase10.T1_Sub82AfterScroll(DataSet: TDataSet);
begin
  Sobo18.Button024Click(Self);
end;

procedure TBase10.T4_Sub61AfterScroll(DataSet: TDataSet);
begin
  Sobo46.Button023Click(Self);
end;

procedure TBase10.T4_Sub62AfterScroll(DataSet: TDataSet);
begin
  Sobo46.Button024Click(Self);
end;

//--특별관리--//
procedure TBase10.T1_Sub61AfterCancel(DataSet: TDataSet);
begin
  T1_Sub61AfterScroll(T1_Sub61);
end;

procedure TBase10.T1_Sub61AfterScroll(DataSet: TDataSet);
begin
  Bcode:= T1_Sub61.FieldByName('Bcode').AsString;
  Gssum:= T1_Sub61.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T1_Sub61AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T1_Sub61AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM G6_Ggeo WHERE ID=@ID ';
    translate(Sqlen, '@ID',    T1_Sub61ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T1_Sub61.Delete;

  end; end;

end;

procedure TBase10.T1_Sub61BeforePost(DataSet: TDataSet);
begin

  if(T1_Sub61.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO G6_Ggeo '+
    '(Hcode, Gcode, Bcode, Grat1, Grat2, Grat3, '+
    ' Grat4, Grat5, Grat6, Grat7, Grat8, Grat9, Gssum) VALUES '+
    '(''@Hcode'',''@Gcode'',''@Bcode'',  @Grat1,  @Grat2,  @Grat3, '+
    '   @Grat4  ,  @Grat5  ,  @Grat6  ,  @Grat7,  @Grat8,  @Grat9,  @Gssum  )';

    Translate(Sqlen, '@Hcode', T1_Sub61Hcode.AsString);
    Translate(Sqlen, '@Gcode', T1_Sub61Gcode.AsString);
    Translate(Sqlen, '@Bcode', T1_Sub61Bcode.AsString);
    TransAuto(Sqlen, '@Grat1', T1_Sub61Grat1.AsString);
    TransAuto(Sqlen, '@Grat2', T1_Sub61Grat2.AsString);
    TransAuto(Sqlen, '@Grat3', T1_Sub61Grat3.AsString);
    TransAuto(Sqlen, '@Grat4', T1_Sub61Grat4.AsString);
    TransAuto(Sqlen, '@Grat5', T1_Sub61Grat5.AsString);
    TransAuto(Sqlen, '@Grat6', T1_Sub61Grat6.AsString);
    TransAuto(Sqlen, '@Grat7', T1_Sub61Grat7.AsString);
    TransAuto(Sqlen, '@Grat8', T1_Sub61Grat8.AsString);
    TransAuto(Sqlen, '@Grat9', T1_Sub61Grat9.AsString);
    TransAuto(Sqlen, '@Gssum', T1_Sub61Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'G6_GGEO_ID_GEN');

  end else begin

    Sqlen := 'UPDATE G6_Ggeo SET '+
    'Gcode=''@Gcode'',Bcode=''@Bcode'',Grat1= @Grat1 ,Grat2= @Grat2 ,Grat3= @Grat3 ,Grat4= @Grat4 ,'+
    'Grat5=  @Grat5  ,Grat6=  @Grat6  ,Grat7= @Grat7 ,Grat8= @Grat8 ,Grat9= @Grat9 ,Gssum= @Gssum  '+
    'WHERE ID=@ID and Hcode=''@Hcode''';

    Translate(Sqlen, '@Hcode', T1_Sub61Hcode.AsString);
    Translate(Sqlen, '@Gcode', T1_Sub61Gcode.AsString);
    Translate(Sqlen, '@Bcode', T1_Sub61Bcode.AsString);
    TransAuto(Sqlen, '@Grat1', T1_Sub61Grat1.AsString);
    TransAuto(Sqlen, '@Grat2', T1_Sub61Grat2.AsString);
    TransAuto(Sqlen, '@Grat3', T1_Sub61Grat3.AsString);
    TransAuto(Sqlen, '@Grat4', T1_Sub61Grat4.AsString);
    TransAuto(Sqlen, '@Grat5', T1_Sub61Grat5.AsString);
    TransAuto(Sqlen, '@Grat6', T1_Sub61Grat6.AsString);
    TransAuto(Sqlen, '@Grat7', T1_Sub61Grat7.AsString);
    TransAuto(Sqlen, '@Grat8', T1_Sub61Grat8.AsString);
    TransAuto(Sqlen, '@Grat9', T1_Sub61Grat9.AsString);
    TransAuto(Sqlen, '@Gssum', T1_Sub61Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T1_Sub61ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T1_Sub61BeforeClose(DataSet: TDataSet);
begin
  With T1_Sub61 do
  if(State in dsEditModes)Then Post;
end;

//--특별관리--//
procedure TBase10.T1_Sub62AfterCancel(DataSet: TDataSet);
begin
  T1_Sub62AfterScroll(T1_Sub62);
end;

procedure TBase10.T1_Sub62AfterScroll(DataSet: TDataSet);
begin
  Gcode:= T1_Sub62.FieldByName('Gcode').AsString;
  Gssum:= T1_Sub62.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T1_Sub62AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T1_Sub62AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM G6_Ggeo WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T1_Sub62ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T1_Sub62.Delete;

  end; end;

end;

procedure TBase10.T1_Sub62BeforePost(DataSet: TDataSet);
begin

  if(T1_Sub62.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO G6_Ggeo '+
    '(Hcode, Gcode, Bcode, Grat1, Grat2, Grat3, '+
    ' Grat4, Grat5, Grat6, Grat7, Grat8, Grat9, Gssum) VALUES '+
    '(''@Hcode'',''@Gcode'',''@Bcode'',  @Grat1,  @Grat2,  @Grat3, '+
    '   @Grat4  ,  @Grat5  ,  @Grat6  ,  @Grat7,  @Grat8,  @Grat9,  @Gssum  )';

    Translate(Sqlen, '@Hcode', T1_Sub62Hcode.AsString);
    Translate(Sqlen, '@Gcode', T1_Sub62Gcode.AsString);
    Translate(Sqlen, '@Bcode', T1_Sub62Bcode.AsString);
    TransAuto(Sqlen, '@Grat1', T1_Sub62Grat1.AsString);
    TransAuto(Sqlen, '@Grat2', T1_Sub62Grat2.AsString);
    TransAuto(Sqlen, '@Grat3', T1_Sub62Grat3.AsString);
    TransAuto(Sqlen, '@Grat4', T1_Sub62Grat4.AsString);
    TransAuto(Sqlen, '@Grat5', T1_Sub62Grat5.AsString);
    TransAuto(Sqlen, '@Grat6', T1_Sub62Grat6.AsString);
    TransAuto(Sqlen, '@Grat7', T1_Sub62Grat7.AsString);
    TransAuto(Sqlen, '@Grat8', T1_Sub62Grat8.AsString);
    TransAuto(Sqlen, '@Grat9', T1_Sub62Grat9.AsString);
    TransAuto(Sqlen, '@Gssum', T1_Sub62Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'G6_GGEO_ID_GEN');

  end else begin

    Sqlen := 'UPDATE G6_Ggeo SET '+
    'Gcode=''@Gcode'',Bcode=''@Bcode'',Grat1= @Grat1 ,Grat2= @Grat2 ,Grat3= @Grat3 ,Grat4= @Grat4 ,'+
    'Grat5=  @Grat5  ,Grat6=  @Grat6  ,Grat7= @Grat7 ,Grat8= @Grat8 ,Grat9= @Grat9 ,Gssum= @Gssum  '+
    'WHERE ID=@ID and Hcode=''@Hcode'' ';

    Translate(Sqlen, '@Hcode', T1_Sub62Hcode.AsString);
    Translate(Sqlen, '@Gcode', T1_Sub62Gcode.AsString);
    Translate(Sqlen, '@Bcode', T1_Sub62Bcode.AsString);
    TransAuto(Sqlen, '@Grat1', T1_Sub62Grat1.AsString);
    TransAuto(Sqlen, '@Grat2', T1_Sub62Grat2.AsString);
    TransAuto(Sqlen, '@Grat3', T1_Sub62Grat3.AsString);
    TransAuto(Sqlen, '@Grat4', T1_Sub62Grat4.AsString);
    TransAuto(Sqlen, '@Grat5', T1_Sub62Grat5.AsString);
    TransAuto(Sqlen, '@Grat6', T1_Sub62Grat6.AsString);
    TransAuto(Sqlen, '@Grat7', T1_Sub62Grat7.AsString);
    TransAuto(Sqlen, '@Grat8', T1_Sub62Grat8.AsString);
    TransAuto(Sqlen, '@Grat9', T1_Sub62Grat9.AsString);
    TransAuto(Sqlen, '@Gssum', T1_Sub62Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T1_Sub62ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T1_Sub62BeforeClose(DataSet: TDataSet);
begin
  With T1_Sub62 do
  if(State in dsEditModes)Then Post;
end;

//--거래명세서--//
procedure TBase10.T2_Sub11AfterCancel(DataSet: TDataSet);
begin
  T2_Sub11AfterScroll(T2_Sub11);
end;

procedure TBase10.T2_Sub11AfterScroll(DataSet: TDataSet);
begin
  Ocode:= T2_Sub11.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub11.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub11.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub11.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T2_Sub11AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub11AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub11ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub11ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Translate(Sqlen, '@Scode', '1');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end;

    T2_Sub11.Delete;

  end; end;

end;

procedure TBase10.T2_Sub11BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub11.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'', now())';

    Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub11Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub11Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub11Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub11Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub11Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub11Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub11Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub11Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub11Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub11Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub11Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub11Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub11Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub11Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub11Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub11Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub11Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM');
  //Base10.Update_Icode(nSqry,'S1_SSUB_ID_NUM');

    //--//
  { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

      Sqlen := 'INSERT INTO Sg_Csum '+
      '(Gdate, Scode, Gcode, Hcode, Gbigo, Gbsum) VALUES '+
      '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Gbigo'',  @Gbsum  )';

      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Translate(Sqlen, '@Scode', 'A');
      Translate(Sqlen, '@Gcode', T2_Sub11Bcode.AsString);
      Translate(Sqlen, '@Hcode', T2_Sub11Hcode.AsString);
      Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString   );
      TransAuto(Sqlen, '@Gbsum', T2_Sub11Gsqut.AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end; }

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'',Ocode=''@Ocode'', '+
    'Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'',Pubun=''@Pubun'', ';
    Sqlen :=
    'Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Grat1=  @Grat1  , '+
    'Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  ,Yesno=''@Yesno'', '+
    'Gjisa=''@Gjisa'' WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub11Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub11Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub11Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub11Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub11Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub11Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub11Jubun.AsString);
    Translate(Sqlon, '@Pubun', T2_Sub11Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub11Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub11Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub11Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub11Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub11Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub11Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub11Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub11Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub11Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub11ID.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    //--//
  { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

      Sqlen := 'UPDATE Sg_Csum SET '+
      'Gdate=''@Gdate'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
      'Gbsum=  @Gbsum  WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';

      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Translate(Sqlen, '@Scode', 'A');
      Translate(Sqlen, '@Gcode', T2_Sub11Bcode.AsString);
      Translate(Sqlen, '@Hcode', T2_Sub11Hcode.AsString);
      Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString   );
      TransAuto(Sqlen, '@Gbsum', T2_Sub11Gsqut.AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end; }

  end;

end;

procedure TBase10.T2_Sub11BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub11 do
  if(State in dsEditModes)Then Post;
end;

//--입고명세서--//
procedure TBase10.T2_Sub21AfterCancel(DataSet: TDataSet);
begin
  T2_Sub21AfterScroll(T2_Sub21);
end;

procedure TBase10.T2_Sub21AfterScroll(DataSet: TDataSet);
begin
  Ocode:= T2_Sub21.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub21.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub21.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub21.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T2_Sub21AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub21AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub21ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub21ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
      Translate(Sqlen, '@Scode', '2');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T2_Sub21.Delete;

  end; end;

end;

procedure TBase10.T2_Sub21BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub21.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'', now())';

    Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub21Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub21Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub21Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub21Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub21Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub21Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub21Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub21Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub21Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub21Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub21Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub21Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub21Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub21Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub21Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub21Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub21Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM');
  //Base10.Update_Icode(nSqry,'S1_SSUB_ID_NUM');

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'',Ocode=''@Ocode'', '+
    'Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'',Pubun=''@Pubun'', ';
    Sqlen :=
    'Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Grat1=  @Grat1  , '+
    'Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  ,Yesno=''@Yesno'', '+
    'Gjisa=''@Gjisa'' WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub21Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub21Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub21Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub21Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub21Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub21Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub21Jubun.AsString);
    Translate(Sqlon, '@Pubun', T2_Sub21Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub21Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub21Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub21Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub21Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub21Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub21Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub21Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub21Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub21Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub21ID.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T2_Sub21BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub21 do
  if(State in dsEditModes)Then Post;
end;

//--기타명세서--//
procedure TBase10.T2_Sub31AfterCancel(DataSet: TDataSet);
begin
  T2_Sub31AfterScroll(T2_Sub31);
end;

procedure TBase10.T2_Sub31AfterScroll(DataSet: TDataSet);
begin
  Ocode:= T2_Sub31.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub31.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub31.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub31.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T2_Sub31AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub31AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub31ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub31Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub31ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub31Gdate.AsString);
      if T2_Sub31Scode.AsString='Z' then
      Translate(Sqlen, '@Scode', '3') else
      Translate(Sqlen, '@Scode', '1');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T2_Sub31.Delete;

  end; end;

end;

procedure TBase10.T2_Sub31BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub31.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'', now())';

    Translate(Sqlen, '@Gdate', T2_Sub31Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub31Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub31Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub31Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub31Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub31Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub31Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub31Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub31Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub31Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub31Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub31Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub31Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub31Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub31Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub31Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub31Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub31Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM');
  //Base10.Update_Icode(nSqry,'S1_SSUB_ID_NUM');

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'',Ocode=''@Ocode'', '+
    'Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'',Pubun=''@Pubun'', ';
    Sqlen :=
    'Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Grat1=  @Grat1  , '+
    'Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  ,Yesno=''@Yesno'', '+
    'Gjisa=''@Gjisa'' WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub31Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub31Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub31Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub31Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub31Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub31Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub31Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub31Jubun.AsString);
    Translate(Sqlon, '@Pubun', T2_Sub31Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub31Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub31Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub31Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub31Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub31Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub31Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub31Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub31Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub31Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub31ID.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T2_Sub31BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub31 do
  if(State in dsEditModes)Then Post;
end;

//--입고(반품명세서)--//
procedure TBase10.T2_Sub41AfterCancel(DataSet: TDataSet);
begin
  T2_Sub41AfterScroll(T2_Sub41);
end;

procedure TBase10.T2_Sub41AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T2_Sub41.FieldByName('Gdate').AsString;
  Ocode:= T2_Sub41.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub41.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub41.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub41.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T2_Sub41AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub41AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub41ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub41Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub41ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub41Gdate.AsString);
      Translate(Sqlen, '@Scode', '2');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T2_Sub41.Delete;

  end; end;

end;

procedure TBase10.T2_Sub41BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub41.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'', now())';

    Translate(Sqlen, '@Gdate', T2_Sub41Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub41Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub41Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub41Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub41Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub41Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub41Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub41Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub41Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub41Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub41Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub41Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub41Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub41Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub41Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub41Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub41Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub41Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM');
  //Base10.Update_Icode(nSqry,'S1_SSUB_ID_NUM');

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Ocode=''@Ocode'',Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'', ';
    Sqlen :=
    'Pubun=''@Pubun'',Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  , '+
    'Grat1=  @Grat1  ,Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  , '+
    'Yesno=''@Yesno'',Gjisa=''@Gjisa'',Time2=  now() '+
    'WHERE ID=@ID and Gdate=''@Sdate''';

    Translate(Sqlon, '@Gdate', T2_Sub41Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub41Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub41Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub41Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub41Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub41Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub41Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub41Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub41Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub41Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub41Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub41Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub41Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub41Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub41Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub41Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub41Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub41Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub41ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T2_Sub41BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub41 do
  if(State in dsEditModes)Then Post;
end;

//--폐기(반품명세서)--//
procedure TBase10.T2_Sub51AfterCancel(DataSet: TDataSet);
begin
  T2_Sub51AfterScroll(T2_Sub51);
end;

procedure TBase10.T2_Sub51AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T2_Sub51.FieldByName('Gdate').AsString;
  Ocode:= T2_Sub51.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub51.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub51.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub51.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T2_Sub51AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub51AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Bdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub51ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub51Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Bdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub51ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub51Gdate.AsString);
      Translate(Sqlen, '@Scode', '3');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T2_Sub51.Delete;

  end; end;

end;

procedure TBase10.T2_Sub51BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub51.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S1_Ssub '+
    '(Bdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'', Time1)';

    Translate(Sqlen, '@Gdate', T2_Sub51Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub51Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub51Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub51Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub51Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub51Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub51Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub51Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub51Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub51Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub51Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub51Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub51Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub51Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub51Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub51Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub51Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub51Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM');
  //Base10.Update_Icode(nSqry,'S1_SSUB_ID_NUM');

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Bdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Ocode=''@Ocode'',Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'', ';
    Sqlen :=
    'Pubun=''@Pubun'',Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  , '+
    'Grat1=  @Grat1  ,Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  , '+
    'Yesno=''@Yesno'',Gjisa=''@Gjisa'',Time2=  now() '+
    'WHERE ID=@ID and Bdate=''@Sdate''';

    Translate(Sqlon, '@Gdate', T2_Sub51Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub51Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub51Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub51Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub51Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub51Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub51Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub51Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub51Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub51Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub51Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub51Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub51Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub51Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub51Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub51Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub51Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub51Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub51ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T2_Sub51BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub51 do
  if(State in dsEditModes)Then Post;
end;

//--제작명세서--//
procedure TBase10.T2_Sub61AfterCancel(DataSet: TDataSet);
begin
  T2_Sub61AfterScroll(T2_Sub61);
end;

procedure TBase10.T2_Sub61AfterScroll(DataSet: TDataSet);
begin
{ Ocode:= T2_Sub11.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub11.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub11.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub11.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T2_Sub61AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub61AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub61ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub61Ocode.AsString='B')and(T2_Sub61Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub61ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub61ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
      Translate(Sqlen, '@Scode', '1');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub61Ocode.AsString='B')and(T2_Sub61Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub61ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end;

  //S2101:=S2101-T2_Sub61Gsqut.AsFloat;
  //S2102:=S2102-T2_Sub61Gssum.AsFloat;
    T2_Sub61.Delete;

  end; end;

end;

procedure TBase10.T2_Sub61BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub61.State=dsInsert)Then begin

  { Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'')';

    Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub61Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub61Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub61Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub61Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub61Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub61Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub61Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub61Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub61Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub61Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub61Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub61Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub61Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub61Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub61Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub61Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub61Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM'); }

  //S2101:=S2101+T2_Sub61Gsqut.AsFloat;
  //S2102:=S2102+T2_Sub61Gssum.AsFloat;

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'',Ocode=''@Ocode'', '+
    'Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'',Pubun=''@Pubun'', ';
    Sqlen :=
    'Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Grat1=  @Grat1  , '+
    'Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  ,Yesno=''@Yesno'', '+
    'Gjisa=''@Gjisa'' WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub61Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub61Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub61Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub61Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub61Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub61Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub61Jubun.AsString);
    Translate(Sqlon, '@Pubun', T2_Sub61Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub61Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub61Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub61Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub61Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub61Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub61Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub61Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub61Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub61Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub61ID.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  //S2101:=S2101+T2_Sub61Gsqut.AsFloat+Gsqut;
  //S2102:=S2102+T2_Sub61Gssum.AsFloat+Gssum;

  end;

end;

procedure TBase10.T2_Sub61BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub61 do
  if(State in dsEditModes)Then Post;
end;

//--제작명세서--//
procedure TBase10.T2_Sub62AfterCancel(DataSet: TDataSet);
begin
  T2_Sub62AfterScroll(T2_Sub62);
end;

procedure TBase10.T2_Sub62AfterScroll(DataSet: TDataSet);
begin
  Gssum:=-T2_Sub62.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T2_Sub62AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub62AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM S2_Ssub WHERE ID=@ID and Ycode=''@Ycode'' ';
    TransAuto(Sqlen, '@ID',    T2_Sub62ID.AsString);
    TransAuto(Sqlen, '@Ycode', T2_Sub62Ycode.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S2602:=S2602-T2_Sub62Gssum.AsFloat;
    T2_Sub62.Delete;

  end; end; }

end;

procedure TBase10.T2_Sub62BeforePost(DataSet: TDataSet);
begin

{ if(T2_Sub62.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO S2_Ssub '+
    '(Gdate, Gubun, Scode, Gcode, Gname, Hcode, '+
    ' Ocode, Oname, Bcode, Jubun, Gbigo, Gssum, '+
    ' Ycode ) VALUES '+
    '(''@Gdate'',''@Gubun'',''@Scode'',''@Gcode'',''@Gname'',''@Hcode'', '+
    ' ''@Ocode'',''@Oname'',''@Bcode'',''@Jubun'',''@Gbigo'',  @Gssum  , '+
    ' ''@Ycode'' )';

    Translate(Sqlen, '@Gdate', T2_Sub62Gdate.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub62Gubun.AsString);
    Translate(Sqlen, '@Scode', T2_Sub62Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub62Gcode.AsString);
    Translate(Sqlen, '@Gname', T2_Sub62Gname.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub62Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub62Ocode.AsString);
    Translate(Sqlen, '@Oname', T2_Sub62Oname.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub62Bcode.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub62Jubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub62Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub62Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub62Gdang.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub62Gssum.AsString);
    TransAuto(Sqlen, '@Ycode', T2_Sub62Ycode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'S2_SSUB_ID_GEN');

    S2602:=S2602+T2_Sub62Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE S2_Ssub SET '+
    'Gubun=''@Gubun'',Scode=''@Scode'',Gcode=''@Gcode'',Gname=''@Gname'', '+
    'Hcode=''@Hcode'',Ocode=''@Ocode'',Oname=''@Oname'',Bcode=''@Bcode'', '+
    'Jubun=''@Jubun'',Gbigo=''@Gbigo'',Gssum=  @Gssum  '+
    'WHERE ID=@ID and Ycode=''@Ycode'' ';

    Translate(Sqlen, '@Gdate', T2_Sub62Gdate.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub62Gubun.AsString);
    Translate(Sqlen, '@Scode', T2_Sub62Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub62Gcode.AsString);
    Translate(Sqlen, '@Gname', T2_Sub62Gname.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub62Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub62Ocode.AsString);
    Translate(Sqlen, '@Oname', T2_Sub62Oname.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub62Bcode.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub62Jubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub62Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub62Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub62Gdang.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub62Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub62ID.AsString);
    TransAuto(Sqlen, '@Ycode', T2_Sub62Ycode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S2602:=S2602+T2_Sub62Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T2_Sub62BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub62 do
  if(State in dsEditModes)Then Post;
end;

//--원천징수--//
procedure TBase10.T2_Sub81AfterCancel(DataSet: TDataSet);
begin
  T2_Sub81AfterScroll(T2_Sub81);
end;

procedure TBase10.T2_Sub81AfterScroll(DataSet: TDataSet);
begin
{ Gssum:=-T2_Sub81.FieldByName('Gssum').AsFloat;
  Gisum:=-T2_Sub81.FieldByName('Gisum').AsFloat;
  Gosum:=-T2_Sub81.FieldByName('Gosum').AsFloat;
  Gbsum:=-T2_Sub81.FieldByName('Gbsum').AsFloat; }
end;

procedure TBase10.T2_Sub81AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub81AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM T1_Gbun WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T2_Sub81ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T2_Sub81.Delete;

  end; end;

end;

procedure TBase10.T2_Sub81BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub81.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO T1_Gbun '+
    '(Hcode, Gcode, Gname, Gjisa, Jubun, Bebon) VALUES '+
    '(''@Hcode'',''@Gcode'',''@Gname'',''@Gjisa'',''@Jubun'',''@Bebon'')';

    Translate(Sqlen, '@Hcode', T2_Sub81Hcode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub81Gcode.AsString);
    Translate(Sqlen, '@Gname', T2_Sub81Gname.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub81Gjisa.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub81Jubun.AsString);
    Translate(Sqlen, '@Bebon', T2_Sub81Bebon.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'T1_GBUN_ID_GEN');

  end else begin

    Sqlen := 'UPDATE T1_Gbun SET '+
    'Hcode=''@Hcode'',Gcode=''@Gcode'',Gname=''@Gname'', '+
    'Gjisa=''@Gjisa'',Jubun=''@Jubun'',Bebon=''@Bebon'' WHERE ID=@ID ';

    Translate(Sqlen, '@Hcode', T2_Sub81Hcode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub81Gcode.AsString);
    Translate(Sqlen, '@Gname', T2_Sub81Gname.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub81Gjisa.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub81Jubun.AsString);
    Translate(Sqlen, '@Bebon', T2_Sub81Bebon.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub81ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T2_Sub81BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub81 do
  if(State in dsEditModes)Then Post;
end;

//--신간명세서--//
procedure TBase10.T2_Sub91AfterCancel(DataSet: TDataSet);
begin
  T2_Sub91AfterScroll(T2_Sub91);
end;

procedure TBase10.T2_Sub91AfterScroll(DataSet: TDataSet);
begin
  Ocode:= T2_Sub91.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub91.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub91.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub91.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T2_Sub91AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub91AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub91ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub91Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub91ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub91Gdate.AsString);
      Translate(Sqlen, '@Scode', '1');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T2_Sub91.Delete;

  end; end;

end;

procedure TBase10.T2_Sub91BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub91.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'', now())';

    Translate(Sqlen, '@Gdate', T2_Sub91Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub91Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub91Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub91Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub91Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub91Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub91Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub91Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub91Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub91Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub91Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub91Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub91Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub91Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub91Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub91Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub91Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub91Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM');
  //Base10.Update_Icode(nSqry,'S1_SSUB_ID_NUM');

  end else begin

    Sqlen := 'UPDATE S1_Ssub SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'',Ocode=''@Ocode'', '+
    'Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'',Pubun=''@Pubun'', ';
    Sqlon :=
    'Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Grat1=  @Grat1  , '+
    'Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  ,Yesno=''@Yesno'', '+
    'Gjisa=''@Gjisa'' WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub91Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub91Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub91Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub91Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub91Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub91Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub91Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub91Jubun.AsString);
    Translate(Sqlon, '@Pubun', T2_Sub91Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub91Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub91Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub91Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub91Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub91Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub91Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub91Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub91Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub91Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub91ID.AsString);

    Base10.Socket.RunSQL(Sqlen+Sqlon);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T2_Sub91BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub91 do
  if(State in dsEditModes)Then Post;
end;

//--Master-Ggeo--//
procedure TBase10.T3_Sub81AfterCancel(DataSet: TDataSet);
begin
  T3_Sub81AfterScroll(T3_Sub81);
end;

procedure TBase10.T3_Sub81AfterScroll(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T3_Sub81AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T3_Sub81AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM H2_Gbun WHERE ID=@ID ';
    translate(Sqlen, '@ID',    T3_Sub81ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T3_Sub81.Delete;

  end; end;

end;

procedure TBase10.T3_Sub81BeforePost(DataSet: TDataSet);
begin

  if(T3_Sub81.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H2_Gbun '+
    '(Scode, Gname, Oname) VALUES '+
    '(''@Scode'',''@Gname'',''@Oname'')';

    Translate(Sqlen, '@Scode', T3_Sub81Scode.AsString);
    Translate(Sqlen, '@Gname', T3_Sub81Gcode.AsString);
    TransAuto(Sqlen, '@Oname', T3_Sub81Ocode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'H2_Gbun_ID_GEN');

  end else begin

    Sqlen := 'UPDATE H2_Gbun SET '+
    'Scode=''@Scode'',Gname=''@Gname'',Oname=''@Oname'' '+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Scode', T3_Sub81Scode.AsString);
    Translate(Sqlen, '@Gname', T3_Sub81Gcode.AsString);
    TransAuto(Sqlen, '@Oname', T3_Sub81Ocode.AsString);
    TransAuto(Sqlen, '@ID',    T3_Sub81ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T3_Sub81BeforeClose(DataSet: TDataSet);
begin
  With T3_Sub81 do
  if(State in dsEditModes)Then Post;
end;

//--Master-Book--//
procedure TBase10.T3_Sub82AfterCancel(DataSet: TDataSet);
begin
  T3_Sub82AfterScroll(T3_Sub82);
end;

procedure TBase10.T3_Sub82AfterScroll(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T3_Sub82AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T3_Sub82AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM H2_Gbun WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T3_Sub82ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T3_Sub82.Delete;

  end; end;

end;

procedure TBase10.T3_Sub82BeforePost(DataSet: TDataSet);
begin

  if(T3_Sub82.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H2_Gbun '+
    '(Scode, Gname, Oname) VALUES '+
    '(''@Scode'',''@Gname'',''@Oname'')';

    Translate(Sqlen, '@Scode', T3_Sub82Scode.AsString);
    Translate(Sqlen, '@Gname', T3_Sub82Gcode.AsString);
    TransAuto(Sqlen, '@Oname', T3_Sub82Ocode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'H2_Gbun_ID_GEN');

  end else begin

    Sqlen := 'UPDATE H2_Gbun SET '+
    'Scode=''@Scode'',Gname=''@Gname'',Oname=''@Oname'' '+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Scode', T3_Sub82Scode.AsString);
    Translate(Sqlen, '@Gname', T3_Sub82Gcode.AsString);
    TransAuto(Sqlen, '@Oname', T3_Sub82Ocode.AsString);
    TransAuto(Sqlen, '@ID',    T3_Sub82ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T3_Sub82BeforeClose(DataSet: TDataSet);
begin
  With T3_Sub82 do
  if(State in dsEditModes)Then Post;
end;

//--입금전표--//
procedure TBase10.T4_Sub11AfterCancel(DataSet: TDataSet);
begin
  T4_Sub11AfterScroll(T4_Sub11);
end;

procedure TBase10.T4_Sub11AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T4_Sub11.FieldByName('Gdate').AsString;
  Gssum:=-T4_Sub11.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T4_Sub11AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub11AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
    St1: String;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM T5_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
    TransAuto(Sqlen, '@ID',    T4_Sub11ID.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub11Gdate.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T4_Sub11.Delete;

  end; end;
  
end;

procedure TBase10.T4_Sub11BeforePost(DataSet: TDataSet);
begin

  if(T4_Sub11.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO T5_Ssub '+
    '(Hcode, Sdate, Gdate, Gssum, Pubun, Gbigo) VALUES '+
    '(''@Hcode'',''@Sdate'',''@Gdate'',  @Gssum  ,''@Pubun'',''@Gbigo'')';

    Translate(Sqlen, '@Hcode', T4_Sub11Hcode.AsString);
    Translate(Sqlen, '@Sdate', T4_Sub11Sdate.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub11Gdate.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub11Gssum.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub11Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub11Gbigo.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'T5_SSUB_ID_GEN');

  end else begin

    Sqlen := 'UPDATE T5_Ssub SET '+
    'Hcode=''@Hcode'',Sdate=''@Sdate'',Gdate=''@Gdate'',Gssum=  @Gssum  ,'+
    'Pubun=''@Pubun'',Gbigo=''@Gbigo'''+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Hcode', T4_Sub11Hcode.AsString);
    Translate(Sqlen, '@Sdate', T4_Sub11Sdate.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub11Gdate.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub11Gssum.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub11Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub11Gbigo.AsString);
    TransAuto(Sqlen, '@ID',    T4_Sub11ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T4_Sub11BeforeClose(DataSet: TDataSet);
begin
  With T4_Sub11 do
  if(State in dsEditModes)Then Post;
end;

//--출금전표--//
procedure TBase10.T4_Sub12AfterCancel(DataSet: TDataSet);
begin
  T4_Sub12AfterScroll(T4_Sub12);
end;

procedure TBase10.T4_Sub12AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T4_Sub12.FieldByName('Gdate').AsString;
  Gssum:=-T4_Sub12.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T4_Sub12AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub12AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM H1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
    TransAuto(Sqlen, '@ID',    T4_Sub12ID.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub12Gdate.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S4102:=S4102-T4_Sub12Gssum.AsFloat;
    T4_Sub12.Delete;

  end; end; }

end;

procedure TBase10.T4_Sub12BeforePost(DataSet: TDataSet);
begin

{ if(T4_Sub12.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H1_Ssub '+
    '(Gdate, Gubun, Hcode, Scode, Gcode, Gname, '+
    ' Tcode, Ocode, Oname, Pubun, Gbigo, Gssum, '+
    ' Idnum) VALUES '+
    '(''@Gdate'',''@Gubun'',''@Hcode'',''@Scode'',''@Gcode'',''@Gname'', '+
    ' ''@Tcode'',''@Ocode'',''@Oname'',''@Pubun'',''@Gbigo'',  @Gssum  , '+
    '   @Idnum  )';

    TransAuto(Sqlen, '@Idnum', T4_Sub12Idnum.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub12Gdate.AsString);
    Translate(Sqlen, '@Gubun', T4_Sub12Gubun.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub12Hcode.AsString);
    Translate(Sqlen, '@Scode', T4_Sub12Scode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub12Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub12Gname.AsString);
    Translate(Sqlen, '@Tcode', T4_Sub12Tcode.AsString);
    Translate(Sqlen, '@Ocode', T4_Sub12Ocode.AsString);
    Translate(Sqlen, '@Oname', T4_Sub12Oname.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub12Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub12Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub12Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'H1_SSUB_ID_GEN');

    S4102:=S4102+T4_Sub12Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE H1_Ssub SET '+
    'Gdate=''@Gdate'',Gubun=''@Gubun'',Hcode=''@Hcode'',Scode=''@Scode'', '+
    'Gcode=''@Gcode'',Gname=''@Gname'',Tcode=''@Tcode'',Ocode=''@Ocode'', '+
    'Oname=''@Oname'',Pubun=''@Pubun'',Gbigo=''@Gbigo'',Gssum=  @Gssum  , '+
    'Idnum=  @Idnum  '+
    'WHERE ID=@ID and Gdate=''@Sdate''';

    TransAuto(Sqlen, '@Idnum', T4_Sub12Idnum.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub12Gdate.AsString);
    Translate(Sqlen, '@Gubun', T4_Sub12Gubun.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub12Hcode.AsString);
    Translate(Sqlen, '@Scode', T4_Sub12Scode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub12Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub12Gname.AsString);
    Translate(Sqlen, '@Tcode', T4_Sub12Tcode.AsString);
    Translate(Sqlen, '@Ocode', T4_Sub12Ocode.AsString);
    Translate(Sqlen, '@Oname', T4_Sub12Oname.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub12Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub12Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub12Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T4_Sub12ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S4102:=S4102+T4_Sub12Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T4_Sub12BeforeClose(DataSet: TDataSet);
begin
{ With T4_Sub12 do
  if(State in dsEditModes)Then Post; }
end;

//--대체입금--//
procedure TBase10.T4_Sub21AfterCancel(DataSet: TDataSet);
begin
  T4_Sub21AfterScroll(T4_Sub21);
end;

procedure TBase10.T4_Sub21AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T4_Sub21.FieldByName('Gdate').AsString;
  Gssum:=-T4_Sub21.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T4_Sub21AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub21AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
    St1: String;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    St1:=T4_Sub21Idnum.AsString;
    if St1='' Then St1:='0';

    Sqlen := 'DELETE FROM H4_Iyeo WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID', St1);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    Sqlen := 'DELETE FROM H1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
    TransAuto(Sqlen, '@ID',    T4_Sub21ID.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub21Gdate.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S4201:=S4201-T4_Sub21Gssum.AsFloat;
    T4_Sub21.Delete;

  end; end; }

end;

procedure TBase10.T4_Sub21BeforePost(DataSet: TDataSet);
begin

{ if(T4_Sub21.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H1_Ssub '+
    '(Gdate, Gubun, Hcode, Scode, Gcode, Gname, '+
    ' Tcode, Ocode, Oname, Pubun, Gbigo, Gssum, '+
    ' Idnum) VALUES '+
    '(''@Gdate'',''@Gubun'',''@Hcode'',''@Scode'',''@Gcode'',''@Gname'', '+
    ' ''@Tcode'',''@Ocode'',''@Oname'',''@Pubun'',''@Gbigo'',  @Gssum  , '+
    '   @Idnum  )';

    TransAuto(Sqlen, '@Idnum', T4_Sub21Idnum.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub21Gdate.AsString);
    Translate(Sqlen, '@Gubun', T4_Sub21Gubun.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub21Hcode.AsString);
    Translate(Sqlen, '@Scode', T4_Sub21Scode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub21Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub21Gname.AsString);
    Translate(Sqlen, '@Tcode', T4_Sub21Tcode.AsString);
    Translate(Sqlen, '@Ocode', T4_Sub21Ocode.AsString);
    Translate(Sqlen, '@Oname', T4_Sub21Oname.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub21Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub21Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub21Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'H1_SSUB_ID_GEN');

    S4201:=S4201+T4_Sub21Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE H1_Ssub SET '+
    'Gdate=''@Gdate'',Gubun=''@Gubun'',Hcode=''@Hcode'',Scode=''@Scode'', '+
    'Gcode=''@Gcode'',Gname=''@Gname'',Tcode=''@Tcode'',Ocode=''@Ocode'', '+
    'Oname=''@Oname'',Pubun=''@Pubun'',Gbigo=''@Gbigo'',Gssum=  @Gssum  , '+
    'Idnum=  @Idnum  '+
    'WHERE ID=@ID and Gdate=''@Sdate''';

    TransAuto(Sqlen, '@Idnum', T4_Sub21Idnum.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub21Gdate.AsString);
    Translate(Sqlen, '@Gubun', T4_Sub21Gubun.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub21Hcode.AsString);
    Translate(Sqlen, '@Scode', T4_Sub21Scode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub21Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub21Gname.AsString);
    Translate(Sqlen, '@Tcode', T4_Sub21Tcode.AsString);
    Translate(Sqlen, '@Ocode', T4_Sub21Ocode.AsString);
    Translate(Sqlen, '@Oname', T4_Sub21Oname.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub21Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub21Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub21Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T4_Sub21ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S4201:=S4201+T4_Sub21Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T4_Sub21BeforeClose(DataSet: TDataSet);
begin
{ With T4_Sub21 do
  if(State in dsEditModes)Then Post; }
end;

//--대체출금--//
procedure TBase10.T4_Sub22AfterCancel(DataSet: TDataSet);
begin
  T4_Sub22AfterScroll(T4_Sub22);
end;

procedure TBase10.T4_Sub22AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T4_Sub22.FieldByName('Gdate').AsString;
  Gssum:=-T4_Sub22.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T4_Sub22AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub22AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM H1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
    TransAuto(Sqlen, '@ID',    T4_Sub22ID.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub22Gdate.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S4202:=S4202-T4_Sub22Gssum.AsFloat;
    T4_Sub22.Delete;

  end; end; }

end;

procedure TBase10.T4_Sub22BeforePost(DataSet: TDataSet);
begin

{ if(T4_Sub22.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H1_Ssub '+
    '(Gdate, Gubun, Hcode, Scode, Gcode, Gname, '+
    ' Tcode, Ocode, Oname, Pubun, Gbigo, Gssum, '+
    ' Idnum) VALUES '+
    '(''@Gdate'',''@Gubun'',''@Hcode'',''@Scode'',''@Gcode'',''@Gname'', '+
    ' ''@Tcode'',''@Ocode'',''@Oname'',''@Pubun'',''@Gbigo'',  @Gssum  , '+
    '   @Idnum  )';

    TransAuto(Sqlen, '@Idnum', T4_Sub22Idnum.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub22Gdate.AsString);
    Translate(Sqlen, '@Gubun', T4_Sub22Gubun.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub22Hcode.AsString);
    Translate(Sqlen, '@Scode', T4_Sub22Scode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub22Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub22Gname.AsString);
    Translate(Sqlen, '@Tcode', T4_Sub22Tcode.AsString);
    Translate(Sqlen, '@Ocode', T4_Sub22Ocode.AsString);
    Translate(Sqlen, '@Oname', T4_Sub22Oname.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub22Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub22Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub22Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'H1_SSUB_ID_GEN');

    S4202:=S4202+T4_Sub22Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE H1_Ssub SET '+
    'Gdate=''@Gdate'',Gubun=''@Gubun'',Hcode=''@Hcode'',Scode=''@Scode'', '+
    'Gcode=''@Gcode'',Gname=''@Gname'',Tcode=''@Tcode'',Ocode=''@Ocode'', '+
    'Oname=''@Oname'',Pubun=''@Pubun'',Gbigo=''@Gbigo'',Gssum=  @Gssum  , '+
    'Idnum=  @Idnum  '+
    'WHERE ID=@ID and Gdate=''@Sdate''';

    TransAuto(Sqlen, '@Idnum', T4_Sub22Idnum.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub22Gdate.AsString);
    Translate(Sqlen, '@Gubun', T4_Sub22Gubun.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub22Hcode.AsString);
    Translate(Sqlen, '@Scode', T4_Sub22Scode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub22Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub22Gname.AsString);
    Translate(Sqlen, '@Tcode', T4_Sub22Tcode.AsString);
    Translate(Sqlen, '@Ocode', T4_Sub22Ocode.AsString);
    Translate(Sqlen, '@Oname', T4_Sub22Oname.AsString);
    Translate(Sqlen, '@Pubun', T4_Sub22Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub22Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub22Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T4_Sub22ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S4202:=S4202+T4_Sub22Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T4_Sub22BeforeClose(DataSet: TDataSet);
begin
{ With T4_Sub22 do
  if(State in dsEditModes)Then Post; }
end;

//--내 역 비--//
procedure TBase10.T4_Sub31AfterCancel(DataSet: TDataSet);
begin
  T4_Sub31AfterScroll(T4_Sub31);
end;

procedure TBase10.T4_Sub31AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T4_Sub31.FieldByName('Gdate').AsString;
  Gssum:=-T4_Sub31.FieldByName('Gssum').AsFloat;
end;

procedure TBase10.T4_Sub31AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub31AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM T1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
    TransAuto(Sqlen, '@ID',    T4_Sub31ID.AsString);
    Translate(Sqlen, '@Gdate', T4_Sub31Gdate.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T4_Sub31.Delete;

  end; end;

end;

procedure TBase10.T4_Sub31BeforePost(DataSet: TDataSet);
begin

  if(T4_Sub31.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO T1_Ssub '+
    '(Gdate, Hcode, Gcode, Gname, Name1, Name2,'+
    ' Gnumb, Gbigo, Gsqut, Gdang, Gssum) VALUES '+
    '(''@Gdate'',''@Hcode'',''@Gcode'',''@Gname'',''@Name1'',''@Name2'','+
    ' ''@Gnumb'',''@Gbigo'',  @Gsqut  ,  @Gdang  ,  @Gssum  )';

    Translate(Sqlen, '@Gdate', T4_Sub31Gdate.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub31Hcode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub31Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub31Gname.AsString);
    Translate(Sqlen, '@Name1', T4_Sub31Name1.AsString);
    Translate(Sqlen, '@Name2', T4_Sub31Name2.AsString);
    Translate(Sqlen, '@Gnumb', T4_Sub31Gnumb.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub31Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T4_Sub31Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T4_Sub31Gdang.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub31Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'T1_SSUB_ID_GEN');

  end else begin

    Sqlen := 'UPDATE T1_Ssub SET '+
    'Gdate=''@Gdate'',Hcode=''@Hcode'',Gcode=''@Gcode'',Gname=''@Gname'','+
    'Name1=''@Name1'',Name2=''@Name2'',Gnumb=''@Gnumb'',Gbigo=''@Gbigo'','+
    'Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Gssum=  @Gssum  '+
    'WHERE ID=@ID and Gdate=''@Sdate''';

    Translate(Sqlen, '@Gdate', T4_Sub31Gdate.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub31Hcode.AsString);
    Translate(Sqlen, '@Gcode', T4_Sub31Gcode.AsString);
    Translate(Sqlen, '@Gname', T4_Sub31Gname.AsString);
    Translate(Sqlen, '@Name1', T4_Sub31Name1.AsString);
    Translate(Sqlen, '@Name2', T4_Sub31Name2.AsString);
    Translate(Sqlen, '@Gnumb', T4_Sub31Gnumb.AsString);
    Translate(Sqlen, '@Gbigo', T4_Sub31Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T4_Sub31Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T4_Sub31Gdang.AsString);
    TransAuto(Sqlen, '@Gssum', T4_Sub31Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T4_Sub31ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T4_Sub31BeforeClose(DataSet: TDataSet);
begin
  With T4_Sub31 do
  if(State in dsEditModes)Then Post;
end;

procedure TBase10.T4_Sub51AfterCancel(DataSet: TDataSet);
begin
  T4_Sub51AfterScroll(T4_Sub51);
end;

procedure TBase10.T4_Sub51AfterScroll(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub51AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub51AfterDelete(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T4_Sub51BeforePost(DataSet: TDataSet);
begin

{ if(T4_Sub51.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO T3_Ssub '+
    '(Gdate, Hcode, Gqut3, Gqut4) VALUES '+
    '(''@Gdate'',''@Hcode'',  @Gqut3  ,  @Gqut4  )';

    Translate(Sqlen, '@Gdate', T4_Sub51Gdate.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub51Hcode.AsString);
    TransAuto(Sqlen, '@Gqut3', T4_Sub51Gqut3.AsString);
    TransAuto(Sqlen, '@Gqut4', T4_Sub51Gqut4.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end else begin

    Sqlen := 'UPDATE T3_Ssub SET '+
    'Hcode=''@Hcode'',Gqut3=  @Gqut3  ,Gqut4=  @Gqut4  '+
    'WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T4_Sub51Gdate.AsString);
    Translate(Sqlen, '@Hcode', T4_Sub51Hcode.AsString);
    TransAuto(Sqlen, '@Gqut3', T4_Sub51Gqut3.AsString);
    TransAuto(Sqlen, '@Gqut4', T4_Sub51Gqut4.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end; }

end;

procedure TBase10.T4_Sub51BeforeClose(DataSet: TDataSet);
begin
  With T4_Sub51 do
  if(State in dsEditModes)Then Post;
end;

//--원장변경--//
procedure TBase10.T5_Sub11AfterCancel(DataSet: TDataSet);
begin
  T5_Sub11AfterScroll(T5_Sub11);
end;

procedure TBase10.T5_Sub11AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T5_Sub11.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub11.FieldByName('Gssum').AsFloat;
  Gosum:=-T5_Sub11.FieldByName('Gosum').AsFloat;
  Gbsum:=-T5_Sub11.FieldByName('Gbsum').AsFloat;
end;

procedure TBase10.T5_Sub11AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub11AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM Sg_Csum WHERE ID=@ID ';
      TransAuto(Sqlen, '@ID',    T5_Sub11ID.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE Sg_Csum SET Scode=''@Scode'' WHERE ID=@ID ';
      TransAuto(Sqlen, '@ID',    T5_Sub11ID.AsString);
      Translate(Sqlen, '@Scode', '4');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T5_Sub11.Delete;

  end; end;

end;

procedure TBase10.T5_Sub11BeforePost(DataSet: TDataSet);
begin

  if(T5_Sub11.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO Sg_Csum '+
    '(Gdate, Scode, Gcode, Hcode, Gbigo, Gssum, '+
    ' Gosum, Gbsum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Gbigo'',  @Gssum  , '+
    '   @Gosum  ,  @Gbsum  )';

    Translate(Sqlen, '@Gdate', T5_Sub11Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub11Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub11Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub11Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub11Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub11Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub11Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub11Gbsum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'SG_CSUM_ID_GEN');

  end else begin

    Sqlen := 'UPDATE Sg_Csum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gbigo=''@Gbigo'',Gssum=  @Gssum  ,Gosum=  @Gosum  ,Gbsum=  @Gbsum  '+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub11Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub11Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub11Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub11Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub11Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub11Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub11Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub11Gbsum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub11ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T5_Sub11BeforeClose(DataSet: TDataSet);
begin
  With T5_Sub11 do
  if(State in dsEditModes)Then Post;
end;

//--원장변경--//
procedure TBase10.T5_Sub12AfterCancel(DataSet: TDataSet);
begin
  T5_Sub12AfterScroll(T5_Sub12);
end;

procedure TBase10.T5_Sub12AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T5_Sub12.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub12.FieldByName('Gssum').AsFloat;
  Gosum:=-T5_Sub12.FieldByName('Gosum').AsFloat;
  Gbsum:=-T5_Sub12.FieldByName('Gbsum').AsFloat;
end;

procedure TBase10.T5_Sub12AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub12AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM Sg_Gsum WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub12ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T5_Sub12.Delete;

  end; end;

end;

procedure TBase10.T5_Sub12BeforePost(DataSet: TDataSet);
begin

  if(T5_Sub12.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO Sg_Gsum '+
    '(Gdate, Scode, Gcode, Hcode, Gbigo, Gssum, '+
    ' Gosum, Gbsum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Gbigo'',  @Gssum  , '+
    '   @Gosum  ,  @Gbsum  )';

    Translate(Sqlen, '@Gdate', T5_Sub12Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub12Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub12Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub12Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub12Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub12Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub12Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub12Gbsum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'SG_GSUM_ID_GEN');

  end else begin

    Sqlen := 'UPDATE Sg_Gsum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gbigo=''@Gbigo'',Gssum=  @Gssum  ,Gosum=  @Gosum  ,Gbsum=  @Gbsum  '+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub12Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub12Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub12Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub12Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub12Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub12Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub12Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub12Gbsum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub12ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T5_Sub12BeforeClose(DataSet: TDataSet);
begin
  With T5_Sub12 do
  if(State in dsEditModes)Then Post;
end;

//--재고변경--//
procedure TBase10.T5_Sub21AfterCancel(DataSet: TDataSet);
begin
  T5_Sub21AfterScroll(T5_Sub21);
end;

procedure TBase10.T5_Sub21AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T5_Sub21.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub21.FieldByName('Gssum').AsFloat;
  Gosum:=-T5_Sub21.FieldByName('Gosum').AsFloat;
  Gbsum:=-T5_Sub21.FieldByName('Gbsum').AsFloat;
end;

procedure TBase10.T5_Sub21AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub21AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM Sg_Csum WHERE ID=@ID ';
      TransAuto(Sqlen, '@ID',    T5_Sub21ID.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE Sg_Csum SET Scode=''@Scode'' WHERE ID=@ID ';
      TransAuto(Sqlen, '@ID',    T5_Sub21ID.AsString);
      Translate(Sqlen, '@Scode', '2');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T5_Sub21.Delete;

  end; end;

end;

procedure TBase10.T5_Sub21BeforePost(DataSet: TDataSet);
begin

  if(T5_Sub21.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO Sg_Csum '+
    '(Gdate, Scode, Gcode, Hcode, Gbigo, Gssum, '+
    ' Gosum, Gbsum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Gbigo'',  @Gssum  , '+
    '   @Gosum  ,  @Gbsum  )';

    Translate(Sqlen, '@Gdate', T5_Sub21Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub21Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub21Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub21Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub21Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub21Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub21Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub21Gbsum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'SG_CSUM_ID_GEN');

  end else begin

    Sqlen := 'UPDATE Sg_Csum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gbigo=''@Gbigo'',Gssum=  @Gssum  ,Gosum=  @Gosum  ,Gbsum=  @Gbsum  '+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub21Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub21Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub21Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub21Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub21Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub21Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub21Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub21Gbsum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub21ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T5_Sub21BeforeClose(DataSet: TDataSet);
begin
  With T5_Sub21 do
  if(State in dsEditModes)Then Post;
end;

//--재고변경--//
procedure TBase10.T5_Sub22AfterCancel(DataSet: TDataSet);
begin
  T5_Sub22AfterScroll(T5_Sub22);
end;

procedure TBase10.T5_Sub22AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T5_Sub22.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub22.FieldByName('Gssum').AsFloat;
  Gosum:=-T5_Sub22.FieldByName('Gosum').AsFloat;
  Gbsum:=-T5_Sub22.FieldByName('Gbsum').AsFloat;
end;

procedure TBase10.T5_Sub22AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub22AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM Sg_Csum WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub22ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T5_Sub22.Delete;

  end; end;

end;

procedure TBase10.T5_Sub22BeforePost(DataSet: TDataSet);
begin

  if(T5_Sub22.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO Sg_Csum '+
    '(Gdate, Scode, Gcode, Hcode, Gbigo, Gssum, '+
    ' Gosum, Gbsum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Gbigo'',  @Gssum  , '+
    '   @Gosum  ,  @Gbsum  )';

    Translate(Sqlen, '@Gdate', T5_Sub22Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub22Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub22Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub22Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub22Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub22Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub22Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub22Gbsum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'SG_CSUM_ID_GEN');

  end else begin

    Sqlen := 'UPDATE Sg_Csum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gbigo=''@Gbigo'',Gssum=  @Gssum  ,Gosum=  @Gosum  ,Gbsum=  @Gbsum  '+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub22Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub22Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub22Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub22Hcode.AsString);
    Translate(Sqlen, '@Gbigo', T5_Sub22Gbigo.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub22Gssum.AsString);
    TransAuto(Sqlen, '@Gosum', T5_Sub22Gosum.AsString);
    TransAuto(Sqlen, '@Gbsum', T5_Sub22Gbsum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub22ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TBase10.T5_Sub22BeforeClose(DataSet: TDataSet);
begin
  With T5_Sub22 do
  if(State in dsEditModes)Then Post;
end;

//--초기미수--//
procedure TBase10.T5_Sub31AfterCancel(DataSet: TDataSet);
begin
  T5_Sub31AfterScroll(T5_Sub31);
end;

procedure TBase10.T5_Sub31AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T5_Sub31.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub31.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T5_Sub31AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub31AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM In_Gsum WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub31ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S5301:=S5301-T5_Sub31Gssum.AsFloat;
    T5_Sub31.Delete;

  end; end; }

end;

procedure TBase10.T5_Sub31BeforePost(DataSet: TDataSet);
begin

{ if(T5_Sub31.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO In_Gsum '+
    '(Gdate, Scode, Gcode, Hcode, Gssum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gssum  )';

    Translate(Sqlen, '@Gdate', T5_Sub31Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub31Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub31Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub31Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub31Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'IN_GSUM_ID_GEN');

    S5301:=S5301+T5_Sub31Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE In_Gsum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gssum=  @Gssum  WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub31Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub31Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub31Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub31Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub31Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub31ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S5301:=S5301+T5_Sub31Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T5_Sub31BeforeClose(DataSet: TDataSet);
begin
{ With T5_Sub31 do
  if(State in dsEditModes)Then Post; }
end;

//--초기미수--//
procedure TBase10.T5_Sub32AfterCancel(DataSet: TDataSet);
begin
  T5_Sub32AfterScroll(T5_Sub32);
end;

procedure TBase10.T5_Sub32AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T5_Sub32.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub32.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T5_Sub32AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub32AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM In_Gsum WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub32ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S5302:=S5302-T5_Sub32Gssum.AsFloat;
    T5_Sub32.Delete;

  end; end; }

end;

procedure TBase10.T5_Sub32BeforePost(DataSet: TDataSet);
begin

{ if(T5_Sub32.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO In_Gsum '+
    '(Gdate, Scode, Gcode, Hcode, Gssum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gssum  )';

    Translate(Sqlen, '@Gdate', T5_Sub32Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub32Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub32Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub32Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub32Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'IN_GSUM_ID_GEN');

    S5302:=S5302+T5_Sub32Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE In_Gsum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gssum=  @Gssum  WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub32Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub32Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub32Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub32Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub32Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub32ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S5302:=S5302+T5_Sub32Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T5_Sub32BeforeClose(DataSet: TDataSet);
begin
{ With T5_Sub32 do
  if(State in dsEditModes)Then Post; }
end;

//--초기재고--//
procedure TBase10.T5_Sub41AfterCancel(DataSet: TDataSet);
begin
  T5_Sub41AfterScroll(T5_Sub41);
end;

procedure TBase10.T5_Sub41AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T5_Sub41.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub41.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T5_Sub41AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub41AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM In_Csum WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub41ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S5401:=S5401-T5_Sub41Gssum.AsFloat;
    T5_Sub41.Delete;

  end; end; }

end;

procedure TBase10.T5_Sub41BeforePost(DataSet: TDataSet);
begin

{ if(T5_Sub41.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO In_Csum '+
    '(Gdate, Scode, Gcode, Hcode, Gssum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gssum  )';

    Translate(Sqlen, '@Gdate', T5_Sub41Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub41Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub41Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub41Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub41Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'IN_CSUM_ID_GEN');

    S5401:=S5401+T5_Sub41Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE In_Csum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gssum=  @Gssum  WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub41Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub41Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub41Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub41Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub41Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub41ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S5401:=S5401+T5_Sub41Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T5_Sub41BeforeClose(DataSet: TDataSet);
begin
{ With T5_Sub41 do
  if(State in dsEditModes)Then Post; }
end;

//--초기재고--//
procedure TBase10.T5_Sub42AfterCancel(DataSet: TDataSet);
begin
  T5_Sub42AfterScroll(T5_Sub42);
end;

procedure TBase10.T5_Sub42AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T5_Sub42.FieldByName('Gdate').AsString;
  Gssum:=-T5_Sub42.FieldByName('Gssum').AsFloat; }
end;

procedure TBase10.T5_Sub42AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub42AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM In_Csum WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub42ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S5402:=S5402-T5_Sub42Gssum.AsFloat;
    T5_Sub42.Delete;

  end; end; }

end;

procedure TBase10.T5_Sub42BeforePost(DataSet: TDataSet);
begin

{ if(T5_Sub42.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO In_Csum '+
    '(Gdate, Scode, Gcode, Hcode, Gssum) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gssum  )';

    Translate(Sqlen, '@Gdate', T5_Sub42Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub42Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub42Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub42Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub42Gssum.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'IN_CSUM_ID_GEN');

    S5402:=S5402+T5_Sub42Gssum.AsFloat;

  end else begin

    Sqlen := 'UPDATE In_Csum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gssum=  @Gssum  WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T5_Sub42Gdate.AsString);
    Translate(Sqlen, '@Scode', T5_Sub42Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub42Gcode.AsString);
    Translate(Sqlen, '@Hcode', T5_Sub42Hcode.AsString);
    TransAuto(Sqlen, '@Gssum', T5_Sub42Gssum.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub42ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S5402:=S5402+T5_Sub42Gssum.AsFloat+Gssum;

  end; }

end;

procedure TBase10.T5_Sub42BeforeClose(DataSet: TDataSet);
begin
{ With T5_Sub42 do
  if(State in dsEditModes)Then Post; }
end;

//--초기계정금--//
procedure TBase10.T5_Sub51AfterCancel(DataSet: TDataSet);
begin
  T5_Sub51AfterScroll(T5_Sub51);
end;

procedure TBase10.T5_Sub51AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T5_Sub51.FieldByName('Gdate').AsString;
  Gosum:=-T5_Sub51.FieldByName('Clas1').AsFloat;
  Gbsum:=-T5_Sub51.FieldByName('Clas2').AsFloat;
  Gjsum:=-T5_Sub51.FieldByName('Clas3').AsFloat; }
end;

procedure TBase10.T5_Sub51AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub51AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM H1_Gbun WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub51ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S5501:=S5501-T5_Sub51Clas1.AsFloat;
    S5502:=S5502-T5_Sub51Clas2.AsFloat;
    S5503:=S5503-T5_Sub51Clas3.AsFloat;
    T5_Sub51.Delete;

  end; end; }

end;

procedure TBase10.T5_Sub51BeforePost(DataSet: TDataSet);
begin

{ if(T5_Sub51.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H1_Gbun '+
    '(Scode, Gcode, Gname, Oname, Gdate, Clas1, '+
    ' Clas2, Clas3, Hcode ) VALUES '+
    '(''@Scode'',''@Gcode'',''@Gname'',''@Oname'',''@Gdate'',  @Clas1, '+
    '   @Clas2  ,  @Clas3  ,''@Hcode'' )';

    Translate(Sqlen, '@Scode', T5_Sub51Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub51Gcode.AsString);
    Translate(Sqlen, '@Gname', T5_Sub51Gname.AsString);
    Translate(Sqlen, '@Oname', T5_Sub51Oname.AsString);
    Translate(Sqlen, '@Gdate', T5_Sub51Gdate.AsString);
    TransAuto(Sqlen, '@Clas1', T5_Sub51Clas1.AsString);
    TransAuto(Sqlen, '@Clas2', T5_Sub51Clas2.AsString);
    TransAuto(Sqlen, '@Clas3', T5_Sub51Clas3.AsString);
    TransAuto(Sqlen, '@Hcode', T5_Sub51Hcode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'H1_GBUN_ID_GEN');

    S5501:=S5501+T5_Sub51Clas1.AsFloat;
    S5502:=S5502+T5_Sub51Clas2.AsFloat;
    S5503:=S5503+T5_Sub51Clas3.AsFloat;

  end else begin

    Sqlen := 'UPDATE H1_Gbun SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Gname=''@Gname'',Oname=''@Oname'', '+
    'Gdate=''@Gdate'',Clas1=  @Clas1  ,Clas2=  @Clas2  ,Clas3=  @Clas3    '+
    'WHERE ID=@ID and Hcode=''@Hcode''';

    Translate(Sqlen, '@Scode', T5_Sub51Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub51Gcode.AsString);
    Translate(Sqlen, '@Gname', T5_Sub51Gname.AsString);
    Translate(Sqlen, '@Oname', T5_Sub51Oname.AsString);
    Translate(Sqlen, '@Gdate', T5_Sub51Gdate.AsString);
    TransAuto(Sqlen, '@Clas1', T5_Sub51Clas1.AsString);
    TransAuto(Sqlen, '@Clas2', T5_Sub51Clas2.AsString);
    TransAuto(Sqlen, '@Clas3', T5_Sub51Clas3.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub51ID.AsString);
    TransAuto(Sqlen, '@Hcode', T5_Sub51Hcode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S5501:=S5501+T5_Sub51Clas1.AsFloat+Gosum;
    S5502:=S5502+T5_Sub51Clas2.AsFloat+Gbsum;
    S5503:=S5503+T5_Sub51Clas3.AsFloat+Gjsum;

  end; }

end;

procedure TBase10.T5_Sub51BeforeClose(DataSet: TDataSet);
begin
{ With T5_Sub51 do
  if(State in dsEditModes)Then Post; }
end;

//--초기계정금--//
procedure TBase10.T5_Sub52AfterCancel(DataSet: TDataSet);
begin
  T5_Sub52AfterScroll(T5_Sub52);
end;

procedure TBase10.T5_Sub52AfterScroll(DataSet: TDataSet);
begin
{ Gdate:= T5_Sub52.FieldByName('Gdate').AsString;
  Gosum:=-T5_Sub52.FieldByName('Clas1').AsFloat;
  Gbsum:=-T5_Sub52.FieldByName('Clas2').AsFloat;
  Gjsum:=-T5_Sub52.FieldByName('Clas3').AsFloat; }
end;

procedure TBase10.T5_Sub52AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T5_Sub52AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

{ MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM H2_Gbun WHERE ID=@ID ';
    TransAuto(Sqlen, '@ID',    T5_Sub52ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    S5504:=S5504-T5_Sub52Clas1.AsFloat;
    S5505:=S5505-T5_Sub52Clas2.AsFloat;
    S5506:=S5506-T5_Sub52Clas3.AsFloat;
    T5_Sub52.Delete;

  end; end; }

end;

procedure TBase10.T5_Sub52BeforePost(DataSet: TDataSet);
begin

{ if(T5_Sub52.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H2_Gbun '+
    '(Scode, Gcode, Gname, Oname, Gdate, Clas1, '+
    ' Clas2, Clas3, Hcode ) VALUES '+
    '(''@Scode'',''@Gcode'',''@Gname'',''@Oname'',''@Gdate'',  @Clas1, '+
    '   @Clas2  ,  @Clas3  ,''@Hcode'' )';

    Translate(Sqlen, '@Scode', T5_Sub52Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub52Gcode.AsString);
    Translate(Sqlen, '@Gname', T5_Sub52Gname.AsString);
    Translate(Sqlen, '@Oname', T5_Sub52Oname.AsString);
    Translate(Sqlen, '@Gdate', T5_Sub52Gdate.AsString);
    TransAuto(Sqlen, '@Clas1', T5_Sub52Clas1.AsString);
    TransAuto(Sqlen, '@Clas2', T5_Sub52Clas2.AsString);
    TransAuto(Sqlen, '@Clas3', T5_Sub52Clas3.AsString);
    TransAuto(Sqlen, '@Hcode', T5_Sub52Hcode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(mSqry,'H2_GBUN_ID_GEN');

    S5504:=S5504+T5_Sub52Clas1.AsFloat;
    S5505:=S5505+T5_Sub52Clas2.AsFloat;
    S5506:=S5506+T5_Sub52Clas3.AsFloat;

  end else begin

    Sqlen := 'UPDATE H2_Gbun SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Gname=''@Gname'',Oname=''@Oname'', '+
    'Gdate=''@Gdate'',Clas1=  @Clas1  ,Clas2=  @Clas2  ,Clas3=  @Clas3    '+
    'WHERE ID=@ID and Hcode=''@Hcode''';

    Translate(Sqlen, '@Scode', T5_Sub52Scode.AsString);
    Translate(Sqlen, '@Gcode', T5_Sub52Gcode.AsString);
    Translate(Sqlen, '@Gname', T5_Sub52Gname.AsString);
    Translate(Sqlen, '@Oname', T5_Sub52Oname.AsString);
    Translate(Sqlen, '@Gdate', T5_Sub52Gdate.AsString);
    TransAuto(Sqlen, '@Clas1', T5_Sub52Clas1.AsString);
    TransAuto(Sqlen, '@Clas2', T5_Sub52Clas2.AsString);
    TransAuto(Sqlen, '@Clas3', T5_Sub52Clas3.AsString);
    TransAuto(Sqlen, '@ID',    T5_Sub52ID.AsString);
    TransAuto(Sqlen, '@Hcode', T5_Sub52Hcode.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    S5504:=S5504+T5_Sub52Clas1.AsFloat+Gosum;
    S5505:=S5505+T5_Sub52Clas2.AsFloat+Gbsum;
    S5506:=S5506+T5_Sub52Clas3.AsFloat+Gjsum;

  end; }

end;

procedure TBase10.T5_Sub52BeforeClose(DataSet: TDataSet);
begin
{ With T5_Sub52 do
  if(State in dsEditModes)Then Post; }
end;

//--New Data--//
procedure TBase10.T1_Sub11NewRecord(DataSet: TDataSet);
begin
  T1_Sub11Grat1.Value :=0; T1_Sub11Grat2.Value :=0;
  T1_Sub11Grat3.Value :=0; T1_Sub11Grat4.Value :=0;
  T1_Sub11Grat5.Value :=0; T1_Sub11Grat6.Value :=0;
  T1_Sub11Grat7.Value :=0; T1_Sub11Grat8.Value :=0;
  T1_Sub11Grat9.Value :=0; T1_Sub11Gqut1.Value :=0;
end;

procedure TBase10.T1_Sub21NewRecord(DataSet: TDataSet);
begin
  T1_Sub21Grat1.Value :=0; T1_Sub21Grat2.Value :=0;
  T1_Sub21Grat3.Value :=0; T1_Sub21Grat4.Value :=0;
  T1_Sub21Grat5.Value :=0; T1_Sub21Grat6.Value :=0;
  T1_Sub21Grat7.Value :=0; T1_Sub21Grat8.Value :=0;
  T1_Sub21Grat9.Value :=0; T1_Sub21Gqut1.Value :=0;
end;

procedure TBase10.T1_Sub31NewRecord(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T1_Sub41NewRecord(DataSet: TDataSet);
begin
  T1_Sub41Gdang.Value :=0;
  T1_Sub41Grat1.Value :=0; T1_Sub41Grat2.Value :=0;
  T1_Sub41Grat3.Value :=0; T1_Sub41Grat4.Value :=0;
end;

procedure TBase10.T1_Sub51NewRecord(DataSet: TDataSet);
begin
  T1_Sub51Grat1.Value :=0; T1_Sub51Grat2.Value :=0;
  T1_Sub51Grat3.Value :=0; T1_Sub51Grat4.Value :=0;
  T1_Sub51Grat5.Value :=0; T1_Sub51Grat6.Value :=0;
  T1_Sub51Grat7.Value :=0; T1_Sub51Grat8.Value :=0;
  T1_Sub51Grat9.Value :=0; T1_Sub51Gqut1.Value :=0;
end;

procedure TBase10.T1_Sub61NewRecord(DataSet: TDataSet);
begin
  T1_Sub61Gcode.Value :=Sobo16.Edit101.Text;
  T1_Sub61Hcode.Value :=Sobo16.Edit307.Text;
end;

procedure TBase10.T1_Sub62NewRecord(DataSet: TDataSet);
begin
  T1_Sub62Bcode.Value :=Sobo16.Edit201.Text;
  T1_Sub62Hcode.Value :=Sobo16.Edit307.Text;
  T1_Sub62Gssum.Value :=Gssum;
end;

procedure TBase10.T1_Sub71NewRecord(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T1_Sub72NewRecord(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T1_Sub81NewRecord(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T1_Sub82NewRecord(DataSet: TDataSet);
begin
//
end;

procedure TBase10.T2_Sub11NewRecord(DataSet: TDataSet);
begin
  T2_Sub11Scode.Value:='X';
  T2_Sub11Gdate.Value:=Sobo21.Edit101.Text;
  T2_Sub11Gubun.Value:=Sobo21.Edit102.Text;
  T2_Sub11Jubun.Value:=Sobo21.Edit103.Text;
  T2_Sub11Gcode.Value:=Sobo21.Edit104.Text;
  T2_Sub11Gjisa.Value:=Sobo21.Edit106.Text;
  T2_Sub11Hcode.Value:=Sobo21.Edit107.Text;
  T2_Sub11Ocode.Value:='B';
  T2_Sub11Yesno.Value:='1';
  T2_Sub11Pubun.Value:=Pubun;
  if Pubun='' Then begin
  if Sobo21.Edit102.Text='출고' Then
  T2_Sub11Pubun.Value:='위탁';
  if Sobo21.Edit102.Text='반품' Then
  T2_Sub11Pubun.Value:='비품'; end;
  T2_Sub11Gsqut.Value:=0; T2_Sub11Gdang.Value:=0;
  T2_Sub11Grat1.Value:=0; T2_Sub11Gssum.Value:=0;
  T2_Sub11Jeago.Value:=0;
end;

procedure TBase10.T2_Sub21NewRecord(DataSet: TDataSet);
begin
  T2_Sub21Scode.Value:='Y';
  T2_Sub21Gdate.Value:=Sobo22.Edit101.Text;
  T2_Sub21Gubun.Value:=Sobo22.Edit102.Text;
  T2_Sub21Jubun.Value:=Sobo22.Edit103.Text;
  T2_Sub21Gcode.Value:=Sobo22.Edit104.Text;
  T2_Sub21Gjisa.Value:=Sobo22.Edit106.Text;
  T2_Sub21Hcode.Value:=Sobo22.Edit107.Text;
  T2_Sub21Ocode.Value:='B';
  T2_Sub21Yesno.Value:='1';
  T2_Sub21Pubun.Value:=Pubun;
  if Pubun='' Then begin
  if Sobo22.Edit102.Text='입고' Then
  T2_Sub21Pubun.Value:='신간';
  if Sobo22.Edit102.Text='반품' Then
  T2_Sub21Pubun.Value:='반품'; end;
  T2_Sub21Gsqut.Value:=0; T2_Sub21Gdang.Value:=0;
  T2_Sub21Grat1.Value:=0; T2_Sub21Gssum.Value:=0;
  T2_Sub21Jeago.Value:=0;
end;

procedure TBase10.T2_Sub31NewRecord(DataSet: TDataSet);
begin
  if Sobo23.Edit104.Text='' then
  T2_Sub31Scode.Value:='Z' else
  T2_Sub31Scode.Value:='X';
  T2_Sub31Gdate.Value:=Sobo23.Edit101.Text;
  T2_Sub31Gubun.Value:=Sobo23.Edit102.Text;
  T2_Sub31Jubun.Value:=Sobo23.Edit103.Text;
  T2_Sub31Gcode.Value:=Sobo23.Edit104.Text;
  T2_Sub31Gjisa.Value:=Sobo23.Edit106.Text;
  T2_Sub31Hcode.Value:=Sobo23.Edit107.Text;
  T2_Sub31Ocode.Value:='B';
  T2_Sub31Yesno.Value:='1';
  T2_Sub31Pubun.Value:=Pubun;
  if Pubun='' Then begin
  if Sobo23.Edit102.Text='출고' Then
  T2_Sub31Pubun.Value:='위탁';
  if Sobo23.Edit102.Text='반품' Then
  T2_Sub31Pubun.Value:='비품'; end;
  T2_Sub31Gsqut.Value:=0; T2_Sub31Gdang.Value:=0;
  T2_Sub31Grat1.Value:=0; T2_Sub31Gssum.Value:=0;
  T2_Sub31Jeago.Value:=0;
end;

procedure TBase10.T2_Sub41NewRecord(DataSet: TDataSet);
begin
  T2_Sub41Scode.Value:='Y';
  T2_Sub41Hcode.Value:=Sobo24.Edit107.Text;
  T2_Sub41Jubun.Value:='';
  T2_Sub41Gcode.Value:='';
  T2_Sub41Gjisa.Value:='';
  T2_Sub41Ocode.Value:='B';
  T2_Sub41Yesno.Value:='2';
  T2_Sub41Gubun.Value:='입고';
  T2_Sub41Pubun.Value:='반품';
  T2_Sub41Gsqut.Value:=0; T2_Sub41Gdang.Value:=0;
  T2_Sub41Grat1.Value:=0; T2_Sub41Gssum.Value:=0;
  T2_Sub41Jeago.Value:=0;
  if Gdate<>'' Then
  T2_Sub41Gdate.Value:=Gdate else
  T2_Sub41Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TBase10.T2_Sub51NewRecord(DataSet: TDataSet);
begin
  T2_Sub51Scode.Value:='X';
  T2_Sub51Hcode.Value:=Sobo25.Edit107.Text;
  T2_Sub51Jubun.Value:='';
  T2_Sub51Gcode.Value:='';
  T2_Sub51Gjisa.Value:='';
  T2_Sub51Ocode.Value:='B';
  T2_Sub51Yesno.Value:='2';
  T2_Sub51Gubun.Value:='반품';
  T2_Sub51Pubun.Value:='비품';
  T2_Sub51Gsqut.Value:=0; T2_Sub51Gdang.Value:=0;
  T2_Sub51Grat1.Value:=0; T2_Sub51Gssum.Value:=0;
  T2_Sub51Jeago.Value:=0;
  if Gdate<>'' Then
  T2_Sub51Gdate.Value:=Gdate else
  T2_Sub51Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TBase10.T2_Sub61NewRecord(DataSet: TDataSet);
begin
{ T2_Sub61Gubun.Value:=Sobo26.Edit103.Text;
  T2_Sub61Bcode.Value:=Sobo26.Edit104.Text;
  T2_Sub61Ycode.Value:=Sobo26.Edit107.Text;
  T2_Sub61Gssum.Value:=0;
  if Gdate<>'' Then
  T2_Sub61Gdate.Value:=Gdate else
  T2_Sub61Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T2_Sub62NewRecord(DataSet: TDataSet);
begin
{ T2_Sub62Gubun.Value:=Sobo26.Edit203.Text;
  T2_Sub62Gcode.Value:=Sobo26.Edit204.Text;
  T2_Sub62Ycode.Value:=Sobo26.Edit207.Text;
  T2_Sub62Gssum.Value:=0;
  if Gdate<>'' Then
  T2_Sub62Gdate.Value:=Gdate else
  T2_Sub62Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T2_Sub81NewRecord(DataSet: TDataSet);
begin
  T2_Sub81Hcode.Value:=Sobo13.Edit107.Text;
  T2_Sub81Gname.Value:='시내';
end;

procedure TBase10.T2_Sub91NewRecord(DataSet: TDataSet);
begin
  T2_Sub91Scode.Value:='X';
  T2_Sub91Gdate.Value:=Sobo29.Edit101.Text;
  T2_Sub91Gubun.Value:=Sobo29.Edit102.Text;
  T2_Sub91Jubun.Value:=Sobo29.Edit103.Text;
  T2_Sub91Bcode.Value:=Sobo29.Edit104.Text;
  T2_Sub91Gjisa.Value:=Sobo29.Edit109.Text;
  T2_Sub91Hcode.Value:=Sobo29.Edit107.Text;
  T2_Sub91Ocode.Value:='B';
  T2_Sub91Yesno.Value:='1';
  T2_Sub91Pubun.Value:=Sobo29.Edit106.Text;
{ if Pubun='' Then begin
  if Sobo29.Edit102.Text='출고' Then
  T2_Sub91Pubun.Value:='위탁';
  if Sobo29.Edit102.Text='반품' Then
  T2_Sub91Pubun.Value:='비품'; end; }
  T2_Sub91Gsqut.Value:=0; T2_Sub91Gdang.Value:=0;
  T2_Sub91Grat1.Value:=0; T2_Sub91Gssum.Value:=0;
  T2_Sub91Jeago.Value:=0;
end;

procedure TBase10.T3_Sub81NewRecord(DataSet: TDataSet);
begin
{ if Sobo16.RadioButton101.Checked=True Then
  T3_Sub81Scode.Value:='A';
  if Sobo16.RadioButton102.Checked=True Then
  T3_Sub81Scode.Value:='B';
  if Sobo16.RadioButton103.Checked=True Then
  T3_Sub81Scode.Value:='C'; }
end;

procedure TBase10.T3_Sub82NewRecord(DataSet: TDataSet);
begin
//T3_Sub82Scode.Value:='D';
end;

procedure TBase10.T4_Sub11NewRecord(DataSet: TDataSet);
begin
  T4_Sub11Gdate.Value:=Sobo41.Edit101.Text;
  T4_Sub11Pubun.Value:='현금';
  T4_Sub11Gssum.Value:=0;
end;

procedure TBase10.T4_Sub12NewRecord(DataSet: TDataSet);
begin
{ T4_Sub12Gubun.Value:='출금';
  T4_Sub12Pubun.Value:='현금';
  T4_Sub12Hcode.Value:=Sobo41.Edit207.Text;
  T4_Sub12Scode.Value:='Y';
  T4_Sub12Gssum.Value:=0;
  if Gdate<>'' Then
  T4_Sub12Gdate.Value:=Gdate else
  T4_Sub12Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T4_Sub21NewRecord(DataSet: TDataSet);
begin
{ T4_Sub21Gubun.Value:='입금';
  T4_Sub21Pubun.Value:='현금';
  T4_Sub21Hcode.Value:=Sobo42.Edit107.Text;
  T4_Sub21Scode.Value:='A';
  T4_Sub21Gssum.Value:=0;
  if Gdate<>'' Then
  T4_Sub21Gdate.Value:=Gdate else
  T4_Sub21Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T4_Sub22NewRecord(DataSet: TDataSet);
begin
{ T4_Sub22Gubun.Value:='출금';
  T4_Sub22Pubun.Value:='현금';
  T4_Sub22Hcode.Value:=Sobo42.Edit207.Text;
  T4_Sub22Scode.Value:='B';
  T4_Sub22Gssum.Value:=0;
  if Gdate<>'' Then
  T4_Sub22Gdate.Value:=Gdate else
  T4_Sub22Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T4_Sub31NewRecord(DataSet: TDataSet);
begin
  T4_Sub31Gssum.Value:=0;
  T4_Sub31Gdate.Value:=Sobo43.Edit101.Text;
end;

procedure TBase10.T4_Sub61NewRecord(DataSet: TDataSet);
begin
  T4_Sub61ID.Value:=0;
  T4_Sub61Grat1.Value:=0;
  T4_Sub61Gosum.Value:=0;
  T4_Sub61Gssum.Value:=0;
  T4_Sub61Date1.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
  T4_Sub61Date2.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
  T4_Sub61Date3.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
  T4_Sub61Date4.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TBase10.T4_Sub62NewRecord(DataSet: TDataSet);
begin
  T4_Sub62ID.Value:=0;
  T4_Sub62Class.Value:=0;
  T4_Sub62Gsusu.Value:=0;
  T4_Sub62Gssum.Value:=0;
  T4_Sub62Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TBase10.T5_Sub11NewRecord(DataSet: TDataSet);
begin
  T5_Sub11Hcode.Value:=Sobo51.Edit107.Text;
  T5_Sub11Scode.Value:='D';
  T5_Sub11Gssum.Value:=0;
  T5_Sub11Gosum.Value:=0;
  T5_Sub11Gbsum.Value:=0;
  if Gdate<>'' Then
  T5_Sub11Gdate.Value:=Gdate else
  T5_Sub11Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TBase10.T5_Sub12NewRecord(DataSet: TDataSet);
begin
{ T5_Sub12Hcode.Value:=Sobo51.Edit207.Text;
  if Sobo51.Panel202.Caption='입고처명' Then
  T5_Sub12Scode.Value:='Y';
  T5_Sub12Gssum.Value:=0;
  T5_Sub12Gosum.Value:=0;
  T5_Sub12Gbsum.Value:=0;
  if Gdate<>'' Then
  T5_Sub12Gdate.Value:=Gdate else
  T5_Sub12Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T5_Sub21NewRecord(DataSet: TDataSet);
begin
  T5_Sub21Hcode.Value:=Sobo52.Edit107.Text;
  T5_Sub21Scode.Value:='B';
  T5_Sub21Gssum.Value:=0;
  T5_Sub21Gosum.Value:=0;
  T5_Sub21Gbsum.Value:=0;
  if Gdate<>'' Then
  T5_Sub21Gdate.Value:=Gdate else
  T5_Sub21Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TBase10.T5_Sub22NewRecord(DataSet: TDataSet);
begin
{ T5_Sub22Hcode.Value:=Sobo52.Edit207.Text;
  T5_Sub22Scode.Value:='B';
  T5_Sub22Gssum.Value:=0;
  T5_Sub22Gosum.Value:=0;
  T5_Sub22Gbsum.Value:=0;
  if Gdate<>'' Then
  T5_Sub22Gdate.Value:=Gdate else
  T5_Sub22Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T5_Sub31NewRecord(DataSet: TDataSet);
begin
{ T5_Sub31Hcode.Value:=Sobo53.Edit107.Text;
  if Sobo53.Panel101.Caption='거래처명' Then
  T5_Sub31Scode.Value:='X';
  if Sobo53.Panel101.Caption='거 래 처' Then
  T5_Sub31Scode.Value:='Z';
  T5_Sub31Gssum.Value:=0;
  if Gdate<>'' Then
  T5_Sub31Gdate.Value:=Gdate else
  T5_Sub31Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T5_Sub32NewRecord(DataSet: TDataSet);
begin
{ T5_Sub32Hcode.Value:=Sobo53.Edit207.Text;
  if Sobo53.Panel201.Caption='입고처명' Then
  T5_Sub32Scode.Value:='Y';
  T5_Sub32Gssum.Value:=0;
  if Gdate<>'' Then
  T5_Sub32Gdate.Value:=Gdate else
  T5_Sub32Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T5_Sub41NewRecord(DataSet: TDataSet);
begin
{ T5_Sub41Hcode.Value:=Sobo54.Edit107.Text;
  T5_Sub41Scode.Value:='A';
  T5_Sub41Gssum.Value:=0;
  if Gdate<>'' Then
  T5_Sub41Gdate.Value:=Gdate else
  T5_Sub41Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T5_Sub42NewRecord(DataSet: TDataSet);
begin
{ T5_Sub42Hcode.Value:=Sobo54.Edit207.Text;
  T5_Sub42Scode.Value:='B';
  T5_Sub42Gssum.Value:=0;
  if Gdate<>'' Then
  T5_Sub42Gdate.Value:=Gdate else
  T5_Sub42Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T5_Sub51NewRecord(DataSet: TDataSet);
begin
{ T5_Sub51Hcode.Value:=Sobo55.Edit107.Text;
  if Sobo55.RadioButton101.Checked=True Then
  T5_Sub51Scode.Value:='1';
  if Sobo55.RadioButton102.Checked=True Then
  T5_Sub51Scode.Value:='2';
  if Sobo55.RadioButton103.Checked=True Then
  T5_Sub51Scode.Value:='3';
  if Sobo55.RadioButton104.Checked=True Then
  T5_Sub51Scode.Value:='0';
  T5_Sub51Clas1.Value:=0;
  T5_Sub51Clas2.Value:=0;
  T5_Sub51Clas3.Value:=0;
  if Gdate<>'' Then
  T5_Sub51Gdate.Value:=Gdate else
  T5_Sub51Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TBase10.T5_Sub52NewRecord(DataSet: TDataSet);
begin
{ T5_Sub52Hcode.Value:=Sobo55.Edit207.Text;
  T5_Sub52Clas1.Value:=0;
  T5_Sub52Clas2.Value:=0;
  T5_Sub52Clas3.Value:=0;
  if Gdate<>'' Then
  T5_Sub52Gdate.Value:=Gdate else
  T5_Sub52Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

//--New Calcf--//
procedure TBase10.T1_Sub11CalcFields(DataSet: TDataSet);
var St1,St2,St3: String;
begin

  St1 := 'Select Gubun,Jubun,Ocode,Gposa,Gnumb,Guper,Gjomo,Gtel1,Gtel2,Gfax1,Gfax2,Gpost,Gadd1,Gadd2,';
  St2 := ' Gpper,Gbigo,Name1,Name2,Email,Yesno,Hcode,Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Grat7,Grat9 ';
  St3 := 'From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';

  Translate(St3, '@Gcode', T1_Sub11.FieldByName('Gcode').AsString);
  Translate(St3, '@Hcode', '');

  Base10.Socket.RunSQL(St1+St2+St3);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
  //T1_Sub11.FieldByName('Gubun').AsString:=Base10.Socket.GetData(1, 1);
    T1_Sub11.FieldByName('Jubun').AsString:=Base10.Socket.GetData(1, 2);
    T1_Sub11.FieldByName('Ocode').AsString:=Base10.Socket.GetData(1, 3);
    T1_Sub11.FieldByName('Gposa').AsString:=Base10.Socket.GetData(1, 4);
    T1_Sub11.FieldByName('Gnumb').AsString:=Base10.Socket.GetData(1, 5);
    T1_Sub11.FieldByName('Guper').AsString:=Base10.Socket.GetData(1, 6);
    T1_Sub11.FieldByName('Gjomo').AsString:=Base10.Socket.GetData(1, 7);
    T1_Sub11.FieldByName('Gtel1').AsString:=Base10.Socket.GetData(1, 8);
    T1_Sub11.FieldByName('Gtel2').AsString:=Base10.Socket.GetData(1, 9);
    T1_Sub11.FieldByName('Gfax1').AsString:=Base10.Socket.GetData(1,10);
    T1_Sub11.FieldByName('Gfax2').AsString:=Base10.Socket.GetData(1,11);
    T1_Sub11.FieldByName('Gpost').AsString:=Base10.Socket.GetData(1,12);
    T1_Sub11.FieldByName('Gadd1').AsString:=Base10.Socket.GetData(1,13);
    T1_Sub11.FieldByName('Gadd2').AsString:=Base10.Socket.GetData(1,14);
    T1_Sub11.FieldByName('Gpper').AsString:=Base10.Socket.GetData(1,15);
    T1_Sub11.FieldByName('Gbigo').AsString:=Base10.Socket.GetData(1,16);
    T1_Sub11.FieldByName('Name1').AsString:=Base10.Socket.GetData(1,17);
    T1_Sub11.FieldByName('Name2').AsString:=Base10.Socket.GetData(1,18);
    T1_Sub11.FieldByName('Email').AsString:=Base10.Socket.GetData(1,19);
    T1_Sub11.FieldByName('Yesno').AsString:=Base10.Socket.GetData(1,20);
    T1_Sub11.FieldByName('Hcode').AsString:=Base10.Socket.GetData(1,21);
    T1_Sub11.FieldByName('Grat1').AsString:=Base10.Socket.GetData(1,22);
    T1_Sub11.FieldByName('Grat2').AsString:=Base10.Socket.GetData(1,23);
    T1_Sub11.FieldByName('Grat3').AsString:=Base10.Socket.GetData(1,24);
    T1_Sub11.FieldByName('Grat4').AsString:=Base10.Socket.GetData(1,25);
    T1_Sub11.FieldByName('Grat5').AsString:=Base10.Socket.GetData(1,26);
    T1_Sub11.FieldByName('Grat6').AsString:=Base10.Socket.GetData(1,27);
    T1_Sub11.FieldByName('Grat7').AsString:=Base10.Socket.GetData(1,28);
    T1_Sub11.FieldByName('Grat9').AsString:=Base10.Socket.GetData(1,29);
    T1_Sub11.FieldByName('Gtels').AsString:=T1_Sub11.FieldByName('Gtel1').AsString+
                                        '-'+T1_Sub11.FieldByName('Gtel2').AsString;
    T1_Sub11.FieldByName('Gfaxs').AsString:=T1_Sub11.FieldByName('Gfax1').AsString+
                                        '-'+T1_Sub11.FieldByName('Gfax2').AsString;
    T1_Sub11.FieldByName('Gadds').AsString:=T1_Sub11.FieldByName('Gadd1').AsString+
                                        ' '+T1_Sub11.FieldByName('Gadd2').AsString;
  end;

  St1 := 'Select Gname From G1_Gbun Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';

  Translate(St1, '@Gcode', T1_Sub11.FieldByName('Gubun').AsString);
  Translate(St1, '@Hcode', '');

  Base10.Socket.RunSQL(St1);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    if Base10.Socket.GetData(1, 1)='' then
    T1_Sub11.FieldByName('Sname').AsString:='' else
    T1_Sub11.FieldByName('Sname').AsString:=Base10.Socket.GetData(1, 1);
  end;

end;

procedure TBase10.T2_Sub82CalcFields(DataSet: TDataSet);
var St1,St2: Double;
begin
  St1:=T2_Sub82.FieldByName('Gnums').AsFloat;
       if (St1>00) and (St1<=03) Then St2:=01
  else if (St1>03) and (St1<=06) Then St2:=02
  else if (St1>06) and (St1<=09) Then St2:=03
  else if (St1>09) and (St1<=12) Then St2:=04
  else if (St1>12) and (St1<=15) Then St2:=05
  else if (St1>15) and (St1<=18) Then St2:=06
  else if (St1>18) and (St1<=21) Then St2:=07
  else if (St1>21) and (St1<=24) Then St2:=08
  else if (St1>24) and (St1<=27) Then St2:=09
  else if (St1>27) and (St1<=30) Then St2:=10
  else if (St1>30) and (St1<=33) Then St2:=11
  else if (St1>33) and (St1<=36) Then St2:=12
  else if (St1>36) and (St1<=39) Then St2:=13
  else if (St1>39) and (St1<=42) Then St2:=14
  else if (St1>42) and (St1<=45) Then St2:=15
  else if (St1>45) and (St1<=47) Then St2:=16
  else if (St1>47) and (St1<=50) Then St2:=17
  else if (St1>50) and (St1<=53) Then St2:=18
  else if (St1>53) and (St1<=56) Then St2:=19
  else if (St1>56) and (St1<=59) Then St2:=20;
  T2_Sub82.FieldByName('Gnum1').AsFloat:=St2;
  T2_Sub82.FieldByName('Gnum2').AsFloat:=St1;
{ T2_Sub82.FieldByName('GsumX').AsFloat:=
  T2_Sub82.FieldByName('Gssum').AsFloat-T2_Sub82.FieldByName('Gbsum').AsFloat; }
end;

procedure TBase10._Gs_Gsum_(St0,St1,St2,St3,Field1,Field2:String;Sq1,Sq2:Double);
var Ts1,Ts2: Double;
begin
{
  Sqlen := 'Select %Gqut1,%Gsum1 From Gs_Gsum Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gsum1', Field2);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);

    Sqlen := 'UPDATE Gs_Gsum SET '+
    '%Gqut1=@Gqut1 ,%Gsum1=@Gsum1 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts2+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Gs_Gsum '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gsum1) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;
}
end;

procedure TBase10._Gs_Csum_(St0,St1,St2,St3,Field1,Field2:String;Sq1,Sq2:Double);
var Ts1,Ts2: Double;
begin
{
  Sqlen := 'Select %Gqut1,%Gsum1 From Gs_Csum Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode''and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gsum1', Field2);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);

    Sqlen := 'UPDATE Gs_Csum SET '+
    '%Gqut1=@Gqut1 ,%Gsum1=@Gsum1 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts2+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Gs_Csum '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gsum1) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;
}
end;

procedure TBase10._Sv_Gsum_(St0,St1,St2,St4,St5,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3: Double;
begin
{
  Sqlen := 'Select %Gqut1,%Gsum1,%Gsum2 From Sv_Gsum Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gubun=''@Gubun'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gsum1', Field2);
  TransAuto(Sqlen, '%Gsum2', Field3);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Gubun', St4);
  Translate(Sqlen, '@Hcode', St5);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);

    Sqlen := 'UPDATE Sv_Gsum SET '+
    '%Gqut1=@Gqut1 ,%Gsum1=@Gsum1 ,%Gsum2=@Gsum2 WHERE '+
    'Gcode=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gubun=''@Gubun'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Gubun', St4);
    Translate(Sqlen, '@Hcode', St5);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts2+Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Ts3+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Gsum '+
    '(Gdate, Scode, Gcode, Gubun, Hcode, %Gqut1, %Gsum1, %Gsum2) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Gubun'',''@Hcode'',  @Gqut1  ,  @Gsum1,  @Gsum2  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Gubun', St4);
    Translate(Sqlen, '@Hcode', St5);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;
}
end;

procedure TBase10._Sv_Csum_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3: Double;
begin
{
  Sqlen := 'Select %Gqut1,%Gqut2,%Gsum1 From Sv_Csum Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gqut2', Field2);
  TransAuto(Sqlen, '%Gsum1', Field3);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);

    Sqlen := 'UPDATE Sv_Csum SET '+
    '%Gqut1=@Gqut1 ,%Gqut2=@Gqut2 ,%Gsum1=@Gsum1 WHERE '+
    'Gcode=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2+Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts3+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Csum '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gqut2, %Gsum1) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gqut2,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;
}
end;

procedure TBase10._Sv_Chng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gsum1,%Gsum2,Gdate From Sv_Chng Where '+D_Select+
  'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gsum1', Field2);
  TransAuto(Sqlen, '%Gsum2', Field3);

  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := 0;

    if St0 > Ts0 Then Ts4:=Sq2;

    Sqlen := 'UPDATE Sv_Chng SET '+
    '%Gqut1=@Gqut1 ,%Gsum1=@Gsum1 ,%Gsum2=@Gsum2 WHERE '+
    'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts2+Sq2)); }
    TransAuto(Sqlen, '@Gqut1', '0');
    TransAuto(Sqlen, '@Gsum1', '0');
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Ts3+Ts4));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Chng '+
    '(Scode, Gcode, Hcode, %Gqut1, %Gsum1, %Gsum2) VALUES '+
    '(''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gsum1  ,  @Gsum2  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2)); }
    TransAuto(Sqlen, '@Gqut1', '0');
    TransAuto(Sqlen, '@Gsum1', '0');
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sv_Chnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gsum1,%Gsum2,Gdate From Sv_Chng Where '+D_Select+
  'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gsum1', Field2);
  TransAuto(Sqlen, '%Gsum2', Field3);

  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := 0;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Chng SET '+
    '%Gqut1=@Gqut1 ,%Gsum1=@Gsum1 ,%Gsum2=@Gsum2 WHERE '+
    'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Ts4));
  { TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts2+Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Ts3+Sq2)); }
    TransAuto(Sqlen, '@Gsum1', '0');
    TransAuto(Sqlen, '@Gsum2', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Chng '+
    '(Scode, Gcode, Hcode, %Gqut1, %Gsum1, %Gsum2) VALUES '+
    '(''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gsum1  ,  @Gsum2  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
  { TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Sq2)); }
    TransAuto(Sqlen, '@Gsum1', '0');
    TransAuto(Sqlen, '@Gsum2', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sv_Ghng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gqut2,%Gsum1,Gdate From Sv_Ghng Where '+D_Select+
  'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gqut2', Field2);
  TransAuto(Sqlen, '%Gsum1', Field3);

  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := 0;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Ghng SET '+
    '%Gqut1=@Gqut1 ,%Gqut2=@Gqut2 ,%Gsum1=@Gsum1 WHERE '+
    'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2+Ts4));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts3+Sq2)); }
    TransAuto(Sqlen, '@Gqut1', '0');
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2+Ts4));
    TransAuto(Sqlen, '@Gsum1', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Ghng '+
    '(Scode, Gcode, Hcode, %Gqut1, %Gqut2, %Gsum1) VALUES '+
    '(''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gqut2  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2)); }
    TransAuto(Sqlen, '@Gqut1', '0');
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sv_Ghnb_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gqut2,%Gsum1,Gdate From Sv_Ghng Where '+D_Select+
  'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gqut2', Field2);
  TransAuto(Sqlen, '%Gsum1', Field3);

  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := 0;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Ghng SET '+
    '%Gqut1=@Gqut1 ,%Gqut2=@Gqut2 ,%Gsum1=@Gsum1 WHERE '+
    'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2-Ts4));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts3+Sq2)); }
    TransAuto(Sqlen, '@Gqut1', '0');
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2-Ts4));
    TransAuto(Sqlen, '@Gsum1', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Ghng '+
    '(Scode, Gcode, Hcode, %Gqut1, %Gqut2, %Gsum1) VALUES '+
    '(''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gqut2  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(-Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2)); }
    TransAuto(Sqlen, '@Gqut1', '0');
    TransAuto(Sqlen, '@Gqut2', FloatToStr(-Sq1));
    TransAuto(Sqlen, '@Gsum1', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sv_Ghnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gqut2,%Gsum1,Gdate From Sv_Ghng Where '+D_Select+
  'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gqut2', Field2);
  TransAuto(Sqlen, '%Gsum1', Field3);

  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := 0;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Ghng SET '+
    '%Gqut1=@Gqut1 ,%Gqut2=@Gqut2 ,%Gsum1=@Gsum1 WHERE '+
    'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Ts4));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts3+Sq2)); }
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Ts4));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2));
    TransAuto(Sqlen, '@Gsum1', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Ghng '+
    '(Scode, Gcode, Hcode, %Gqut1, %Gqut2, %Gsum1) VALUES '+
    '(''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gqut2  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
  { TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', '0');
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2)); }
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', '0');
    TransAuto(Sqlen, '@Gsum1', '0');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sg_Chng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gsum1,%Gsum2,Gdate From Sv_Chng Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gsum1', Field2);
  TransAuto(Sqlen, '%Gsum2', Field3);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := Sq2;

    if St0 > Ts0 Then Ts4:=Sq2;

    Sqlen := 'UPDATE Sv_Chng SET '+
    '%Gqut1=@Gqut1 ,%Gsum1=@Gsum1 ,%Gsum2=@Gsum2 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts2+Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Ts3+Ts4));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Chng '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gsum1, %Gsum2) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gsum1  ,  @Gsum2  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sg_Chnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gsum1,%Gsum2,Gdate From Sv_Chng Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gsum1', Field2);
  TransAuto(Sqlen, '%Gsum2', Field3);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := Sq1;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Chng SET '+
    '%Gqut1=@Gqut1 ,%Gsum1=@Gsum1 ,%Gsum2=@Gsum2 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Ts4));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts2+Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Ts3+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Chng '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gsum1, %Gsum2) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gsum1  ,  @Gsum2  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gsum1', Field2);
    TransAuto(Sqlen, '%Gsum2', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));
    TransAuto(Sqlen, '@Gsum2', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sg_Ghng_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gqut2,%Gsum1,Gdate From Sv_Ghng Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gqut2', Field2);
  TransAuto(Sqlen, '%Gsum1', Field3);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := Sq1;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Ghng SET '+
    '%Gqut1=@Gqut1 ,%Gqut2=@Gqut2 ,%Gsum1=@Gsum1 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2+Ts4));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts3+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Ghng '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gqut2, %Gsum1) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gqut2  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sg_Ghnb_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gqut2,%Gsum1,Gdate From Sv_Ghng Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gqut2', Field2);
  TransAuto(Sqlen, '%Gsum1', Field3);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := Sq1;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Ghng SET '+
    '%Gqut1=@Gqut1 ,%Gqut2=@Gqut2 ,%Gsum1=@Gsum1 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2-Ts4));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts3+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Ghng '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gqut2, %Gsum1) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gqut2  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(-Sq1));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._Sg_Ghnp_(St0,St1,St2,St3,Field1,Field2,Field3:String;Sq1,Sq2:Double);
var Ts1,Ts2,Ts3,Ts4: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gqut1,%Gqut2,%Gsum1,Gdate From Sv_Ghng Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gqut1', Field1);
  TransAuto(Sqlen, '%Gqut2', Field2);
  TransAuto(Sqlen, '%Gsum1', Field3);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts2 := StrToIntDef(Base10.Socket.GetData(1, 2),0);
    Ts3 := StrToIntDef(Base10.Socket.GetData(1, 3),0);
    Ts0 := Base10.Socket.GetData(1, 4);
    Ts4 := Sq1;

    if St0 > Ts0 Then Ts4:=Sq1;

    Sqlen := 'UPDATE Sv_Ghng SET '+
    '%Gqut1=@Gqut1 ,%Gqut2=@Gqut2 ,%Gsum1=@Gsum1 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Ts1+Ts4));
    TransAuto(Sqlen, '@Gqut2', FloatToStr(Ts2));
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts3+Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Ghng '+
    '(Gdate, Scode, Gcode, Hcode, %Gqut1, %Gqut2, %Gsum1) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gqut1  ,  @Gqut2  ,  @Gsum1  )';

    TransAuto(Sqlen, '%Gqut1', Field1);
    TransAuto(Sqlen, '%Gqut2', Field2);
    TransAuto(Sqlen, '%Gsum1', Field3);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gqut1', FloatToStr(Sq1));
    TransAuto(Sqlen, '@Gqut2', '0');
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq2));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._H1_Gbun_(St0,St1,St2,St3,Field1:String;Sq1:Double);
var Ts1: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gsum1,Gdate From H1_Gbun Where '+D_Select+
  'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gsum1', Field1);

  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts0 := Base10.Socket.GetData(1, 2);

    if St0 > Ts0 Then begin

    Sqlen := 'UPDATE H1_Gbun SET '+
    '%Gsum1=@Gsum1 WHERE '+
    'Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gsum1', Field1);

    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts1+Sq1));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end;
  end;

end;

procedure TBase10._H2_Gbun_(St0,St1,St2,St3,Field1:String;Sq1:Double);
var Ts1: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gsum1,Gdate From Sv_Gsum Where '+D_Select+
  'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gsum1', Field1);

  Translate(Sqlen, '@Gdate', St0);
  Translate(Sqlen, '@Scode', St1);
  Translate(Sqlen, '@Gcode', St2);
  Translate(Sqlen, '@Hcode', St3);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts0 := Base10.Socket.GetData(1, 2);

    Sqlen := 'UPDATE Sv_Gsum SET '+
    '%Gsum1=@Gsum1 WHERE '+
    'Gdate=''@Gdate'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gsum1', Field1);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts1+Sq1));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end else begin

    Sqlen := 'INSERT INTO Sv_Gsum '+
    '(Gdate, Scode, Gcode, Hcode, %Gsum1) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',  @Gsum1  )';

    TransAuto(Sqlen, '%Gsum1', Field1);

    Translate(Sqlen, '@Gdate', St0);
    Translate(Sqlen, '@Scode', St1);
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', St3);
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Sq1));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end;

end;

procedure TBase10._H5_Bang_(St0,St1,St2,Field1:String;Sq1:Double);
var Ts1: Double;
    Ts0: String;
begin

  Sqlen := 'Select %Gsum1,Gdate From H5_Bang Where '+D_Select+
  'ID=@ID and Hcode=''@Hcode''';

  TransAuto(Sqlen, '%Gsum1', Field1);

  TransAuto(Sqlen, '@ID', St1);
  Translate(Sqlen, '@Hcode', St2);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    Ts1 := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    Ts0 := Base10.Socket.GetData(1, 2);

    if St0 > Ts0 Then begin

    Sqlen := 'UPDATE H5_Bang SET '+
    '%Gsum1=@Gsum1 WHERE '+
    'ID=@ID and Hcode=''@Hcode''';

    TransAuto(Sqlen, '%Gsum1', Field1);

    TransAuto(Sqlen, '@ID', St1);
    Translate(Sqlen, '@Hcode', St2);
    TransAuto(Sqlen, '@Gsum1', FloatToStr(Ts1+Sq1));

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end;
  end;

end;

procedure TBase10._S_Repla1(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);
    if(St5='증정')Then begin

      _Gs_Gsum_(Sw0,St1,St2,St6,'Gjqut','Gjsum',Sq1,Sq2);
      _Sv_Gsum_(St0,St1,St2,St4,St6,'Gjqut','Gjsum','Gssum',Sq1,Sq2);
      _Sv_Chng_(St0,St1,St2,St6,'Gjqut','Gjsum','Gssum',Sq1,Sq2);

    end else
    if(St3='출고')
    or(St3='입고')Then begin

      _Gs_Gsum_(Sw0,St1,St2,St6,'Goqut','Gosum',Sq1,Sq2);
      _Sv_Gsum_(St0,St1,St2,St4,St6,'Goqut','Gosum','Gssum',Sq1,Sq2);
      _Sv_Chng_(St0,St1,St2,St6,'Goqut','Gosum','Gssum',Sq1,Sq2);

    end else
    if(St3='반품')Then begin

      _Gs_Gsum_(Sw0,St1,St2,St6,'Gbqut','Gbsum',Sq1,Sq2);
      _Sv_Gsum_(St0,St1,St2,St4,St6,'Gbqut','Gbsum','Gssum',Sq1,Sq2);
      _Sv_Chng_(St0,St1,St2,St6,'Gbqut','Gbsum','Gssum',Sq1,Sq2);

    end;
  end;
end;

procedure TBase10._B_Repla1(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);
    if(St3='입고')Then begin

      _Gs_Csum_(Sw0,St1,St2,St6,'Giqut','Gosum',Sq1, 0 );
      _Sv_Csum_(St0,St1,St2,St6,'Giqut','Gsusu','Gosum',Sq1, 0 );
      _Sv_Ghng_(St0,St1,St2,St6,'Giqut','Gsusu','Gosum',Sq1, 0 );

    end else
    if(St4='증정')Then begin

      _Gs_Csum_(Sw0,St1,St2,St6,'Gjqut','Gosum',Sq1, 0 );
      _Sv_Csum_(St0,St1,St2,St6,'Gjqut','Gsqut','Gosum',Sq1,Sq2);
      _Sv_Ghng_(St0,St1,St2,St6,'Gjqut','Gsqut','Gosum',Sq1,Sq2);

    end else
    if(St3='출고')Then begin

      _Gs_Csum_(Sw0,St1,St2,St6,'Goqut','Gosum',Sq1,Sq2);
      _Sv_Csum_(St0,St1,St2,St6,'Goqut','Gsqut','Gosum',Sq1,Sq2);
      _Sv_Ghng_(St0,St1,St2,St6,'Goqut','Gsqut','Gosum',Sq1,Sq2);

    end else
    if(St4='비품')or(St4='폐기')Then begin

      if(St5='Y')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Giqut','Gbsum',Sq1, 0 );
        _Sv_Csum_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
        _Sv_Ghng_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
      end;

      if(St5='X')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gpqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sv_Ghnp_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

      if(St5='Z')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gpqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sv_Ghnb_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

    end else
    if(St3='반품')Then begin

      if(St5='Y')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Giqut','Gbsum',Sq1, 0 );
        _Sv_Csum_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
        _Sv_Ghng_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
      end;

      if(St5='X')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gbqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sv_Ghng_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

      if(St5='Z')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gbqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sv_Ghng_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

    end;
  end;
end;

procedure TBase10._H_Repla1(St0,St1,St2,St3,St4,St5:String;Sq1:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);

    if((St3='입금')and(St1='X'))or
      ((St3='입금')and(St1='Z'))or
      ((St3='출금')and(St1='Y'))Then begin

      _Gs_Gsum_(Sw0,St1,St2,St5,'Gsusu','Gosum',Sq1, 0 );
      _Sv_Gsum_(St0,St1,St2,St4,St5,'Gsusu','Gosum','Gbsum',Sq1, 0 );
      _Sv_Chnp_(St0,St1,St2,St5,'Gsusu','Gosum','Gbsum',Sq1, 0 );

    end else
    if((St3='출금')and(St1='X'))or
      ((St3='출금')and(St1='Z'))or
      ((St3='입금')and(St1='Y'))Then begin

      _Gs_Gsum_(Sw0,St1,St2,St5,'Gsusu','Gosum',-Sq1, 0 );
      _Sv_Gsum_(St0,St1,St2,St4,St5,'Gsusu','Gosum','Gbsum',-Sq1, 0 );
      _Sv_Chnp_(St0,St1,St2,St5,'Gsusu','Gosum','Gbsum',-Sq1, 0 );

    end;

  end;
end;

procedure TBase10._G_Repla1(St0,St1,St2,St3:String;Sq1:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);

    _Gs_Gsum_(Sw0,St1,St2,St3,'GsumX','Gosum',Sq1, 0 );
    _Sv_Chnp_(St0,St1,St2,St3,'Gssum','Gosum','Gbsum',Sq1, 0 );

  end;
end;

procedure TBase10._J_Repla1(St0,St1,St2,St3:String;Sq1:Double);
var Sw0: String;
    Su1: Double;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);

    _Gs_Csum_(Sw0,St1,St2,St3,'GsumX','Gosum',Sq1, 0 );
    _Sv_Ghnp_(St0,St1,St2,St3,'Gsqut','Gosum','Gbsum',-Sq1, 0 );

  end;
end;

procedure TBase10._S_Repla2(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);
    if(St5='증정')Then begin

      _Gs_Gsum_(Sw0,St1,St2,St6,'Gjqut','Gjsum',Sq1,Sq2);
      _Sv_Gsum_(St0,St1,St2,St4,St6,'Gjqut','Gjsum','Gssum',Sq1,Sq2);
      _Sg_Chng_(St0,St1,St2,St6,'Gjqut','Gjsum','Gssum',Sq1,Sq2);

    end else
    if(St3='출고')
    or(St3='입고')Then begin

      _Gs_Gsum_(Sw0,St1,St2,St6,'Goqut','Gosum',Sq1,Sq2);
      _Sv_Gsum_(St0,St1,St2,St4,St6,'Goqut','Gosum','Gssum',Sq1,Sq2);
      _Sg_Chng_(St0,St1,St2,St6,'Goqut','Gosum','Gssum',Sq1,Sq2);

    end else
    if(St3='반품')Then begin

      _Gs_Gsum_(Sw0,St1,St2,St6,'Gbqut','Gbsum',Sq1,Sq2);
      _Sv_Gsum_(St0,St1,St2,St4,St6,'Gbqut','Gbsum','Gssum',Sq1,Sq2);
      _Sg_Chng_(St0,St1,St2,St6,'Gbqut','Gbsum','Gssum',Sq1,Sq2);

    end;
  end;
end;

procedure TBase10._B_Repla2(St0,St1,St2,St3,St4,St5,St6:String;Sq1,Sq2:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);
    if(St3='입고')Then begin

      _Gs_Csum_(Sw0,St1,St2,St6,'Giqut','Gosum',Sq1, 0 );
      _Sv_Csum_(St0,St1,St2,St6,'Giqut','Gsusu','Gosum',Sq1, 0 );
      _Sg_Ghng_(St0,St1,St2,St6,'Giqut','Gsusu','Gosum',Sq1, 0 );

    end else
    if(St4='증정')Then begin

      _Gs_Csum_(Sw0,St1,St2,St6,'Gjqut','Gosum',Sq1, 0 );
      _Sv_Csum_(St0,St1,St2,St6,'Gjqut','Gsqut','Gosum',Sq1,Sq2);
      _Sg_Ghng_(St0,St1,St2,St6,'Gjqut','Gsqut','Gosum',Sq1,Sq2);

    end else
    if(St3='출고')Then begin

      _Gs_Csum_(Sw0,St1,St2,St6,'Goqut','Gosum',Sq1,Sq2);
      _Sv_Csum_(St0,St1,St2,St6,'Goqut','Gsqut','Gosum',Sq1,Sq2);
      _Sg_Ghng_(St0,St1,St2,St6,'Goqut','Gsqut','Gosum',Sq1,Sq2);

    end else
    if(St4='비품')or(St4='폐기')Then begin

      if(St5='Y')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Giqut','Gbsum',Sq1, 0 );
        _Sv_Csum_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
        _Sg_Ghng_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
      end;

      if(St5='X')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gpqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sg_Ghnp_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

      if(St5='Z')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gpqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sg_Ghnb_(St0,St1,St2,St6,'Gpqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

    end else
    if(St3='반품')Then begin

      if(St5='Y')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Giqut','Gbsum',Sq1, 0 );
        _Sv_Csum_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
        _Sg_Ghng_(St0,St1,St2,St6,'Giqut','Gsusu','Gbsum',Sq1, 0 );
      end;

      if(St5='X')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gbqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sg_Ghng_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

      if(St5='Z')Then begin
        _Gs_Csum_(Sw0,St1,St2,St6,'Gbqut','Gbsum',Sq1,Sq2);
        _Sv_Csum_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
        _Sg_Ghng_(St0,St1,St2,St6,'Gbqut','Gsqut','Gbsum',Sq1,Sq2);
      end;

    end;
  end;
end;

procedure TBase10._H_Repla2(St0,St1,St2,St3,St4,St5:String;Sq1:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);

    if((St3='입금')and(St1='X'))or
      ((St3='입금')and(St1='Z'))or
      ((St3='출금')and(St1='Y'))Then begin

      _Gs_Gsum_(Sw0,St1,St2,St5,'Gsusu','Gosum',Sq1, 0 );
      _Sv_Gsum_(St0,St1,St2,St4,St5,'Gsusu','Gosum','Gbsum',Sq1, 0 );
      _Sg_Chnp_(St0,St1,St2,St5,'Gsusu','Gosum','Gbsum',Sq1, 0 );

    end else
    if((St3='출금')and(St1='X'))or
      ((St3='출금')and(St1='Z'))or
      ((St3='입금')and(St1='Y'))Then begin

      _Gs_Gsum_(Sw0,St1,St2,St5,'Gsusu','Gosum',-Sq1, 0 );
      _Sv_Gsum_(St0,St1,St2,St4,St5,'Gsusu','Gosum','Gbsum',-Sq1, 0 );
      _Sg_Chnp_(St0,St1,St2,St5,'Gsusu','Gosum','Gbsum',-Sq1, 0 );

    end;

  end;
end;

procedure TBase10._G_Repla2(St0,St1,St2,St3:String;Sq1:Double);
var Sw0: String;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);

    _Gs_Gsum_(Sw0,St1,St2,St3,'GsumX','Gosum',Sq1, 0 );
    _Sg_Chnp_(St0,St1,St2,St3,'Gssum','Gosum','Gbsum',Sq1, 0 );

  end;
end;

procedure TBase10._J_Repla2(St0,St1,St2,St3:String;Sq1:Double);
var Sw0: String;
    Su1: Double;
begin
  if(St1<>'')and(St2<>'')Then begin
    Sw0:=Copy(St0,1,7);

    _Gs_Csum_(Sw0,St1,St2,St3,'GsumX','Gosum',Sq1, 0 );
    _Sg_Ghnp_(St0,St1,St2,St3,'Gsqut','Gosum','Gbsum',-Sq1, 0 );

  end;
end;

procedure TBase10._Z_Repla1(St0,St1,St2,St3,St4,St5,St6:String;Sq1:Double);
begin
  if(St1<>'')and(St2<>'')Then begin

  if((St5='A')or(St5='B'))Then begin
    if(St3='입금')Then begin
    if(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Gosum',Sq1);
    if(St4='어음')Then _H2_Gbun_(St0,St1,St2,St6,'Gjsum',Sq1);
    if(St4='은행')Then _H2_Gbun_(St0,St1,St2,St6,'Gbsum',Sq1);
    end;
    if(St3='출금')Then begin
    if(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Gosum',-Sq1);
    if(St4='어음')Then _H2_Gbun_(St0,St1,St2,St6,'Gjsum',-Sq1);
    if(St4='은행')Then _H2_Gbun_(St0,St1,St2,St6,'Gbsum',-Sq1);
    end;
  end else begin
    if(St3='입금')Then begin
    if(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Goqut',Sq1);
    if(St4='어음')Then _H2_Gbun_(St0,St1,St2,St6,'Gjqut',Sq1);
    if(St4='은행')Then _H2_Gbun_(St0,St1,St2,St6,'Gbqut',Sq1);
    end;
    if(St3='출금')Then begin
    if(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Goqut',-Sq1);
    if(St4='어음')Then _H2_Gbun_(St0,St1,St2,St6,'Gjqut',-Sq1);
    if(St4='은행')Then _H2_Gbun_(St0,St1,St2,St6,'Gbqut',-Sq1);
    end;
  end;

  end;

  St1:='0'; St2:='00000';
  if(St5='A')or(St5='B')Then begin
    if(St3='입금')and(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Gosum', Sq1);
    if(St3='출금')and(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Gosum',-Sq1);
  end else begin
    if(St3='입금')and(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Goqut', Sq1);
    if(St3='출금')and(St4='현금')Then _H2_Gbun_(St0,St1,St2,St6,'Goqut',-Sq1);
  end;

end;

procedure TBase10._W_Repla1(St0,St1,St2,St3,St4:String;Sq1:Double);
begin
  if(St1>'0')and(St3='은행')Then begin

    if(St2='입금')Then
      _H5_Bang_(St0,St1,St4,'Gssum',Sq1);
    if(St2='출금')Then
      _H5_Bang_(St0,St1,St4,'Gsusu',Sq1);

  end;
end;

procedure TBase10.Socket3Error(Sender: TObject; Socket: TCustomWinSocket;
  ErrorEvent: TErrorEvent; var ErrorCode: Integer);
begin
{ if ErrorEvent = eeConnect then begin
    ShowMessage('Socket Connect Error!');
  end; }
  ErrorCode := 0;
  Socket.Close;
end;

procedure TBase10.Insert_ID(TableX: TClientDataSet; GENERATOR: String);
var Str: String;
begin
  Str := 'Select gen_id(' + GENERATOR +',0),Count(*) From G0_Gbun';
  Str := 'Select LAST_INSERT_ID('''+Copy(GENERATOR,1,7)+''')';
  Str := 'Select LAST_INSERT_ID()';
  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    TableX.Edit;
    TableX.FieldByName('ID').AsString := Base10.Socket.GetData(1, 1);
    TableX.Post;
  end;
end;

procedure TBase10.Update_ID(TableX: TClientDataSet; GENERATOR: String);
var Str: String;
begin
  Str := 'Select gen_id(' + GENERATOR +',0),Count(*) From G0_Gbun';
  Str := 'Select LAST_INSERT_ID('''+Copy(GENERATOR,1,7)+''')';
  Str := 'Select LAST_INSERT_ID()';
  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    TableX.FieldByName('ID').AsFloat := StrToIntDef(Base10.Socket.GetData(1, 1),0);
  end;
end;

procedure TBase10.Insert_Idnum(TableX: TClientDataSet; GENERATOR: String);
var Str: String;
begin
  Str := 'Select ID From S1_Ssub Where ID=@ID';
  Translate(Str, '@ID', GENERATOR);
  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    TableX.FieldByName('Idnum').AsFloat := StrToIntDef(Base10.Socket.GetData(1, 1),0);
  end;
end;

procedure TBase10.Update_Idnum(TableX: TClientDataSet; GENERATOR: String);
var Str: String;
begin
  Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
           'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
           'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
           'Gcode=''@Gcode'' and Scode=''@Scode'' and Gjisa=''@Gjisa''';

  Translate(Sqlen, '@Hcode', TableX.FieldByName('Hcode').Value);
  Translate(Sqlen, '@Gdate', TableX.FieldByName('Gdate').Value);
  Translate(Sqlen, '@Gubun', TableX.FieldByName('Gubun').Value);
  Translate(Sqlen, '@Jubun', TableX.FieldByName('Jubun').Value);
  Translate(Sqlen, '@Gcode', TableX.FieldByName('Gcode').Value);
  Translate(Sqlen, '@Scode', TableX.FieldByName('Scode').Value);
  Translate(Sqlen, '@Gjisa', TableX.FieldByName('Gjisa').Value);
  Str:=Seek_Name(Sqlen);

  if Str<>'' then begin
    TableX.FieldByName('Idnum').AsFloat := StrToIntDef(Str,0);
  end else begin
    Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
             'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
             'Gubun=''@Gubun''';

    Translate(Sqlen, '@Hcode', TableX.FieldByName('Hcode').Value);
    Translate(Sqlen, '@Gdate', TableX.FieldByName('Gdate').Value);
    Translate(Sqlen, '@Gubun', TableX.FieldByName('Gubun').Value);
    Str:=Seek_Name(Sqlen);

    TableX.FieldByName('Idnum').AsFloat := StrToIntDef(Str,0)+1;
  end;
    Sqlen := 'UPDATE S1_Ssub SET Idnum=@Idnum '+
             'WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', TableX.FieldByName('Gdate').Value);
    TransAuto(Sqlen, '@Idnum', TableX.FieldByName('Idnum').Value);
    TransAuto(Sqlen, '@ID',    TableX.FieldByName('ID').Value);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
end;

procedure TBase10.Update_Icode(TableX: TClientDataSet; GENERATOR: String);
var Str,Sts: String;
begin
  Str:='';
  Sts:='';
  Sqlen := 'Select Max(Idnum),Max(Icode) From S1_Ssub Where '+D_Select+
           'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
           'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
           'Gcode=''@Gcode'' and Scode=''@Scode'' and '+
           'Ocode=''@Ocode'' and Gjisa=''@Gjisa''';

  Translate(Sqlen, '@Hcode', TableX.FieldByName('Hcode').Value);
  Translate(Sqlen, '@Gdate', TableX.FieldByName('Gdate').Value);
  Translate(Sqlen, '@Gubun', TableX.FieldByName('Gubun').Value);
  Translate(Sqlen, '@Jubun', TableX.FieldByName('Jubun').Value);
  Translate(Sqlen, '@Gcode', TableX.FieldByName('Gcode').Value);
  Translate(Sqlen, '@Scode', TableX.FieldByName('Scode').Value);
  Translate(Sqlen, '@Ocode', TableX.FieldByName('Ocode').Value);
  Translate(Sqlen, '@Gjisa', TableX.FieldByName('Gjisa').Value);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    Str:=Base10.Socket.GetData(1, 1);
    Sts:=Base10.Socket.GetData(1, 2);
  end;

  if Str<>'' then begin
    TableX.FieldByName('Idnum').AsFloat := StrToInt64Def(Str,0);
    TableX.FieldByName('Icode').AsFloat := StrToInt64Def(Sts,0);
  end else begin
    Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
             'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
             'Gubun=''@Gubun'' and Ocode=''@Ocode''';

    Translate(Sqlen, '@Hcode', TableX.FieldByName('Hcode').Value);
    Translate(Sqlen, '@Gdate', TableX.FieldByName('Gdate').Value);
    Translate(Sqlen, '@Gubun', TableX.FieldByName('Gubun').Value);
    Translate(Sqlen, '@Ocode', TableX.FieldByName('Ocode').Value);
    Str:=Seek_Name(Sqlen);

    TableX.FieldByName('Idnum').AsFloat := StrToInt64Def(Str,0)+1;
    if Sts='' then
    TableX.FieldByName('Icode').AsFloat := TableX.FieldByName('ID').AsFloat
    else
    TableX.FieldByName('Icode').AsFloat := StrToInt64Def(Sts,0);
  end;
    Sqlen := 'UPDATE S1_Ssub SET Idnum=@Idnum, Icode=@Icode '+
             'WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', TableX.FieldByName('Gdate').Value);
    TransAuto(Sqlen, '@Idnum', TableX.FieldByName('Idnum').Value);
    TransAuto(Sqlen, '@Icode', TableX.FieldByName('Icode').Value);
    TransAuto(Sqlen, '@ID',    TableX.FieldByName('ID').Value);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
end;

function TBase10.Seek_Name(_Gcode1:String) : String;
var Str: String;
begin
  Result := '';
  Str := _Gcode1;
  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    Result := Base10.Socket.GetData(1, 1);
  end;
{ Sqlen := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
  Translate(Sqlen, '@Gcode', St3);
  St3:=Base10.Seek_Name(Sqlen); }
end;

function TBase10.Seek_Code(_Gcode1,_Gcode2,_Gcode3:String) : String;
var Str: String;
begin
  Result := '';

  if _Gcode2='X' Then
  Str := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Y' Then
  Str := 'Select Gname From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Z' Then
  Str := 'Select Gname,Gposa From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='B' Then
  Str := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';

  Translate(Str, '@Gcode', _Gcode1);
  Translate(Str, '@Hcode', _Gcode3);

  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    Result := Base10.Socket.GetData(1, 1);
    if _Gcode2='Z' Then
    Result := Base10.Socket.GetData(1, 1)+'.'+Base10.Socket.GetData(1, 2);
  end else begin
  //--//
  if _Gcode2='X' Then
  Str := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Y' Then
  Str := 'Select Gname From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Z' Then
  Str := 'Select Gname,Gposa From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='B' Then
  Str := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';

  Translate(Str, '@Gcode', _Gcode1);
  Translate(Str, '@Hcode', '');

  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    Result := Base10.Socket.GetData(1, 1);
    if _Gcode2='Z' Then
    Result := Base10.Socket.GetData(1, 1)+'.'+Base10.Socket.GetData(1, 2);
  end;
  //--//
  end;

{ if _Gcode2='X' Then
  Str := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Y' Then
  Str := 'Select Gname From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Z' Then
  Str := 'Select Gname,Gposa From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='B' Then
  Str := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';

  Translate(Str, '@Gcode', _Gcode1);
  Translate(Str, '@Hcode', _Gcode3);

  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    Result := Base10.Socket.GetData(1, 1);
    if _Gcode2='Z' Then
    Result := Base10.Socket.GetData(1, 1)+'.'+Base10.Socket.GetData(1, 2);
  end; }
end;

function TBase10.Seek_Bigo(_Gcode1,_Gcode2,_Gcode3:String) : String;
var Str: String;
begin
  Result := '';

  if _Gcode2='X' Then
  Str := 'Select Jubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Y' Then
  Str := 'Select Jubun From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Z' Then
  Str := 'Select Jubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';

  Translate(Str, '@Gcode', _Gcode1);
  Translate(Str, '@Hcode', _Gcode3);

  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    if Base10.Socket.GetData(1, 1)<>'' then
    Result := '-'+Base10.Socket.GetData(1, 1)+'-';
  end else begin
  //--//
  if _Gcode2='X' Then
  Str := 'Select Jubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Y' Then
  Str := 'Select Jubun From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  if _Gcode2='Z' Then
  Str := 'Select Jubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';

  Translate(Str, '@Gcode', _Gcode1);
  Translate(Str, '@Hcode', '');

  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    if Base10.Socket.GetData(1, 1)<>'' then
    Result := '-'+Base10.Socket.GetData(1, 1)+'-';
  end;
  //--//
  end;

{ if _Gcode2='X' Then
  Str := 'Select Jubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
  if _Gcode2='Y' Then
  Str := 'Select Jubun From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode''';
  if _Gcode2='Z' Then
  Str := 'Select Jubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode''';

  Translate(Str, '@Gcode', _Gcode1);

  Base10.Socket.RunSQL(Str);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    if Base10.Socket.GetData(1, 1)<>'' then
    Result := '-'+Base10.Socket.GetData(1, 1)+'-';
  end; }
end;

function TBase10.Seek_Uses(_Gcode1:String) : String;
begin
{ Base10.Socket.RunSQL(_Gcode1);
  Base10.Socket.busyloop;
  Result:=Base10.Socket.Body_Data; }
{ if Base10.Socket.Body_Data <> 'X' then
  Result := 'O' else Result := 'X'; }
{ Result := 'O'; }
  Sqlen :='Select @F11 From Id_Logn Where '+
          'Hcode='+#39+Hnnnn+#39+' and '+
          'Gname='+#39+Logn1+#39+' and '+
          'Gcode='+#39+Logn2+#39+' and '+
          'Gpass='+#39+Logn3+#39;
  Translate(Sqlen, '@F11', _Gcode1);
  if Base10.Seek_Name(Sqlen)='X' then
     Result := 'X' else
  if Base10.Seek_Name(Sqlen)='R' then
     Result := 'R' else
     Result := 'O';
end;

function TBase10.Seek_Ggeo(_Gcode1:String) : String;
begin
  if _Gcode1='' then begin
  ShowMessage(E_Ggeo);
  Result := 'X'
  end else
  Result := 'O';
end;

function TBase10.Seek_Hgeo(_Gcode1,_Gcode2,_Gcode3:String) : String;
var Str: String;
begin
  if _Gcode2<>'' then begin

    if _Gcode1='X' then begin
      Sqlen := 'Select Gcode From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', '');
      Str:=Base10.Seek_Name(Sqlen);

      if Str='' then begin
      Sqlen := 'Select Gcode From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', _Gcode3);
      Str:=Base10.Seek_Name(Sqlen);
      end;

      if Str='' then _Gcode2 := '';
    end;
    if _Gcode1='Y' then begin
      Sqlen := 'Select Gcode From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', '');
      Str:=Base10.Seek_Name(Sqlen);

      if Str='' then begin
      Sqlen := 'Select Gcode From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', _Gcode3);
      Str:=Base10.Seek_Name(Sqlen);
      end;

      if Str='' then _Gcode2 := '';
    end;
    if _Gcode1='Z' then begin
      Sqlen := 'Select Gcode From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', '');
      Str:=Base10.Seek_Name(Sqlen);

      if Str='' then begin
      Sqlen := 'Select Gcode From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', _Gcode3);
      Str:=Base10.Seek_Name(Sqlen);
      end;

      if Str='' then _Gcode2 := '';
    end;
    if _Gcode1='B' then begin
      Sqlen := 'Select Gcode From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', '');
      Str:=Base10.Seek_Name(Sqlen);

      if Str='' then begin
      Sqlen := 'Select Gcode From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', _Gcode2);
      Translate(Sqlen, '@Hcode', _Gcode3);
      Str:=Base10.Seek_Name(Sqlen);
      end;

      if Str='' then _Gcode2 := '';
    end;

    Result := 'O';
  end;
  if _Gcode2='' then begin
    if _Gcode1='X' then
    ShowMessage('거래처를 입력해 주세요.');
    if _Gcode1='Y' then
    ShowMessage('입고처를 입력해 주세요.');
    if _Gcode1='Z' then
    ShowMessage('거래처를 입력해 주세요.');
    if _Gcode1='B' then
    ShowMessage('도서명을 입력해 주세요.');
    if _Gcode1='8' then
    ShowMessage('은행명을 입력해 주세요.');
    if _Gcode1='1' then
    ShowMessage('계정과목을 입력해 주세요.');
    Result := 'X'
  end;
end;

function TBase10.Seek_Hname(_Gcode1,_Gcode2:String) : String;
var Str: String;
begin
  Result := '';

  Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  Translate(Sqlen, '@Gcode', _Gcode1);
  Translate(Sqlen, '@Hcode', '');
  Str:=Base10.Seek_Name(Sqlen);

  if Str='' then begin
  Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  Translate(Sqlen, '@Gcode', _Gcode1);
  Translate(Sqlen, '@Hcode', _Gcode2);
  Str:=Base10.Seek_Name(Sqlen);
  end;

  Result := Str;
end;

function TBase10.Seek_Jisa(_Gcode1,_Gcode2:String) : String;
var I: Integer;
begin
  I := Pos('|', _Gcode1);
  Result := '';

  if _Gcode2='1' then
  if I > 0 then begin
    if Copy(_Gcode1, I+1, Length(_Gcode1))='' then
    Result := '' else
    Result := '-'+Copy(_Gcode1, I+1, Length(_Gcode1))
  end else begin
    if _Gcode1='' then
    Result := '' else
    Result := '-'+_Gcode1;
  end;

  if _Gcode2='2' then
  if I > 0 then
  Result := Copy(_Gcode1, 1, I-1)+')';

  if _Gcode2='3' then
  if I > 0 then begin
    if Copy(_Gcode1, I+1, Length(_Gcode1))='' then
    Result := '' else
    Result := Copy(_Gcode1, I+1, Length(_Gcode1))
  end else begin
    if _Gcode1='' then
    Result := '' else
    Result := _Gcode1;
  end;

  if _Gcode2='4' then
  if I > 0 then
  Result := Copy(_Gcode1, 1, I-1);
end;

procedure TBase10.Init_Show(Sender: TObject);
begin
  Tong40.Color:=clWhite;
  Tong40.myLabel3d1.Caption:='Loading 로딩중 (10%)';
  if Base10.Database.Database<>'book_07_db' then
  Application.ProcessMessages;

  Tong40.Show;
  Tong40.Update;

  Base10.OpenShow(Base10.G7_Ggeo);
  Sqlen := 'Select Hcode,Gcode,Gname,Chek1,Chek2,Yes35 From G7_Ggeo '+
           'Where '+D_Open;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.G7_Ggeo)
  else
  ShowMessage(E_Open);

  Tong40.myLabel3d1.Caption:='Loading 로딩중 (20%)';

  if Base10.Database.Database<>'book_07_db' then
    Application.ProcessMessages;

  Base10.OpenShow(Base10.G1_Ggeo);
  Sqlen := 'Select Hcode,Gcode,Gname,Ocode,Gubun,Pubun From G1_Ggeo '+
           'Where '+D_Open+' and '+'Hcode'+'<'+#39+'x'+#39;
  Translate(Sqlen, '@Hcode', Hnnnn);
  LoadData_G1_Ggeo(Sqlen);
{
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.G1_Ggeo)
  else ShowMessage(E_Open);
}
  Tong40.myLabel3d1.Caption:='Loading 로딩중 (50%)';
  if Base10.Database.Database<>'book_07_db' then
  Application.ProcessMessages;

  Base10.OpenShow(Base10.G2_Ggwo);
  Sqlen := 'Select Hcode,Gcode,Gname,Ocode,Gubun,Pubun From G2_Ggwo '+
           'Where '+D_Open+' and '+'Hcode'+'<'+#39+'x'+#39;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.G2_Ggwo)
  else ShowMessage(E_Open);
  Tong40.myLabel3d1.Caption:='Loading 로딩중 (70%)';
  if Base10.Database.Database<>'book_07_db' then
  Application.ProcessMessages;

  Base10.OpenShow(Base10.G4_Book);
  Sqlen := 'Select Hcode,Gcode,Gname,Ocode,Gubun,Gdang,Grat8,Bigo4 From G4_Book '+
           'Where '+D_Open+' and '+'Hcode'+'<'+#39+'x'+#39;
  LoadData_G4_Book(Sqlen);
{
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.G4_Book)
  else ShowMessage(E_Open);
}
  Tong40.myLabel3d1.Caption:='Loading 로딩중 (100%)';
  if Base10.Database.Database<>'book_07_db' then
  Application.ProcessMessages;

  Tong40.Hide;
  Tong40.Color:=clLime;
  Tong40.myLabel3d1.Caption:='자료 검색중 입니다.';
{ Tong40.Free; }
end;

procedure TBase10.LoadData_G1_Ggeo(fStr: string);
begin
  with ZMySqlQuery1 do
  begin
    Close;
    Sql.Clear;
    Sql.Text := fStr;
    Open;
  end;

  while not ZMySqlQuery1.Eof do
  begin
    G1_Ggeo.Append;

    G1_Ggeo.FieldByName('HCODE').Value := Base10.ZMySqlQuery1.FieldByName('HCODE').Value;
    G1_Ggeo.FieldByName('GCODE').Value := Base10.ZMySqlQuery1.FieldByName('GCODE').Value;
    G1_Ggeo.FieldByName('GNAME').Value := Base10.ZMySqlQuery1.FieldByName('GNAME').Value;
    G1_Ggeo.FieldByName('OCODE').Value := Base10.ZMySqlQuery1.FieldByName('OCODE').Value;
    G1_Ggeo.FieldByName('GUBUN').Value := Base10.ZMySqlQuery1.FieldByName('GUBUN').Value;
    G1_Ggeo.FieldByName('PUBUN').Value := Base10.ZMySqlQuery1.FieldByName('PUBUN').Value;

    ZMySqlQuery1.Next;
  end;
  if G1_Ggeo.State in [dsInsert] then
    G1_Ggeo.Post;
end;

procedure TBase10.LoadData_G4_Book(fStr: string);
begin
  with ZMySqlQuery1 do
  begin
    Close;
    Sql.Clear;
    Sql.Text := fStr;
    Open;
  end;

  while not ZMySqlQuery1.Eof do
  begin
    G4_Book.Append;

    G4_Book.FieldByName('HCODE').Value := Base10.ZMySqlQuery1.FieldByName('HCODE').Value;
    G4_Book.FieldByName('GCODE').Value := Base10.ZMySqlQuery1.FieldByName('GCODE').Value;
    G4_Book.FieldByName('GNAME').Value := Base10.ZMySqlQuery1.FieldByName('GNAME').Value;
    G4_Book.FieldByName('OCODE').Value := Base10.ZMySqlQuery1.FieldByName('OCODE').Value;
    G4_Book.FieldByName('GUBUN').Value := Base10.ZMySqlQuery1.FieldByName('GUBUN').Value;
    G4_Book.FieldByName('GDANG').Value := Base10.ZMySqlQuery1.FieldByName('GDANG').Value;
    G4_Book.FieldByName('GRAT8').Value := Base10.ZMySqlQuery1.FieldByName('GRAT8').Value;
    G4_Book.FieldByName('BIGO4').Value := Base10.ZMySqlQuery1.FieldByName('BIGO4').Value;

    ZMySqlQuery1.Next;
  end;
  if G4_Book.State in [dsInsert] then
    G4_Book.Post;
end;
end.
