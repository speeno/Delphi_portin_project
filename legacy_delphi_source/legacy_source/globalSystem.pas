unit globalSystem;

interface

uses
  SysUtils, Classes, StdCtrls, Dialogs, IniFiles, Forms,
  Mask, DateUtil, Math, SysConst;
{
  Windows, Messages, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Mask;
}

//############################################>> 문자 관련

// ======================================= IniFile 관련
procedure WriteIni(const IniFileName, Section, Id, Value : string); overload;
procedure WriteIni(const IniFileName, Section, Id: string; Value: Integer); overload;
function  ReadIniStr(const IniFileName, Section, Id: string; FDefault: string = ''): string;
function  ReadIniInt(const IniFileName, Section, Id: string; FDefault: integer): Integer;
// ======================================= 문자 check
function IsAlpha(const Chr: Char) : Boolean;//영문자인가
function IsNumeric(const FParam : string) : Boolean;//숫자문자인가?
function IsKorean(const FParam : string) : Boolean;//첫문자가 한글인가?
function IsCompleteKoreanChr(FStr: string; FIdx: Integer): Boolean;//완전한 한글이면 true
function Get_UpperCase(const FChr: Char): Char;//소문자를 대문자로
// ========================================= 문자열 조작
function  FillSpace(const Src: string; Len: integer; FType: string): string;
// S에서 T를 찾아 모두 제거
function  RemoveStr(const T, S : string) : string;
//Str : 채워질 문자열, ChrToFill : 채울문자열, fType : 오른쪽 또는 왼쪽, Len : 결과갑의 총길이
function FillChr(const Str, ChrToFill, fType : string; Len : Integer) : string;
function ReverseStr(const Str: string): string;//Reverse string
function ReplaceStr(const Src, S1, S2: string): string;//Src의 S1을 S2로 치환
function Get_ShortName(const FStr: string): string;
function GetSpace(const nNum : integer) : string;//지정된 수의 space문자열 return
//FLen보다 문자열이 길면 두 개로 나눔.
procedure SplitStr(const FStr: string; FLen: integer; var FRet1, FRet2: string);
procedure ReplaceStrs(Strings: TStrings; const S1, S2: string);//Strings의 S1을 S2로 치환
// ======================================= 문자변환
function  Str2Float(const FStr: string): Double;//문자를 float로
function  Str2Int(const FStr: string): Integer;//문자를 Integer로
// ======================================= 문자포맷
function GetBusiNoFmt(const FStr: string): string;//사업자번호형태 return
function GetZipNoFmt(const FStr: string): string;//우편번호형태 return
function GetResNoFmt(const FStr: string): string;//주민등록번호형태 return

const
  ftLeft  = 'L';
  ftRight = 'R';

  // =========================== 기타 mask
  mskBusiNo = '999-99-99999;0;_';
  mskResNo  = '999999-9999999;0;_';
  mskZipNo  = '999-999;0;_';
//<<############################################ 문자 관련

//############################################>> 날짜/시간 관련
procedure WaitTime(MyHour, MyMin, MySec : integer);//지정시간 동안 wait

// =========================== 날짜(문자) 변경
function Str2Date(const FDate : string) : TDateTime;//문자를 날짜 type으로 바꿈.('20000101'을 날짜로 바꿈)
function Date2Str(const FDate: TDateTime): string;//날자를 '20000105' 형태로 return
function Date2Kor1(const FDate: string): string;//날자를 '1999년 09월 02일' 형식으로 만듬
function Month2Kor1(const FMonth: string): string;//날자를 '1999년 09월 ' 형식으로 만듬
function FirstDay(const FDate: string):string;//월의 첫날 return
function LastDay(const FDate: string):string;//월의 마지막날 return
function LeapYear(const FDate: TDateTime): Boolean;//윤년 체크
function GetEngMonthName(FMonth : Integer) : string;//영문 월 return
// ===== 날짜 유효성 체크
function DateInvalid(const FDate : string) : boolean;
function DateInvalidA(const FDate : string): Boolean;//DateInvalid와 다르게 메세지를 띄우지 않는다.
//<<=================== 날짜를 영문으로
function AddMonth(const FDate: string; Cnt: Integer): string;//param이 날자로 넘어옴
function AddMonth2(const FMonth: string; FCnt: Integer): string;//param이 월로 넘어옴
function AddMonth3(const FMonth: string; FCnt: Integer): string;//param이 2021.07 형태로 넘어옴
function AddDate(const FDate: string; Cnt: Integer): string;//날짜 plus, minus.
function GetDayOfWeek(const FDate: string): string;
function GetYear(const FDate: string): string;//연도 return
function GetYYYYMM(const FDate: string): string;//년+월 return
function GetYYYY_MM(const FDate: string): string;//년+월 return
function GetYYYY_MM_DD(const FDate : string): string;//YYYY.MM.DD형태로 RETURN
function GetMM_DD(const FDate : string): string;//MM.DD형태로 RETURN
function GetMonth(const FDate: string): string;//월 return
function DayPlus(const FDate: string; FInc: integer): string;//날짜 +, -
function GetMonthPrd(const FDate1, FDate2: string): Integer;//2개의 월의 개월수 return
procedure ClearDir(Path: string);
function Get_exe_path: string;

