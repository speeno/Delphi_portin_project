unit globalCommon;

interface

uses StdCtrls, SysUtils;

procedure SetMonth2Combo(fCombo: TComboBox);

var
  gCompany_name: string;

implementation

uses globalSystem;

procedure SetMonth2Combo(fCombo: TComboBox);
var
  pMonth_1,
  pMonth_2: string;//날짜형태를 'yyyymm'형태로 바꾼 문자
begin
  fCombo.Items.Clear;
  // 오늘이 속한 월을 구함
  pMonth_2 := GetYYYYMM(Date2Str(Date));//'yyyymm'형태
  pMonth_1 := '200701';
  while pMonth_1 <= pMonth_2 do
  begin
    fCombo.Items.Insert(0, GetYYYY_MM(pMonth_1));//yyyy.mm 형태로 insert
    pMonth_1 := AddMonth2(pMonth_1, 1);//1개월 plus.
  end;
  // ===>> 오늘이 속한 월을 ItemIndex로 지정
  pMonth_1 := GetYYYY_MM(Date2Str(Date));//'yyyy.mm'형태
  fCombo.ItemIndex := fCombo.Items.IndexOf(pMonth_1);
end;

end.
 