const
  DaysPerMonth: array[1..12] of Byte = (31, 28, 31, 30, 31, 30,
                                        31, 31, 30, 31, 30, 31);

//<<############################################ 날짜/시간 관련

//############################################>> 숫자 관련
function Num2KoreanA(const Fig1: Real; Fig2 : Integer) : string;//Num2Korean에서 사용
//숫자를 한글로. Fig2 :1=>한글금액, 2=>한자금액
function Num2Korean(const Fig1 : Real; FIG2 : integer):string;
function StrR(Value: Extended; Len, Digits: integer): string;
//integer->str로 변환. 0이면 '0'을 return
function Int2Str_0(const FValue: integer): string;
//float->str로 변한. 00:소수이하는 0, 결과가 0이면 '0'으로 표시
function Float2Str_00(const FValue: Double): string;
//float->str로 변한. 0X:소수이하는 0, 결과가 0이면 ''로 표시
function Float2Str_0X(const FValue: Double): string;
//float->str로 변한. 20:소수이하는 2, 결과가 0이면 '0'으로 표시
function Float2Str_20(const FValue: Double): string;
//float->str로 변한. 소수이하도 고려
function Float2Str(const FValue: Double; FDec: integer): string;

function Rounder(X : Extended; FDec: integer): Extended;//반올림

const
  // ============================== 숫자 format
  dfNormal  = '#,###';
  dfNormalZ = '#,##0';
  dfDec_2   = '#,##0.#0';//소수 둘째자리까지 표시
  efNormalZ = '#0';
  efDec_2   = '###0.##';//소수 둘째자리까지 표시
//<<############################################ 숫자 관련

//############################################>> 시스템 관련

//function Is_OS_2000: Boolean;//os가 windows 2000인가?

//############################################>> 시스템 관련
//############################################>> 출력 관련
var
  gSL: TStringList;
  // ======================>> 프린터 인덱스
  gPrinterIdx: integer;
const
  // ======================>> 출력용지 종류
  pk80Col  = 0;//80Col
  pk136Col = 1;//136Col
  pkA4Ver  = 2;//A4세로
  pkA4Hor  = 3;//A4가로
  pkB4Ver  = 4;//B4세로
  pkB4Hor  = 5;//B4가로
  // ======================>> 문자필드의 경우 정렬방법
  agLeft   = 0;//왼쪽
  agRight  = 1;//오른쪽
  agCenter = 2;//가운데
  // ======================>> 칼럼헤더 레벨
  hlOne_1 = 0;//1단
  hlOne_2 = 1;//1단(필드결합 가능)
  hlTwo   = 2;//2단
  // ======================>> 레코드 출력시 웃줄, 밑줄 표시 상수
  lnUpper  = '1';//윗줄 그음
  lnBottom = '2';//밑줄 그음
  lnBoth   = '3';//웃줄, 밑줄 그음
//<<############################################ 출력 관련

implementation

function IsAlpha(const Chr: Char) : Boolean;//영문자인가
begin
  Result := (UpperCase(Chr) >= 'A') and (UpperCase(Chr) <= 'Z');
end;

function Get_UpperCase(const FChr: Char): Char;//소문자를 대문자로
begin
  if (FChr >= 'a') and (FChr <= 'z') then
    Result := Chr(Byte(FChr) - 32)
  else
    Result := FChr;
end;

function IsKorean(const FParam : string) : Boolean;//첫문자가 한글인가?
begin
  if FParam = '' then//빈문자열이면
  begin
    Result := False;
    Exit;
  end;
  Result := Ord(FParam[1]) > 127;
end;

//IniFileName : File Path + FileName(string 기록)
procedure WriteIni(const IniFileName, Section, Id, Value : string);
var
  IniFile: TIniFile;
begin
  IniFile := TIniFile.Create(IniFileName);
  IniFile.WriteString(Section, Id, Value);
  IniFile.Free;
end;
//IniFileName : File Path + FileName(integer 기록)
procedure WriteIni(const IniFileName, Section, Id: String; Value : Integer);
var
  IniFile: TIniFile;
begin
  IniFile := TIniFile.Create(IniFileName);
  IniFile.WriteInteger(Section, Id, Value);
  IniFile.Free;
end;
//IniFileName : File Path + FileName(read string)
function ReadIniStr(const IniFileName, Section, Id: string; FDefault: string = ''): string;
var
  IniFile: TIniFile;
begin
  IniFile := TIniFile.Create(IniFileName);
  Result := IniFile.ReadString(Section, Id, FDefault);
  IniFile.Free;
end;

//IniFileName : File Path + FileName(read integer)
function ReadIniInt(const IniFileName, Section, Id: string; FDefault: integer): Integer;
var
  IniFile: TIniFile;
begin
  IniFile := TIniFile.Create(IniFileName);
  Result := IniFile.ReadInteger(Section, Id, FDefault);
  IniFile.Free;
end;
// S에서 T를 모두 제거.
function RemoveStr(const T, S : string) : string;
var
  Str : string;
begin
  Str := S;
  while Pos(T, Str) > 0 do begin
    Delete(Str, Pos(T, Str), Length(T));
  end;
  Result := Str;
end;

function GetSpace(const nNum : integer) : string;//지정된 수의 space문자열 return
const
  Spc_10 = '          ';//space 10
var
  Spc : string;
  J : integer;
begin
  for J := 1 to (nNum div 10) do
    Spc := Spc + Spc_10;

  Result := Spc + Copy(Spc_10, 1, nNum mod 10);
end;

//Str : 채워질 문자열, ChrToFill : 채울문자열, fType : 오른쪽 또는 왼쪽, Len : 결과갑의 총길이
function FillChr(const Str, ChrToFill, fType : string; Len : Integer) : string;
var
  i, sLen : Integer;
  nStr : string;
begin
  nStr := '';
  sLen := Length(Str);
  for i := 1 to Len - sLen do
    nStr := nStr + ChrToFill;

  if fType = 'L' then
    Result := nStr + Str
  else
    Result := Str + nStr;
end;

function ReverseStr(const Str: string): string;//Reverse string
var
  i: integer;
begin
  Result := '';
  if Str = '' then
    Exit;

  for i := Length(Str) downto 1 do
    Result := Result + Str[i];
end;

// Src의 S1을 S2로 치환
function ReplaceStr(const Src, S1, S2: string): string;
var
  Idx: integer;
  FSrc: string;
begin
  FSrc := Src;
  Idx := Pos(S1, FSrc);
  while Idx > 0 do
  begin
    Delete(FSrc, Idx, Length(S1));
    Insert(S2, FSrc, Idx);

    Idx := Pos(S1, FSrc);
  end;
  Result := FSrc;
end;

// Strings의 S1을 S2로 치환
procedure ReplaceStrs(Strings: TStrings; const S1, S2: string);
var
  i: integer;
  FStrings: TStrings;
begin
  FStrings := Strings;
  for i := 0 to FStrings.Count - 1 do
    FStrings[i] := ReplaceStr(FStrings[i], S1, S2);
end;
// 숫자문자인가?
function IsNumeric(const FParam : string) : Boolean;
var
  i : integer;
begin
  Result := True;
  if FParam = '' then//빈문자열이면
  begin
    Result := False;
    Exit;
  end;
  
  for i := 1 to Length(FParam) do
  begin
    if (FParam[i] < '0') or (FParam[i] > '9') then
    begin
      Result := False;
      Break;
    end;
  end;
end;

function FillSpace(const Src: string; Len: integer; FType: string): string;
begin
  Result := GetSpace(Len - Length(Src));
  if FType = ftLeft then
    Result := Result + Src
  else
    Result := Src + Result;
end;

function Str2Float(const FStr: string): Double;//문자를 float로
var
  i: Integer;
  pValue: string;
begin
  pValue := '';
  for i := 1 to Length(FStr) do
  begin
    if (FStr[i] >= '0') and (FStr[i] <= '9') or (FStr[i] = '.') or (FStr[i] = '-') then
      pValue := pValue + FStr[i];
  end;

  if pValue = '' then
    Result := 0
  else
    Result := StrToFloat(pValue);
end;

function Str2Int(const FStr: string): Integer;//문자를 Integer로
var
  pValue: string;
begin
  pValue := RemoveStr(',', FStr);
  if pValue = '' then
    Result := 0
  else
    Result := StrToInt(pValue);
end;
// FIdx번째 문자가 한글을 구성하는 2번 Byte인가?
function IsCompleteKoreanChr(FStr: string; FIdx: Integer): Boolean;
var
  pFlag : Boolean;
  pI: Integer;
begin
  pFlag := False;
  for pI := 1 to FIdx do
  begin
    if (not pFlag) and (Ord(FStr[pI]) > 127) then
      pFlag := True
    else
      pFlag := False;
  end;
  Result := not pFlag;
end;

//StrLen보다 문자열이 길면 두 개로 나눔.
procedure SplitStr(const FStr: string; FLen: integer; var FRet1, FRet2: string);
var
  i : integer;
  pStr : string;
begin
  if Length(FStr) > FLen then//지정된 길이보다 크면
  begin
    pStr := Copy(FStr, 1, FLen);
    if FStr[FLen + 1] = ' ' then//FLen이 3인데 FStr이 'abc def'인 경우
    begin
      FRet1 := pStr;
      FRet2 := Copy(FStr, FLen + 1, 150);
    end
    else begin//FLen이 5인데 FStr이 'abc def'인 경우는 abc와 def를 분리한다.
              //즉, 공백 앞에서 분리한다.
      for i := Length(pStr) downto 1 do
        if pStr[i] = ' ' then
          Break;
      FRet1 := Copy(pStr, 1, i - 1);
      FRet2 := Copy(FStr, i + 1, 150);//150은 임의로 준 숫자
    end;
  end
  else begin
    FRet1 := FStr;
    FRet2 := '';
  end;
end;

function Get_ShortName(const FStr: string): string;
begin
  Result := RemoveStr('(주)', RemoveStr(' ', FStr));
  Result := RemoveStr('(유)', RemoveStr('(사)', RemoveStr('(재)', RemoveStr('(의)', RemoveStr('(학)', Result)))));
end;

function GetBusiNoFmt(const FStr: string): string;//사업자번호 return
begin
  if Length(FStr) = 10 then
    Result := FormatMaskText(mskBusiNo, FStr)
  else
    Result := FStr;
end;

function GetZipNoFmt(const FStr: string): string;//우편번호형태 return
begin
  if Length(Trim(FStr)) = 6 then
    Result := FormatMaskText(mskZipNo, FStr)
  else
    Result := FStr;
end;

function GetResNoFmt(const FStr: string): string;//주민등록번호형태 return
begin
  if Length(FStr) = 13 then
    Result := FormatMaskText(mskResNo, FStr)
  else
    Result := FStr;
end;

function GetYYYY_MM_DD(const FDate : string): string;//YYYY.MM.DD형태로 RETURN
const
  pcYYYYMMDD   = '9999.99.99;0;_';
begin
  if Trim(FDate) = '' then
    Result := ''
  else
    Result := FormatMaskText(pcYYYYMMDD, FDate);
end;

function GetMM_DD(const FDate : string): string;//MM.DD형태로 RETURN
const
  pcYMMDD   = '99.99;0;_';
begin
  if FDate = '' then
    Result := ''
  else
    Result := FormatMaskText(pcYMMDD, Copy(FDate, 5, 4));
end;

function DateInvalid(const FDate : string) : Boolean;// ===== 날짜 유효성 체크
var
  nDate : TDateTime;
  Year, Month, Day : Word;
begin
  Result := False;

  try
    Year  := StrToInt(Copy(FDate, 1, 4));
    Month := StrToInt(Copy(FDate, 5, 2));
    Day   := StrToInt(Copy(FDate, 7, 2));
    nDate := EncodeDate(Year, Month, Day)
  except on EConvertError do begin
      ShowMessage('날짜가 유효하지 않습니다 !!!');
      Result := True;
    end;
  end;
end;
// ===== 날짜 유효성 체크. 얘는 DateInvalid와 다르게 메세지를 띄우지 않는다.
function DateInvalidA(const FDate : string): Boolean;
var
  nDate : TDateTime;
  Year, Month, Day : Word;
begin
  Result := False;

  try
    Year  := StrToInt(Copy(FDate, 1, 4));
    Month := StrToInt(Copy(FDate, 5, 2));
    Day   := StrToInt(Copy(FDate, 7, 2));
    nDate := EncodeDate(Year, Month, Day)    
  except on EConvertError do
    Result := True;
  end;
end;

function FirstDay(const FDate: string):string;//월의 첫날 return
begin
  Result := Copy(FDate, 1, 6) + '01';
end;

function LastDay(const FDate: string):string;//월의 마지막날 return
var
  Dy : Integer;
  Year, Month, Day : Word;
begin
  Year  := StrToInt(Copy(FDate, 1, 4));
  Month := StrToInt(Copy(FDate, 5, 2));
  Day   := StrToInt(Copy(FDate, 7, 2));

  Dy := DaysPerMonth[Month];
  if (Month = 2) and LeapYear(EncodeDate(Year, Month, Day)) then
    Inc(Dy);
  Result := Copy(FDate, 1, 6) + IntToStr(Dy);
end;

function LeapYear(const FDate: TDateTime): Boolean;//윤년인가?
var
  Year,
  Month,
  Day : Word;
begin
  DecodeDate(FDate, Year, Month, Day);
  Result:=(Year mod 4 = 0) and ((Year mod 100 <> 0) or (Year mod 400 = 0));
end;

procedure WaitTime(MyHour, MyMin, MySec : integer);//지정시간 동안 wait
var
  TimeString : string;
  BeginTime : TDateTime;
  ToTime    : TDateTime;
  TempTime  : TDateTime;
begin
  BeginTime := Time;  { now time }
  TimeString := IntToStr(MyHour) + ':' + IntToStr(MyMin) + ':' + IntToStr(MySec);
  ToTime := StrToTime(TimeString);
  TempTime := (Time - BeginTime); { <-- start time = 12:00:00 A.M }
  while TempTime < ToTime do
    TempTime := (Time - BeginTime);
end;

function GetEngMonthName(FMonth : Integer) : string;//영문 월 return
const
  Ary : array [1..12] of string = ('January',   'February', 'March',    'April',
                                   'May',       'June',     'July',     'August',
                                   'September', 'October',  'November', 'December');
begin
  Result := Ary[FMonth];
end;
//문자를 날짜 type으로 바꿈.('20000101'을 날짜로 바꿈)
function Str2Date(const FDate : string) : TDateTime;
var
  Year, Month, Day : Word;
begin
  try
    Year  := StrToInt(Copy(FDate, 1, 4));
    Month := StrToInt(Copy(FDate, 5, 2));
    Day   := StrToInt(Copy(FDate, 7, 2));
    Result := EncodeDate(Year, Month, Day);
  except//예외사항 발생하면 오늘날짜 return
    Result := Date;
  end;
end;

//월 plus, minus. param이 날자로 넘어옴
function AddMonth(const FDate: string; Cnt: Integer): string;
var
  nDate : TDateTime;
  Year, Month, Day : Word;
  i : Integer;
  rDay, sDay : Integer;
begin
  nDate := Date;
  
  Year  := StrToInt(Copy(FDate, 1, 4));
  Month := StrToInt(Copy(FDate, 5, 2));
  Day   := StrToInt(Copy(FDate, 7, 2));
  rDay  := Day;//임시보관

  if Cnt > 0 then
    for i := 1 to Cnt do
    begin
      nDate := EncodeDate(Year, Month, 1);
      nDate := nDate + 31;//31일을 더하면 다음달임.
      DecodeDate(nDate, Year, Month, Day);
    end
  else
    for i := -1 downto Cnt do
    begin
      nDate := EncodeDate(Year, Month, 1);//월의 첫날을 Encode
      nDate := nDate - 1;//월의 첫날에서 1일을 차감
      DecodeDate(nDate, Year, Month, Day);
    end;

  sDay := DaysPerMonth[Month];
  if (Month = 2) and LeapYear(nDate) then
    Inc(sDay);

  if rDay > sDay then
    rDay := sDay;

  Result := FormatDateTime('YYYYMMDD', EncodeDate(Year, Month, rDay));
end;

function AddMonth3(const FMonth: string; FCnt: Integer): string;//param이 2021.07 형태로 넘어옴
var
  pI,
  pYear,
  pMonth: integer;
begin
  pYear := StrToInt(Copy(FMonth, 1, 4));
  pMonth := StrToInt(Copy(FMonth, 6, 2));

  if FCnt > 0 then
    for pI := 1 to FCnt do
    begin
      Inc(pMonth);
      if pMonth > 12 then
      begin
        Inc(pYear);
        pMonth := 1;
      end;
    end
  else
    for pI := -1 downto FCnt do
    begin
      Dec(pMonth);
      if pMonth < 1 then
      begin
        Dec(pYear);
        pMonth := 12;
      end;
    end;
  Result := IntToStr(pYear) + '.' + FormatFloat('00', pMonth);
end;

//'200101' 형태의 자료에 월 plus, minus. param이 월로 넘어옴
function AddMonth2(const FMonth: string; FCnt: Integer): string;
var
  pI,
  pYear,
  pMonth: integer;
begin
  pYear := StrToInt(Copy(FMonth, 1, 4));
  pMonth := StrToInt(Copy(FMonth, 5, 2));

  if FCnt > 0 then
    for pI := 1 to FCnt do
    begin
      Inc(pMonth);
      if pMonth > 12 then
      begin
        Inc(pYear);
        pMonth := 1;
      end;
    end
  else
    for pI := -1 downto FCnt do
    begin
      Dec(pMonth);
      if pMonth < 1 then
      begin
        Dec(pYear);
        pMonth := 12;
      end;
    end;
  Result := IntToStr(pYear) + FormatFloat('00', pMonth);
end;

function AddDate(const FDate: string; Cnt: Integer): string;//날짜 plus, minus.
var
  nDate : TDateTime;
  Year, Month, Day : Word;
begin
  Year  := StrToInt(Copy(FDate, 1, 4));
  Month := StrToInt(Copy(FDate, 5, 2));
  Day   := StrToInt(Copy(FDate, 7, 2));

  nDate := EncodeDate(Year, Month, Day);
  nDate := nDate + Cnt;
  Result := FormatDateTime('YYYYMMDD', nDate);
end;

function GetDayOfWeek(const FDate: string): string;
const
  sAry : array[1..7] of string = ('일요일', '월요일', '화요일', '수요일',
                                  '목요일', '금요일', '토요일');
begin
  Result := sAry[DayOfWeek(Str2Date(FDate))]
end;

function Date2Kor1(const FDate: string): string;
begin
  Result := Copy(FDate, 1, 4) + '년 ' +
            Copy(FDate, 5, 2) + '월 ' +
            Copy(FDate, 7, 2) + '일';
end;

function Month2Kor1(const FMonth: string): string;//월을 '1999년 09월' 형식으로 만듬
begin
  Result := Copy(FMonth, 1, 4) + '년 ' +
            Copy(FMonth, 5, 2) + '월';
end;

function Date2Str(const FDate: TDateTime): string;
begin
  Result := FormatDateTime('YYYYMMDD', FDate);
end;

function GetYear(const FDate: string): string;//연도 return
begin
  Result := Copy(FDate, 1, 4);
end;

function GetYYYYMM(const FDate: string): string;//년+월을 return
begin
  Result := Copy(FDate, 1, 6);
end;

function GetYYYY_MM(const FDate: string): string;//년+월 return
begin
  Result := Copy(FDate, 1, 4) + '.' + Copy(FDate, 5, 2);;
end;

function GetMonth(const FDate: string): string;//월을 return
begin
  Result := Copy(FDate, 5, 2);
end;

function DayPlus(const FDate: string; FInc: integer): string;
var
  ADate: TDateTime;
begin
  ADate := Str2Date(FDate);
  ADate := ADate + FInc;

  Result := Date2Str(ADate);
end;

function GetMonthPrd(const FDate1, FDate2: string): Integer;
var
  pYear1,
  pYear2,
  pMonth1,
  pMonth2,
  pYearDiff: Integer;
begin
  pYear1 := StrToInt(Copy(FDate1, 1, 4));
  pYear2 := StrToInt(Copy(FDate2, 1, 4));
  pMonth1 := StrToInt(Copy(FDate1, 5, 2));
  pMonth2 := StrToInt(Copy(FDate2, 5, 2));

  if (pYear1 = pYear2) and (pMonth1 = pMonth2) then//년,월이 모두 같으면
  begin
    Result := 1;
    Exit;
  end;

  if pYear1 = pYear2 then//년이 같으면
  begin
    Result := pMonth2 - pMonth1 + 1;
    Exit;
  end;

  pYearDiff := pYear2 - pYear1 - 1;
  Result := 12 * pYearDiff + (12 - pMonth1) + pMonth2 + 1;
end;

// 기간이 05.25 ~ 06.24인 경우 GetMonthPrd에서는 2개월이다.
// 2개월에 걸친 기간이므로.
// 그러나 GetMonthPrd2로 계산하면 1개월이다.
// 이는 보험등의 계약에 대한 개월수로서 민법에 따른 계산이다.
// 즉, 05.25부터 다음달(6월) 24일(25일 전일)까지가 1개월로 취급되기 때문이다.
function GetMonthPrd2(const FDate1, FDate2: string): Integer;
var
  pYear1,
  pYear2,
  pMonth1,
  pMonth2,
  pDay1,
  pDay2 : Integer;
begin
  pYear1  := StrToInt(Copy(FDate1, 1, 4));
  pYear2  := StrToInt(Copy(FDate2, 1, 4));
  pMonth1 := StrToInt(Copy(FDate1, 5, 2));
  pMonth2 := StrToInt(Copy(FDate2, 5, 2));
  pDay1   := StrToInt(Copy(FDate1, 7, 2));
  pDay2   := StrToInt(Copy(FDate2, 7, 2));

  pMonth2 := pMonth2 + (pYear2 - pYear1) * 12;
  Result := pMonth2 - pMonth1;
  if pDay2 >= pDay1 then
    Inc(Result);
end;

function StrR(Value: Extended; Len, Digits: integer): string;
begin
  Result := FloatToStr(Int(Value));
  while Length(Result) < Len do
    Result := '0' + Result;
end;
//Fig2 :1=>한글금액, 2=>한자금액
function Num2KoreanA(const Fig1: Real; Fig2 : Integer) : string;
const
  xA: array[1..9, 1..2] of string = (('일', '壹'), ('이', '貳'), ('삼', '參'),
                                     ('사', '四'), ('오', '五'), ('육', '六'),
                                     ('칠', '七'), ('팔', '八'), ('구', '九'));
  xB: array[1..4, 1..2] of string = (('천', '阡'), ('백', '百'),
                                     ('십', '拾'), ('', ''));
var
  xC: array[1..4] of string;
var
   i,
   j : integer;
   S : string ;
begin
  for i := 1 to 4 do//일단 이렇게 하고.
    xC[i] := '';
    
  for i := 1 to 4 do
    xC[i] := Copy(StrR(Fig1, 4, 0), i, 1);

  S := '';
  for i := 1 to 4 do
  begin
    if (xC[i] = '0') or (xC[i] = '') then
      Continue;
    j := StrToInt(xC[i]);
    S := S + xA[j, Fig2] + xB[i, Fig2];
  end;
  Result := S;
end;
//Fig2 :1=>한글금액, 2=>한자금액
function Num2Korean(const Fig1 : Real; Fig2 : integer):string;//숫자를 한글로 표시
//**********************************************
const
  qAA: array[1..4] of string = ('1000000000000', '100000000', '10000', '1');
  qBB: array[1..4, 1..2] of string = (('조', '兆'), ('억', '億'), ('만', '萬'), ('', ''));
var
  xHan,
  i: integer;
  FNew,
  FTmp: Real;
begin
  xHan := Fig2;
  FNew := Int(Fig1);

  for i:=1 to 4 do
  begin
    FTmp := Int(FNew / StrToFloat(qAA[i]));
    if FTmp > 0 then
    begin
      FNew  :=FNew - (FTmp * StrToFloat(qAA[i]));
      Result := Result + Num2KoreanA(FTmp, xHan) + qBB[i, xHan];
    end;
  end;
end;

//반올림
//Rounder(123.125, -2) => 123.13
//Rounder(123.124, -2) => 123.12
//Rounder(12345, 2) => 12300
//Rounder(12355, 2) => 12400
function Rounder(X : Extended; FDec: integer): Extended;
begin
  Result := X * (Power(10, FDec * (-1)));
  Result := Trunc(Result) + Trunc(Frac(Result) * 2);
  Result := Result / Power(10, FDec * (-1));
end;
{
function Is_OS_2000: Boolean;//os가 windows 2000인가?
const
  sWin2000              = '2000 ';
  VER_PLATFORM_WINDOWS_2000 = VER_PLATFORM_WIN32_NT;
  Windows2000_Version = 5;
type
  TWindowsSystem = (wsWIN3, wsWIN9X, wsWINNT);
begin
  Result := False;
  if Win32Platform = VER_PLATFORM_WIN32_NT then
  begin
    if Win32MajorVersion >= Windows2000_Version then
      Result := True;
  end;
end;
}
//integer->str로 변환. 0이면 '0'을 return
function Int2Str_0(const FValue: integer): string;
begin
  Result := FormatFloat(dfNormalZ, FValue);
end;

//float->str로 변한. 00:소수이하는 0, 결과가 0이면 '0'으로 표시
function Float2Str_00(const FValue: Double): string;
begin
  Result := FormatFloat(dfNormalZ, FValue);
end;

//float->str로 변한. 0X:소수이하는 0, 결과가 0이면 ''로 표시
function Float2Str_0X(const FValue: Double): string;
begin
  Result := FormatFloat(dfNormal, FValue);
end;

//float->str로 변한. 20:소수이하는 0, 결과가 0이면 '0'으로 표시
function Float2Str_20(const FValue: Double): string;
begin
  Result := FormatFloat(dfDec_2, FValue);
end;

//float->str로 변한. 소수이하도 고려
function Float2Str(const FValue: Double; FDec: integer): string;
var
  i: integer;
  pStr: string;
begin
  pStr := '#,##0';
  if FDec > 0 then
  begin
    pStr := pStr + '.';
    for i := 1 to FDec - 1 do
      pStr := pStr + '#';
    pStr := pStr + '0';
  end;
  Result := FormatFloat(pStr, FValue);
end;

procedure ClearDir(Path: string);
var
  SrchRec: TSearchRec;
  uResult : Integer;
begin
  if Path[Length(Path)] <> '\' then
    Path := Path + '\';

  uResult := FindFirst(Path + '*.*', faAnyFile, SrchRec);
  try
    while uResult = 0 do begin
      if (SrchRec.Name[1] <> '.') and (SrchRec.Attr <> faVolumeID) then
      begin
        if SrchRec.Attr and faDirectory > 0 then
        begin
          ClearDir(Path + SrchRec.Name);
          RmDir(Path + SrchRec.Name);
        end
        else begin
          //$00000001은 faReadOnly 상수임. 이것 대신 faReadOnly를 사용하면
          //error 발생. 이유는 모름
          if SrchRec.Attr and $00000001 > 0 then
            FileSetAttr(Path + SrchRec.Name, faArchive);
          DeleteFile(Path + SrchRec.Name);
        end;
      end;
      uResult := FindNext(SrchRec);
    end;
  finally
    FindClose(SrchRec);
  end;
end;

function Get_exe_path: string;
begin
  Result := ExtractFilePath(Application.ExeName);
end;

end.
