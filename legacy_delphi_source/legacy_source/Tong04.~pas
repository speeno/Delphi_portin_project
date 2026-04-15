unit Tong04;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Printers, IniFiles, Db, Mylabel, StdCtrls, ExtCtrls, FR_Chart,
  FR_Prntr, FR_Class, FR_View, FR_Pars, FR_Intrp, FR_DSet, FR_DBSet, FR_DBRel;

type
  TTong40 = class(TForm)
    FontDialog: TFontDialog;
    myLabel3d1: TmyLabel3d;
    procedure PrinTing00(St0,St1,St2,St3,St4,St5,St6,St7,St8,St9: String);
    procedure PrinTing01(Str: String);
    procedure PrinTing02(Str: String);
    procedure PrinTing03(Str: String);
    procedure PrinTing04(Str: String);
    procedure PrinTing08(_Scode,_Gcode,_Gdate,_Gubun,_Jubun,_Hcode: String);
    procedure PrinTing09(Str: String);
    procedure Print_11_01(Sender: TObject);
    procedure Print_11_02(Sender: TObject);
    procedure Print_12_01(Sender: TObject);
    procedure Print_12_02(Sender: TObject);
    procedure Print_13_01(Sender: TObject);
    procedure Print_13_02(Sender: TObject);
    procedure Print_14_01(Sender: TObject);
    procedure Print_14_02(Sender: TObject);
    procedure Print_14_11(Sender: TObject);
    procedure Print_15_01(Sender: TObject);
    procedure Print_15_02(Sender: TObject);
    procedure Print_16_01(Sender: TObject);
    procedure Print_16_02(Sender: TObject);
    procedure Print_17_01(Sender: TObject);
    procedure Print_17_02(Sender: TObject);
    procedure Print_17_03(Sender: TObject);
    procedure Print_18_01(Sender: TObject);
    procedure Print_18_02(Sender: TObject);
    procedure Print_19_01(Sender: TObject);
    procedure Print_19_02(Sender: TObject);
    procedure Print_10_01(Sender: TObject);
    procedure Print_10_02(Sender: TObject);
    procedure Print_21_01(Sender: TObject);
    procedure Print_21_02(Sender: TObject);
    procedure Print_22_01(Sender: TObject);
    procedure Print_22_02(Sender: TObject);
    procedure Print_23_01(Sender: TObject);
    procedure Print_23_02(Sender: TObject);
    procedure Print_24_01(Sender: TObject);
    procedure Print_24_02(Sender: TObject);
    procedure Print_25_01(Sender: TObject);
    procedure Print_25_02(Sender: TObject);
    procedure Print_26_01(Sender: TObject);
    procedure Print_26_02(Sender: TObject);
    procedure Print_27_01(Sender: TObject);
    procedure Print_27_02(Sender: TObject);
    procedure Print_28_01(Sender: TObject);
    procedure Print_28_02(Sender: TObject);
    procedure Print_29_01(Sender: TObject);
    procedure Print_29_02(Sender: TObject);
    procedure Print_20_01(Sender: TObject);
    procedure Print_20_02(Sender: TObject);
    procedure Print_31_01(Sender: TObject);
    procedure Print_31_02(Sender: TObject);
    procedure Print_32_01(Sender: TObject);
    procedure Print_32_02(Sender: TObject);
    procedure Print_33_01(Sender: TObject);
    procedure Print_33_02(Sender: TObject);
    procedure Print_33_03(Sender: TObject);
    procedure Print_33_04(Sender: TObject);
    procedure Print_34_01(Sender: TObject);
    procedure Print_34_02(Sender: TObject);
    procedure Print_34_05(Sender: TObject);
    procedure Print_34_06(Sender: TObject);
    procedure Print_35_01(Sender: TObject);
    procedure Print_35_02(Sender: TObject);
    procedure Print_36_01(Sender: TObject);
    procedure Print_36_02(Sender: TObject);
    procedure Print_37_01(Sender: TObject);
    procedure Print_37_02(Sender: TObject);
    procedure Print_38_01(Sender: TObject);
    procedure Print_38_02(Sender: TObject);
    procedure Print_39_01(Sender: TObject);
    procedure Print_39_02(Sender: TObject);
    procedure Print_39_03(Sender: TObject);
    procedure Print_39_04(Sender: TObject);
    procedure Print_39_05(Sender: TObject);
    procedure Print_39_06(Sender: TObject);
    procedure Print_39_07(Sender: TObject);
    procedure Print_39_08(Sender: TObject);
    procedure Print_39_09(Sender: TObject);
    procedure Print_39_11(Sender: TObject);
    procedure Print_39_21(Sender: TObject);
    procedure Print_30_01(Sender: TObject);
    procedure Print_30_02(Sender: TObject);
    procedure Print_41_01(Sender: TObject);
    procedure Print_41_02(Sender: TObject);
    procedure Print_42_01(Sender: TObject);
    procedure Print_42_02(Sender: TObject);
    procedure Print_43_01(Sender: TObject);
    procedure Print_43_02(Sender: TObject);
    procedure Print_44_01(Sender: TObject);
    procedure Print_44_02(Sender: TObject);
    procedure Print_45_01(Sender: TObject);
    procedure Print_45_02(Sender: TObject);
    procedure Print_46_01(Sender: TObject);
    procedure Print_46_02(Sender: TObject);
    procedure Print_47_01(Sender: TObject);
    procedure Print_47_02(Sender: TObject);
    procedure Print_48_01(Sender: TObject);
    procedure Print_48_02(Sender: TObject);
    procedure Print_49_01(Sender: TObject);
    procedure Print_49_02(Sender: TObject);
    procedure Print_40_01(Sender: TObject);
    procedure Print_40_02(Sender: TObject);
    procedure Print_51_01(Sender: TObject);
    procedure Print_51_02(Sender: TObject);
    procedure Print_52_01(Sender: TObject);
    procedure Print_52_02(Sender: TObject);
    procedure Print_53_01(Sender: TObject);
    procedure Print_53_02(Sender: TObject);
    procedure Print_54_01(Sender: TObject);
    procedure Print_54_02(Sender: TObject);
    procedure Print_55_01(Sender: TObject);
    procedure Print_55_02(Sender: TObject);
    procedure Print_55_03(Sender: TObject);
    procedure Print_55_04(Sender: TObject);
    procedure Print_56_01(Sender: TObject);
    procedure Print_56_02(Sender: TObject);
    procedure Print_57_01(Sender: TObject);
    procedure Print_57_02(Sender: TObject);
    procedure Print_58_01(Sender: TObject);
    procedure Print_58_02(Sender: TObject);
    procedure Print_59_01(Sender: TObject);
    procedure Print_59_02(Sender: TObject);
    procedure Print_59_11(Sender: TObject);
    procedure Print_59_12(Sender: TObject);
    procedure Print_50_01(Sender: TObject);
    procedure Print_50_02(Sender: TObject);
    procedure Print_61_01(Sender: TObject);
    procedure Print_61_02(Sender: TObject);
    procedure Print_62_01(Sender: TObject);
    procedure Print_62_02(Sender: TObject);
    procedure Print_63_01(Sender: TObject);
    procedure Print_63_02(Sender: TObject);
    procedure Print_64_01(Sender: TObject);
    procedure Print_64_02(Sender: TObject);
    procedure Print_65_01(Sender: TObject);
    procedure Print_65_02(Sender: TObject);
    procedure Print_66_01(Sender: TObject);
    procedure Print_66_02(Sender: TObject);
    procedure Print_67_01(Sender: TObject);
    procedure Print_67_02(Sender: TObject);
    procedure Print_68_01(Sender: TObject);
    procedure Print_68_02(Sender: TObject);
    procedure Print_69_01(Sender: TObject);
    procedure Print_69_02(Sender: TObject);
    procedure Print_60_01(Sender: TObject);
    procedure Print_60_02(Sender: TObject);
    procedure Print_99_01(Sender: TObject);
    procedure Print_99_02(Sender: TObject);
    procedure _Gg_Magn_(Str:String);
    procedure _Sv_Gsum_(_S1_Ssub,_H1_Ssub,_Sv_Gsum: String);
    procedure _Sv_Chng_(_S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng: String);
    procedure _Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng: String);
    procedure _Sb_Ghng_(_Sb_Csum,_Sv_Ghng: String);
    procedure SetTring01(Str1,Str2,Str3,Str4,Str5,Str6: String);
    procedure SetTring02(Str1,Str2,Str3,Str4,Str5,Str6: String);
    procedure SetTring11(Str1,Str2,Str3,Str4,Str5,Str6: String);
    procedure SetTring12(Str1,Str2,Str3,Str4,Str5,Str6: String);
    procedure SetTring13(Str1,Str2,Str3,Str4,Str5,Str6: String);
    procedure FormShow(Sender: TObject);
    procedure FormHide(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Tong40: TTong40;
  p_Sdate: String;
  p_GsumX,p_GsumY,p_Print,p_Count,p_Total: Double;

implementation

{$R *.DFM}

uses Base01,Tong02,Tong06,Seek01,Seek02,Seek05,Seak05,Seak08,TcpLib,Chul,
     Subu11,Subu12,Subu13,Subu14,Subu15,Subu16,Subu17,Subu18,Subu19,Subu10,
     Subu21,Subu22,Subu23,Subu24,Subu25,Subu26,Subu27,Subu28,Subu29,Subu20,
     Subu31,Subu32,Subu33,Subu34,Subu35,Subu36,Subu37,Subu38,Subu39,Subu30,
     Subu14_1,Subu38_2,Subu39_1,Subu39_2,Subu42_1,Subu44_1,Subu45_1,
     Subu34_1,Subu55_1,Subu58_1,Subu99,
     Subu41,Subu42,Subu43,Subu44,Subu45,Subu46,Subu47,Subu48,Subu49,Subu40,
     Subu51,Subu52,Subu53,Subu54,Subu55,Subu56,Subu57,Subu58,Subu59,Subu50,
     Subu61,Subu62,Subu63,Subu64,Subu65,Subu66,Subu67,Subu68,Subu69,Subu60,
     Seep11,Seep13,Seok03;

procedure TTong40.PrinTing00(St0,St1,St2,St3,St4,St5,St6,St7,St8,St9: String);
var SetupIni : TIniFile;
    SearchRec : TSearchRec;
    Sp1,Sp2: String;
    ff1,ff2: Integer;
    i, rCnt: Integer;
begin
  // read
  SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
  with SetupIni do begin
    FontDialog.Font.Name := ReadString( 'Fonts', 'Name',  '');
    FontDialog.Font.Size := ReadInteger('Fonts', 'Size',  10);
    p_Print := ReadInteger('Print', 'Print', 1 );
    p_Count := ReadInteger('Print', 'Count', 10);
    p_Total := ReadInteger('Print', 'Total', 1 );
    RBand   := ReadInteger('Print', 'List1', 10);
    i := ReadInteger('Fonts', 'Style', 3 );
    if i=1 Then FontDialog.Font.Style:= [];
    if i=2 Then FontDialog.Font.Style:= [fsItalic];
    if i=3 Then FontDialog.Font.Style:= [fsBold];
    if i=4 Then FontDialog.Font.Style:= [fsBold,fsItalic];
    if i=5 Then FontDialog.Font.Style:= [fsUnderline];
    if i=6 Then FontDialog.Font.Style:= [fsItalic,fsUnderline];
    if i=7 Then FontDialog.Font.Style:= [fsBold,fsUnderline];
    if i=8 Then FontDialog.Font.Style:= [fsBold,fsItalic,fsUnderline];
  end;
  SetupIni.Free;
  if (St0='21')or(St0='22')or(St0='23')or(St0='24')or(St0='25')or(St0='29') Then begin

    oSqry:=nSqry;

    ff1 := FindFirst( GetExecPath + 'Report\Report_2_11.frf', faAnyFile, SearchRec);  //2
    ff2 := FindFirst( GetExecPath + 'Report\Report_2_13.frf', faAnyFile, SearchRec);  //0

    if(St0 = '22')and(Base10.Database.Database='book_kb_db')then begin
      Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

      Tong60.frReport21_01.Clear;
      Tong60.frReport21_01.LoadFromFile(GetExecPath + 'Report\Report_2_19.frf');

      Tong60.frUserDataset21_01.RangeEndCount:=Tong60.frReport20_00('1');
      oSqry.First;
      With Tong60.frReport21_01 do begin
        ShowReport;
      end;

      oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
    end else
    if(ff1 = 0)then begin
      Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

      Tong60.frReport21_01.Clear;
      Tong60.frReport21_01.LoadFromFile(GetExecPath + 'Report\Report_2_11.frf');

      Tong60.frUserDataset21_01.RangeEndCount:=Tong60.frReport20_00('1');
      oSqry.First;
      With Tong60.frReport21_01 do begin
        if St1='2' then
        ShowReport else
        if PrepareReport then
        PrintPreparedReport(' ',1,true, frall);
      end;

      oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
    end else
    if(ff2 = 0)then begin
      Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

      Tong60.frReport20_01.Clear;
      Tong60.frReport20_01.LoadFromFile(GetExecPath + 'Report\Report_2_13.frf');

      Tong60.frUserDataset20_01.RangeEndCount:=Tong60.frReport20_00('1');
      oSqry.First;
      rCnt := oSqry.RecordCount;
      With Tong60.frReport20_01 do begin
        if St1='2' then
        ShowReport
        else if PrepareReport then
        PrintPreparedReport(' ',1,true, frall);
      end;
      oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
    end else begin
    { oSqry:=Base10.T2_Sub11;
      oSqry.LoadFromFile(GetExecPath + 'Data\Chulpan.cds'); }
      PrinTing01('7');
    end;

  end;


  if St0='32' Then begin
     if St1='1' Then begin

       oSqry:=Sobo28.T2_Sub81;

       ff1 := FindFirst( GetExecPath + 'Report\Report_2_14.frf', faAnyFile, SearchRec);

       if(ff1 = 0)then begin
         Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

         Tong60.frReport23_01.Clear;
         Tong60.frReport23_01.LoadFromFile(GetExecPath + 'Report\Report_2_14.frf');

         Tong60.frUserDataset23_01.RangeEndCount:=oSqry.FieldByName('Gqut2').AsInteger;
         Tong60.frReport23_01.Dataset:=Tong60.frUserDataset23_01;
         With Tong60.frReport23_01 do begin
           ShowReport;
         end;
         oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
       end;

     end;
     if St1='2' Then begin

       oSqry:=Sobo28.T2_Sub81;

       ff1 := FindFirst( GetExecPath + 'Report\Report_2_14.frf', faAnyFile, SearchRec);

       if(ff1 = 0)then begin
         Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

         Tong60.frReport23_01.Clear;
         Tong60.frReport23_01.LoadFromFile(GetExecPath + 'Report\Report_2_14.frf');

         Tong60.frUserDataset23_01.RangeEndCount:=oSqry.FieldByName('Gqut2').AsInteger;
         Tong60.frReport23_01.Dataset:=Tong60.frUserDataset23_01;
         With Tong60.frReport23_01 do begin
           if PrepareReport then
           PrintPreparedReport(' ',1,true, frall);
         end;
         oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
       end;

     end;
  end;

  if St0='28' Then begin
     if St1='1' Then begin

       ff1 := FindFirst( GetExecPath + 'Report\Report_2_83.frf', faAnyFile, SearchRec);
       ff2 := FindFirst( GetExecPath + 'Report\Report_2_84.frf', faAnyFile, SearchRec);

       if(ff1 = 0)then begin

         ff1 := mSqry.FieldByName('Gnum1').Value;

         oSqry:=Base10.T2_Sub01;
         Base10.OpenExit(oSqry);
         Base10.OpenShow(oSqry);

         Sp1:=' Order By Gcode,Gdate';
         Sp2:='Gdate'+'>='+#39+St2+#39+' and '+
              'Gdate'+'<='+#39+St3+#39+' and '+
              'Gcode'+' ='+#39+St4+#39;

         Sqlen := 'Select * From S3_Ssub Where '+D_Select+Sp2+Sp1;
         Base10.Socket.RunSQL(Sqlen);
         Base10.Socket.busyloop;
         if Base10.Socket.body_data <> 'ERROR' then
           Base10.Socket.ClientGrid(oSqry)
         else ShowMessage(E_Open);

         oSqry.First;
         Tong60.frUserDataset28_01.RangeEndCount:=ff1;

         Tong60.frReport28_01.Clear;
         Tong60.frReport28_01.LoadFromFile(GetExecPath + 'Report\Report_2_83.frf');

         With Tong60.frReport28_01 do begin
           ShowReport;
         end;

       end else
       if(ff2 = 0)then begin

         ff2 := mSqry.FieldByName('Gnum1').Value;

         oSqry:=Base10.T2_Sub01;
         Base10.OpenExit(oSqry);
         Base10.OpenShow(oSqry);

         Sp1:=' Order By Gcode,Gdate';
         Sp2:='Gdate'+'>='+#39+St2+#39+' and '+
              'Gdate'+'<='+#39+St3+#39+' and '+
              'Gcode'+' ='+#39+St4+#39;

         Sqlen := 'Select * From S3_Ssub Where '+D_Select+Sp2+Sp1;
         Base10.Socket.RunSQL(Sqlen);
         Base10.Socket.busyloop;
         if Base10.Socket.body_data <> 'ERROR' then
           Base10.Socket.ClientGrid(oSqry)
         else ShowMessage(E_Open);

         oSqry.First;
         Tong60.frUserDataset28_02.RangeEndCount:=ff2;

         Tong60.frReport28_02.Clear;
         Tong60.frReport28_02.LoadFromFile(GetExecPath + 'Report\Report_2_84.frf');

         With Tong60.frReport28_02 do begin
           ShowReport;
         end;

       end else begin
       { mSqry:=Base10.T2_Sub82;
         mSqry.LoadFromFile(GetExecPath + 'Data\Chulpan.cds'); }
         oSqry:=Base10.T2_Sub01;
         Base10.OpenExit(oSqry);
         Base10.OpenShow(oSqry);

         Sp1:=' Order By Gcode,Gdate';
         Sp2:='Gdate'+'>='+#39+St2+#39+' and '+
              'Gdate'+'<='+#39+St3+#39+' and '+
              'Gcode'+' ='+#39+St4+#39;

         Sqlen := 'Select * From S3_Ssub Where '+D_Select+Sp2+Sp1;
         Base10.Socket.RunSQL(Sqlen);
         Base10.Socket.busyloop;
         if Base10.Socket.body_data <> 'ERROR' then
           Base10.Socket.ClientGrid(oSqry)
         else ShowMessage(E_Open);

         PrinTing03('9');
       end;

     end;
     if St1='2' Then begin

       ff1 := FindFirst( GetExecPath + 'Report\Report_2_83.frf', faAnyFile, SearchRec);
       ff2 := FindFirst( GetExecPath + 'Report\Report_2_84.frf', faAnyFile, SearchRec);

       if(ff1 = 0)then begin

         Bmark:=mSqry.GetBookmark; mSqry.DisableControls;
         mSqry.First;
         While mSqry.EOF=False do begin
           ff1 := ff1+mSqry.FieldByName('Gnum1').Value;
           mSqry.Next;
         end;
         mSqry.GotoBookmark(Bmark); mSqry.FreeBookmark(Bmark); mSqry.EnableControls;

         oSqry:=Base10.T2_Sub01;
         Base10.OpenExit(oSqry);
         Base10.OpenShow(oSqry);

         Sp1:=' Order By Gcode,Gdate';
         Sp2:='Gdate'+'>='+#39+St2+#39+' and '+
              'Gdate'+'<='+#39+St3+#39;

         Sqlen := 'Select * From S3_Ssub Where '+D_Select+Sp2+Sp1;
         Base10.Socket.RunSQL(Sqlen);
         Base10.Socket.busyloop;
         if Base10.Socket.body_data <> 'ERROR' then
           Base10.Socket.ClientGrid(oSqry)
         else ShowMessage(E_Open);

         oSqry.First;
         Tong60.frUserDataset28_01.RangeEndCount:=ff1;

         Tong60.frReport28_01.Clear;
         Tong60.frReport28_01.LoadFromFile(GetExecPath + 'Report\Report_2_83.frf');

         With Tong60.frReport28_01 do begin
           ShowReport;
         end;

       end else
       if(ff2 = 0)then begin

         Bmark:=mSqry.GetBookmark; mSqry.DisableControls;
         mSqry.First;
         While mSqry.EOF=False do begin
           ff2 := ff2+mSqry.FieldByName('Gnum1').Value;
           mSqry.Next;
         end;
         mSqry.GotoBookmark(Bmark); mSqry.FreeBookmark(Bmark); mSqry.EnableControls;

         oSqry:=Base10.T2_Sub01;
         Base10.OpenExit(oSqry);
         Base10.OpenShow(oSqry);

         Sp1:=' Order By Gcode,Gdate';
         Sp2:='Gdate'+'>='+#39+St2+#39+' and '+
              'Gdate'+'<='+#39+St3+#39;

         Sqlen := 'Select * From S3_Ssub Where '+D_Select+Sp2+Sp1;
         Base10.Socket.RunSQL(Sqlen);
         Base10.Socket.busyloop;
         if Base10.Socket.body_data <> 'ERROR' then
           Base10.Socket.ClientGrid(oSqry)
         else ShowMessage(E_Open);

         oSqry.First;
         Tong60.frUserDataset28_02.RangeEndCount:=ff2;

         Tong60.frReport28_02.Clear;
         Tong60.frReport28_02.LoadFromFile(GetExecPath + 'Report\Report_2_84.frf');

         With Tong60.frReport28_02 do begin
           ShowReport;
         end;

       end else begin
       { mSqry:=Base10.T2_Sub82;
         mSqry.LoadFromFile(GetExecPath + 'Data\Chulpan.cds'); }
         While mSqry.EOF=False do begin
         oSqry:=Base10.T2_Sub01;
         Base10.OpenExit(oSqry);
         Base10.OpenShow(oSqry);

         Sp1:=' Order By Gcode,Gdate';
         Sp2:='Gdate'+'>='+#39+St2+#39+' and '+
              'Gdate'+'<='+#39+St3+#39+' and '+
              'Gcode'+' ='+#39+St4+#39;

         Sqlen := 'Select * From S3_Ssub Where '+D_Select+Sp2+Sp1;
         Base10.Socket.RunSQL(Sqlen);
         Base10.Socket.busyloop;
         if Base10.Socket.body_data <> 'ERROR' then
           Base10.Socket.ClientGrid(oSqry)
         else ShowMessage(E_Open);

         PrinTing03('9');
         mSqry.Next;
         end;
       end;

     end;
  end;


  if St0='49' Then begin
     p_Sdate:=St2;
     if St1='1' Then begin

       oSqry:=Sobo49.T4_Sub91;

       ff1 := FindFirst( GetExecPath + 'Report\Report_4_95.frf', faAnyFile, SearchRec);
       ff2 := FindFirst( GetExecPath + 'Report\Report_4_96.frf', faAnyFile, SearchRec);

       if(ff1 = 0)then begin
         Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

         Tong60.frReport40_01.Clear;
         Tong60.frReport40_01.LoadFromFile(GetExecPath + 'Report\Report_4_95.frf');

         Tong60.frUserDataset40_01.RangeEndCount:=1;
         With Tong60.frReport40_01 do begin
           ShowReport;
         end;
         oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
       end else
       if(ff2 = 0)then begin
         Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

         Tong60.frReport40_02.Clear;
         Tong60.frReport40_02.LoadFromFile(GetExecPath + 'Report\Report_4_96.frf');

         Tong60.frUserDataset40_02.RangeEndCount:=1;
         With Tong60.frReport40_02 do begin
           ShowReport;
         end;
         oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
       end else begin
       { oSqry:=Base10.T4_Sub91;
         oSqry.LoadFromFile(GetExecPath + 'Data\Chulpan.cds'); }
         if oSqry.Locate('Gcode',St4,[loCaseInsensitive])=True then
         PrinTing02('8');
       end;

     end;
     if St1='2' Then begin

       oSqry:=Sobo49.T4_Sub91;

       ff1 := FindFirst( GetExecPath + 'Report\Report_4_95.frf', faAnyFile, SearchRec);
       ff2 := FindFirst( GetExecPath + 'Report\Report_4_96.frf', faAnyFile, SearchRec);

       if(ff1 = 0)then begin
         Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

         Tong60.frReport40_01.Clear;
         Tong60.frReport40_01.LoadFromFile(GetExecPath + 'Report\Report_4_95.frf');

         oSqry.First;
         Tong60.frUserDataset40_01.RangeEndCount:=oSqry.RecordCount;
         With Tong60.frReport40_01 do begin
           ShowReport;
         end;

         oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
       end else
       if(ff2 = 0)then begin
         Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

         Tong60.frReport40_02.Clear;
         Tong60.frReport40_02.LoadFromFile(GetExecPath + 'Report\Report_4_96.frf');

         oSqry.First;
         Tong60.frUserDataset40_02.RangeEndCount:=oSqry.RecordCount;
         With Tong60.frReport40_02 do begin
           ShowReport;
         end;

         oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
       end else begin
       { oSqry:=Base10.T4_Sub91;
         oSqry.LoadFromFile(GetExecPath + 'Data\Chulpan.cds'); }
         While oSqry.EOF=False do begin
         PrinTing02('8');
         oSqry.Next;
         end;
       end;

     end;
     if St1='3' Then begin
     { oSqry:=Base10.T4_Sub91;
       oSqry.LoadFromFile(GetExecPath + 'Data\Chulpan.cds'); }
       if oSqry.Locate('Gcode',St4,[loCaseInsensitive])=True then
       PrinTing02('9');
     end;
     if St1='4' Then begin
     { oSqry:=Base10.T4_Sub91;
       oSqry.LoadFromFile(GetExecPath + 'Data\Chulpan.cds'); }
       While oSqry.EOF=False do begin
       PrinTing02('9');
       oSqry.Next;
       end;
     end;
  end;
end;

{-한국솔루션-}
procedure TTong40.PrinTing01(Str: String);
var
  p_Scode,p_Gdate,p_Gcode,p_Gname,p_Bcode,p_Bname: String;
  p_Gubun,p_Jubun,p_Pubun,p_Gjeja,p_PageQ,P_Gbigo: String;
  p_Gsqut,p_Gdang,p_Grat1,p_Gssum,p_Gqut1,p_Gqut2: Double;
  p_Gsum1,p_Gsum2,p_GsumA,p_GsumB: Double;
  p_Sline,p_Count,p_Spage,p_Pages: Integer;
  gpCol, gpRow, gpCnt, gpHeg, gpWth, qpCnt: Integer;
begin

  Tong40._Gg_Magn_(Str); {7}
  PrinTing09(Str);

  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;
  oSqry.First;
  p_Count:=0; p_Spage:=0; p_Pages:=0; p_GsumA:=0; p_GsumB:=0;
  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
      p_Spage:=p_Spage+1;
    end else begin
      p_Scode:=oSqry.FieldByName('Scode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
    { PrinTing08(p_Scode,p_Gcode,p_Gdate,p_Gubun,p_Jubun); }
      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
        p_GsumA:=p_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
        p_GsumB:=p_GsumB+oSqry.FieldByName('Gssum').AsInteger;
        oSqry.Next;
        if(oSqry.EOF=False)Then p_Pages:=p_Pages+1;
      end;
      oSqry.MoveBy(-p_Pages);
      p_Pages:=p_Pages+1;
      p_Spage:=p_Spage+1;
      if(p_Pages=010)or(p_Pages=020)or(p_Pages=030)or(p_Pages=040)or(p_Pages=050)or
        (p_Pages=060)or(p_Pages=070)or(p_Pages=080)or(p_Pages=090)or(p_Pages=100)or
        (p_Pages=110)or(p_Pages=120)or(p_Pages=130)or(p_Pages=140)or(p_Pages=150)or
        (p_Pages=160)or(p_Pages=170)or(p_Pages=180)or(p_Pages=190)or(p_Pages=200)Then begin
         p_Pages:=Trunc(p_Pages/10);
         p_Pages:=p_Pages+0;
      end else begin
         p_Pages:=Trunc(p_Pages/10);
         p_Pages:=p_Pages+1;
      end;
    end;
    p_Scode:=oSqry.FieldByName('Scode').AsString;
    p_Gname:=oSqry.FieldByName('Gname').AsString;;
    if p_Scode='X' Then begin

      Sqlen := 'Select Gname,Gtel1,Gtel2 From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        p_Gname:=Base10.Socket.GetData(1, 1);
        p_Gbigo:=Base10.Socket.GetData(1, 2)+
             ')'+Base10.Socket.GetData(1, 3);
      end;

    end;
    if p_Scode='Y' Then begin

      Sqlen := 'Select Gname,Gtel1,Gtel2 From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        p_Gname:=Base10.Socket.GetData(1, 1);
        p_Gbigo:=Base10.Socket.GetData(1, 2)+
             ')'+Base10.Socket.GetData(1, 3);
      end;

    end;
    if p_Scode='Z' Then begin

      Sqlen := 'Select Gname,Gtel1,Gtel2 From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        p_Gname:=Base10.Socket.GetData(1, 1);
        p_Gbigo:=Base10.Socket.GetData(1, 2)+
             ')'+Base10.Socket.GetData(1, 3);
      end;

    end;
    Printer.BeginDoc;
    Printer.Canvas.Create;
    Printer.Canvas.Font:=FontDialog.Font;
    gpCol:=0; gpRow:=0; gpCnt:=0;
    gpWth:=Printer.Canvas.TextWidth('A');
    gpHeg:=Printer.Canvas.TextHeight('A');
    gpHeg:=gpHeg+(gpHeg div 6);
    if lSqry.FieldByName('L63').Value<>0 Then gpWth:=lSqry.FieldByName('L63').Value;
    if lSqry.FieldByName('L64').Value<>0 Then gpHeg:=lSqry.FieldByName('L64').Value;
    p_PageQ:=IntToStr(p_Pages)+'/'+IntToStr(p_Spage);
    // Line 1
    Inc(gpCnt,lSqry.FieldByName('Top').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').AsInteger;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L11').Value; //거래일자
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gdate );
      gpCol:=gpWth*lSqry.FieldByName('L12').Value; //거래구분
      Printer.Canvas.TextOut(gpCol, gpRow, oSqry.FieldByName('Pubun').AsString );
      gpCol:=gpWth*lSqry.FieldByName('L13').Value; //폐 이 지
      Printer.Canvas.TextOut(gpCol, gpRow, p_PageQ );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //코    드
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gcode );
      gpCol:=gpWth*lSqry.FieldByName('L22').Value; //거래처명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gname );
      gpCol:=gpWth*lSqry.FieldByName('L23').Value; //합계수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_GsumA)]) );
      gpCol:=gpWth*lSqry.FieldByName('L24').Value; //합계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_GsumB)]) );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').AsInteger;
    p_Gqut1:=0; p_Gsum1:=0;
    p_Count:=0; p_Sline:=0; qpCnt:=gpCnt;
    While(p_Sline<10)and(p_Count<=100)and
      (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
      p_Count:=p_Count+1;
      p_Sline:=p_Sline+1;

      p_Bcode:=oSqry.FieldByName('Bcode').AsString;
      p_Gsqut:=oSqry.FieldByName('Gsqut').AsFloat;
      p_Gdang:=oSqry.FieldByName('Gdang').AsFloat;
      p_Grat1:=oSqry.FieldByName('Grat1').AsFloat;
      p_Gssum:=oSqry.FieldByName('Gssum').AsFloat;
      p_Gsum2:=p_Gsum2+(p_Gsqut*p_Gdang);
      p_Gqut1:=p_Gqut1+p_Gsqut;
      p_Gsum1:=p_Gsum1+p_Gssum;

      Sqlen := 'Select Gname,Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Bcode);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        p_Bname:=Base10.Socket.GetData(1, 1);
        p_Gjeja:=Base10.Socket.GetData(1, 2);
      end;

      gpCol:=gpWth*lSqry.FieldByName('L56').Value; //(Count)
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%03s',[FormatFloat('###0',p_Count)]) );
      gpCol:=gpWth*lSqry.FieldByName('L31').Value; //도서코드
      Printer.Canvas.TextOut(gpCol, gpRow, p_Bcode );
      gpCol:=gpWth*lSqry.FieldByName('L32').Value; //도 서 명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Bname );
      gpCol:=gpWth*lSqry.FieldByName('L53').Value; //저 자 명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gjeja );
      gpCol:=gpWth*lSqry.FieldByName('L33').Value; //도서수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%05s',[FormatFloat('###,###,##0',p_Gsqut)]) );
      gpCol:=gpWth*lSqry.FieldByName('L41').Value; //도서단가
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%06s',[FormatFloat('###,###,##0',p_Gdang)]) );
      gpCol:=gpWth*lSqry.FieldByName('L42').Value; //도서비율
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%03s',[FormatFloat('###,###,##0',p_Grat1)]) );
      gpCol:=gpWth*lSqry.FieldByName('L43').Value; //도서금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gssum)]) );
      Inc(qpCnt,lSqry.FieldByName('L93').AsInteger); gpRow:=gpHeg*qpCnt+lSqry.FieldByName('L58').AsInteger+
                                                               (p_Count*lSqry.FieldByName('L57').AsInteger);
      oSqry.Next;
      if(oSqry.EOF=True)Then p_Count:=101;
    end;
    // Bottom 1
    Inc(gpCnt,lSqry.FieldByName('L94').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L51').Value; //소계수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%05s',[FormatFloat('###,###,##0',p_Gqut1)]) );
      gpCol:=gpWth*lSqry.FieldByName('L52').Value; //소계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gsum1)]) );
      gpCol:=gpWth*lSqry.FieldByName('L54').Value; //합계수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%05s',[FormatFloat('###,###,##0',p_GsumA)]) );
      gpCol:=gpWth*lSqry.FieldByName('L55').Value; //합계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_GsumB)]) );
{-2-}
    if(oSqry.EOF=True)Then p_Sline:=p_Sline-1;
    oSqry.MoveBy(-p_Sline);
    // Bottom 9
    Inc(gpCnt,lSqry.FieldByName('L99').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').AsInteger;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L11').Value; //거래일자
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gdate );
      gpCol:=gpWth*lSqry.FieldByName('L12').Value; //거래구분
      Printer.Canvas.TextOut(gpCol, gpRow, oSqry.FieldByName('Pubun').AsString );
      gpCol:=gpWth*lSqry.FieldByName('L13').Value; //폐 이 지
      Printer.Canvas.TextOut(gpCol, gpRow, p_PageQ );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //코    드
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gcode );
      gpCol:=gpWth*lSqry.FieldByName('L22').Value; //거래처명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gname );
      gpCol:=gpWth*lSqry.FieldByName('L23').Value; //합계수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_GsumA)]) );
      gpCol:=gpWth*lSqry.FieldByName('L24').Value; //합계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_GsumB)]) );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').AsInteger;
    p_Gqut1:=0; p_Gsum1:=0;
    p_Count:=0; p_Sline:=0; qpCnt:=gpCnt;
    While(p_Sline<10)and(p_Count<=100)and
      (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
      p_Count:=p_Count+1;
      p_Sline:=p_Sline+1;

      p_Bcode:=oSqry.FieldByName('Bcode').AsString;
      p_Gsqut:=oSqry.FieldByName('Gsqut').AsFloat;
      p_Gdang:=oSqry.FieldByName('Gdang').AsFloat;
      p_Grat1:=oSqry.FieldByName('Grat1').AsFloat;
      p_Gssum:=oSqry.FieldByName('Gssum').AsFloat;
      p_Gsum2:=p_Gsum2+(p_Gsqut*p_Gdang);
      p_Gqut1:=p_Gqut1+p_Gsqut;
      p_Gsum1:=p_Gsum1+p_Gssum;

      Sqlen := 'Select Gname,Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Bcode);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        p_Bname:=Base10.Socket.GetData(1, 1);
        p_Gjeja:=Base10.Socket.GetData(1, 2);
      end;

      gpCol:=gpWth*lSqry.FieldByName('L56').Value; //(Count)
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%03s',[FormatFloat('###0',p_Count)]) );
      gpCol:=gpWth*lSqry.FieldByName('L31').Value; //도서코드
      Printer.Canvas.TextOut(gpCol, gpRow, p_Bcode );
      gpCol:=gpWth*lSqry.FieldByName('L32').Value; //도 서 명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Bname );
      gpCol:=gpWth*lSqry.FieldByName('L53').Value; //저 자 명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gjeja );
      gpCol:=gpWth*lSqry.FieldByName('L33').Value; //도서수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%05s',[FormatFloat('###,###,##0',p_Gsqut)]) );
      gpCol:=gpWth*lSqry.FieldByName('L41').Value; //도서단가
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%06s',[FormatFloat('###,###,##0',p_Gdang)]) );
      gpCol:=gpWth*lSqry.FieldByName('L42').Value; //도서비율
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%03s',[FormatFloat('###,###,##0',p_Grat1)]) );
      gpCol:=gpWth*lSqry.FieldByName('L43').Value; //도서금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gssum)]) );
      Inc(qpCnt,lSqry.FieldByName('L93').AsInteger); gpRow:=gpHeg*qpCnt+lSqry.FieldByName('L59').AsInteger+
                                                               (p_Count*lSqry.FieldByName('L57').AsInteger);
      oSqry.Next;
      if(oSqry.EOF=True)Then p_Count:=101;
    end;
    // Bottom 1
    Inc(gpCnt,lSqry.FieldByName('L94').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L51').Value; //소계수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%05s',[FormatFloat('###,###,##0',p_Gqut1)]) );
      gpCol:=gpWth*lSqry.FieldByName('L52').Value; //소계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gsum1)]) );
      gpCol:=gpWth*lSqry.FieldByName('L54').Value; //합계수량
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%05s',[FormatFloat('###,###,##0',p_GsumA)]) );
      gpCol:=gpWth*lSqry.FieldByName('L55').Value; //합계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_GsumB)]) );
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
      p_Gqut1:=0; p_Gsum1:=0;
    end else begin
      p_Count:=0; p_GsumA:=0; p_GsumB:=0; p_Spage:=0; p_Pages:=0;
    end;
    Printer.Canvas.TextOut(gpCol, gpRow, '');
    Printer.EndDoc;
  end;
  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
end;

procedure TTong40.PrinTing02(Str: String);
var
  p_Gcode,p_Gdate,p_Gnumb,p_Gname,p_Gposa,p_Gadds,p_Guper: String;
  p_Gnum1,p_Name1,p_Posa1,p_Gadd1,p_Uper1,p_Jomo1,p_Gjomo: String;
  p_Sline,p_Spage,p_Space,p_Gssum: Double;
  gpCol, gpRow, gpCnt, gpHeg, gpWth: Integer;
begin

{ Tong40._Gg_Magn_('8');
  PrinTing09('8'); }
  Tong40._Gg_Magn_(Str); {8}
  PrinTing09(Str);

  p_Spage:=0;
  p_Gnum1:=lSqry.FieldByName('F11').AsString;
  p_Name1:=lSqry.FieldByName('F12').AsString;
  p_Posa1:=lSqry.FieldByName('F21').AsString;
  p_Gadd1:=lSqry.FieldByName('F22').AsString+
       ' '+lSqry.FieldByName('F31').AsString+
       ' '+lSqry.FieldByName('F32').AsString;
  p_Uper1:=lSqry.FieldByName('F41').AsString;
  p_Jomo1:=lSqry.FieldByName('F42').AsString;
  p_Gdate:=p_Sdate;
  p_Sline:=oSqry.RecNo;
  p_Gcode:=oSqry.FieldByName('Gcode').AsString;
  if p_Total=1 Then
  p_Gssum:=oSqry.FieldByName('Gssum').AsInteger;
  if p_Total=2 Then
  p_Gssum:=oSqry.FieldByName('Gsusu').AsInteger;
  if p_Gssum=0 Then Exit;
  if oSqry.FieldByName('Scode').AsString='X' Then begin

    Sqlen :=
    'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo '+
    'From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Gcode);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      p_Gnumb:=Base10.Socket.GetData(1, 1);
      p_Gname:=Base10.Socket.GetData(1, 2);
      p_Gposa:=Base10.Socket.GetData(1, 3);
      p_Gadds:=Base10.Socket.GetData(1, 4)+' '+
               Base10.Socket.GetData(1, 5);
      p_Guper:=Base10.Socket.GetData(1, 6);
      p_Gjomo:=Base10.Socket.GetData(1, 7);
    end;

  end;
  if oSqry.FieldByName('Scode').AsString='Y' Then begin

    Sqlen :=
    'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo '+
    'From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Gcode);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      p_Gnumb:=Base10.Socket.GetData(1, 1);
      p_Gname:=Base10.Socket.GetData(1, 2);
      p_Gposa:=Base10.Socket.GetData(1, 3);
      p_Gadds:=Base10.Socket.GetData(1, 4)+' '+
               Base10.Socket.GetData(1, 5);
      p_Guper:=Base10.Socket.GetData(1, 6);
      p_Gjomo:=Base10.Socket.GetData(1, 7);
    end;

  end;
  if oSqry.FieldByName('Scode').AsString='Z' Then begin

    Sqlen :=
    'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo '+
    'From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Gcode);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      p_Gnumb:=Base10.Socket.GetData(1, 1);
      p_Gname:=Base10.Socket.GetData(1, 2);
      p_Gposa:=Base10.Socket.GetData(1, 3);
      p_Gadds:=Base10.Socket.GetData(1, 4)+' '+
               Base10.Socket.GetData(1, 5);
      p_Guper:=Base10.Socket.GetData(1, 6);
      p_Gjomo:=Base10.Socket.GetData(1, 7);
    end;

  end;
  p_Spage:=p_Spage+1;
  Printer.BeginDoc;
  Printer.Canvas.Create;
  Printer.Canvas.Font:=FontDialog.Font;
  gpCol:=0; gpRow:=0; gpCnt:=0;
  gpWth:=Printer.Canvas.TextWidth('A');
  gpHeg:=Printer.Canvas.TextHeight('A');
  gpHeg:=gpHeg+(gpHeg div 6);
  if lSqry.FieldByName('L63').Value<>0 Then gpWth:=lSqry.FieldByName('L63').Value;
  if lSqry.FieldByName('L64').Value<>0 Then gpHeg:=lSqry.FieldByName('L64').Value;
  if p_Print=1 Then begin
    // Line 1
    Inc(gpCnt,lSqry.FieldByName('Top').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      if lSqry.FieldByName('L45').AsInteger<>0 Then
      Printer.Canvas.Font.Size:=lSqry.FieldByName('L45').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L11').Value; //등록번호
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,01,1) );
      gpCol:=gpWth*lSqry.FieldByName('L12').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,02,1) );
      gpCol:=gpWth*lSqry.FieldByName('L13').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,03,1) );
      gpCol:=gpWth*lSqry.FieldByName('L14').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,04,1) );
      gpCol:=gpWth*lSqry.FieldByName('L15').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,05,1) );
      gpCol:=gpWth*lSqry.FieldByName('L16').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,06,1) );
      gpCol:=gpWth*lSqry.FieldByName('L17').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,07,1) );
      gpCol:=gpWth*lSqry.FieldByName('L18').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,08,1) );
      gpCol:=gpWth*lSqry.FieldByName('L19').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,09,1) );
      gpCol:=gpWth*lSqry.FieldByName('L26').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,10,1) );
      gpCol:=gpWth*lSqry.FieldByName('L27').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,11,1) );
      gpCol:=gpWth*lSqry.FieldByName('L28').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,12,1) );
      gpCol:=gpWth*lSqry.FieldByName('L29').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,13,1) );
      
      gpCol:=(gpWth*lSqry.FieldByName('L11').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,01,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L12').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,02,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L13').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,03,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L14').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,04,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L15').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,05,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L16').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,06,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L17').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,07,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L18').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,08,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L19').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,09,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L26').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,10,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L27').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,11,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L28').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,12,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L29').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,13,1) );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //거래처명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Name1 );
      gpCol:=(gpWth*lSqry.FieldByName('L21').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gname );
      gpCol:=gpWth*lSqry.FieldByName('L22').Value; //대표자명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Posa1 );
      gpCol:=(gpWth*lSqry.FieldByName('L22').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gposa );
    // Line 3
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=08;
      gpCol:=gpWth*lSqry.FieldByName('L23').Value; //주    소
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadd1 );
      gpCol:=(gpWth*lSqry.FieldByName('L23').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadds );
    // Line 4
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L31').Value; //업    태
      Printer.Canvas.TextOut(gpCol, gpRow, p_Uper1 );
      gpCol:=(gpWth*lSqry.FieldByName('L31').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Guper );
      gpCol:=gpWth*lSqry.FieldByName('L32').Value; //종    목
      Printer.Canvas.TextOut(gpCol, gpRow, p_Jomo1 );
      gpCol:=(gpWth*lSqry.FieldByName('L32').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gjomo );
    // Line 5
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      p_Space:=p_Count-Length(FloatToStr(p_Gssum));
      gpCol:=gpWth*lSqry.FieldByName('L41').Value; //년자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,1,4) );
      gpCol:=gpWth*lSqry.FieldByName('L42').Value; //월자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L43').Value; //일자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,9,2) );
      if lSqry.FieldByName('L45').AsInteger<>0 Then
      Printer.Canvas.Font.Size:=lSqry.FieldByName('L45').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L44').Value; //공백
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Space)]),10,1) );
      gpCol:=gpWth*lSqry.FieldByName('L71').Value; //금액02
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),02,1) );
      gpCol:=gpWth*lSqry.FieldByName('L72').Value; //금액03
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),03,1) );
      gpCol:=gpWth*lSqry.FieldByName('L73').Value; //금액04
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),04,1) );
      gpCol:=gpWth*lSqry.FieldByName('L74').Value; //금액05
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),05,1) );
      gpCol:=gpWth*lSqry.FieldByName('L75').Value; //금액06
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),06,1) );
      gpCol:=gpWth*lSqry.FieldByName('L76').Value; //금액07
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),07,1) );
      gpCol:=gpWth*lSqry.FieldByName('L77').Value; //금액08
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),08,1) );
      gpCol:=gpWth*lSqry.FieldByName('L78').Value; //금액09
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),09,1) );
      gpCol:=gpWth*lSqry.FieldByName('L79').Value; //금액10
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),10,1) );
    // Line 6
    Inc(gpCnt,lSqry.FieldByName('L93').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L51').Value; //월자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L52').Value; //일자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,9,2) );
      gpCol:=gpWth*lSqry.FieldByName('L53').Value; //품목
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F51').AsString );
      gpCol:=gpWth*lSqry.FieldByName('L54').Value; //공급가액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%10s',[FormatFloat('###,###,##0',p_Gssum)]) );
    // Bottom 1
    //Inc(gpCnt,lSqry.FieldByName('L95').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
    //  gpCol:=gpWth*lSqry.FieldByName('L55').Value; //
    //  Printer.Canvas.TextOut(gpCol, gpRow, '========================  이  하  여  백  ========================' );
    // Bottom 1
    Inc(gpCnt,lSqry.FieldByName('L94').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      gpCol:=gpWth*lSqry.FieldByName('L56').Value; //합계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gssum)]) );
      gpCol:=gpWth*lSqry.FieldByName('L57').Value; //영수청구
    { if lSqry.FieldByName('L46').AsInteger<>0 Then begin
        if Str='8' then Printer.Canvas.TextOut(gpCol, gpRow, '영수' );
        if Str='9' then Printer.Canvas.TextOut(gpCol, gpRow, '청구' );
      end; }
    // Bottom 0
    Inc(gpCnt,lSqry.FieldByName('L99').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
  end;
  if p_Print=2 Then begin
    // Line 1
    Inc(gpCnt,lSqry.FieldByName('Top').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      if lSqry.FieldByName('L45').AsInteger<>0 Then
      Printer.Canvas.Font.Size:=lSqry.FieldByName('L45').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L11').Value; //등록번호
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,01,1) );
      gpCol:=gpWth*lSqry.FieldByName('L12').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,02,1) );
      gpCol:=gpWth*lSqry.FieldByName('L13').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,03,1) );
      gpCol:=gpWth*lSqry.FieldByName('L14').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,04,1) );
      gpCol:=gpWth*lSqry.FieldByName('L15').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,05,1) );
      gpCol:=gpWth*lSqry.FieldByName('L16').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,06,1) );
      gpCol:=gpWth*lSqry.FieldByName('L17').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,07,1) );
      gpCol:=gpWth*lSqry.FieldByName('L18').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,08,1) );
      gpCol:=gpWth*lSqry.FieldByName('L19').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,09,1) );
      gpCol:=gpWth*lSqry.FieldByName('L26').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,10,1) );
      gpCol:=gpWth*lSqry.FieldByName('L27').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,11,1) );
      gpCol:=gpWth*lSqry.FieldByName('L28').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,12,1) );
      gpCol:=gpWth*lSqry.FieldByName('L29').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,13,1) );

      gpCol:=(gpWth*lSqry.FieldByName('L11').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,01,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L12').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,02,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L13').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,03,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L14').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,04,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L15').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,05,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L16').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,06,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L17').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,07,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L18').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,08,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L19').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,09,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L26').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,10,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L27').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,11,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L28').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,12,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L29').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,13,1) );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //거래처명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Name1 );
      gpCol:=(gpWth*lSqry.FieldByName('L21').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gname );
      gpCol:=gpWth*lSqry.FieldByName('L22').Value; //대표자명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Posa1 );
      gpCol:=(gpWth*lSqry.FieldByName('L22').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gposa );
    // Line 3
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=08;
      gpCol:=gpWth*lSqry.FieldByName('L23').Value; //주    소
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadd1 );
      gpCol:=(gpWth*lSqry.FieldByName('L23').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadds );
    // Line 4
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L31').Value; //업    태
      Printer.Canvas.TextOut(gpCol, gpRow, p_Uper1 );
      gpCol:=(gpWth*lSqry.FieldByName('L31').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Guper );
      gpCol:=gpWth*lSqry.FieldByName('L32').Value; //종    목
      Printer.Canvas.TextOut(gpCol, gpRow, p_Jomo1 );
      gpCol:=(gpWth*lSqry.FieldByName('L32').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gjomo );
    // Line 5
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      p_Space:=p_Count-Length(FloatToStr(p_Gssum));
      gpCol:=gpWth*lSqry.FieldByName('L41').Value; //년자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,1,4) );
      gpCol:=gpWth*lSqry.FieldByName('L42').Value; //월자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L43').Value; //일자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,9,2) );
      if lSqry.FieldByName('L45').AsInteger<>0 Then
      Printer.Canvas.Font.Size:=lSqry.FieldByName('L45').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L44').Value; //공백
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Space)]),10,1) );
      gpCol:=gpWth*lSqry.FieldByName('L71').Value; //금액02
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),02,1) );
      gpCol:=gpWth*lSqry.FieldByName('L72').Value; //금액03
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),03,1) );
      gpCol:=gpWth*lSqry.FieldByName('L73').Value; //금액04
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),04,1) );
      gpCol:=gpWth*lSqry.FieldByName('L74').Value; //금액05
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),05,1) );
      gpCol:=gpWth*lSqry.FieldByName('L75').Value; //금액06
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),06,1) );
      gpCol:=gpWth*lSqry.FieldByName('L76').Value; //금액07
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),07,1) );
      gpCol:=gpWth*lSqry.FieldByName('L77').Value; //금액08
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),08,1) );
      gpCol:=gpWth*lSqry.FieldByName('L78').Value; //금액09
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),09,1) );
      gpCol:=gpWth*lSqry.FieldByName('L79').Value; //금액10
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),10,1) );
    // Line 6
    Inc(gpCnt,lSqry.FieldByName('L93').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L51').Value; //월자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L52').Value; //일자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,9,2) );
      gpCol:=gpWth*lSqry.FieldByName('L53').Value; //품목
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F51').AsString );
      gpCol:=gpWth*lSqry.FieldByName('L54').Value; //공급가액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%10s',[FormatFloat('###,###,##0',p_Gssum)]) );
    // Bottom 1
    //Inc(gpCnt,lSqry.FieldByName('L95').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
    //  gpCol:=gpWth*lSqry.FieldByName('L55').Value; //
    //  Printer.Canvas.TextOut(gpCol, gpRow, '========================  이  하  여  백  ========================' );
    // Bottom 1
    Inc(gpCnt,lSqry.FieldByName('L94').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
      gpCol:=gpWth*lSqry.FieldByName('L56').Value; //합계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gssum)]) );
      gpCol:=gpWth*lSqry.FieldByName('L57').Value; //영수청구
    { if lSqry.FieldByName('L46').AsInteger<>0 Then begin
        if Str='8' then Printer.Canvas.TextOut(gpCol, gpRow, '영수' );
        if Str='9' then Printer.Canvas.TextOut(gpCol, gpRow, '청구' );
      end; }

    // Bottom 0
    Inc(gpCnt,lSqry.FieldByName('L99').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').Value;
      Printer.Canvas.Font.Size:=10;
      if lSqry.FieldByName('L45').AsInteger<>0 Then
      Printer.Canvas.Font.Size:=lSqry.FieldByName('L45').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L11').Value; //등록번호
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,01,1) );
      gpCol:=gpWth*lSqry.FieldByName('L12').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,02,1) );
      gpCol:=gpWth*lSqry.FieldByName('L13').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,03,1) );
      gpCol:=gpWth*lSqry.FieldByName('L14').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,04,1) );
      gpCol:=gpWth*lSqry.FieldByName('L15').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,05,1) );
      gpCol:=gpWth*lSqry.FieldByName('L16').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,06,1) );
      gpCol:=gpWth*lSqry.FieldByName('L17').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,07,1) );
      gpCol:=gpWth*lSqry.FieldByName('L18').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,08,1) );
      gpCol:=gpWth*lSqry.FieldByName('L19').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,09,1) );
      gpCol:=gpWth*lSqry.FieldByName('L26').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,10,1) );
      gpCol:=gpWth*lSqry.FieldByName('L27').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,11,1) );
      gpCol:=gpWth*lSqry.FieldByName('L28').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,12,1) );
      gpCol:=gpWth*lSqry.FieldByName('L29').Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnum1,13,1) );

      gpCol:=(gpWth*lSqry.FieldByName('L11').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,01,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L12').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,02,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L13').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,03,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L14').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,04,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L15').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,05,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L16').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,06,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L17').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,07,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L18').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,08,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L19').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,09,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L26').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,10,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L27').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,11,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L28').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,12,1) );
      gpCol:=(gpWth*lSqry.FieldByName('L29').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gnumb,13,1) );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //거래처명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Name1 );
      gpCol:=(gpWth*lSqry.FieldByName('L21').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gname );
      gpCol:=gpWth*lSqry.FieldByName('L22').Value; //대표자명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Posa1 );
      gpCol:=(gpWth*lSqry.FieldByName('L22').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gposa );
    // Line 3
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').Value;
      Printer.Canvas.Font.Size:=08;
      gpCol:=gpWth*lSqry.FieldByName('L23').Value; //주    소
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadd1 );
      gpCol:=(gpWth*lSqry.FieldByName('L23').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadds );
    // Line 4
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L31').Value; //업    태
      Printer.Canvas.TextOut(gpCol, gpRow, p_Uper1 );
      gpCol:=(gpWth*lSqry.FieldByName('L31').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Guper );
      gpCol:=gpWth*lSqry.FieldByName('L32').Value; //종    목
      Printer.Canvas.TextOut(gpCol, gpRow, p_Jomo1 );
      gpCol:=(gpWth*lSqry.FieldByName('L32').Value)+(gpWth*lSqry.FieldByName('L96').Value);
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gjomo );
    // Line 5
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').Value;
      Printer.Canvas.Font.Size:=10;
      p_Space:=p_Count-Length(FloatToStr(p_Gssum));
      gpCol:=gpWth*lSqry.FieldByName('L41').Value; //년자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,1,4) );
      gpCol:=gpWth*lSqry.FieldByName('L42').Value; //월자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L43').Value; //일자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,9,2) );
      if lSqry.FieldByName('L45').AsInteger<>0 Then
      Printer.Canvas.Font.Size:=lSqry.FieldByName('L45').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L44').Value; //공백
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Space)]),10,1) );
      gpCol:=gpWth*lSqry.FieldByName('L71').Value; //금액02
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),02,1) );
      gpCol:=gpWth*lSqry.FieldByName('L72').Value; //금액03
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),03,1) );
      gpCol:=gpWth*lSqry.FieldByName('L73').Value; //금액04
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),04,1) );
      gpCol:=gpWth*lSqry.FieldByName('L74').Value; //금액05
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),05,1) );
      gpCol:=gpWth*lSqry.FieldByName('L75').Value; //금액06
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),06,1) );
      gpCol:=gpWth*lSqry.FieldByName('L76').Value; //금액07
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),07,1) );
      gpCol:=gpWth*lSqry.FieldByName('L77').Value; //금액08
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),08,1) );
      gpCol:=gpWth*lSqry.FieldByName('L78').Value; //금액09
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),09,1) );
      gpCol:=gpWth*lSqry.FieldByName('L79').Value; //금액10
      Printer.Canvas.TextOut(gpCol, gpRow, Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),10,1) );
    // Line 6
    Inc(gpCnt,lSqry.FieldByName('L93').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').Value;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L51').Value; //월자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L52').Value; //일자
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,9,2) );
      gpCol:=gpWth*lSqry.FieldByName('L53').Value; //품목
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F51').AsString );
      gpCol:=gpWth*lSqry.FieldByName('L54').Value; //공급가액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%10s',[FormatFloat('###,###,##0',p_Gssum)]) );
    // Bottom 1
    //Inc(gpCnt,lSqry.FieldByName('L95').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L58').Value;
    //  gpCol:=gpWth*lSqry.FieldByName('L55').Value; //
    //  Printer.Canvas.TextOut(gpCol, gpRow, '========================  이  하  여  백  ========================' );
    // Bottom 1
    Inc(gpCnt,lSqry.FieldByName('L94').AsInteger); gpRow:=gpHeg*gpCnt+lSqry.FieldByName('L59').Value;
      gpCol:=gpWth*lSqry.FieldByName('L56').Value; //합계금액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gssum)]) );
      gpCol:=gpWth*lSqry.FieldByName('L57').Value; //영수청구
    { if lSqry.FieldByName('L46').AsInteger<>0 Then begin
        if Str='8' then Printer.Canvas.TextOut(gpCol, gpRow, '영수' );
        if Str='9' then Printer.Canvas.TextOut(gpCol, gpRow, '청구' );
      end; }
  end;
  Printer.Canvas.TextOut(gpCol, gpRow, '');
  Printer.EndDoc;
end;

procedure TTong40.PrinTing03(Str: String);
var
  p_Gnum1,p_Gnum2,p_Gname,p_Gposa,p_Gadds: String;
  p_Gadd1,p_Gadd2,p_Gdate,p_Gcode,p_Date1: String;
  p_Sline,p_Spage,p_Gssum,p_Gisum,p_Gosum,p_Gbsum,p_Grat1: Double;
  gpCol, gpRow, gpCnt, gpHeg, gpWth, qpCnt: Integer;
begin

  Tong40._Gg_Magn_(Str); {9}
  PrinTing09(Str);

  oSqry.First;
  While oSqry.EOF=False do begin
    p_Gcode:=oSqry.FieldByName('Gcode').AsString;

    Sqlen :=
    'Select Gname,Gposa,Gadd1,Gadd2,Oadd1,Oadd2,Gnumb,Gnum1 '+
    'From G3_Gjeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Gcode);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      p_Gname:=Base10.Socket.GetData(1, 1);
      p_Gposa:=Base10.Socket.GetData(1, 2);
      p_Gadd1:=Base10.Socket.GetData(1, 3)+' '+
               Base10.Socket.GetData(1, 4);
      p_Gadd2:=Base10.Socket.GetData(1, 5)+' '+
               Base10.Socket.GetData(1, 6);
      p_Gnum1:=Base10.Socket.GetData(1, 7);
      p_Gnum2:=Base10.Socket.GetData(1, 8);
    end;

  //p_Spage:=nSqry.RecNo;
    Printer.BeginDoc;
    Printer.Canvas.Create;
    Printer.Canvas.Font:=FontDialog.Font;
    gpCol:=0; gpRow:=0; gpCnt:=0;
    gpWth:=Printer.Canvas.TextWidth('A');
    gpHeg:=Printer.Canvas.TextHeight('A');
    gpHeg:=gpHeg+(gpHeg div 6);
    if lSqry.FieldByName('L63').Value<>0 Then gpWth:=lSqry.FieldByName('L63').Value;
    if lSqry.FieldByName('L64').Value<>0 Then gpHeg:=lSqry.FieldByName('L64').Value;
    // Line 1
    Inc(gpCnt,lSqry.FieldByName('Top').AsInteger); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L11').Value; //관리번호
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%03s',[FormatFloat('###,###,##0',p_Spage)]) );
    // Line 2
    Inc(gpCnt,lSqry.FieldByName('L91').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L12').Value; //등록번호
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F11').AsString );
      gpCol:=gpWth*lSqry.FieldByName('L13').Value; //상 호 명
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F12').AsString );
      gpCol:=gpWth*lSqry.FieldByName('L14').Value; //대 표 자
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F21').AsString );
    // Line 3
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L12').Value; //주민번호
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F41').AsString );
      p_Gadds:=lSqry.FieldByName('F22').AsString+' '+
               lSqry.FieldByName('F31').AsString+' '+
               lSqry.FieldByName('F32').AsString;
      gpCol:=gpWth*lSqry.FieldByName('L13').Value; //주    소
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadds );
    // Line 4
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //상 호 명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gname );
      gpCol:=gpWth*lSqry.FieldByName('L22').Value; //등록번호
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gnum1 );
    // Line 5
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //주    소
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadd2 );
    // Line 6
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //성    명
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gposa );
      gpCol:=gpWth*lSqry.FieldByName('L22').Value; //주민번호
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gnum2 );
    // Line 7
    Inc(gpCnt,lSqry.FieldByName('L92').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L21').Value; //주    소
      Printer.Canvas.TextOut(gpCol, gpRow, p_Gadd1 );
    // Line 8
    Inc(gpCnt,lSqry.FieldByName('L93').AsInteger); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font.Size:=10;
      gpCol:=gpWth*lSqry.FieldByName('L23').Value; //구    분
      Printer.Canvas.TextOut(gpCol, gpRow, 'O' );
    // Line 9
    Inc(gpCnt,lSqry.FieldByName('L94').AsInteger); gpRow:=gpHeg*gpCnt;
    p_Sline:=0; qpCnt:=gpCnt;
    While(oSqry.EOF=False)and(p_Sline<4)do begin
      p_Sline:=p_Sline+1;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Gssum:=oSqry.FieldByName('Gssum').AsInteger;
      p_Gisum:=oSqry.FieldByName('Gisum').AsInteger;
      p_Gosum:=oSqry.FieldByName('Gosum').AsInteger;
      p_Gbsum:=oSqry.FieldByName('Gbsum').AsInteger;
      p_Grat1:=oSqry.FieldByName('Grat1').AsInteger;
      gpCol:=gpWth*lSqry.FieldByName('L31').Value; //지급년
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,1,4) );
      gpCol:=gpWth*lSqry.FieldByName('L32').Value; //지급월
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L33').Value; //지급일
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,9,2) );
      gpCol:=gpWth*lSqry.FieldByName('L34').Value; //소득년
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,1,4) );
      gpCol:=gpWth*lSqry.FieldByName('L35').Value; //소득월
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Gdate,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L36').Value; //지급액
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gssum)]) );
      gpCol:=gpWth*lSqry.FieldByName('L37').Value; //세  율
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%03s',[FormatFloat('###,###,##0',p_Grat1)]) );
      gpCol:=gpWth*lSqry.FieldByName('L38').Value; //소득세
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gisum)]) );
      gpCol:=gpWth*lSqry.FieldByName('L39').Value; //주민세
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gosum)]) );
      gpCol:=gpWth*lSqry.FieldByName('L48').Value; //합  계
      Printer.Canvas.TextOut(gpCol, gpRow, Format('%12s',[FormatFloat('###,###,##0',p_Gbsum)]) );
      Inc(qpCnt,lSqry.FieldByName('L95').AsInteger); gpRow:=gpHeg*qpCnt;
      oSqry.Next;
    end;
    // Bottom 1
    Inc(gpCnt,lSqry.FieldByName('L96').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L41').Value; //지급년
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Date1,1,4) );
      gpCol:=gpWth*lSqry.FieldByName('L42').Value; //지급월
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Date1,6,2) );
      gpCol:=gpWth*lSqry.FieldByName('L43').Value; //지급일
      Printer.Canvas.TextOut(gpCol, gpRow, Copy(p_Date1,9,2) );
    // Bottom 2
    Inc(gpCnt,lSqry.FieldByName('L97').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L51').Value; //의무자
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F21').AsString );
    // Bottom 3
    Inc(gpCnt,lSqry.FieldByName('L98').AsInteger); gpRow:=gpHeg*gpCnt;
      gpCol:=gpWth*lSqry.FieldByName('L53').Value; //귀  하
      Printer.Canvas.TextOut(gpCol, gpRow, lSqry.FieldByName('F42').AsString );
    // Bottom 0
    Inc(gpCnt,lSqry.FieldByName('L99').AsInteger); gpRow:=gpHeg*gpCnt;
    Printer.Canvas.TextOut(gpCol, gpRow, '');
    Printer.EndDoc;
  end;
end;

procedure TTong40.PrinTing04(Str: String);
var
  SetupIni : TIniFile;
  F: TextFile;
  St0,St1,St2,St3,S_Gposa: String;
  S_Gcode,S_Gname,p_Gcode,p_Bcode,p_Jubun: String;
  p_Gdate,p_Gubun,p_Gname,p_Bname,p_Gbigo: String;
  p_GsumA,p_GsumB,p_Gqut1,p_Gsum1: Double;
  p_Gnumb,p_Count,p_Pages,p_Spage: Integer;
begin

  SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
  With SetupIni do begin
    S_Gcode:=ReadString('Remote', 'Code', '');
    S_Gname:=ReadString('Remote', 'Name', '');
    S_Gposa:=ReadString('Remote', 'Posa', '');
    St0    :=ReadString('Remote', 'Seek', '');
  end;
  SetupIni.Free;

if St0='1' Then begin
  //날       개//
  St0:='                                   ';
  St1:=FormatDateTime('yyyy"."mm"."dd',Date);
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'01.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\');
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'02.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'03.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'04.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'05.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'06.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'07.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'08.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'09.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=Copy(St1,3,2)+Copy(St1,6,2)+Copy(St1,9,2)+'10.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  AssignFile(F, GetExecPath + 'Remote\'+St2);
  Rewrite(F);
  p_Count:=0; p_Pages:=0; p_Spage:=0; p_GsumA:=0; p_GsumB:=0;
  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
    end else begin
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
      p_Spage:=p_Spage+1;
      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
        p_Count:=p_Count+1;
        p_GsumA:=p_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
        p_GsumB:=p_GsumB+oSqry.FieldByName('Gssum').AsInteger;
        oSqry.Next;
        if(oSqry.EOF=False)Then p_Pages:=p_Pages+1;
      end;
      oSqry.MoveBy(-p_Pages);
    end;

    Sqlen := 'Select Gbigo From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Gcode);
    p_Gname:=Base10.Seek_Name(Sqlen);

    While(p_Count<=1000)and
      (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
      p_Bcode:=oSqry.FieldByName('Bcode').AsString;

      Sqlen := 'Select Gbigo From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Bcode);
      p_Bname:=Base10.Seek_Name(Sqlen);

      //Line Loop
      St3:='';
      St3:=St3+'2';
      St3:=St3+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2);
    //St3:=St3+Format('%04s',[FormatFloat('########0',p_Spage)] );
      St3:=St3+Copy(St2,8,1)+Format('%03s',[FormatFloat('000',p_Spage)] );
           if oSqry.FieldByName('Pubun').AsString='위탁' Then St3:=St3+'1'
      else if oSqry.FieldByName('Pubun').AsString='현매' Then St3:=St3+'2'
      else if oSqry.FieldByName('Pubun').AsString='매절' Then St3:=St3+'3'
      else if oSqry.FieldByName('Pubun').AsString='증정' Then St3:=St3+'4'
      else if oSqry.FieldByName('Pubun').AsString='납품' Then St3:=St3+'5'
      else St3:=St3+'1';
      St3:=St3+Format('%-06s',[p_Gname] );
      St3:=St3+'0-0604';
      St3:=St3+Format('%-06s',[p_Bname] );
      St3:=St3+Format('%-05s',[FormatFloat('########0',oSqry.FieldByName('Gsqut').AsFloat)] );
      St3:=St3+Format('%-09s',[FormatFloat('########0',oSqry.FieldByName('Gdang').AsFloat)] );
      St3:=St3+Format('%-03s',[FormatFloat('########0',oSqry.FieldByName('Grat1').AsFloat)] );
      St3:=St3+'    '+Format('%-10s',[oSqry.FieldByName('Gbigo').AsString] );
      St3:=St3+'  ';
      Writeln(F, St3);
      //Line 01 end
      p_Count:=p_Count+1;
      oSqry.Next;
      if(oSqry.EOF=True)Then p_Count:=1001;
    end;
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
      p_Gqut1:=0; p_Gsum1:=0;
    end else begin
      p_GsumA:=0; p_GsumB:=0; p_Count:=0; p_Pages:=0;
    end;
  end;
  CloseFile(F);
end;
if St0='2' Then begin
  //날       개//
  St0:='                                                  ';
  St1:=FormatDateTime('yyyy"."mm"."dd',Date);
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'1.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\');
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'2.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'3.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'4.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'5.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'6.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'7.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'8.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  if FileExists( St3 ) then begin
  St2:=S_Gcode+'A'+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'9.TXT';
  St3:=FileSearch( St2, GetExecPath + 'Remote\'); end;
  AssignFile(F, GetExecPath + 'Remote\'+St2);
  Rewrite(F);
  St3:='WinType';
  Writeln(F, St3);
  St3:='발신자료명 : 출고전표내역(출판사 -> 물류창고)';
  Writeln(F, St3);
  St3:='작  성  자 : '+S_Gposa;         {작성자 }
  Writeln(F, St3);
  St3:='관리구분No : 2';
  Writeln(F, St3);
  St3:='출판사확인 : ';
  St3:=St3+Format('%-07s',[S_Gcode] );  {출판사코드 }
  St3:=St3+'('+S_Gname+')';             {출판사명 }
  Writeln(F, St3);
  St3:='';
  Writeln(F, St3);
  p_Count:=1; p_Pages:=0; p_Spage:=0; p_GsumA:=0; p_GsumB:=0; p_Gnumb:=2000;
  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
    end else begin
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
      p_Spage:=p_Spage+1;
      p_Gnumb:=p_Gnumb+1;

      Sqlen := 'Select Gbigo,Jubun,Gname '+
      'From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        S_Gcode:=Base10.Socket.GetData(1, 1);
        S_Gname:=Base10.Socket.GetData(1, 2);
        p_Gname:=Base10.Socket.GetData(1, 3);
      end;

      St3:='';
      St3:=St3+'A';               {전표번호: 14자 문자 (유일해야함) }
      St3:=St3+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2)+'-';
      St3:=St3+IntToStr(p_Gnumb);
      St3:=St3+' ';
                                  {출고일자: 10자 문자 }
      St3:=St3+Copy(St1,1,4)+'-'+Copy(St1,6,2)+'-'+Copy(St1,9,2);
      St3:=St3+' ';
      St3:=St3+'   0';            {덩 어 수: 4숫자 없으면 zero}
      St3:=St3+' ';
      St3:=St3+'Z';               {출판사코드: 무조건 Z }
      St3:=St3+' ';
      St3:=St3+Format('%-07s',[S_Gcode] ); {서점코드: 7문자}
      St3:=St3+' ';
      St3:=St3+'위탁';            {위탁구분: 반드시 위탁}
      St3:=St3+' ';
      if oSqry.FieldByName('Pubun').AsString='신간' Then
      St3:=St3+'신간' else
      St3:=St3+'일반';            {주문구분: 일반,신간중에 선택}
      St3:=St3+' ';
      if S_Gname='지방' Then
      St3:=St3+'지방' else
      if S_Gname='철도' Then
      St3:=St3+'철도' else
      if S_Gname='화물' Then
      St3:=St3+'화물' else
      if S_Gname='택배' Then
      St3:=St3+'택배' else
      if S_Gname='지방' Then
      St3:=St3+'지방' else
      St3:=St3+'시내';            {출고구분: 시내,지방,철도,화물,택배,기타중에 선택}
      St3:=St3+' ';
      if oSqry.FieldByName('Jubun').AsString='현매' Then
      St3:=St3+'현매' else
      if oSqry.FieldByName('Jubun').AsString='매절' Then
      St3:=St3+'매절' else
      if oSqry.FieldByName('Jubun').AsString='납품' Then
      St3:=St3+'납품' else
      if oSqry.FieldByName('Jubun').AsString='기증' Then
      St3:=St3+'기증' else
      St3:=St3+'일반';            {결재구분: 일반,현매,매절,기증,남품,본사,기타중에 선택}
      St3:=St3+' ';
      St3:=St3+St0+St0;           {비고사항: 100자 문자}
      St3:=St3+';';
      St3:=St3+' ';
      St3:=St3+p_Gname;
    { if S_Gname<>'' Then
      St3:=St3+'/'+S_Gname; }
      Writeln(F, St3);

      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
      { p_Count:=p_Count+1; }
        p_GsumA:=p_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
        p_GsumB:=p_GsumB+oSqry.FieldByName('Gssum').AsInteger;
        oSqry.Next;
        if(oSqry.EOF=False)Then p_Pages:=p_Pages+1;
      end;
      oSqry.MoveBy(-p_Pages);
    end;

    Sqlen := 'Select Gbigo From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Gcode);
    p_Gname:=Base10.Seek_Name(Sqlen);

    While(p_Count<=1000)and
      (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
      p_Bcode:=oSqry.FieldByName('Bcode').AsString;

      Sqlen := 'Select Gbigo From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Bcode);
      p_Bname:=Base10.Seek_Name(Sqlen);

      //Line Loop
      St3:=' ';               {Space 1}
      St3:=St3+Format('%04s',[FormatFloat('########0',p_Count)] );                            {순    번: 4숫자}
      St3:=St3+'  ';
      St3:=St3+Format('%-14s',[p_Bcode] );                                                    {도서코드: 15자리 (15자리 이하시 나머지는 space처리) }

      St3:=St3+Format('%09s',[FormatFloat('########0',oSqry.FieldByName('Gsqut').AsFloat)] ); {출고부수: 9자리 (동일) }
      St3:=St3+' ';
      St3:=St3+Format('%09s',[FormatFloat('########0',oSqry.FieldByName('Gdang').AsFloat)] ); {도서정가: 9자리 (동일) }
      St3:=St3+' ';
      if oSqry.FieldByName('Grat1').AsFloat<100 Then {출고비율: 99.9 포맷->100% 출고시는 100과 space 1자리 }
      St3:=St3+Format('%02s',[FormatFloat('########0',oSqry.FieldByName('Grat1').AsFloat)] )+'.0' else
      St3:=St3+Format('%04s',[FormatFloat('########0',oSqry.FieldByName('Grat1').AsFloat)] );
    //St3:=St3+Format('%-3.1d',[FormatFloat('########0',oSqry.FieldByName('Grat1').AsFloat)] );

      St3:=St3+' ';
      St3:=St3+Format('%12s',[FormatFloat('########0',oSqry.FieldByName('Gssum').AsFloat)] ); {출고금액: 12자리 (동일) }
      St3:=St3+' ';
      St3:=St3+Format('%20s',[oSqry.FieldByName('Gbigo').AsString] );                         {비고사항: 20자리 }
      St3:=St3+';';
      St3:=St3+' ';           {Space 1}
      St3:=St3+p_Bname;       {도서명 표기}
      Writeln(F, St3);

      //Line 01 end
      p_Count:=p_Count+1;
      oSqry.Next;
      if(oSqry.EOF=True)Then p_Count:=1001;
    end;
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
      p_Gqut1:=0; p_Gsum1:=0;
    end else begin
      p_GsumA:=0; p_GsumB:=0; p_Count:=1; p_Pages:=0;
    end;
  end;
  CloseFile(F);
end;
if St0='3' Then begin
  //수   레   사//
  St0:='                                                  ';
  St1:=FormatDateTime('yyyy"."mm"."dd',Date);

  St2:=S_Gcode+'-'+Copy(St1,6,2)+Copy(St1,9,2)+'.TXT'; // 가람기획-(P58)

  AssignFile(F, GetExecPath + 'Remote\'+St2);
  Rewrite(F);

  p_Count:=0; p_Pages:=0; p_Spage:=0; p_GsumA:=0; p_GsumB:=0; p_Gnumb:=2000;

  if oSqry.FieldByName('Jubun').AsString = '1' then
     p_Pages:= 200
  else
  if oSqry.FieldByName('Jubun').AsString = '2' then
     p_Pages:= 400
  else
  if oSqry.FieldByName('Jubun').AsString = '3' then
     p_Pages:= 600
  else
  if oSqry.FieldByName('Jubun').AsString = '4' then
     p_Pages:= 800;

  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
    end else begin
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
      p_Spage:=p_Spage+1;
      p_Gnumb:=p_Gnumb+1;

      Sqlen := 'Select Gbigo,Gname '+
      'From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        p_Bcode:=Base10.Socket.GetData(1, 1);
        p_Gname:=Base10.Socket.GetData(1, 2);
      end;

      p_Count:=0;

      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
        p_Count:=p_Count+1;
        p_GsumA:=p_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
        p_GsumB:=p_GsumB+oSqry.FieldByName('Gssum').AsInteger;
        oSqry.Next;
        if(oSqry.EOF=False)Then p_Pages:=p_Pages+1;
      end;
      oSqry.MoveBy(-p_Pages);


      St3:='####';
      St3:=St3+Copy(S_Gcode,2,2);

      if oSqry.FieldByName('Gubun').AsString='출고' Then
      St3:=St3+'1'
      else
      if oSqry.FieldByName('Gubun').AsString='반품' Then
      St3:=St3+'2'
      else
      St3:=St3+'1';

      St3:=St3+Copy(St1,1,4)+Copy(St1,6,2)+Copy(St1,9,2);     {출고일자: 10자 문자 }
      St3:=St3+Format('%03s',[FormatFloat('000',p_Pages)] );  {폐 이 지: 03자 문자 }
      St3:=St3+Format('%03s',[FormatFloat('000',p_Spage)] );  {Count}

      St3:=St3+'0';

      if oSqry.FieldByName('Pubun').AsString='위탁' Then
      St3:=St3+'0'
      else
      if oSqry.FieldByName('Pubun').AsString='현매' Then
      St3:=St3+'1'
      else
      if oSqry.FieldByName('Pubun').AsString='매절' Then
      St3:=St3+'2'
      else
      if oSqry.FieldByName('Pubun').AsString='납품' Then
      St3:=St3+'3'
      else
      if oSqry.FieldByName('Pubun').AsString='신간' Then
      St3:=St3+'4'
      else
      St3:=St3+'0';

      St3:=St3+'00';

      if Length(oSqry.FieldByName('Gcode').AsString)=3 then begin
      St3:=St3+Copy(oSqry.FieldByName('Gcode').AsString,1,3);
      St3:=St3+' ';
      end else
      if Length(oSqry.FieldByName('Gcode').AsString)=4 then
      St3:=St3+Copy(oSqry.FieldByName('Gcode').AsString,1,4);

      St3:=St3+Copy(p_Bcode,1,5);

      Writeln(F, St3);

      St3:='      ';

      St3:=St3+p_Gname;

      Writeln(F, St3);

      St3:=Format('%09s',[FormatFloat('000000000',p_GsumB)] );
      St3:=St3+'0';

      St3:=St3+Format('%05s',[FormatFloat('00000',p_GsumA)] );
      St3:=St3+'0';

      St3:=St3+Format('%03s',[FormatFloat('000',p_Count)] );

      Writeln(F, St3);

      Sqlen := 'Select Jubun From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);

      St3:=Base10.Seek_Name(Sqlen);
      if St3='신  간' then
      St3:='신간 도서입니다'
      else
      St3:='';
      Writeln(F, St3);

    end;

    Sqlen := 'Select Gbigo From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Gcode);
    p_Gname:=Base10.Seek_Name(Sqlen);

    While(p_Count<=1000)and
      (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)do begin
      p_Bcode:=oSqry.FieldByName('Bcode').AsString;

      Sqlen := 'Select Gbigo From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
      Translate(Sqlen, '@Gcode', p_Bcode);
      p_Bname:=Base10.Seek_Name(Sqlen);

      //Line Loop
      St3:=Copy(p_Bname,1,5);
      St3:=St3+Format('%05s',[FormatFloat('00000',oSqry.FieldByName('Gsqut').AsFloat)] );
      St3:=St3+Format('%07s',[FormatFloat('0000000',oSqry.FieldByName('Gdang').AsFloat)] ); {도서정가: 9자리 (동일) }
      St3:=St3+Format('%03s',[FormatFloat('000',oSqry.FieldByName('Grat1').AsFloat)] );
      Writeln(F, St3);

      p_Count:=p_Count+1;
      oSqry.Next;
      if(oSqry.EOF=True)Then p_Count:=1001;
    end;
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and(oSqry.EOF=False)Then begin
      p_Gqut1:=0; p_Gsum1:=0;
    end else begin
      p_GsumA:=0; p_GsumB:=0; p_Count:=1; p_Pages:=0;
    end;
  end;
  CloseFile(F);
end;
end;

procedure TTong40.PrinTing08(_Scode,_Gcode,_Gdate,_Gubun,_Jubun,_Hcode: String);
var St1,St2,St3: String;
    _S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng: String;
begin
  sSqry:=Base10.T3_Sub91;
  Base10.OpenExit(sSqry);
  Base10.OpenShow(sSqry);

  {-Sv_Chng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Chng '+
          'Where '+D_Select+
          'Gdate < '+#39+_Gdate+#39+' and  '+
          'Hcode = '+#39+_Hcode+#39;
  St1:=Base10.Seek_Name(Sqlen);

  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+_Gdate+#39+' and '+
            'Scode'+' ='+#39+_Scode+#39+' and '+
            'Gcode'+' ='+#39+_Gcode+#39+' and '+
            'Hcode'+' ='+#39+_Hcode+#39;
  _Sg_Gsum:=_S1_Ssub;
  _Sv_Chng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Scode'+' ='+#39+_Scode+#39+' and '+
            'Gcode'+' ='+#39+_Gcode+#39+' and '+
            'Hcode'+' ='+#39+_Hcode+#39;
  St2:='Gubun='+#39+'입금'+#39+' and ';
  St3:='Gubun='+#39+'출금'+#39+' and ';
  St1:='';
  St1:=St1+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St1:=St1+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St2+D_Select+_S1_Ssub+' ) as Gosum,';
  St1:=St1+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St3+D_Select+_S1_Ssub+' ) as Gbsum ';
  St1:=St1+' From H1_Ssub S Where '+D_Select+_S1_Ssub;
  _H1_Ssub:= St1;

  if ePrnt='2' then begin
  St1:='';
  St1:=St1+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St1:=St1+' Sum(if('+St2+D_Select+_S1_Ssub+',gssum,0))as Gosum,';
  St1:=St1+' Sum(if('+St3+D_Select+_S1_Ssub+',gssum,0))as Gbsum ';
  St1:=St1+' From H1_Ssub S Where '+D_Select+_S1_Ssub;
  _H1_Ssub:= St1;
  end;

  {Sv_Chng}
  Sqlen :='Select Gcode,Sum(Gssum)as Gssum,Sum(Gsusu)as Gsusu '+
          'From Sv_Chng Where '+D_Select+_Sv_Chng+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
    List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 1,List1],0)-StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;

  {S1_Ssub}
  Sqlen :='Select Gcode,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
          'From S1_Ssub Where '+D_Select+_S1_Ssub+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
    List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;

  {H1_Ssub}
  Sqlen :=_H1_Ssub+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
    List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat-
    StrToIntDef(SGrid.Cells[ 2,List1],0)+StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.Post;
  end;

  {Sg_Gsum}
  Sqlen :='Select Gcode,Sum(Gbsum)as Gbsum '+
          'From Sg_Gsum Where '+D_Select+_Sg_Gsum+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
    List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 1,List1],0);
    sSqry.Post;
  end;

  p_GsumX:=0;
  sSqry.First;
  While sSqry.EOF=False do begin
    p_GsumX:=p_GsumX+sSqry.FieldByName('GsumX').AsFloat;
    sSqry.Next;
  end;
end;

procedure TTong40.PrinTing09(Str: String);
var
  Device : array[0 .. 255] of char;
  Driver : array[0 .. 255] of char;
  DePort : array[0 .. 32] of char;
  hDMode : THandle;
  pDMode : PDevMode;
begin
  if lSqry.FieldByName('L62').Value<>2970 then
  begin
    Printer.GetPrinter(Device, Driver, DePort, hDMode);
    if hDMode = 0 then
      Exit;
    pDMode := GlobalLock(hDMode);

    if pDMode = nil then
      Exit;
    pDMode^.dmFields     :=(pDMode^.dmFields)or(DM_PAPERLENGTH)or(DM_PAPERWIDTH);
    pDMode^.dmPaperSize  :=DMPAPER_USER;
    pDMode^.dmPaperWidth :=lSqry.FieldByName('L61').Value;
    pDMode^.dmPaperLength:=lSqry.FieldByName('L62').Value;
    Printer.SetPrinter(Device, Driver, DePort, hDMode);
    GlobalUnlock(hDMode);
  end;
end;

procedure TTong40.Print_11_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen11, Seen11);
     nPrnt:='11'; Seen11.ShowModal;
     Seen11.Free;
  end;
end;

procedure TTong40.Print_11_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen13, Seen13);
     nPrnt:='11'; Seen13.ShowModal;
     Seen13.Free;
  end;
end;

procedure TTong40.Print_12_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen11, Seen11);
     nPrnt:='12'; Seen11.ShowModal;
     Seen11.Free;
  end;
end;

procedure TTong40.Print_12_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen13, Seen13);
     nPrnt:='12'; Seen13.ShowModal;
     Seen13.Free;
  end;
end;

procedure TTong40.Print_13_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen11, Seen11);
     nPrnt:='13'; Seen11.ShowModal;
     Seen11.Free;
  end;
end;

procedure TTong40.Print_13_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen13, Seen13);
     nPrnt:='13'; Seen13.ShowModal;
     Seen13.Free;
  end;
end;

procedure TTong40.Print_14_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen11, Seen11);
     nPrnt:='14'; Seen11.ShowModal;
     Seen11.Free;
  end;
end;

procedure TTong40.Print_14_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen13, Seen13);
     nPrnt:='14'; Seen13.ShowModal;
     Seen13.Free;
  end;
end;

procedure TTong40.Print_14_11(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_1_40.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo14_1.Edit103.Text;
      FindObject('Memo04').Memo.Text:=Sobo14_1.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_15_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen11, Seen11);
     nPrnt:='15'; Seen11.ShowModal;
     Seen11.Free;
  end;
end;

procedure TTong40.Print_15_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen13, Seen13);
     nPrnt:='15'; Seen13.ShowModal;
     Seen13.Free;
  end;
end;

procedure TTong40.Print_16_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_1_61.frf');
      FindObject('Memo91').Memo.Text:=Sobo16.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo16.Edit101.Text;
      FindObject('Memo04').Memo.Text:=Sobo16.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_16_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_1_62.frf');
      FindObject('Memo91').Memo.Text:=Sobo16.Edit208.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo16.Edit201.Text;
      FindObject('Memo04').Memo.Text:=Sobo16.Edit202.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_17_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen11, Seen11);
     nPrnt:='17'; Seen11.ShowModal;
     Seen11.Free;
  end;
end;

procedure TTong40.Print_17_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Application.CreateForm(TSeen13, Seen13);
     nPrnt:='17'; Seen13.ShowModal;
     Seen13.Free;
  end;
end;

procedure TTong40.Print_17_03(Sender: TObject);
var ff3: Integer;
    SearchRec : TSearchRec;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;

    ff3 := FindFirst( GetExecPath + 'Report\Report_1_71.frf', faAnyFile, SearchRec);

    if(ff3 = 0)then begin
      Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

      Tong60.frDBDataSet00_00.DataSet:=oSqry;

      With Tong60.frReport00_00 do begin
        Clear;
        LoadFromFile(GetExecPath + 'Report\Report_1_71.frf');

        {-G7_Ggeo-}
        Sqlen := 'Select '+
        'Sum02,Sum04,Sum06,Sum09,Sum12,Sum15,Sum18,Sum19,Sum21,Sum22,Sum25,Sum32,Sum33,'+
        'Sum34,Sum38,Sum39,Sum40,Sum41,Sum42,Yes33,Yes34,Yes35,Yes41,Yes42,Yes43,Yes44,'+
        'Yes45,Yes51,Yes52,Yes53,Yes54,Yes55,Sum36,Bigo1 '+
        'From G7_Ggeo Where '+D_Select+'Gcode'+'='+#39+oSqry.FieldByName('Gcode').AsString+#39;

        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.busyloop;
        if Base10.Socket.body_data <> 'ERROR' then
           Base10.Socket.MakeGrid(SGrid)
        else ShowMessage(E_Open);

        FindObject('Memo40').Memo.Text:=SGrid.Cells[ 0,1];
        FindObject('Memo42').Memo.Text:=SGrid.Cells[ 1,1];
        FindObject('Memo44').Memo.Text:=SGrid.Cells[ 2,1];
        FindObject('Memo46').Memo.Text:=SGrid.Cells[ 3,1];
        FindObject('Memo69').Memo.Text:=SGrid.Cells[ 4,1];
        FindObject('Memo71').Memo.Text:=SGrid.Cells[ 5,1];
        FindObject('Memo50').Memo.Text:=SGrid.Cells[ 6,1];
        FindObject('Memo51').Memo.Text:=SGrid.Cells[ 7,1];
        FindObject('Memo53').Memo.Text:=SGrid.Cells[ 8,1];
        FindObject('Memo54').Memo.Text:=SGrid.Cells[ 9,1];
        FindObject('Memo67').Memo.Text:=SGrid.Cells[10,1];
        FindObject('Memo73').Memo.Text:=SGrid.Cells[11,1];
        FindObject('Memo62').Memo.Text:=SGrid.Cells[12,1];
        FindObject('Memo63').Memo.Text:=SGrid.Cells[13,1];
        FindObject('Memo56').Memo.Text:=SGrid.Cells[14,1];
        FindObject('Memo57').Memo.Text:=SGrid.Cells[15,1];
        FindObject('Memo59').Memo.Text:=SGrid.Cells[16,1];
        FindObject('Memo60').Memo.Text:=SGrid.Cells[17,1];
        FindObject('Memo75').Memo.Text:=SGrid.Cells[18,1];
        FindObject('Memo101').Memo.Text:=SGrid.Cells[32,1];
        FindObject('Memo100').Memo.Text:=SGrid.Cells[33,1];
        if SGrid.Cells[19,1]='1' then
        FindObject('Memo64').Memo.Text:='청구' else
        FindObject('Memo64').Memo.Text:='미청구';
        if SGrid.Cells[20,1]='1' then
        FindObject('Memo65').Memo.Text:='청구' else
        FindObject('Memo65').Memo.Text:='미청구';
        if SGrid.Cells[21,1]='1' then begin
        FindObject('Memo76').Memo.Text:='V';
        FindObject('Memo77').Memo.Text:='';
        end else begin
        FindObject('Memo76').Memo.Text:='';
        FindObject('Memo77').Memo.Text:='V';
        end;
        if SGrid.Cells[22,1]='1' then
        FindObject('Memo79').Memo.Text:='청구' else
        FindObject('Memo79').Memo.Text:='미청구';
        if SGrid.Cells[23,1]='1' then
        FindObject('Memo80').Memo.Text:='청구' else
        FindObject('Memo80').Memo.Text:='미청구';
        if SGrid.Cells[24,1]='1' then
        FindObject('Memo81').Memo.Text:='청구' else
        FindObject('Memo81').Memo.Text:='미청구';
        if SGrid.Cells[25,1]='1' then
        FindObject('Memo82').Memo.Text:='청구' else
        FindObject('Memo82').Memo.Text:='미청구';
        if SGrid.Cells[26,1]='1' then
        FindObject('Memo83').Memo.Text:='청구' else
        FindObject('Memo83').Memo.Text:='미청구';
        if SGrid.Cells[27,1]='1' then
        FindObject('Memo84').Memo.Text:='청구' else
        FindObject('Memo84').Memo.Text:='미청구';
        if SGrid.Cells[28,1]='1' then
        FindObject('Memo85').Memo.Text:='청구' else
        FindObject('Memo85').Memo.Text:='미청구';
        if SGrid.Cells[29,1]='1' then
        FindObject('Memo86').Memo.Text:='청구' else
        FindObject('Memo86').Memo.Text:='미청구';
        if SGrid.Cells[30,1]='1' then
        FindObject('Memo87').Memo.Text:='청구' else
        FindObject('Memo87').Memo.Text:='미청구';
        if SGrid.Cells[31,1]='1' then
        FindObject('Memo88').Memo.Text:='청구' else
        FindObject('Memo88').Memo.Text:='미청구';

        ShowReport;
      end;

      oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
    end;
  end;
end;

procedure TTong40.Print_18_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_18_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_19_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_19_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_10_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_10_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_21_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
  //oSqry.SaveToFile(GetExecPath + 'Data\Chulpan.cds');
    Tong40.PrinTing00('21','1','','','','','','','','');
  end;
end;

procedure TTong40.Print_21_02(Sender: TObject);
var ff3: Integer;
    SearchRec : TSearchRec;
begin
  if nSqry.Active=True Then begin
    oSqry:=tSqry;

    ff3 := FindFirst( GetExecPath + 'Report\Report_2_12.frf', faAnyFile, SearchRec);

    if(ff3 = 0)then begin
      Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

      Tong60.frDBDataSet00_00.DataSet:=oSqry;

      With Tong60.frReport00_00 do begin
        Clear;
        LoadFromFile(GetExecPath + 'Report\Report_2_12.frf');
        FindObject('Memo11').Memo.Text:=oSqry.FieldByName('Name1').AsString;
        FindObject('Memo12').Memo.Text:=oSqry.FieldByName('Name2').AsString;
        FindObject('Memo13').Memo.Text:=oSqry.FieldByName('Scode').AsString;
      //Tong60.frReport21_20('1');
      //ShowReport;
        if PrepareReport then
        PrintPreparedReport(' ',1,true, frall);
      end;

      oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
    end else begin
      Tong40.PrinTing00('21','2','','','','','','','','');
    end;
  { Application.CreateForm(TSeen22, Seen22);
    Seen22.QuickRep1SrartPrnt('1');
    Seen22.Free; }
  end;
end;

procedure TTong40.Print_22_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
  //oSqry.SaveToFile(GetExecPath + 'Data\Chulpan.cds');
    Tong40.PrinTing00('22','1','','','','','','','','');
  end;
end;

procedure TTong40.Print_22_02(Sender: TObject);
var ff3: Integer;
    SearchRec : TSearchRec;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;

    ff3 := FindFirst( GetExecPath + 'Report\Report_2_12.frf', faAnyFile, SearchRec);

    if(ff3 = 0)then begin
      Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

      Tong60.frDBDataSet00_00.DataSet:=oSqry;

      With Tong60.frReport00_00 do begin
        Clear;
        LoadFromFile(GetExecPath + 'Report\Report_2_12.frf');
      //Tong60.frReport21_20('1');
      //ShowReport;
        if PrepareReport then
        PrintPreparedReport(' ',1,true, frall);
      end;

      oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
    end else begin
      Tong40.PrinTing00('21','2','','','','','','','','');
    end;
  { if Tong20.ShowModal=mrOK Then begin
    oSqry:=nSqry;
    ePrnt:=Tong20.Edit1.Text;
    Application.CreateForm(TSeen21, Seen21);
    Seen21.QuickRep1SrartPrnt('2');
    Seen21.Free;
    end; }
  end;
end;

procedure TTong40.Print_23_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
  //oSqry.SaveToFile(GetExecPath + 'Data\Chulpan.cds');
    Tong40.PrinTing00('23','1','','','','','','','','');
  end;
end;

procedure TTong40.Print_23_02(Sender: TObject);
var ff3: Integer;
    SearchRec : TSearchRec;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;

    ff3 := FindFirst( GetExecPath + 'Report\Report_2_12.frf', faAnyFile, SearchRec);

    if(ff3 = 0)then begin
      Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

      Tong60.frDBDataSet00_00.DataSet:=oSqry;

      With Tong60.frReport00_00 do begin
        Clear;
        LoadFromFile(GetExecPath + 'Report\Report_2_12.frf');
      //Tong60.frReport21_20('1');
      //ShowReport;
        if PrepareReport then
        PrintPreparedReport(' ',1,true, frall);
      end;

      oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
    end else begin
      Tong40.PrinTing00('21','2','','','','','','','','');
    end;
  { if Tong20.ShowModal=mrOK Then begin
    oSqry:=nSqry;
    ePrnt:=Tong20.Edit1.Text;
    Application.CreateForm(TSeen21, Seen21);
    Seen21.QuickRep1SrartPrnt('3');
    Seen21.Free;
    end; }
  end;
end;

procedure TTong40.Print_24_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_41.frf');
      FindObject('Memo91').Memo.Text:=Sobo24.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo24.Edit101.Text+' - '+Sobo24.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_24_02(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_42.frf');
      FindObject('Memo91').Memo.Text:=Sobo24.Edit109.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo24.Edit101.Text+' - '+Sobo24.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo24.Button101.Caption;
      FindObject('Memo11').Memo.Text:=Sobo24.DBGrid201.Columns.Items[0].Title.Caption;

      if(Sobo24.DBGrid201.Columns.Items[0].Title.Caption='도 서 명')or
        (Sobo24.DBGrid201.Columns.Items[0].Title.Caption='도서구분')Then
        FindObject('Memo00').Memo.Text:='도서별 집계 현황' else
        FindObject('Memo00').Memo.Text:='거래처 집계 현황';

      if Sobo24.Button101.Caption='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_25_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_51.frf');
      FindObject('Memo91').Memo.Text:=Sobo25.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo25.Edit101.Text+' - '+Sobo25.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_25_02(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_52.frf');
      FindObject('Memo91').Memo.Text:=Sobo25.Edit109.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo25.Edit101.Text+' - '+Sobo25.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo25.Button101.Caption;
      FindObject('Memo11').Memo.Text:=Sobo25.DBGrid201.Columns.Items[0].Title.Caption;

      if(Sobo25.DBGrid201.Columns.Items[0].Title.Caption='도 서 명')or
        (Sobo25.DBGrid201.Columns.Items[0].Title.Caption='도서구분')Then
        FindObject('Memo00').Memo.Text:='도서별 집계 현황' else
        FindObject('Memo00').Memo.Text:='입고처 집계 현황';

      if Sobo25.Button101.Caption='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_26_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

  { With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_61.frf');
      FindObject('Memo91').Memo.Text:=Sobo26.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo26.Edit101.Text+' - '+Sobo26.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo26.Edit103.Text;
      FindObject('Memo06').Memo.Text:=Sobo26.Edit105.Text;
      ShowReport;
    end; }

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen26, Seen26);
    Seen26.QuickRep1SrartPrnt('1');
    Seen26.Free; }
  end;
end;

procedure TTong40.Print_26_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_62.frf');
      FindObject('Memo91').Memo.Text:=Sobo26.Edit208.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo26.Edit201.Text+' - '+Sobo26.Edit202.Text;
      FindObject('Memo04').Memo.Text:=Sobo26.Edit203.Text;
      FindObject('Memo06').Memo.Text:=Sobo26.Edit205.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen26, Seen26);
    Seen26.QuickRep1SrartPrnt('2');
    Seen26.Free; }
  end;
end;

procedure TTong40.Print_27_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

  { With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_71.frf');
      FindObject('Memo91').Memo.Text:=Sobo27.Edit109.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo27.Edit101.Text+' - '+Sobo27.Edit102.Text;
      ShowReport;
    end; }

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen26, Seen26);
    Seen26.QuickRep1SrartPrnt('3');
    Seen26.Free; }
  end;
end;

procedure TTong40.Print_27_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

  { With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_72.frf');
      FindObject('Memo91').Memo.Text:=Sobo27.Edit109.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo27.Edit101.Text+' - '+Sobo27.Edit102.Text;
      ShowReport;
    end; }

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen26, Seen26);
    Seen26.QuickRep1SrartPrnt('4');
    Seen26.Free; }
  end;
end;

procedure TTong40.Print_28_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  { oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_81.frf');
      FindObject('Memo91').Memo.Text:=Sobo28.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo28.Edit101.Text+' - '+Sobo28.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo28.Edit104.Text+' - '+Sobo28.Edit106.Text;

      if Sobo28.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls; }
  { Application.CreateForm(TSeen24, Seen24);
    Seen24.QuickRep1SrartPrnt('1');
    Seen24.Free; }
  end;
end;

procedure TTong40.Print_28_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
  { oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_82.frf');
      FindObject('Memo91').Memo.Text:=Sobo28.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo28.Edit101.Text+' - '+Sobo28.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo28.Edit104.Text+' - '+Sobo28.Edit106.Text;

      if Sobo28.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls; }
  { Application.CreateForm(TSeen25, Seen25);
    Seen25.QuickRep1SrartPrnt('1');
    Seen25.Free; }
  end;
end;

procedure TTong40.Print_29_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
  //oSqry.SaveToFile(GetExecPath + 'Data\Chulpan.cds');
    Tong40.PrinTing00('29','1','','','','','','','','');
  end;
end;

procedure TTong40.Print_29_02(Sender: TObject);
var ff3: Integer;
    SearchRec : TSearchRec;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;

    ff3 := FindFirst( GetExecPath + 'Report\Report_2_12.frf', faAnyFile, SearchRec);

    if(ff3 = 0)then begin
    end else begin
      Tong40.PrinTing00('21','2','','','','','','','','');
    end;
  { if Tong20.ShowModal=mrOK Then begin
    oSqry:=nSqry;
    ePrnt:=Tong20.Edit1.Text;
    Application.CreateForm(TSeen21, Seen21);
    Seen21.QuickRep1SrartPrnt('9');
    Seen21.Free;
    end; }
  end;
end;

procedure TTong40.Print_20_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_20_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_31_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_11.frf');
      FindObject('Memo91').Memo.Text:=Sobo31.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo31.Edit101.Text+' - '+Sobo31.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo31.Edit104.Text;
      FindObject('Memo06').Memo.Text:=Sobo31.Edit106.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen31, Seen31);
    Seen31.QuickRep1SrartPrnt('1');
    Seen31.Free; }
  end;
end;

procedure TTong40.Print_31_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_12.frf');
      FindObject('Memo91').Memo.Text:=Sobo31.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo31.Edit101.Text+' - '+Sobo31.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo31.Edit104.Text;
      FindObject('Memo06').Memo.Text:=Sobo31.Edit106.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen32, Seen32);
    Seen32.QuickRep1SrartPrnt('1');
    Seen32.Free; }
  end;
end;

procedure TTong40.Print_32_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_21.frf');
      FindObject('Memo91').Memo.Text:=Sobo32.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo32.Edit101.Text+' - '+Sobo32.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo32.Edit103.Text;
      FindObject('Memo06').Memo.Text:=Sobo32.Edit104.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen33, Seen33);
    Seen33.QuickRep1SrartPrnt('1');
    Seen33.Free; }
  end;
end;

procedure TTong40.Print_32_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_22.frf');
      FindObject('Memo91').Memo.Text:=Sobo32.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo32.Edit101.Text+' - '+Sobo32.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo32.Edit103.Text;
      FindObject('Memo06').Memo.Text:=Sobo32.Edit104.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen34, Seen34);
    Seen34.QuickRep1SrartPrnt('1');
    Seen34.Free; }
  end;
end;

procedure TTong40.Print_33_01(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_32.frf');
      FindObject('Memo91').Memo.Text:=Sobo33.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo33.Edit101.Text+' - '+Sobo33.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo33.Edit104.Text+' - '+Sobo33.Edit106.Text;

      if Sobo33.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen35, Seen35);
    Seen35.QuickRep1SrartPrnt('1');
    Seen35.Free; }
  end;
end;

procedure TTong40.Print_33_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_31.frf');
      FindObject('Memo91').Memo.Text:=Sobo33.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo33.Edit101.Text+' - '+Sobo33.Edit102.Text;

      if(Sobo33.Edit106.Text='' )and(Sobo33.Button101.Caption<>'')Then begin
        FindObject('Memo03').Memo.Text:='분  류  명 :';
        FindObject('Memo04').Memo.Text:=Sobo33.Button101.Caption;
      end;
      if(Sobo33.Edit106.Text<>'')and(Sobo33.Button101.Caption='' )Then begin
        FindObject('Memo03').Memo.Text:='도  서  명 :';
        FindObject('Memo04').Memo.Text:=Sobo33.Edit104.Text+' - '+Sobo33.Edit106.Text;
      end;
      if(Sobo33.Edit106.Text='' )and(Sobo33.Button101.Caption='' )Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen35, Seen35);
    Seen35.QuickRep1SrartPrnt('2');
    Seen35.Free; }
  end;
end;

procedure TTong40.Print_33_03(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
  //Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_33.frf');
      FindObject('Memo91').Memo.Text:=Sobo33.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo33.Edit101.Text+' - '+Sobo33.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo33.Edit104.Text+' - '+Sobo33.Edit106.Text;

      if Sobo33.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

  //oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen35, Seen35);
    Seen35.QuickRep1SrartPrnt('1');
    Seen35.Free; }
  end;
end;

procedure TTong40.Print_33_04(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
  //Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_34.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo14_1.Edit103.Text;
      FindObject('Memo04').Memo.Text:=Sobo14_1.Edit102.Text;

      ShowReport;
    end;

  //oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen35, Seen35);
    Seen35.QuickRep1SrartPrnt('1');
    Seen35.Free; }
  end;
end;

procedure TTong40.Print_34_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_41.frf');
      FindObject('Memo91').Memo.Text:=Sobo34.Edit108.Text+mPrnt;
      FindObject('Memo00').Memo.Text:='정품(폐기)현황';
      FindObject('Memo02').Memo.Text:=Sobo34.Edit101.Text+' - '+Sobo34.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_34_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  { oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_41.frf');
      FindObject('Memo91').Memo.Text:=Sobo34.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo34.Edit101.Text+' - '+Sobo34.Edit102.Text;

      if(Sobo34.Edit106.Text='' )and(Sobo34.Button101.Caption<>'')Then begin
        FindObject('Memo03').Memo.Text:='분  류  명 :';
        FindObject('Memo04').Memo.Text:=Sobo34.Button101.Caption;
      end;
      if(Sobo34.Edit106.Text<>'')and(Sobo34.Button101.Caption='' )Then begin
        FindObject('Memo03').Memo.Text:='도  서  명 :';
        FindObject('Memo04').Memo.Text:=Sobo34.Edit104.Text+' - '+Sobo34.Edit106.Text;
      end;
      if(Sobo34.Edit106.Text='' )and(Sobo34.Button101.Caption='' )Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo34.DBGrid101.Columns.Items[6].Title.Caption ='폐기수량' Then begin
        FindObject('Memo17').Memo.Text:='폐기수량';
        FindObject('Memo27').Memo.Text:='[Gpqut]';
        FindObject('Memo37').Memo.Text:='[Sum(Gpqut)]';
        FindObject('Memo47').Memo.Text:='[Sum(Gpqut)]';
      end else begin
        FindObject('Memo17').Memo.Text:='변경수량';
        FindObject('Memo27').Memo.Text:='[Gpsum]';
        FindObject('Memo37').Memo.Text:='[Sum(Gpsum)]';
        FindObject('Memo47').Memo.Text:='[Sum(Gpsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls; }
  { Application.CreateForm(TSeen37, Seen37);
    Seen37.QuickRep1SrartPrnt('2');
    Seen37.Free; }
  end;
end;

procedure TTong40.Print_34_05(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_45.frf');
      FindObject('Memo91').Memo.Text:=Sobo34_1.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo34_1.Edit101.Text+' - '+Sobo34_1.Edit102.Text);
      FindObject('Memo04').Memo.Text:=AutoFrx(Sobo34_1.Edit104.Text+' - '+Sobo34_1.Edit106.Text);
      FindObject('Memo11').Memo.Text:='분류코드';
      FindObject('Memo12').Memo.Text:='분류명';

      if Sobo34_1.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_34_06(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_45.frf');
      FindObject('Memo91').Memo.Text:=Sobo34_1.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo34_1.Edit101.Text+' - '+Sobo34_1.Edit102.Text);
      FindObject('Memo04').Memo.Text:=AutoFrx(Sobo34_1.Edit104.Text+' - '+Sobo34_1.Edit106.Text);
      FindObject('Memo11').Memo.Text:='도서코드';
      FindObject('Memo12').Memo.Text:='도서명';

      if Sobo34_1.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_35_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_41.frf');
      FindObject('Memo91').Memo.Text:=Sobo35.Edit108.Text+mPrnt;
      FindObject('Memo00').Memo.Text:='반품(폐기)현황';
      FindObject('Memo02').Memo.Text:=Sobo35.Edit101.Text+' - '+Sobo35.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_35_02(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_52.frf');
      FindObject('Memo91').Memo.Text:=Sobo35.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo35.Edit101.Text+' - '+Sobo35.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo35.Edit104.Text+' - '+Sobo35.Edit106.Text;

      if Sobo35.Button101.Caption<>'' Then begin
        FindObject('Memo04').Memo.Text:=Sobo35.Button101.Caption;
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_36_01(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_61.frf');
      FindObject('Memo91').Memo.Text:=Sobo36.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo36.Edit101.Text+' - '+Sobo36.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo36.Edit104.Text+' - '+Sobo36.Edit106.Text;

      if Sobo36.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo36.DBGrid101.Columns.Items[5].Title.Caption ='폐기수량' Then begin
        FindObject('Memo16').Memo.Text:='폐기수량';
        FindObject('Memo26').Memo.Text:='[Gpqut]';
        FindObject('Memo36').Memo.Text:='[Sum(Gpqut)]';
        FindObject('Memo46').Memo.Text:='[Sum(Gpqut)]';
      end else begin
        FindObject('Memo16').Memo.Text:='변경수량';
        FindObject('Memo26').Memo.Text:='[Gpsum]';
        FindObject('Memo36').Memo.Text:='[Sum(Gpsum)]';
        FindObject('Memo46').Memo.Text:='[Sum(Gpsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_36_02(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_62.frf');
      FindObject('Memo91').Memo.Text:=Sobo36.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo36.Edit101.Text+' - '+Sobo36.Edit102.Text;
      FindObject('Memo04').Memo.Text:=Sobo36.Edit104.Text+' - '+Sobo36.Edit106.Text;

      if Sobo36.Button101.Caption<>'' Then begin
        FindObject('Memo04').Memo.Text:=Sobo36.Button101.Caption;
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_37_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_71.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo37.Edit101.Text+' - '+Sobo37.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_37_02(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_71.frf');
      FindObject('Memo91').Memo.Text:=Sobo37.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo37.Edit101.Text+' - '+Sobo37.Edit102.Text;

      if(Sobo37.Edit106.Text='' )and(Sobo37.Button101.Caption<>'')Then begin
        FindObject('Memo03').Memo.Text:='담  당  자';
        FindObject('Memo04').Memo.Text:=Sobo37.Button101.Caption;
      end;
      if(Sobo37.Edit106.Text<>'')and(Sobo37.Button101.Caption='' )Then begin
        FindObject('Memo03').Memo.Text:='거래처명 :';
        FindObject('Memo04').Memo.Text:=Sobo37.Edit104.Text+' - '+Sobo37.Edit106.Text;
      end;
      if(Sobo37.Edit106.Text='' )and(Sobo37.Button101.Caption='' )Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo37.DBGrid101.Columns.Items[5].Title.Caption ='증정수량' Then begin
        FindObject('Memo16').Memo.Text:='증정수량';
        FindObject('Memo26').Memo.Text:='[Gjqut]';
        FindObject('Memo36').Memo.Text:='[Sum(Gjqut)]';
        FindObject('Memo46').Memo.Text:='[Sum(Gjqut)]';
      end else begin
        FindObject('Memo16').Memo.Text:='장부차액';
        FindObject('Memo26').Memo.Text:='[Gjsum]';
        FindObject('Memo36').Memo.Text:='[Sum(Gjsum)]';
        FindObject('Memo46').Memo.Text:='[Sum(Gjsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_38_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_38_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_82.frf');
      FindObject('Memo91').Memo.Text:=Sobo38_2.Edit108.Text+mPrnt;
      FindObject('Memo00').Memo.Text:='운 송 비';
      FindObject('Memo02').Memo.Text:=Sobo38_2.Edit101.Text+' - '+Sobo38_2.Edit102.Text;
    //FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:=Sobo38_2.Edit108.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_01(Sender: TObject);
var SearchRec : TSearchRec;
    ff1,ff2: Integer;
begin
  ff1 := FindFirst( GetExecPath + 'Report\Report_3_91.frf', faAnyFile, SearchRec);
  ff2 := FindFirst( GetExecPath + 'Report\Report_3_92.frf', faAnyFile, SearchRec);

if(ff1 = 0)then begin
  if Base10.T4_Sub81.Active=True Then begin
    oSqry:=Base10.T4_Sub81;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo71').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='지방';
      if Sobo39.RadioButton6.Checked=True Then begin
      FindObject('Memo71').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='시내';
      end else
      if Sobo39.RadioButton7.Checked=True Then begin
      FindObject('Memo71').Memo.Text:='지방';
      FindObject('Memo72').Memo.Text:='지방';
      end;

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end else
if(ff2 = 0)then begin
  if Sobo39.T3_Sub91.Active=True Then begin
    oSqry:=Sobo39.T3_Sub91;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_92.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo04').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;
end;

procedure TTong40.Print_39_02(Sender: TObject);
var SearchRec : TSearchRec;
    ff1,ff2: Integer;
begin
  ff1 := FindFirst( GetExecPath + 'Report\Report_3_91.frf', faAnyFile, SearchRec);
  ff2 := FindFirst( GetExecPath + 'Report\Report_3_92.frf', faAnyFile, SearchRec);

if(ff1 = 0)then begin
  if Base10.T4_Sub81.Active=True Then begin
    oSqry:=Base10.T4_Sub81;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo44').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='지방';
      if Sobo39.RadioButton6.Checked=True Then begin
      FindObject('Memo44').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='시내';
      end else
      if Sobo39.RadioButton7.Checked=True Then begin
      FindObject('Memo44').Memo.Text:='지방';
      FindObject('Memo72').Memo.Text:='지방';
      end;

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end else
if(ff2 = 0)then begin
  if Sobo39.T3_Sub91.Active=True Then begin
    oSqry:=Sobo39.T3_Sub91;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_92.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo04').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;
end;

procedure TTong40.Print_39_03(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  //oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo71').Memo.Text:='시내';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_04(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  //oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo71').Memo.Text:='지방';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_05(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  //oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo71').Memo.Text:='택배';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_06(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  //oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo71').Memo.Text:='화물';
      FindObject('Memo13').Memo.Text:='박스';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_07(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  //oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo71').Memo.Text:='직배';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_08(Sender: TObject);
begin
  if oSqry.Active=True Then begin
    oSqry:=Base10.T4_Sub81;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_92.frf');
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo04').Memo.Text:=AutoFrx(Sobo39.Button101.Caption);
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_09(Sender: TObject);
begin
  if oSqry.Active=True Then begin
    oSqry:=Base10.T4_Sub81;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_92.frf');
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_11(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_91.frf');
      FindObject('Memo91').Memo.Text:='';
      FindObject('Memo02').Memo.Text:=Sobo39_1.Edit101.Text+' - '+Sobo39_1.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_39_21(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_92.frf');
      FindObject('Memo91').Memo.Text:='';
      FindObject('Memo02').Memo.Text:=Sobo39_2.Edit101.Text+' - '+Sobo39_2.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_30_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_30_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_41_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_11.frf');
      FindObject('Memo91').Memo.Text:='';
      FindObject('Memo02').Memo.Text:=Sobo41.Edit101.Text+' - '+Sobo41.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen41, Seen41);
    Seen41.QuickRep1SrartPrnt('1');
    Seen41.Free; }
  end;
end;

procedure TTong40.Print_41_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

  { With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_12.frf');
      FindObject('Memo91').Memo.Text:=Sobo41.Edit208.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo41.Edit201.Text+' - '+Sobo41.Edit202.Text;
      FindObject('Memo04').Memo.Text:=Sobo41.Edit203.Text;
      ShowReport;
    end; }

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen41, Seen41);
    Seen41.QuickRep1SrartPrnt('2');
    Seen41.Free; }
  end;
end;

procedure TTong40.Print_42_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_21.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo42.Edit101.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen41, Seen41);
    Seen41.QuickRep1SrartPrnt('3');
    Seen41.Free; }
  end;
end;

procedure TTong40.Print_42_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_22.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo42_1.Edit101.Text+' - '+Sobo42_1.Edit102.Text;
      if Sobo42_1.Edit107.Text<>'' then begin
      FindObject('Memo03').Visible:=True;
      FindObject('Memo04').Visible:=True;
      FindObject('Memo04').Memo.Text:=Sobo42_1.Edit108.Text;
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen41, Seen41);
    Seen41.QuickRep1SrartPrnt('4');
    Seen41.Free; }
  end;
end;

procedure TTong40.Print_43_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_31.frf');
      FindObject('Memo91').Memo.Text:='';
      FindObject('Memo02').Memo.Text:=Sobo43.Edit101.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen43, Seen43);
    Seen43.QuickRep1SrartPrnt('1');
    Seen43.Free; }
  end;
end;

procedure TTong40.Print_43_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

  { With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_32.frf');
      FindObject('Memo91').Memo.Text:=Sobo43.Edit208.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo43.Edit201.Text+' - '+Sobo43.Edit202.Text;
      FindObject('Memo04').Memo.Text:=Sobo43.Edit203.Text;
      FindObject('Memo06').Memo.Text:=Sobo43.Edit204.Text;
      ShowReport;
    end; }

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen43, Seen43);
    Seen43.QuickRep1SrartPrnt('2');
    Seen43.Free; }
  end;
end;

procedure TTong40.Print_44_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_41.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo44.Edit101.Text+' - '+Sobo44.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen43, Seen43);
    Seen43.QuickRep1SrartPrnt('3');
    Seen43.Free; }
  end;
end;

procedure TTong40.Print_44_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_42.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo44_1.Edit101.Text+' - '+Sobo44_1.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen43, Seen43);
    Seen43.QuickRep1SrartPrnt('3');
    Seen43.Free; }
  end;
end;

procedure TTong40.Print_45_01(Sender: TObject);
var St1: Double;
    St2: String;
    sTemp: string;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      sTemp := GetExecPath + 'Report\Report_4_51.frf';  
      LoadFromFile(GetExecPath + 'Report\Report_4_51.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;

      FindObject('Memo00').Memo.Text:='청구서'+'('+Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월)';
      FindObject('Memo02').Memo.Text:='No:'+mSqry.FieldByName('Hcode').AsString;
      FindObject('Memo01').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo06').Memo.Text:=Copy(mSqry.FieldByName('Gdate').AsString,1,4)+'년'+
                                      Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월';

      Sqlen := 'Select Bigo2 From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
      Translate(Sqlen, '@Gcode', mSqry.FieldByName('Hcode').AsString);
      St2:=Base10.Seek_Name(Sqlen);
      if St2<>'' then
      FindObject('Memo193').Memo.Text:=St2;

      St1:=Sobo45.Edit227.Value+Sobo45.Edit228.Value;
      FindObject('Memo201').Memo.Text:=Sobo45.Edit201.Text;
      FindObject('Memo202').Memo.Text:=Sobo45.Edit202.Text;
      FindObject('Memo204').Memo.Text:=Sobo45.Edit204.Text;
      FindObject('Memo205').Memo.Text:=Sobo45.Edit205.Text;
      FindObject('Memo206').Memo.Text:=Sobo45.Edit206.Text;
      FindObject('Memo207').Memo.Text:=Sobo45.Edit207.Text;
      FindObject('Memo208').Memo.Text:=Sobo45.Edit208.Text;
      FindObject('Memo209').Memo.Text:=Sobo45.Edit209.Text;
      FindObject('Memo210').Memo.Text:=Sobo45.Edit210.Text;
      FindObject('Memo211').Memo.Text:=Sobo45.Edit211.Text;
      FindObject('Memo212').Memo.Text:=Sobo45.Edit212.Text;
      FindObject('Memo213').Memo.Text:=Sobo45.Edit213.Text;
      FindObject('Memo214').Memo.Text:=Sobo45.Edit214.Text;
      FindObject('Memo215').Memo.Text:=Sobo45.Edit215.Text;
      FindObject('Memo216').Memo.Text:=Sobo45.Edit216.Text;
      FindObject('Memo217').Memo.Text:=Sobo45.Edit217.Text;
      FindObject('Memo218').Memo.Text:=Sobo45.Edit218.Text;
      if Base10.Database.Database='book_03_db' then begin
        FindObject('Memo64').Memo.Text:=Sobo45.Edit229.Text;
    //  FindObject('Memo219').Memo.Text:=Sobo45.Edit219.Text;
      end;
      FindObject('Memo220').Memo.Text:=Sobo45.Edit220.Text;
      FindObject('Memo221').Memo.Text:=Sobo45.Edit221.Text;
      FindObject('Memo222').Memo.Text:=Sobo45.Edit222.Text;
      FindObject('Memo223').Memo.Text:=Sobo45.Edit223.Text;
      FindObject('Memo224').Memo.Text:=Sobo45.Edit224.Text;
      FindObject('Memo225').Memo.Text:=Sobo45.Edit225.Text;
      FindObject('Memo226').Memo.Text:=Sobo45.Edit226.Text;
      FindObject('Memo227').Memo.Text:=Sobo45.Edit227.Text;
      FindObject('Memo228').Memo.Text:=Sobo45.Edit228.Text;
      FindObject('Memo229').Memo.Text:=Sobo45.Edit229.Text;
      FindObject('Memo230').Memo.Text:='￦'+Sobo45.Edit230.Text;
      FindObject('Memo231').Memo.Text:=Sobo45.Edit231.Text;
      FindObject('Memo232').Memo.Text:=Sobo45.Edit232.Text;
      FindObject('Memo233').Memo.Text:=Sobo45.Edit233.Text;
      FindObject('Memo234').Memo.Text:=Sobo45.Edit234.Text;
      FindObject('Memo235').Memo.Text:=Sobo45.Edit235.Text;
      FindObject('Memo236').Memo.Text:=Sobo45.Edit236.Text;
      FindObject('Memo237').Memo.Text:=Sobo45.Edit237.Text;
      FindObject('Memo238').Memo.Text:=Sobo45.Edit238.Text;
      FindObject('Memo239').Memo.Text:=Sobo45.Edit239.Text;
      FindObject('Memo240').Memo.Text:=Sobo45.Edit240.Text;
      FindObject('Memo242').Memo.Text:=Sobo45.Edit242.Text;
      FindObject('Memo243').Memo.Text:=Sobo45.Edit243.Text;
      FindObject('Memo244').Memo.Text:=Sobo45.Edit244.Text;
      FindObject('Memo245').Memo.Text:=Sobo45.Edit245.Text;
      FindObject('Memo246').Memo.Text:=Sobo45.Edit246.Text;
      FindObject('Memo247').Memo.Text:=Sobo45.Edit247.Text;
      FindObject('Memo248').Memo.Text:=Sobo45.Edit248.Text;
      FindObject('Memo261').Memo.Text:=Sobo45.Edit261.Text;
      FindObject('Memo262').Memo.Text:=Sobo45.Edit262.Text;
      FindObject('Memo263').Memo.Text:=Sobo45.Edit263.Text;
      FindObject('Memo251').Memo.Text:=Sobo45.Edit301.Text;
      FindObject('Memo252').Memo.Text:=Sobo45.Edit302.Text;
      FindObject('Memo253').Memo.Text:=Sobo45.Edit303.Text;

      if(Base10.Database.Database ='book_kb_db')then begin
      FindObject('Memo305').Memo.Text:=Sobo45.Edit315.Text;
      end;

      if(Base10.Database.Database ='chul_01_db')or
        (Base10.Database.Database ='book_01_db')or
        (Base10.Database.Database ='book_04_db')then begin
      FindObject('Memo264').Memo.Text:=Sobo45.Edit264.Text;
      FindObject('Memo265').Memo.Text:=Sobo45.Edit265.Text;
      { if(Sobo45.Edit264.Value=0)and
          (Sobo45.Edit265.Value=0)and
          (Sobo45.Edit225.Value=0)then
         FindObject('Memo125').Memo.Text:='거래명세표 발행 및 작업비:'; }
      end;

      if(Base10.Database.Host='115.68.7.138')and
        (Base10.Database.Database ='book_06_db')then begin
      FindObject('Memo264').Memo.Text:=Sobo45.Edit264.Text;
      FindObject('Memo265').Memo.Text:=Sobo45.Edit265.Text;
      end;

      if Base10.Database.Database<>'chul_01_db' then begin
      FindObject('Memo254').Memo.Text:=Sobo45.Edit304.Text;
      FindObject('Memo255').Memo.Text:=Sobo45.Edit305.Text;
      FindObject('Memo256').Memo.Text:=Sobo45.Edit306.Text;
      FindObject('Memo257').Memo.Text:=Sobo45.Edit307.Text;
      FindObject('Memo258').Memo.Text:=Sobo45.Edit308.Text;
      FindObject('Memo259').Memo.Text:=Sobo45.Edit309.Text;

      FindObject('Memo301').Memo.Text:=Sobo45.Edit310.Text;
      FindObject('Memo303').Memo.Text:=Sobo45.Edit312.Text;

      if FindObject('Memo130').Visible=True then
      FindObject('Memo266').Memo.Text:=Sobo45.Edit266.Text;
      end;

      FindObject('Memo902').Memo.Text:=Sobo45.Edit902.Text;
      FindObject('Memo300').Memo.Text:=Format('%12s',[FormatFloat('###,###,##0',St1)]);

      if(Base10.Database.Host='115.68.3.154')    and
        ((Base10.Database.Database='book_06_db') or (Base10.Database.Database='book_11_db')) then begin
      FindObject('Memo291').Memo.Text:=Sobo45.Edit313.Text;
      FindObject('Memo292').Memo.Text:=Sobo45.Edit314.Text;
      FindObject('Memo293').Memo.Text:=Sobo45.Edit315.Text;

      FindObject('Memo219').Memo.Text:=Sobo45.Edit219.Text;
      FindObject('Memo251').Memo.Text:=Sobo45.Edit301.Text;
      FindObject('Memo252').Memo.Text:=Sobo45.Edit302.Text;
      FindObject('Memo253').Memo.Text:=Sobo45.Edit303.Text;
      FindObject('Memo257').Memo.Text:=Sobo45.Edit247.Text;
      FindObject('Memo258').Memo.Text:=Sobo45.Edit248.Text;
      FindObject('Memo259').Memo.Text:=Sobo45.Edit246.Text;
      FindObject('Memo217').Memo.Text:=Sobo45.Edit264.Text;
      FindObject('Memo254').Memo.Text:=Sobo45.Edit307.Text;
      FindObject('Memo255').Memo.Text:=Sobo45.Edit308.Text;
      FindObject('Memo256').Memo.Text:=Sobo45.Edit309.Text;
      FindObject('Memo301').Memo.Text:=Sobo45.Edit310.Text;
      FindObject('Memo302').Memo.Text:=Sobo45.Edit311.Text;
      FindObject('Memo303').Memo.Text:=Sobo45.Edit312.Text;
      end;

      if (Hnnnn='8800') then
      begin
      FindObject('Memo313').Memo.Text:=Sobo45.Edit313.Text;
      FindObject('Memo314').Memo.Text:=Sobo45.Edit314.Text;
      FindObject('Memo315').Memo.Text:=Sobo45.Edit315.Text;
      end;

      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen45, Seen45);
    Seen45.QuickRep1SrartPrnt('1');
    Seen45.Free; }
  end;
end;

procedure TTong40.Print_45_02(Sender: TObject);
var St1: Double;
    St2: String;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_52.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;

      FindObject('Memo00').Memo.Text:='청구서'+'('+Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월)';
      FindObject('Memo02').Memo.Text:='No:'+mSqry.FieldByName('Hcode').AsString;
      FindObject('Memo01').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo06').Memo.Text:=Copy(mSqry.FieldByName('Gdate').AsString,1,4)+'년'+
                                      Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월';

      Sqlen := 'Select Bigo2 From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
      Translate(Sqlen, '@Gcode', mSqry.FieldByName('Hcode').AsString);
      St2:=Base10.Seek_Name(Sqlen);
      if St2<>'' then
      FindObject('Memo193').Memo.Text:=St2;

      St1:=Sobo45_1.Edit227.Value+Sobo45_1.Edit228.Value;
      FindObject('Memo201').Memo.Text:=Sobo45_1.Edit201.Text;
      FindObject('Memo202').Memo.Text:=Sobo45_1.Edit202.Text;
      FindObject('Memo204').Memo.Text:=Sobo45_1.Edit204.Text;
      FindObject('Memo205').Memo.Text:=Sobo45_1.Edit205.Text;
      FindObject('Memo206').Memo.Text:=Sobo45_1.Edit206.Text;
      FindObject('Memo207').Memo.Text:=Sobo45_1.Edit207.Text;
      FindObject('Memo208').Memo.Text:=Sobo45_1.Edit208.Text;
      FindObject('Memo209').Memo.Text:=Sobo45_1.Edit209.Text;
      FindObject('Memo210').Memo.Text:=Sobo45_1.Edit210.Text;
      FindObject('Memo211').Memo.Text:=Sobo45_1.Edit211.Text;
      FindObject('Memo212').Memo.Text:=Sobo45_1.Edit212.Text;
      FindObject('Memo213').Memo.Text:=Sobo45_1.Edit213.Text;
      FindObject('Memo214').Memo.Text:=Sobo45_1.Edit214.Text;
      FindObject('Memo215').Memo.Text:=Sobo45_1.Edit215.Text;
      FindObject('Memo216').Memo.Text:=Sobo45_1.Edit216.Text;
      FindObject('Memo217').Memo.Text:=Sobo45_1.Edit217.Text;
      FindObject('Memo218').Memo.Text:=Sobo45_1.Edit218.Text;
      if Base10.Database.Database='book_03_db' then
      FindObject('Memo219').Memo.Text:=Sobo45_1.Edit219.Text;
      FindObject('Memo220').Memo.Text:=Sobo45_1.Edit220.Text;
      FindObject('Memo221').Memo.Text:=Sobo45_1.Edit221.Text;
      FindObject('Memo222').Memo.Text:=Sobo45_1.Edit222.Text;
      FindObject('Memo223').Memo.Text:=Sobo45_1.Edit223.Text;
      FindObject('Memo224').Memo.Text:=Sobo45_1.Edit224.Text;
      FindObject('Memo225').Memo.Text:=Sobo45_1.Edit225.Text;
      FindObject('Memo226').Memo.Text:=Sobo45_1.Edit226.Text;
      FindObject('Memo227').Memo.Text:=Sobo45_1.Edit227.Text;
      FindObject('Memo228').Memo.Text:=Sobo45_1.Edit228.Text;
      FindObject('Memo229').Memo.Text:=Sobo45_1.Edit229.Text;
      FindObject('Memo230').Memo.Text:='￦'+Sobo45_1.Edit230.Text;
      FindObject('Memo231').Memo.Text:=Sobo45_1.Edit231.Text;
      FindObject('Memo232').Memo.Text:=Sobo45_1.Edit232.Text;
      FindObject('Memo233').Memo.Text:=Sobo45_1.Edit233.Text;
      FindObject('Memo234').Memo.Text:=Sobo45_1.Edit234.Text;
      FindObject('Memo235').Memo.Text:=Sobo45_1.Edit235.Text;
      FindObject('Memo236').Memo.Text:=Sobo45_1.Edit236.Text;
      FindObject('Memo237').Memo.Text:=Sobo45_1.Edit237.Text;
      FindObject('Memo238').Memo.Text:=Sobo45_1.Edit238.Text;
      FindObject('Memo239').Memo.Text:=Sobo45_1.Edit239.Text;
      FindObject('Memo240').Memo.Text:=Sobo45_1.Edit240.Text;
      FindObject('Memo242').Memo.Text:=Sobo45_1.Edit242.Text;
      FindObject('Memo243').Memo.Text:=Sobo45_1.Edit243.Text;
      FindObject('Memo244').Memo.Text:=Sobo45_1.Edit244.Text;
      FindObject('Memo245').Memo.Text:=Sobo45_1.Edit245.Text;
      FindObject('Memo246').Memo.Text:=Sobo45_1.Edit246.Text;
      FindObject('Memo247').Memo.Text:=Sobo45_1.Edit247.Text;
      FindObject('Memo248').Memo.Text:=Sobo45_1.Edit248.Text;
      FindObject('Memo261').Memo.Text:=Sobo45_1.Edit261.Text;
      FindObject('Memo262').Memo.Text:=Sobo45_1.Edit262.Text;
      FindObject('Memo263').Memo.Text:=Sobo45_1.Edit263.Text;
      FindObject('Memo251').Memo.Text:=Sobo45_1.Edit301.Text;
      FindObject('Memo252').Memo.Text:=Sobo45_1.Edit302.Text;
      FindObject('Memo253').Memo.Text:=Sobo45_1.Edit303.Text;

      if(Base10.Database.Database ='book_kb_db')then begin
      FindObject('Memo305').Memo.Text:=Sobo45.Edit315.Text;
      end;

      if(Base10.Database.Database ='chul_01_db')or
        (Base10.Database.Database ='book_04_db')then begin
      FindObject('Memo264').Memo.Text:=Sobo45.Edit264.Text;
      FindObject('Memo265').Memo.Text:=Sobo45.Edit265.Text;
      { if(Sobo45.Edit264.Value=0)and
          (Sobo45.Edit265.Value=0)and
          (Sobo45.Edit225.Value=0)then
         FindObject('Memo125').Memo.Text:='거래명세표 발행 및 작업비:'; }
      end;

      if(Base10.Database.Host='115.68.7.138')and
        (Base10.Database.Database ='book_06_db')then begin
      FindObject('Memo264').Memo.Text:=Sobo45_1.Edit264.Text;
      FindObject('Memo265').Memo.Text:=Sobo45_1.Edit265.Text;
      end;

      if Base10.Database.Database<>'chul_01_db' then begin
      FindObject('Memo254').Memo.Text:=Sobo45_1.Edit304.Text;
      FindObject('Memo255').Memo.Text:=Sobo45_1.Edit305.Text;
      FindObject('Memo256').Memo.Text:=Sobo45_1.Edit306.Text;
      FindObject('Memo257').Memo.Text:=Sobo45_1.Edit307.Text;
      FindObject('Memo258').Memo.Text:=Sobo45_1.Edit308.Text;
      FindObject('Memo259').Memo.Text:=Sobo45_1.Edit309.Text;

      FindObject('Memo301').Memo.Text:=Sobo45_1.Edit310.Text;
      FindObject('Memo303').Memo.Text:=Sobo45_1.Edit312.Text;

      if FindObject('Memo130').Visible=True then
      FindObject('Memo266').Memo.Text:=Sobo45_1.Edit266.Text;
      end;

      FindObject('Memo902').Memo.Text:=Sobo45_1.Edit902.Text;
      FindObject('Memo300').Memo.Text:=Format('%12s',[FormatFloat('###,###,##0',St1)]);

      if(Base10.Database.Host='115.68.3.154')and
        (Base10.Database.Database='book_06_db')then begin
      FindObject('Memo291').Memo.Text:=Sobo45_1.Edit313.Text;
      FindObject('Memo292').Memo.Text:=Sobo45_1.Edit314.Text;
      FindObject('Memo293').Memo.Text:=Sobo45_1.Edit315.Text;
      FindObject('Memo219').Memo.Text:=Sobo45_1.Edit219.Text;
      FindObject('Memo251').Memo.Text:=Sobo45_1.Edit301.Text;
      FindObject('Memo252').Memo.Text:=Sobo45_1.Edit302.Text;
      FindObject('Memo253').Memo.Text:=Sobo45_1.Edit303.Text;
      FindObject('Memo257').Memo.Text:=Sobo45_1.Edit247.Text;
      FindObject('Memo258').Memo.Text:=Sobo45_1.Edit248.Text;
      FindObject('Memo259').Memo.Text:=Sobo45_1.Edit246.Text;
      FindObject('Memo217').Memo.Text:=Sobo45_1.Edit264.Text;
      FindObject('Memo254').Memo.Text:=Sobo45_1.Edit307.Text;
      FindObject('Memo255').Memo.Text:=Sobo45_1.Edit308.Text;
      FindObject('Memo256').Memo.Text:=Sobo45_1.Edit309.Text;
      FindObject('Memo301').Memo.Text:=Sobo45_1.Edit310.Text;
      FindObject('Memo302').Memo.Text:=Sobo45_1.Edit311.Text;
      FindObject('Memo303').Memo.Text:=Sobo45_1.Edit312.Text;
      end;

      if Hnnnn='8800' then begin
      FindObject('Memo313').Memo.Text:=Sobo45.Edit313.Text;
      FindObject('Memo314').Memo.Text:=Sobo45.Edit314.Text;
      FindObject('Memo315').Memo.Text:=Sobo45.Edit315.Text;
      end;

      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen45, Seen45);
    Seen45.QuickRep1SrartPrnt('1');
    Seen45.Free; }
  end;
end;

procedure TTong40.Print_46_01(Sender: TObject);
var St1: Double;
    St2: String;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_51.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;

      FindObject('Memo00').Memo.Text:='청구서'+'('+Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월)';
      FindObject('Memo02').Memo.Text:='No:'+mSqry.FieldByName('Hcode').AsString;
      FindObject('Memo01').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo06').Memo.Text:=Copy(mSqry.FieldByName('Gdate').AsString,1,4)+'년'+
                                      Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월';

      Sqlen := 'Select Bigo2 From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
      Translate(Sqlen, '@Gcode', mSqry.FieldByName('Hcode').AsString);
      St2:=Base10.Seek_Name(Sqlen);
      if St2<>'' then
      FindObject('Memo193').Memo.Text:=St2;

      St1:=Sobo46.Edit227.Value+Sobo46.Edit228.Value;
      FindObject('Memo201').Memo.Text:=Sobo46.Edit201.Text;
      FindObject('Memo202').Memo.Text:=Sobo46.Edit202.Text;
      FindObject('Memo204').Memo.Text:=Sobo46.Edit204.Text;
      FindObject('Memo205').Memo.Text:=Sobo46.Edit205.Text;
      FindObject('Memo206').Memo.Text:=Sobo46.Edit206.Text;
      FindObject('Memo207').Memo.Text:=Sobo46.Edit207.Text;
      FindObject('Memo208').Memo.Text:=Sobo46.Edit208.Text;
      FindObject('Memo209').Memo.Text:=Sobo46.Edit209.Text;
      FindObject('Memo210').Memo.Text:=Sobo46.Edit210.Text;
      FindObject('Memo211').Memo.Text:=Sobo46.Edit211.Text;
      FindObject('Memo212').Memo.Text:=Sobo46.Edit212.Text;
      FindObject('Memo213').Memo.Text:=Sobo46.Edit213.Text;
      FindObject('Memo214').Memo.Text:=Sobo46.Edit214.Text;
      FindObject('Memo215').Memo.Text:=Sobo46.Edit215.Text;
      FindObject('Memo216').Memo.Text:=Sobo46.Edit216.Text;
      FindObject('Memo217').Memo.Text:=Sobo46.Edit217.Text;
      FindObject('Memo218').Memo.Text:=Sobo46.Edit218.Text;
      FindObject('Memo220').Memo.Text:=Sobo46.Edit220.Text;
      FindObject('Memo221').Memo.Text:=Sobo46.Edit221.Text;
      FindObject('Memo222').Memo.Text:=Sobo46.Edit222.Text;
      FindObject('Memo223').Memo.Text:=Sobo46.Edit223.Text;
      FindObject('Memo224').Memo.Text:=Sobo46.Edit224.Text;
      FindObject('Memo225').Memo.Text:=Sobo46.Edit225.Text;
      FindObject('Memo226').Memo.Text:=Sobo46.Edit226.Text;
      FindObject('Memo227').Memo.Text:=Sobo46.Edit227.Text;
      FindObject('Memo228').Memo.Text:=Sobo46.Edit228.Text;
      FindObject('Memo229').Memo.Text:=Sobo46.Edit229.Text;
      FindObject('Memo230').Memo.Text:='￦'+Sobo46.Edit230.Text;
      FindObject('Memo231').Memo.Text:=Sobo46.Edit231.Text;
      FindObject('Memo232').Memo.Text:=Sobo46.Edit232.Text;
      FindObject('Memo233').Memo.Text:=Sobo46.Edit233.Text;
      FindObject('Memo234').Memo.Text:=Sobo46.Edit234.Text;
      FindObject('Memo235').Memo.Text:=Sobo46.Edit235.Text;
      FindObject('Memo236').Memo.Text:=Sobo46.Edit236.Text;
      FindObject('Memo237').Memo.Text:=Sobo46.Edit237.Text;
      FindObject('Memo238').Memo.Text:=Sobo46.Edit238.Text;
      FindObject('Memo239').Memo.Text:=Sobo46.Edit239.Text;
      FindObject('Memo240').Memo.Text:=Sobo46.Edit240.Text;
      FindObject('Memo242').Memo.Text:=Sobo46.Edit242.Text;
      FindObject('Memo243').Memo.Text:=Sobo46.Edit243.Text;
      FindObject('Memo244').Memo.Text:=Sobo46.Edit244.Text;
      FindObject('Memo245').Memo.Text:=Sobo46.Edit245.Text;
      FindObject('Memo246').Memo.Text:=Sobo46.Edit246.Text;
      FindObject('Memo247').Memo.Text:=Sobo46.Edit247.Text;
      FindObject('Memo248').Memo.Text:=Sobo46.Edit248.Text;
      FindObject('Memo261').Memo.Text:=Sobo46.Edit261.Text;
      FindObject('Memo262').Memo.Text:=Sobo46.Edit262.Text;
      FindObject('Memo263').Memo.Text:=Sobo46.Edit263.Text;
      FindObject('Memo251').Memo.Text:=Sobo46.Edit301.Text;
      FindObject('Memo252').Memo.Text:=Sobo46.Edit302.Text;
      FindObject('Memo253').Memo.Text:=Sobo46.Edit303.Text;

      FindObject('Memo254').Memo.Text:=Sobo46.Edit304.Text;
      FindObject('Memo255').Memo.Text:=Sobo46.Edit305.Text;
      FindObject('Memo256').Memo.Text:=Sobo46.Edit306.Text;
      FindObject('Memo257').Memo.Text:=Sobo46.Edit307.Text;
      FindObject('Memo258').Memo.Text:=Sobo46.Edit308.Text;
      FindObject('Memo259').Memo.Text:=Sobo46.Edit309.Text;

      if(Base10.Database.Database ='book_kb_db')then begin
      FindObject('Memo305').Memo.Text:=Sobo46.Edit315.Text;
      end;

      if(Base10.Database.Database ='chul_01_db')or
        (Base10.Database.Database ='book_04_db')then begin
      FindObject('Memo264').Memo.Text:=Sobo46.Edit264.Text;
      FindObject('Memo265').Memo.Text:=Sobo46.Edit265.Text;
      { if(Sobo46.Edit264.Value=0)and
          (Sobo46.Edit265.Value=0)and
          (Sobo46.Edit225.Value=0)then
         FindObject('Memo125').Memo.Text:='거래명세표 발행 및 작업비:'; }
      end;

      if(Base10.Database.Host='115.68.7.138')and
        (Base10.Database.Database ='book_06_db')then begin
      FindObject('Memo264').Memo.Text:=Sobo46.Edit264.Text;
      FindObject('Memo265').Memo.Text:=Sobo46.Edit265.Text;
      end;

      if Base10.Database.Database<>'chul_01_db' then begin
      FindObject('Memo254').Memo.Text:=Sobo46.Edit304.Text;
      FindObject('Memo255').Memo.Text:=Sobo46.Edit305.Text;
      FindObject('Memo256').Memo.Text:=Sobo46.Edit306.Text;
      FindObject('Memo257').Memo.Text:=Sobo46.Edit307.Text;
      FindObject('Memo258').Memo.Text:=Sobo46.Edit308.Text;
      FindObject('Memo259').Memo.Text:=Sobo46.Edit309.Text;

      FindObject('Memo301').Memo.Text:=Sobo46.Edit310.Text;
      FindObject('Memo303').Memo.Text:=Sobo46.Edit312.Text;

      if FindObject('Memo130').Visible=True then
      FindObject('Memo266').Memo.Text:=Sobo46.Edit266.Text;
      end;

      FindObject('Memo902').Memo.Text:=Sobo46.Edit902.Text;
      FindObject('Memo300').Memo.Text:=Format('%12s',[FormatFloat('###,###,##0',St1)]);

      if(Base10.Database.Host='115.68.3.154')and
        (Base10.Database.Database='book_06_db')then begin
      FindObject('Memo291').Memo.Text:=Sobo46.Edit313.Text;
      FindObject('Memo292').Memo.Text:=Sobo46.Edit314.Text;
      FindObject('Memo293').Memo.Text:=Sobo46.Edit315.Text;
      FindObject('Memo219').Memo.Text:=Sobo46.Edit219.Text;
      FindObject('Memo251').Memo.Text:=Sobo46.Edit301.Text;
      FindObject('Memo252').Memo.Text:=Sobo46.Edit302.Text;
      FindObject('Memo253').Memo.Text:=Sobo46.Edit303.Text;
      FindObject('Memo257').Memo.Text:=Sobo46.Edit247.Text;
      FindObject('Memo258').Memo.Text:=Sobo46.Edit248.Text;
      FindObject('Memo259').Memo.Text:=Sobo46.Edit246.Text;
      FindObject('Memo217').Memo.Text:=Sobo46.Edit264.Text;
      FindObject('Memo254').Memo.Text:=Sobo46.Edit307.Text;
      FindObject('Memo255').Memo.Text:=Sobo46.Edit308.Text;
      FindObject('Memo256').Memo.Text:=Sobo46.Edit309.Text;
      FindObject('Memo301').Memo.Text:=Sobo46.Edit310.Text;
      FindObject('Memo302').Memo.Text:=Sobo46.Edit311.Text;
      FindObject('Memo303').Memo.Text:=Sobo46.Edit312.Text;
      end;

      if Hnnnn='8800' then begin
      FindObject('Memo313').Memo.Text:=Sobo46.Edit313.Text;
      FindObject('Memo314').Memo.Text:=Sobo46.Edit314.Text;
      FindObject('Memo315').Memo.Text:=Sobo46.Edit315.Text;
      end;

      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_46_02(Sender: TObject);
var St1: Double;
    St2: String;
begin
{ if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_51.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;

      FindObject('Memo00').Memo.Text:='청구서'+'('+Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월)';
      FindObject('Memo02').Memo.Text:='No:'+mSqry.FieldByName('Hcode').AsString;
      FindObject('Memo01').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo06').Memo.Text:=Copy(mSqry.FieldByName('Gdate').AsString,1,4)+'년'+
                                      Copy(mSqry.FieldByName('Gdate').AsString,6,2)+'월';

      Sqlen := 'Select Bigo2 From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
      Translate(Sqlen, '@Gcode', mSqry.FieldByName('Hcode').AsString);
      St2:=Base10.Seek_Name(Sqlen);
      if St2<>'' then
      FindObject('Memo193').Memo.Text:=St2;

      St1:=Sobo46.Edit227.Value+Sobo46.Edit228.Value;
      FindObject('Memo201').Memo.Text:=Sobo46.Edit201.Text;
      FindObject('Memo202').Memo.Text:=Sobo46.Edit202.Text;
      FindObject('Memo204').Memo.Text:=Sobo46.Edit204.Text;
      FindObject('Memo205').Memo.Text:=Sobo46.Edit205.Text;
      FindObject('Memo206').Memo.Text:=Sobo46.Edit206.Text;
      FindObject('Memo207').Memo.Text:=Sobo46.Edit207.Text;
      FindObject('Memo208').Memo.Text:=Sobo46.Edit208.Text;
      FindObject('Memo209').Memo.Text:=Sobo46.Edit209.Text;
      FindObject('Memo210').Memo.Text:=Sobo46.Edit210.Text;
      FindObject('Memo211').Memo.Text:=Sobo46.Edit211.Text;
      FindObject('Memo212').Memo.Text:=Sobo46.Edit212.Text;
      FindObject('Memo213').Memo.Text:=Sobo46.Edit213.Text;
      FindObject('Memo214').Memo.Text:=Sobo46.Edit214.Text;
      FindObject('Memo215').Memo.Text:=Sobo46.Edit215.Text;
      FindObject('Memo216').Memo.Text:=Sobo46.Edit216.Text;
      FindObject('Memo217').Memo.Text:=Sobo46.Edit217.Text;
      FindObject('Memo218').Memo.Text:=Sobo46.Edit218.Text;
      FindObject('Memo220').Memo.Text:=Sobo46.Edit220.Text;
      FindObject('Memo221').Memo.Text:=Sobo46.Edit221.Text;
      FindObject('Memo222').Memo.Text:=Sobo46.Edit222.Text;
      FindObject('Memo223').Memo.Text:=Sobo46.Edit223.Text;
      FindObject('Memo224').Memo.Text:=Sobo46.Edit224.Text;
      FindObject('Memo225').Memo.Text:=Sobo46.Edit225.Text;
      FindObject('Memo226').Memo.Text:=Sobo46.Edit226.Text;
      FindObject('Memo227').Memo.Text:=Sobo46.Edit227.Text;
      FindObject('Memo228').Memo.Text:=Sobo46.Edit228.Text;
      FindObject('Memo229').Memo.Text:=Sobo46.Edit229.Text;
      FindObject('Memo230').Memo.Text:='￦'+Sobo46.Edit230.Text;
      FindObject('Memo231').Memo.Text:=Sobo46.Edit231.Text;
      FindObject('Memo232').Memo.Text:=Sobo46.Edit232.Text;
      FindObject('Memo233').Memo.Text:=Sobo46.Edit233.Text;
      FindObject('Memo234').Memo.Text:=Sobo46.Edit234.Text;
      FindObject('Memo235').Memo.Text:=Sobo46.Edit235.Text;
      FindObject('Memo236').Memo.Text:=Sobo46.Edit236.Text;
      FindObject('Memo237').Memo.Text:=Sobo46.Edit237.Text;
      FindObject('Memo238').Memo.Text:=Sobo46.Edit238.Text;
      FindObject('Memo239').Memo.Text:=Sobo46.Edit239.Text;
      FindObject('Memo240').Memo.Text:=Sobo46.Edit240.Text;
      FindObject('Memo242').Memo.Text:=Sobo46.Edit242.Text;
      FindObject('Memo243').Memo.Text:=Sobo46.Edit243.Text;
      FindObject('Memo244').Memo.Text:=Sobo46.Edit244.Text;
      FindObject('Memo245').Memo.Text:=Sobo46.Edit245.Text;
      FindObject('Memo246').Memo.Text:=Sobo46.Edit246.Text;
      FindObject('Memo247').Memo.Text:=Sobo46.Edit247.Text;
      FindObject('Memo248').Memo.Text:=Sobo46.Edit248.Text;
      FindObject('Memo261').Memo.Text:=Sobo46.Edit261.Text;
      FindObject('Memo262').Memo.Text:=Sobo46.Edit262.Text;
      FindObject('Memo263').Memo.Text:=Sobo46.Edit263.Text;
      if FindObject('Memo130').Visible=True then
      FindObject('Memo266').Memo.Text:=Sobo46.Edit266.Text;
      FindObject('Memo300').Memo.Text:=Format('%12s',[FormatFloat('###,###,##0',St1)]);
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_47_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_71.frf');
      FindObject('Memo91').Memo.Text:=Sobo47.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo47.Edit101.Text+' - '+Sobo47.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen47, Seen47);
    Seen47.QuickRep1SrartPrnt('1');
    Seen47.Free; }
  end;
end;

procedure TTong40.Print_47_02(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_72.frf');
      FindObject('Memo91').Memo.Text:=Sobo47.Edit208.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo47.Edit201.Text+' - '+Sobo47.Edit202.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end; }
end;

procedure TTong40.Print_48_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  { oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_81.frf');
      FindObject('Memo91').Memo.Text:=Sobo48.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo48.Edit101.Text+' - '+Sobo48.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls; }
  { Application.CreateForm(TSeen48, Seen48);
    Seen48.QuickRep1SrartPrnt('1');
    Seen48.Free; }
  end;
end;

procedure TTong40.Print_48_02(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Application.CreateForm(TSeen48, Seen48);
    Seen48.QuickRep1SrartPrnt('2');
    Seen48.Free;
  end; }
end;

procedure TTong40.Print_49_01(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_92.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo49.Edit101.Text+' - '+Sobo49.Edit102.Text;
      FindObject('Memo03').Memo.Text:='거래처명 :';
      FindObject('Memo04').Memo.Text:=Sobo49.Edit104.Text+' - '+Sobo49.Edit106.Text;

      if Sobo49.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen49, Seen49);
    Seen49.QuickRep1SrartPrnt('1');
    Seen49.Free; }
  end;
end;

procedure TTong40.Print_49_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_4_91.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo49.Edit101.Text+' - '+Sobo49.Edit102.Text;

      if(Sobo49.Edit106.Text='')and(Sobo49.Button101.Caption<>'') Then begin
        FindObject('Memo03').Memo.Text:='구  분  명 :';
        FindObject('Memo04').Memo.Text:=Sobo49.Button101.Caption;
      end;
      if(Sobo49.Edit106.Text<>'')and(Sobo49.Button101.Caption='') Then begin
        FindObject('Memo03').Memo.Text:='거래처명 :';
        FindObject('Memo04').Memo.Text:=Sobo49.Edit104.Text+' - '+Sobo49.Edit106.Text;
      end;
      if(Sobo49.Edit106.Text='')and(Sobo49.Button101.Caption='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen49, Seen49);
    Seen49.QuickRep1SrartPrnt('2');
    Seen49.Free; }
  end;
end;

procedure TTong40.Print_40_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_40_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_51_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_21.frf');
      FindObject('Memo91').Memo.Text:=Sobo51.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo51.Edit101.Text+' - '+Sobo51.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
    { FindObject('Memo03').Memo.Text:='도  서  명 :';
      FindObject('Memo04').Memo.Text:=Sobo51.Edit104.Text+' - '+Sobo51.Edit106.Text;

      if Sobo51.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end; }
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen51, Seen51);
    Seen51.QuickRep1SrartPrnt('1');
    Seen51.Free; }
  end;
end;

procedure TTong40.Print_51_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

  { With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_12.frf');
      FindObject('Memo91').Memo.Text:=Sobo51.Edit208.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo51.Edit201.Text+' - '+Sobo51.Edit202.Text;
      FindObject('Memo03').Memo.Text:='입고처명 :';
      FindObject('Memo04').Memo.Text:=Sobo51.Edit204.Text+' - '+Sobo51.Edit206.Text;

      if Sobo51.Edit206.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end; }

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen51, Seen51);
    Seen51.QuickRep1SrartPrnt('2');
    Seen51.Free; }
  end;
end;

procedure TTong40.Print_52_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_21.frf');
      FindObject('Memo91').Memo.Text:=Sobo52.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo52.Edit101.Text+' - '+Sobo52.Edit102.Text;
      FindObject('Memo03').Memo.Text:='';
      FindObject('Memo04').Memo.Text:='';
    { FindObject('Memo03').Memo.Text:='도  서  명 :';
      FindObject('Memo04').Memo.Text:=Sobo52.Edit104.Text+' - '+Sobo52.Edit106.Text;

      if Sobo52.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end; }
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen51, Seen51);
    Seen51.QuickRep1SrartPrnt('3');
    Seen51.Free; }
  end;
end;

procedure TTong40.Print_52_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

  { With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_22.frf');
      FindObject('Memo91').Memo.Text:=Sobo52.Edit208.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo52.Edit201.Text+' - '+Sobo52.Edit202.Text;
      FindObject('Memo03').Memo.Text:='도  서  명 :';
      FindObject('Memo04').Memo.Text:=Sobo52.Edit204.Text+' - '+Sobo52.Edit206.Text;

      if Sobo52.Edit206.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end; }

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen51, Seen51);
    Seen51.QuickRep1SrartPrnt('4');
    Seen51.Free; }
  end;
end;

procedure TTong40.Print_53_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_31.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen52, Seen52);
    Seen52.QuickRep1SrartPrnt('1');
    Seen52.Free; }
  end;
end;

procedure TTong40.Print_53_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_32.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen52, Seen52);
    Seen52.QuickRep1SrartPrnt('2');
    Seen52.Free; }
  end;
end;

procedure TTong40.Print_54_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_41.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen52, Seen52);
    Seen52.QuickRep1SrartPrnt('3');
    Seen52.Free; }
  end;
end;

procedure TTong40.Print_54_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_42.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen52, Seen52);
    Seen52.QuickRep1SrartPrnt('4');
    Seen52.Free; }
  end;
end;

procedure TTong40.Print_55_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_51.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen53, Seen53);
    Seen53.QuickRep1SrartPrnt('1');
    Seen53.Free; }
  end;
end;

procedure TTong40.Print_55_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_52.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen54, Seen54);
    Seen54.QuickRep1SrartPrnt('1');
    Seen54.Free; }
  end;
end;

procedure TTong40.Print_55_03(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_53.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo55_1.Edit101.Text+' - '+Sobo55_1.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen53, Seen53);
    Seen53.QuickRep1SrartPrnt('1');
    Seen53.Free; }
  end;
end;

procedure TTong40.Print_55_04(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_54.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo55_1.Edit101.Text+' - '+Sobo55_1.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen53, Seen53);
    Seen53.QuickRep1SrartPrnt('1');
    Seen53.Free; }
  end;
end;

procedure TTong40.Print_56_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_61.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo56.Edit101.Text+' - '+Sobo56.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_56_02(Sender: TObject);
var SearchRec : TSearchRec;
    ff1,ff2: Integer;
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    ff1 := FindFirst( GetExecPath + 'Report\Report_5_62.frf', faAnyFile, SearchRec);
    ff2 := FindFirst( GetExecPath + 'Report\Report_5_63.frf', faAnyFile, SearchRec);

    if(ff2 = 0)then begin
      With Tong60.frReport00_00 do begin
        Clear;
        LoadFromFile(GetExecPath + 'Report\Report_5_63.frf');
        FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
        FindObject('Memo02').Memo.Text:=Sobo56.Edit101.Text+' - '+Sobo56.Edit102.Text;
        ShowReport;
      end;
    end else begin
      With Tong60.frReport00_00 do begin
        Clear;
        LoadFromFile(GetExecPath + 'Report\Report_5_62.frf');
        FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
        FindObject('Memo02').Memo.Text:=Sobo56.Edit101.Text+' - '+Sobo56.Edit102.Text;
        ShowReport;
      end;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_57_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_71.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo57.Edit101.Text+' - '+Sobo57.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_57_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_72.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo57.Edit101.Text+' - '+Sobo57.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_58_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_81.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo58.Edit101.Text+' - '+Sobo58.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_58_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_82.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo58.Edit101.Text+' - '+Sobo58.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_59_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_63.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo56.Edit101.Text+' - '+Sobo56.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_59_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_5_64.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=Sobo56.Edit101.Text+' - '+Sobo56.Edit102.Text;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;

procedure TTong40.Print_59_11(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_46.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen52, Seen52);
    Seen52.QuickRep1SrartPrnt('1');
    Seen52.Free; }
  end;
end;

procedure TTong40.Print_59_12(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_2_46.frf');
      FindObject('Memo91').Memo.Text:=nSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=nSqry.FieldByName('Gdate').AsString;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    //ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen52, Seen52);
    Seen52.QuickRep1SrartPrnt('1');
    Seen52.Free; }
  end;
end;

procedure TTong40.Print_50_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_50_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_61_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_11.frf');
      FindObject('Memo91').Memo.Text:=Sobo61.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo61.Edit101.Text+' - '+Sobo61.Edit102.Text;
      FindObject('Memo03').Memo.Text:='도  서  명 :';
      FindObject('Memo04').Memo.Text:=Sobo61.Edit104.Text+' - '+Sobo61.Edit106.Text;

      if Sobo61.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo61.DBGrid101.Columns.Items[5].Title.Caption ='폐기수량' Then begin
        FindObject('Memo16').Memo.Text:='폐기수량';
        FindObject('Memo26').Memo.Text:='[Gpqut]';
        FindObject('Memo36').Memo.Text:='[Sum(Gpqut)]';
        FindObject('Memo46').Memo.Text:='[Sum(Gpqut)]';
      end else begin
        FindObject('Memo16').Memo.Text:='변경수량';
        FindObject('Memo26').Memo.Text:='[Gpsum]';
        FindObject('Memo36').Memo.Text:='[Sum(Gpsum)]';
        FindObject('Memo46').Memo.Text:='[Sum(Gpsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen61, Seen61);
    Seen61.QuickRep1SrartPrnt('1');
    Seen61.Free; }
  end;
end;

procedure TTong40.Print_61_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_12.frf');
      FindObject('Memo91').Memo.Text:=Sobo61.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo61.Edit101.Text+' - '+Sobo61.Edit102.Text;
      FindObject('Memo03').Memo.Text:='도  서  명 :';
      FindObject('Memo04').Memo.Text:=Sobo61.Edit104.Text+' - '+Sobo61.Edit106.Text;
      if T00=0 Then
      FindObject('Memo04').Memo.Text:=Sobo61.Button101.Caption;

      if(Sobo61.Edit106.Text='')and(Sobo61.Button101.Caption='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen61, Seen61);
    Seen61.QuickRep1SrartPrnt('2');
    Seen61.Free; }
  end;
end;

procedure TTong40.Print_62_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_21.frf');
      FindObject('Memo91').Memo.Text:=Sobo62.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo62.Edit101.Text+' - '+Sobo62.Edit102.Text;
      FindObject('Memo03').Memo.Text:='거래처명 :';
      FindObject('Memo04').Memo.Text:=Sobo62.Edit104.Text+' - '+Sobo62.Edit106.Text;

      if Sobo62.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo62.DBGrid101.Columns.Items[3].Title.Caption ='증정수량' Then begin
        FindObject('Memo14').Memo.Text:='증정수량';
        FindObject('Memo24').Memo.Text:='[Gjqut]';
        FindObject('Memo34').Memo.Text:='[Sum(Gjqut)]';
        FindObject('Memo44').Memo.Text:='[Sum(Gjqut)]';
      end else begin
        FindObject('Memo14').Memo.Text:='장부차액';
        FindObject('Memo24').Memo.Text:='[Gjsum]';
        FindObject('Memo34').Memo.Text:='[Sum(Gjsum)]';
        FindObject('Memo44').Memo.Text:='[Sum(Gjsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen62, Seen62);
    Seen62.QuickRep1SrartPrnt('1');
    Seen62.Free; }
  end;
end;

procedure TTong40.Print_62_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_22.frf');
      FindObject('Memo91').Memo.Text:=Sobo62.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo62.Edit101.Text+' - '+Sobo62.Edit102.Text;
      FindObject('Memo03').Memo.Text:='거래처명 :';
      FindObject('Memo04').Memo.Text:=Sobo62.Edit104.Text+' - '+Sobo62.Edit106.Text;
      if T00=0 Then
      FindObject('Memo04').Memo.Text:=Sobo62.Button101.Caption;

      if(Sobo62.Edit106.Text='')and(Sobo62.Button101.Caption='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen62, Seen62);
    Seen62.QuickRep1SrartPrnt('2');
    Seen62.Free; }
  end;
end;

procedure TTong40.Print_63_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_91.frf');
      FindObject('Memo91').Memo.Text:=Sobo63.Edit106.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo63.Edit101.Text+' - '+Sobo63.Edit102.Text;
      FindObject('Memo03').Memo.Text:='출판사명 :';
      FindObject('Memo04').Memo.Text:=Sobo63.Edit104.Text+' - '+Sobo63.Edit106.Text;

      if Sobo63.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen63, Seen63);
    Seen63.QuickRep1SrartPrnt('1');
    Seen63.Free; }
  end;
end;

procedure TTong40.Print_63_02(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_93.frf');
      FindObject('Memo91').Memo.Text:=Sobo63.Edit106.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo63.Edit101.Text+' - '+Sobo63.Edit102.Text;
      FindObject('Memo03').Memo.Text:='출판사명 :';
      FindObject('Memo04').Memo.Text:=Sobo63.Edit104.Text+' - '+Sobo63.Edit106.Text;

      if Sobo63.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen64, Seen64);
    Seen64.QuickRep1SrartPrnt('1');
    Seen64.Free; }
  end;
end;

procedure TTong40.Print_64_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_92.frf');
      FindObject('Memo91').Memo.Text:=Sobo64.Edit106.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo64.Edit101.Text+' - '+Sobo64.Edit102.Text;
      FindObject('Memo03').Memo.Text:='출판사명 :';
      FindObject('Memo04').Memo.Text:=Sobo64.Edit104.Text+' - '+Sobo64.Edit106.Text;

      if Sobo64.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen63, Seen63);
    Seen63.QuickRep1SrartPrnt('2');
    Seen63.Free; }
  end;
end;

procedure TTong40.Print_64_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
{   oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_42.frf');
      FindObject('Memo91').Memo.Text:=Sobo64.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo64.Edit101.Text+' - '+Sobo64.Edit102.Text;
      FindObject('Memo03').Memo.Text:='거래처명 :';
      FindObject('Memo04').Memo.Text:=Sobo64.Edit104.Text+' - '+Sobo64.Edit106.Text;

      if T00=0 Then
      FindObject('Memo02').Memo.Text:=Sobo64.Button101.Caption;

      if(Sobo64.Edit106.Text='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls; }
  { Application.CreateForm(TSeen64, Seen64);
    Seen64.QuickRep1SrartPrnt('2');
    Seen64.Free; }
  end;
end;

procedure TTong40.Print_65_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_51.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo65.Edit101.Text+' - '+Sobo65.Edit102.Text;
      FindObject('Memo03').Memo.Text:='출판사명 :';
      FindObject('Memo04').Memo.Text:=Sobo65.Edit104.Text+' - '+Sobo65.Edit106.Text;

      if(Sobo65.Edit106.Text='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen65, Seen65);
    Seen65.QuickRep1SrartPrnt('2');
    Seen65.Free; }
  end;
end;

procedure TTong40.Print_65_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_52.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo65.Edit101.Text+' - '+Sobo65.Edit102.Text;

      if Sobo65.Button101.Caption<>'' Then
      FindObject('Memo04').Memo.Text:=Sobo65.Button101.Caption;

      if(Sobo65.Button101.Caption='')and(Sobo65.Edit106.Text='')Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen65, Seen65);
    Seen65.QuickRep1SrartPrnt('1');
    Seen65.Free; }
  end;
end;

procedure TTong40.Print_66_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_61.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo66.Edit101.Text+' - '+Sobo66.Edit102.Text;
      FindObject('Memo03').Memo.Text:='출판사명 :';
      FindObject('Memo04').Memo.Text:=Sobo66.Edit104.Text+' - '+Sobo66.Edit106.Text;

      if(Sobo66.Edit106.Text='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen66, Seen66);
    Seen66.QuickRep1SrartPrnt('2');
    Seen66.Free; }
  end;
end;

procedure TTong40.Print_66_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_62.frf');
      FindObject('Memo91').Memo.Text:=mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo66.Edit101.Text+' - '+Sobo66.Edit102.Text;

      if Sobo66.Button101.Caption<>'' Then
      FindObject('Memo04').Memo.Text:=Sobo66.Button101.Caption;

      if(Sobo66.Button101.Caption='')and(Sobo66.Edit106.Text='')Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen66, Seen66);
    Seen66.QuickRep1SrartPrnt('1');
    Seen66.Free; }
  end;
end;

procedure TTong40.Print_67_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_71.frf');
      FindObject('Memo91').Memo.Text:=Sobo67.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo67.Edit101.Text+' - '+Sobo67.Edit102.Text;
      FindObject('Memo03').Memo.Text:='도  서  명 :';
      FindObject('Memo04').Memo.Text:=Sobo67.Edit104.Text+' - '+Sobo67.Edit106.Text;

      if Sobo67.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo67.DBGrid101.Columns.Items[6].Title.Caption ='폐기수량' Then begin
        FindObject('Memo17').Memo.Text:='폐기수량';
        FindObject('Memo27').Memo.Text:='[Gpqut]';
        FindObject('Memo37').Memo.Text:='[Sum(Gpqut)]';
        FindObject('Memo47').Memo.Text:='[Sum(Gpqut)]';
      end else begin
        FindObject('Memo17').Memo.Text:='변경수량';
        FindObject('Memo27').Memo.Text:='[Gpsum]';
        FindObject('Memo37').Memo.Text:='[Sum(Gpsum)]';
        FindObject('Memo47').Memo.Text:='[Sum(Gpsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen67, Seen67);
    Seen67.QuickRep1SrartPrnt('1');
    Seen67.Free; }
  end;
end;

procedure TTong40.Print_67_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_72.frf');
      FindObject('Memo91').Memo.Text:=Sobo67.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo67.Edit101.Text+' - '+Sobo67.Edit102.Text;
      FindObject('Memo03').Memo.Text:='도  서  명 :';
      FindObject('Memo04').Memo.Text:=Sobo67.Edit104.Text+' - '+Sobo67.Edit106.Text;
      if T00=0 Then
      FindObject('Memo04').Memo.Text:=Sobo67.Button101.Caption;

      if(Sobo67.Edit106.Text='')and(Sobo67.Button101.Caption='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo67.DBGrid101.Columns.Items[6].Title.Caption ='폐기수량' Then begin
        FindObject('Memo17').Memo.Text:='폐기수량';
        FindObject('Memo27').Memo.Text:='[Gpqut]';
        FindObject('Memo37').Memo.Text:='[Sum(Gpqut)]';
        FindObject('Memo47').Memo.Text:='[Sum(Gpqut)]';
      end else begin
        FindObject('Memo17').Memo.Text:='변경수량';
        FindObject('Memo27').Memo.Text:='[Gpsum]';
        FindObject('Memo37').Memo.Text:='[Sum(Gpsum)]';
        FindObject('Memo47').Memo.Text:='[Sum(Gpsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen67, Seen67);
    Seen67.QuickRep1SrartPrnt('2');
    Seen67.Free; }
  end;
end;

procedure TTong40.Print_68_01(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_81.frf');
      FindObject('Memo91').Memo.Text:=Sobo68.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo68.Edit101.Text+' - '+Sobo68.Edit102.Text;
      FindObject('Memo03').Memo.Text:='거래처명 :';
      FindObject('Memo04').Memo.Text:=Sobo68.Edit104.Text+' - '+Sobo68.Edit106.Text;

      if Sobo68.Edit106.Text='' Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo68.DBGrid101.Columns.Items[4].Title.Caption ='증정수량' Then begin
        FindObject('Memo15').Memo.Text:='증정수량';
        FindObject('Memo25').Memo.Text:='[Gjqut]';
        FindObject('Memo35').Memo.Text:='[Sum(Gjqut)]';
        FindObject('Memo45').Memo.Text:='[Sum(Gjqut)]';
      end else begin
        FindObject('Memo15').Memo.Text:='장부차액';
        FindObject('Memo25').Memo.Text:='[Gjsum]';
        FindObject('Memo35').Memo.Text:='[Sum(Gjsum)]';
        FindObject('Memo45').Memo.Text:='[Sum(Gjsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen68, Seen68);
    Seen68.QuickRep1SrartPrnt('1');
    Seen68.Free; }
  end;
end;

procedure TTong40.Print_68_02(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    oSqry:=mSqry;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_6_82.frf');
      FindObject('Memo91').Memo.Text:=Sobo68.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Sobo68.Edit101.Text+' - '+Sobo68.Edit102.Text;
      FindObject('Memo03').Memo.Text:='거래처명 :';
      FindObject('Memo04').Memo.Text:=Sobo68.Edit104.Text+' - '+Sobo68.Edit106.Text;
      if T00=0 Then
      FindObject('Memo04').Memo.Text:=Sobo68.Button101.Caption;

      if(Sobo68.Edit106.Text='')and(Sobo68.Button101.Caption='') Then begin
        FindObject('Memo03').Memo.Text:='';
        FindObject('Memo04').Memo.Text:='';
      end;
      if Sobo68.DBGrid101.Columns.Items[4].Title.Caption ='증정수량' Then begin
        FindObject('Memo15').Memo.Text:='증정수량';
        FindObject('Memo25').Memo.Text:='[Gjqut]';
        FindObject('Memo35').Memo.Text:='[Sum(Gjqut)]';
        FindObject('Memo45').Memo.Text:='[Sum(Gjqut)]';
      end else begin
        FindObject('Memo15').Memo.Text:='장부차액';
        FindObject('Memo25').Memo.Text:='[Gjsum]';
        FindObject('Memo35').Memo.Text:='[Sum(Gjsum)]';
        FindObject('Memo45').Memo.Text:='[Sum(Gjsum)]';
      end;
      ShowReport;
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  { Application.CreateForm(TSeen68, Seen68);
    Seen68.QuickRep1SrartPrnt('2');
    Seen68.Free; }
  end;
end;

procedure TTong40.Print_69_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_69_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_60_01(Sender: TObject);
begin
//
end;

procedure TTong40.Print_60_02(Sender: TObject);
begin
//
end;

procedure TTong40.Print_99_01(Sender: TObject);
var SearchRec : TSearchRec;
    ff1,ff2: Integer;
begin
  ff1 := FindFirst( GetExecPath + 'Report\Report_3_91.frf', faAnyFile, SearchRec);
  ff2 := FindFirst( GetExecPath + 'Report\Report_3_92.frf', faAnyFile, SearchRec);

if(ff1 = 0)then begin
  if Base10.T4_Sub81.Active=True Then begin
    oSqry:=Base10.T4_Sub81;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo99.Edit101.Text);
      FindObject('Memo71').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='지방';
      if Sobo99.RadioButton6.Checked=True Then begin
      FindObject('Memo71').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='시내';
      end else
      if Sobo99.RadioButton7.Checked=True Then begin
      FindObject('Memo71').Memo.Text:='지방';
      FindObject('Memo72').Memo.Text:='지방';
      end;

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end else
if(ff2 = 0)then begin
  if Sobo99.T3_Sub91.Active=True Then begin
    oSqry:=Sobo99.T3_Sub91;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_92.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo04').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo99.Edit101.Text);

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;
end;

procedure TTong40.Print_99_02(Sender: TObject);
var SearchRec : TSearchRec;
    ff1,ff2: Integer;
begin
  ff1 := FindFirst( GetExecPath + 'Report\Report_3_91.frf', faAnyFile, SearchRec);
  ff2 := FindFirst( GetExecPath + 'Report\Report_3_92.frf', faAnyFile, SearchRec);

if(ff1 = 0)then begin
  if Base10.T4_Sub81.Active=True Then begin
    oSqry:=Base10.T4_Sub81;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_91.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);
      FindObject('Memo44').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='지방';
      if Sobo39.RadioButton6.Checked=True Then begin
      FindObject('Memo44').Memo.Text:='시내';
      FindObject('Memo72').Memo.Text:='시내';
      end else
      if Sobo39.RadioButton7.Checked=True Then begin
      FindObject('Memo44').Memo.Text:='지방';
      FindObject('Memo72').Memo.Text:='지방';
      end;

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end else
if(ff2 = 0)then begin
  if Sobo39.T3_Sub91.Active=True Then begin
    oSqry:=Sobo39.T3_Sub91;
    Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_92.frf');
      FindObject('Memo91').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo04').Memo.Text:=mSqry.FieldByName('Hname').AsString;
      FindObject('Memo02').Memo.Text:=AutoFrx(Sobo39.Edit101.Text);

    //ShowReport;
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

    oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
end;
end;

procedure TTong40._Gg_Magn_(Str:String);
begin
  lSqry:=Base10.T1_Sub92;
  Base10.OpenData(lSqry);

  Sqlen := 'Select * From Gg_Magn Where Gu='+#39+Str+#39;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(lSqry)
  else ShowMessage(E_Open);
end;

procedure TTong40._Sv_Gsum_(_S1_Ssub,_H1_Ssub,_Sv_Gsum: String);
var St1: String;
begin
  sSqry:=Base10.T3_Sub91;

  Base10.OpenExit(sSqry);
  Base10.OpenShow(sSqry);

  {-Sv_Gsum-}
  Sqlen :='Select Scode,Gcode,'+
          'Sum(Goqut)as Goqut,Sum(Gjqut)as Gjqut,Sum(Gbqut)as Gbqut,'+
          'Sum(Gosum)as Gosum,Sum(Gjsum)as Gjsum,Sum(Gbsum)as Gbsum,'+
          'Sum(Gsqut)as Gsqut,Sum(Gsusu)as Gsusu,Sum(Gssum)as Gssum '+
          'From Sv_Gsum Where '+D_Select+_Sv_Gsum+' Group By Scode,Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    if _S1_Ssub='0' then
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 2,List1],0)+StrToIntDef(SGrid.Cells[ 3,List1],0)+StrToIntDef(SGrid.Cells[ 4,List1],0)+
    StrToIntDef(SGrid.Cells[ 5,List1],0)+StrToIntDef(SGrid.Cells[ 6,List1],0)+StrToIntDef(SGrid.Cells[ 7,List1],0)+
    StrToIntDef(SGrid.Cells[ 8,List1],0)+StrToIntDef(SGrid.Cells[ 9,List1],0)+StrToIntDef(SGrid.Cells[10,List1],0);
    if _S1_Ssub='1' then
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 2,List1],0)+StrToIntDef(SGrid.Cells[ 3,List1],0)+StrToIntDef(SGrid.Cells[ 4,List1],0)+
    StrToIntDef(SGrid.Cells[ 8,List1],0)+StrToIntDef(SGrid.Cells[ 9,List1],0)+StrToIntDef(SGrid.Cells[10,List1],0);
    if _S1_Ssub='2' then
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 5,List1],0)+StrToIntDef(SGrid.Cells[ 6,List1],0)+StrToIntDef(SGrid.Cells[ 7,List1],0)+
    StrToIntDef(SGrid.Cells[ 8,List1],0)+StrToIntDef(SGrid.Cells[ 9,List1],0)+StrToIntDef(SGrid.Cells[10,List1],0);
    sSqry.Post;
  end;

  {-H1_Ssub-}
  Sqlen :='Select Ocode,Gubun,Sum(Gssum)as Gssum '+
          'From H1_Ssub Where '+D_Select+_H1_Ssub+' Group By Ocode,Gubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    if SGrid.Cells[ 1,List1]='입금' Then
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0)
    else
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat-StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;
end;

procedure TTong40._Sv_Chng_(_S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng: String);
var St1: String;
begin
  sSqry:=Base10.T3_Sub91;

  Base10.OpenExit(sSqry);
  Base10.OpenShow(sSqry);

  {-Sv_Chng-}
  Sqlen :='Select Gcode,Sum(Gssum)as Gssum,Sum(Gsusu)as Gsusu '+
          'From Sv_Chng Where '+D_Select+_Sv_Chng+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 1,List1],0)-StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;

  {-S1_Ssub-}
  Sqlen :='Select Gcode,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
          'From S1_Ssub Where '+D_Select+_S1_Ssub+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;

  {-H1_Ssub-}
  Sqlen :=_H1_Ssub+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat-
    StrToIntDef(SGrid.Cells[ 2,List1],0)+StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.Post;
  end;

  {-Sg_Gsum-}
  Sqlen :='Select Gcode,Sum(Gbsum)as Gbsum '+
          'From Sg_Gsum Where '+D_Select+_Sg_Gsum+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 1,List1],0);
    sSqry.Post;
  end;
end;

procedure TTong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng: String);
var St1,St2,St3,St4: String;
begin
  sSqry:=Base10.T3_Sub91;

  Base10.OpenExit(sSqry);
  Base10.OpenShow(sSqry);

  {-Sv_Ghng-}
  Sqlen :='Select Gcode,Sum(Gsusu)as Gsusu,Sum(Gsqut)as Gsqut,Sum(Obqut)as Obqut,Sum(Obsum)as Obsum '+
          'From Sv_Ghng Where '+D_Select+_Sv_Ghng+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 1,List1],0)-StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.FieldByName('Gbqut').AsFloat:=sSqry.FieldByName('Gbqut').AsFloat+
    StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.Post;
  end;

  {-S1_Ssub-}
  Sqlen :='Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut '+
          'From S1_Ssub Where '+D_Select+_S1_Ssub+
          ' and '+'('+'Bdate'+' is '+'null'+')'+
          ' Group By Bcode,Scode,Gubun,Pubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St2:=SGrid.Cells[ 1,List1];
    if St2='Y' Then begin
      if St4='반품' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
        sSqry.FieldByName('Gbqut').AsFloat:=
        sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end else
      if St3='입고' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
      end;
    end else begin
      if St4='증정' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end else
      if St3='출고' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end else
      if St3='폐기' Then begin
        if(St4='비품')Then begin
          sSqry.FieldByName('Gbqut').AsFloat:=
          sSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
        end else begin
          sSqry.FieldByName('GsumX').AsFloat:=
          sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
        end;
          sSqry.FieldByName('Gpqut').AsFloat:=
          sSqry.FieldByName('Gpqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end else
      if(St4='비품')or(St4='폐기')Then begin
      { if St2='Z' Then
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0); }
        if(St4='비품')Then begin
          if St2='X' Then
          sSqry.FieldByName('Gbqut').AsFloat:=
          sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
          if St2='Z' Then
          sSqry.FieldByName('Gbqut').AsFloat:=
          sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
        end;
        if(St4='폐기')Then begin
          if St2='Z' Then
          sSqry.FieldByName('Gbqut').AsFloat:=
          sSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
        //if St2='Z' Then
          sSqry.FieldByName('Gpqut').AsFloat:=
          sSqry.FieldByName('Gpqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
        end;
      end else
      if St3='반품' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end;
    end;
    sSqry.Post;
  end;


  //---------------유통반품재고-----------------//
  Translate(_S1_Ssub, 'Gdate', 'Bdate');

  {-S1_Ssub-}
  Sqlen :='Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut '+
          'From S1_Ssub Where '+D_Select+_S1_Ssub+
          ' Group By Bcode,Scode,Gubun,Pubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St2:=SGrid.Cells[ 1,List1];
    if St2='Y' Then begin
      if St4='반품' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
        sSqry.FieldByName('Gbqut').AsFloat:=
        sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end else
      if St3='입고' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
      end;
    end else begin
      if St4='증정' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end else
      if St3='출고' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end else
      if(St4='비품')or(St4='폐기')Then begin
      { if St2='Z' Then
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0); }
        if(St4='비품')Then begin
          if St2='X' Then
          sSqry.FieldByName('Gbqut').AsFloat:=
          sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
          if St2='Z' Then
          sSqry.FieldByName('Gbqut').AsFloat:=
          sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
        end;
        if(St4='폐기')Then begin
          if St2='Z' Then
          sSqry.FieldByName('Gbqut').AsFloat:=
          sSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
        //if St2='Z' Then
          sSqry.FieldByName('Gpqut').AsFloat:=
          sSqry.FieldByName('Gpqut').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
        end;
      end else
      if St3='반품' Then begin
        sSqry.FieldByName('GsumX').AsFloat:=
        sSqry.FieldByName('GsumX').AsFloat-StrToIntDef(SGrid.Cells[ 4,List1],0);
      end;
    end;
    sSqry.Post;
  end;
  //---------------유통반품재고-----------------//


  {-Sg_Csum-}
  Sqlen :='Select Scode,Gcode,Sum(Gbsum)as Gbsum '+
          'From Sg_Csum Where '+D_Select+_Sg_Csum+' Group By Scode,Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 1,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    if SGrid.Cells[ 0,List1]='D' then
    sSqry.FieldByName('Gbqut').AsFloat:=
    sSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0)
    else
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;
end;

procedure TTong40._Sb_Ghng_(_Sb_Csum,_Sv_Ghng: String);
var St1,St2,St3,St4: String;
begin
  sSqry:=Base10.T3_Sub91;

  Base10.OpenExit(sSqry);
  Base10.OpenShow(sSqry);

  {-Sv_Ghng-}
  Sqlen :='Select Gcode,Sum(Gsusu)as Gsusu,Sum(Gsqut)as Gsqut,Sum(Obqut)as Obqut,Sum(Obsum)as Obsum '+
          'From Sv_Ghng Where '+D_Select+_Sv_Ghng+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.FieldByName('Gbqut').AsFloat:=sSqry.FieldByName('Gbqut').AsFloat+
    StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.Post;
  end;

  {-Sb_Csum-}
  Sqlen :='Select Gcode,Gubun,Sum(Gsqut)as Gsqut '+
          'From Sb_Csum Where '+D_Select+_Sb_Csum+' Group By Gcode,Gubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    if SGrid.Cells[ 1,List1]='반품' then begin
      sSqry.FieldByName('Gbqut').AsFloat:=
      sSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
    end else
    if SGrid.Cells[ 1,List1]='입고' then begin
      sSqry.FieldByName('GsumX').AsFloat:=
      sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
      sSqry.FieldByName('Gbqut').AsFloat:=
      sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 2,List1],0);
    end else
    if SGrid.Cells[ 1,List1]='재생' then begin
      sSqry.FieldByName('GsumX').AsFloat:=
      sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
      sSqry.FieldByName('Gbqut').AsFloat:=
      sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 2,List1],0);
    end else
    if SGrid.Cells[ 1,List1]='폐기' then begin
      sSqry.FieldByName('Gbqut').AsFloat:=
      sSqry.FieldByName('Gbqut').AsFloat-StrToIntDef(SGrid.Cells[ 2,List1],0);
    end;
    sSqry.Post;
  end;
end;

procedure TTong40.SetTring01(Str1,Str2,Str3,Str4,Str5,Str6: String);
var St1,St2,St3,St4,St5,St6,St7: String;
    _S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng: String;
begin
{ Str1:'X', Str2:Date1, Str3:Date2, Str4:Code1, Str5:Code2 }

  sSqry:=Base10.T3_Sub91;

  Base10.OpenExit(sSqry);
  Base10.OpenShow(sSqry);

  if Str1='X' Then St2:='X';
  if Str1='Y' Then St2:='Y';
  if Str1='Z' Then St2:='Z';

  St3:=''; St4:='';
  if Str4=Str5 Then begin
    if St2='X' Then begin
    Seek10.FilterSing(Str5,Str6);
    While Seek10.Query1.EOF=False do begin
      St3:=St3+St4+'Gcode'+' = '+#39+Seek10.Query1Gcode.AsString+#39;
      St4:=' Or ';
      Seek10.Query1.Next;
    end; end;
    if St2='Y' Then begin
    Seek20.FilterSing(Str5,Str6);
    While Seek20.Query1.EOF=False do begin
      St3:=St3+St4+'Gcode'+' = '+#39+Seek20.Query1Gcode.AsString+#39;
      St4:=' Or ';
      Seek20.Query1.Next;
    end; end;
    if St2='Z' Then begin
    Seek50.FilterSing(Str5,Str6);
    While Seek50.Query1.EOF=False do begin
      St3:=St3+St4+'Gcode'+' = '+#39+Seek50.Query1Gcode.AsString+#39;
      St4:=' Or ';
      Seek50.Query1.Next;
    end; end;
  end else St3:='Gcode'+' ='+#39+Str4+#39;

  St3:='('+St3+')'+' and '+
       'Hcode'+'='+#39+Str6+#39;

  {-Sv_Chng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Chng '+
          'Where '+D_Select+
          'Gdate < '+#39+Str2+#39+' and  '+
          'Hcode = '+#39+Str6+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Str2+#39+' and '+
            'Scode'+' ='+#39+St2+#39+' and '+'('+St3+')';
  _Sg_Gsum:=_S1_Ssub;
  _Sv_Chng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Scode'+' ='+#39+St2+#39+' and '+'('+St3+')';
  if St2='Y' then begin
    St5:='Gubun='+#39+'출금'+#39+' and ';
    St6:='Gubun='+#39+'입금'+#39+' and ';
  end else begin
    St5:='Gubun='+#39+'입금'+#39+' and ';
    St6:='Gubun='+#39+'출금'+#39+' and ';
  end;
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St5+D_Select+_S1_Ssub+' ) as Gosum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St6+D_Select+_S1_Ssub+' ) as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+D_Select+_S1_Ssub;
  _H1_Ssub:= St4;

  if ePrnt='2' then begin
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+' Sum(if('+St5+D_Select+_S1_Ssub+',gssum,0))as Gosum,';
  St4:=St4+' Sum(if('+St6+D_Select+_S1_Ssub+',gssum,0))as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+D_Select+_S1_Ssub;
  _H1_Ssub:= St4;
  end;

  {-Sv_Chng-}
  Sqlen :='Select Gcode,'+
          'Sum(Gssum)as Gssum,Sum(Gsusu)as Gsusu, '+
          'Sum(Goqut)as Goqut,Sum(Gosum)as Gosum, '+
          'Sum(Gbqut)as Gbqut,Sum(Gbsum)as Gbsum  '+
          'From Sv_Chng Where '+D_Select+_Sv_Chng+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('Goqut').AsFloat:=
    sSqry.FieldByName('Goqut').AsFloat+StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.FieldByName('Gosum').AsFloat:=
    sSqry.FieldByName('Gosum').AsFloat+StrToIntDef(SGrid.Cells[ 4,List1],0);
    sSqry.FieldByName('Gbqut').AsFloat:=
    sSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 5,List1],0);
    sSqry.FieldByName('Gbsum').AsFloat:=
    sSqry.FieldByName('Gbsum').AsFloat+StrToIntDef(SGrid.Cells[ 6,List1],0);
    sSqry.FieldByName('Gsusu').AsFloat:=
    sSqry.FieldByName('Gsusu').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+
    StrToIntDef(SGrid.Cells[ 1,List1],0)-StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;

  {-S1_Ssub-}
  Sqlen :='Select Gcode,Gubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
          'From S1_Ssub Where '+D_Select+_S1_Ssub+' Group By Gcode,Gubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    if(SGrid.Cells[ 1,List1]='출고')or(SGrid.Cells[ 1,List1]='입고')then begin
    sSqry.FieldByName('Goqut').AsFloat:=
    sSqry.FieldByName('Goqut').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.FieldByName('Gosum').AsFloat:=
    sSqry.FieldByName('Gosum').AsFloat+StrToIntDef(SGrid.Cells[ 3,List1],0);
    end;
    if SGrid.Cells[ 1,List1]='반품' then begin
    sSqry.FieldByName('Gbqut').AsFloat:=
    sSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.FieldByName('Gbsum').AsFloat:=
    sSqry.FieldByName('Gbsum').AsFloat+StrToIntDef(SGrid.Cells[ 3,List1],0);
    end;
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.Post;
  end;

  {-H1_Ssub-}
  Sqlen :=_H1_Ssub+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('Gsusu').AsFloat:=sSqry.FieldByName('Gsusu').AsFloat+
    StrToIntDef(SGrid.Cells[ 2,List1],0)-StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat-
    StrToIntDef(SGrid.Cells[ 2,List1],0)+StrToIntDef(SGrid.Cells[ 3,List1],0);
    sSqry.Post;
  end;

  {-Sg_Gsum-}
  Sqlen :='Select Gcode,Sum(Gbsum)as Gbsum '+
          'From Sg_Gsum Where '+D_Select+_Sg_Gsum+' Group By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St1:=SGrid.Cells[ 0,List1];
    if sSqry.Locate('Gcode',St1,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St1;
    end;
    sSqry.Edit;
    sSqry.FieldByName('GsumX').AsFloat:=
    sSqry.FieldByName('GsumX').AsFloat+StrToIntDef(SGrid.Cells[ 1,List1],0);
    sSqry.Post;
  end;
end;

procedure TTong40.SetTring02(Str1,Str2,Str3,Str4,Str5,Str6: String);
var St1,St2,St3,St4,St5: String;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin
{ Str1:'A', Str2:Date1, Str3:Date2, Str4:Code1, Str5:Code2 }

  sSqry:=Base10.T3_Sub91;

  Base10.OpenExit(sSqry);
  Base10.OpenShow(sSqry);

  {-Sv_Ghng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
          'Where '+D_Select+
          'Gdate < '+#39+Str2+#39+' and  '+
          'Hcode = '+#39+Str6+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Str2+#39+' and '+
            'Ocode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+Str6+#39;
  _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Str2+#39+' and '+
            'Scode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+Str6+#39;
  _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Scode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+Str6+#39;
  if Str4<>'' then begin
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Str2+#39+' and '+
            'Bcode'+'= '+#39+Str4+#39+' and '+
            'Ocode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+Str6+#39;
  _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Str2+#39+' and '+
            'Gcode'+'= '+#39+Str4+#39+' and '+
            'Scode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+Str6+#39;
  _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Gcode'+'= '+#39+Str4+#39+' and '+
            'Scode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+Str6+#39;
  end;

  {-Sv_Ghng-}
  Sqlen :=
  'Select Gcode,Gsusu,Gsqut '+
  'From Sv_Ghng Where '+D_Select+_Sv_Ghng+
  'Order By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St3:=SGrid.Cells[ 0,List1];

    if sSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St3;
    end;

    sSqry.Edit;
    sSqry.FieldByName('GsumY').AsFloat:=
    sSqry.FieldByName('GsumY').AsFloat+StrToIntDef(SGrid.Cells[ 1,List1],0)-StrToIntDef(SGrid.Cells[ 2,List1],0);
    sSqry.Post;
  end;


  {-S1_Ssub-}
  Sqlen :=
  'Select Bcode,Scode,Gubun,Pubun, '+
  'Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+D_Select+_S1_Ssub+
  'Group By Bcode,Scode,Gubun,Pubun ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 5,List1],0);

    St3:=SGrid.Cells[ 0,List1];

    if sSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St3;
    end;

    sSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    if St5='Y' Then begin
      if St3='입고' Then begin
        sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat+T01;
      end else
      if St3='반품' Then begin
        sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat+T01;
      end;
    end else begin
      if St4='증정' Then begin
        sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat-T01;
      end else
      if St3='출고' Then begin
        sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat-T01;
      end else
      if St3='폐기' Then begin
        if(St4='비품')Then begin
        end else begin
        sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat+T01;
        end;
      end else
      if(St4='비품')or(St4='폐기')Then begin
      //if St5='X' Then
      //sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat-T01;
      //if St5='Z' Then
      //sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat+T01;
      end else
      if St3='반품' Then begin
        sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat-T01;
      end;
    end;
    sSqry.Post;
  end;

  {-Sg_Csum-}
  Sqlen :=
  'Select Scode,Gcode,Sum(Gbsum)as Gbsum '+
  'From Sg_Csum Where '+D_Select+_Sg_Csum+
  'Group By Gcode,Gdate ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 2,List1],0);

    St3:=SGrid.Cells[ 1,List1];

    if sSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      sSqry.Append;
      sSqry.FieldByName('Gcode').AsString:=St3;
    end;

    sSqry.Edit;
    if(SGrid.Cells[ 0,List1]='A')or(SGrid.Cells[ 0,List1]='B')then
    sSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumY').AsFloat+T01;
    sSqry.Post;
  end;
end;

procedure TTong40.SetTring11(Str1,Str2,Str3,Str4,Str5,Str6: String);
var St1,St2,St3,St4,St5,St6,St7: String;
    nSumX,nSumY: Double;
    _S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng: String;
begin
{ Str1:'X', Str2:Date1, Str3:Date2, Str4:Code1, Str5:Code2 }

  uSqry:=Base10.T3_Sub92;
  Refresh;
  Screen.Cursor:=crHourGlass;
  Base10.OpenShow(uSqry);

  if Str1='X' Then St2:='X';
  if Str1='Y' Then St2:='Y';
  if Str1='Z' Then St2:='Z';

  St3:=''; St4:='';
  if Str4=Str5 Then begin
    if St2='X' Then begin
    Seek10.FilterSing(Str5,Str6);
    While Seek10.Query1.EOF=False do begin
      St3:=St3+St4+'Gcode'+' = '+#39+Seek10.Query1Gcode.AsString+#39;
      St4:=' Or ';
      Seek10.Query1.Next;
    end; end;
    if St2='Y' Then begin
    Seek20.FilterSing(Str5,Str6);
    While Seek20.Query1.EOF=False do begin
      St3:=St3+St4+'Gcode'+' = '+#39+Seek20.Query1Gcode.AsString+#39;
      St4:=' Or ';
      Seek20.Query1.Next;
    end; end;
    if St2='Z' Then begin
    Seek50.FilterSing(Str5,Str6);
    While Seek50.Query1.EOF=False do begin
      St3:=St3+St4+'Gcode'+' = '+#39+Seek50.Query1Gcode.AsString+#39;
      St4:=' Or ';
      Seek50.Query1.Next;
    end; end;
  end else St3:='Gcode'+' ='+#39+Str4+#39;

  St3:='('+St3+')'+' and '+
       'Hcode'+'='+#39+Str6+#39;

  {-Sv_Chng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Chng '+
          'Where '+D_Select+
          'Gdate < '+#39+Str2+#39+' and  '+
          'Hcode = '+#39+Str6+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Str2+#39+' and '+
            'Scode'+' ='+#39+St2+#39+' and '+'('+St3+')';
  _Sg_Gsum:=_S1_Ssub;
  _Sv_Chng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Scode'+' ='+#39+St2+#39+' and '+'('+St3+')';
  if St2='Y' then begin
    St5:='Gubun='+#39+'출금'+#39+' and ';
    St6:='Gubun='+#39+'입금'+#39+' and ';
  end else begin
    St5:='Gubun='+#39+'입금'+#39+' and ';
    St6:='Gubun='+#39+'출금'+#39+' and ';
  end;
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St5+D_Select+_S1_Ssub+' ) as Gosum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St6+D_Select+_S1_Ssub+' ) as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+D_Select+_S1_Ssub;
  _H1_Ssub:= St4;

  if ePrnt='2' then begin
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+' Sum(if('+St5+D_Select+_S1_Ssub+',gssum,0))as Gosum,';
  St4:=St4+' Sum(if('+St6+D_Select+_S1_Ssub+',gssum,0))as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+D_Select+_S1_Ssub;
  _H1_Ssub:= St4;
  end;

  Tong40._Sv_Chng_(_S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng);

  St1:='Gdate'+'>='+#39+Str2+#39+' and '+
       'Gdate'+'<='+#39+Str3+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+'('+St3+')';

  {-S1_Ssub-}
  Sqlen :='Select Gdate,Gcode,Gubun,Jubun,Bcode,Gbigo,Gsqut,Gssum '+
          'From S1_Ssub Where '+D_Select+St1+' Order By Gdate,Jubun,Id ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 6,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 7,List1],0);

    St6:=SGrid.Cells[ 0,List1];
    St7:=SGrid.Cells[ 3,List1];

    if uSqry.Locate('Gdate;Jubun',VarArrayOf([St6,St7]),[loCaseInsensitive])=False then begin

      St7:=Base10.Seek_Code(SGrid.Cells[ 4,List1],'B',Str6);

      if SGrid.Cells[ 5,List1]<>'' Then
      St7:=Copy(St7+'('+SGrid.Cells[ 5,List1]+')',1,40);
      uSqry.Append;
      uSqry.FieldByName('Gdate').AsString:=St6;
      uSqry.FieldByName('Gname').AsString:=St7;
      uSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 1,List1];
      uSqry.FieldByName('Jubun').AsString:=SGrid.Cells[ 3,List1];
      uSqry.FieldByName('Gsqut').AsFloat :=0;
    end else begin
      uSqry.Edit;
      uSqry.FieldByName('Gsqut').AsFloat :=
      uSqry.FieldByName('Gsqut').AsFloat + 1;
    end;

    uSqry.Edit;
    St6:=SGrid.Cells[ 2,List1];
    if St6='반품' Then begin
      uSqry.FieldByName('Gbqut').AsFloat:=uSqry.FieldByName('Gbqut').AsFloat+T01;
      uSqry.FieldByName('Gbsum').AsFloat:=uSqry.FieldByName('Gbsum').AsFloat+T02;
    end else
    if(St6='출고')or(St6='입고')Then begin
      uSqry.FieldByName('Goqut').AsFloat:=uSqry.FieldByName('Goqut').AsFloat+T01;
      uSqry.FieldByName('Gosum').AsFloat:=uSqry.FieldByName('Gosum').AsFloat+T02;
    end;
    uSqry.Post;
  end;

  St1:='Gdate'+'>='+#39+Str2+#39+' and '+
       'Gdate'+'<='+#39+Str3+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+'('+St3+')';

  {-H1_Ssub-}
  Sqlen :='Select Gdate,Gcode,Gubun,Pubun,Ocode,Oname,Gbigo,Gssum '+
          'From H1_Ssub Where '+D_Select+St1+' Order By Gdate ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 7,List1],0);

    St6:=SGrid.Cells[ 0,List1];
    St7:='XX';

    if uSqry.Locate('Gdate;Jubun',VarArrayOf([St6,St7]),[loCaseInsensitive])=False then begin
      St7:=SGrid.Cells[ 5,List1];
      if SGrid.Cells[ 3,List1]<>'' Then
      St7:=SGrid.Cells[ 3,List1]+'-'+St7;
      if SGrid.Cells[ 6,List1]<>'' Then
      St7:=St7+'-'+SGrid.Cells[ 6,List1];
      uSqry.Append;
      uSqry.FieldByName('Gdate').AsString:=St6;
      uSqry.FieldByName('Gname').AsString:=St7;
      uSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 1,List1];
      uSqry.FieldByName('Jubun').AsString:='XX';
    end;

    uSqry.Edit;

    if St2='Y' then begin
      if SGrid.Cells[ 2,List1]='출금' Then
      uSqry.FieldByName('Gsusu').AsFloat:=uSqry.FieldByName('Gsusu').AsFloat+T01 else
      uSqry.FieldByName('Gsusu').AsFloat:=uSqry.FieldByName('Gsusu').AsFloat-T01;
    end else begin
      if SGrid.Cells[ 2,List1]='입금' Then
      uSqry.FieldByName('Gsusu').AsFloat:=uSqry.FieldByName('Gsusu').AsFloat+T01 else
      uSqry.FieldByName('Gsusu').AsFloat:=uSqry.FieldByName('Gsusu').AsFloat-T01;
    end;
    uSqry.Post;
  end;

  St1:='Gdate'+'>='+#39+Str2+#39+' and '+
       'Gdate'+'<='+#39+Str3+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+'('+St3+')';

  {-Sg_Gsum-}
  Sqlen :='Select Gdate,Gcode,Gbigo,Gbsum '+
          'From Sg_Gsum Where '+D_Select+St1+' Order By Gdate ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 3,List1],0);

    St6:=SGrid.Cells[ 0,List1];
    St7:='YY';

    if uSqry.Locate('Gdate;Jubun',VarArrayOf([St6,St7]),[loCaseInsensitive])=False then begin
      if SGrid.Cells[ 2,List1]='' Then
      St7:='---장부대조---' else
      St7:='---'+SGrid.Cells[ 2,List1]+'---';
      uSqry.Append;
      uSqry.FieldByName('Gdate').AsString:=St6;
      uSqry.FieldByName('Gname').AsString:=St7;
      uSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 1,List1];
      uSqry.FieldByName('Jubun').AsString:='YY';
    end;

    uSqry.Edit;
    uSqry.FieldByName('Gbsum').AsFloat:=uSqry.FieldByName('Gbsum').AsFloat+T01;
    uSqry.Post;
  end;

  nSumX:=0;
  nSumY:=0;
  sSqry.First;
  While sSqry.EOF=False do begin
    nSumX:=nSumX+sSqry.FieldByName('GsumX').AsFloat;
    sSqry.Next;
  end;

  uSqry.Append;
  uSqry.FieldByName('Gdate').AsString:=' 전일미수 ';
  uSqry.FieldByName('GsumX').AsFloat :=nSumX;
  uSqry.FieldByName('GsumY').AsFloat :=nSumX;
  uSqry.Post;

  uSqry.IndexName := 'IDX'+'GDATE'+'DOWN';
  uSqry.First;
  uSqry.Next;
  While uSqry.EOF=False do begin
    uSqry.Edit;
    uSqry.FieldByName('GsumX').AsFloat:=nSumX;
    nSumX:=nSumX+
    uSqry.FieldByName('Gosum').AsFloat+
    uSqry.FieldByName('Gbsum').AsFloat-
    uSqry.FieldByName('Gsusu').AsFloat;
    uSqry.FieldByName('GsumY').AsFloat:=nSumX;
    uSqry.Post;
    uSqry.Next;
  end;

  uSqry.First;
  oSqry:=uSqry;
  Screen.Cursor:=crDefault;
end;

procedure TTong40.SetTring12(Str1,Str2,Str3,Str4,Str5,Str6: String);
begin
{ Str1:'X', Str2:Date1, Str3:Date2, Str4:Code1, Str5:Code2 }
  if uSqry.Active=True Then begin
    oSqry:=uSqry;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    if Sobo33.Panel102.Caption='거래처명' Then begin
      Seek10.FilterTing(Str4,Str6);
      Str4:=Seek10.Query1Gname.AsString;
      Str5:=Seek10.Query1Gtel1.AsString+')'+Seek10.Query1Gtel2.AsString;
    end;
    if Sobo33.Panel102.Caption='입고처명' Then begin
      Seek20.FilterTing(Str4,Str6);
      Str4:=Seek20.Query1Gname.AsString;
      Str5:=Seek20.Query1Gtel1.AsString+')'+Seek20.Query1Gtel2.AsString;
    end;
    if Sobo33.Panel102.Caption='거 래 처' Then begin
      Seek50.FilterTing(Str4,Str6);
      Str4:=Seek50.Query1Gname.AsString;
      Str5:=Seek50.Query1Gtel1.AsString+')'+Seek50.Query1Gtel2.AsString;
    end;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_11.frf');
      Seak80.FilterTing(Str6);
      FindObject('Memo91').Memo.Text:=Seak80.Query1Gname.AsString+mPrnt;
      FindObject('Memo02').Memo.Text:=Str2+' - '+Str3;
      FindObject('Memo04').Memo.Text:=Str4;
      FindObject('Memo06').Memo.Text:=Str5;
      if Sobo33.Panel102.Caption='입고처명' Then
      FindObject('Memo00').Memo.Text:='입고처 거래 원장' else
      FindObject('Memo00').Memo.Text:='거래처 거래 원장';
      if nPrnt='2' then
      ShowReport else
      if PrepareReport then
      PrintPreparedReport(' ',1,true, frall);
    end;

  { Application.CreateForm(TSeen31, Seen31);
    Seen31.QRLabel01.Caption:=Str2+' - '+Str3;
    Seek10.FilterTing(Str4);
    Seen31.QRLabel02.Caption:=Seek10.Query1Gname.AsString;
    Seen31.QRLabel03.Caption:=Seek10.Query1Gtel1.AsString+')'+Seek10.Query1Gtel2.AsString;
    Seen31.QRLabel91.Caption:='출력일자.'+FormatDateTime('yyyy"."mm"."dd',Date);
    Seen31.QRLabel99.Caption:=mPrnt;
    Seen31.QRDBText11.DataSet:=oSqry; Seen31.QRDBText12.DataSet:=oSqry;
    Seen31.QRDBText13.DataSet:=oSqry; Seen31.QRDBText14.DataSet:=oSqry;
    Seen31.QRDBText15.DataSet:=oSqry; Seen31.QRDBText16.DataSet:=oSqry;
    Seen31.QRDBText17.DataSet:=oSqry; Seen31.QRDBText18.DataSet:=oSqry;
    Seen31.QRDBText19.DataSet:=oSqry; Seen31.QuickRep1.DataSet:=oSqry;
    Seak50.PrinTing(Seen31.QuickRep1);
    Seen31.Free; }
  end;
end;

procedure TTong40.SetTring13(Str1,Str2,Str3,Str4,Str5,Str6: String);
begin
{ Str1:'X', Str2:Date1, Str3:Date2, Str4:Code1, Str5:Code2 }
if Str1='1' Then begin
  oSqry:=nSqry;
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

    Tong60.frDBDataSet00_00.DataSet:=oSqry;

    With Tong60.frReport00_00 do begin
      Clear;
      LoadFromFile(GetExecPath + 'Report\Report_3_33.frf');
      FindObject('Memo91').Memo.Text:=Sobo33.Edit108.Text+mPrnt;
      FindObject('Memo02').Memo.Text:=Str2+' - '+Str3;
      FindObject('Memo00').Memo.Text:='영 업 일 보';
      ShowReport;
    end;

{ Application.CreateForm(TSeen57, Seen57);
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;
  Seen57.QRLabel91.Caption:='출력일자.'+FormatDateTime('yyyy"."mm"."dd',Date);
  Seen57.QRLabel99.Caption:=Mprnt;
  Seen57.QRLabel00.Caption:='영 업 일 보';
  Seen57.QRLabel72.Caption:='구 분 명:';
  Seen57.QRLabel01.Caption:=Str2+' - '+Str3;
  Seen57.QRLabel72.Enabled:=False;
  Seen57.QRLabel02.Enabled:=False;
  Seen57.QRDBText11.DataSet:=oSqry; Seen57.QRDBText12.DataSet:=oSqry;
  Seen57.QRDBText13.DataSet:=oSqry; Seen57.QRDBText14.DataSet:=oSqry;
  Seen57.QRDBText15.DataSet:=oSqry; Seen57.QRDBText16.DataSet:=oSqry;
  Seen57.QRDBText17.DataSet:=oSqry; Seen57.QRDBText18.DataSet:=oSqry;
  Seen57.QRDBText19.DataSet:=oSqry; Seen57.QuickRep1.DataSet:=oSqry;
  Seak50.ShowModal; Seak50.PrinTing(Seen57.QuickRep1);
  Seen57.Free; }
  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
end;
if Str1='2' Then begin
  oSqry:=nSqry;
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;
{ Application.CreateForm(TSeen58, Seen58);
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;
  Seen58.QRLabel91.Caption:='출력일자.'+FormatDateTime('yyyy"."mm"."dd',Date);
  Seen58.QRLabel99.Caption:=Mprnt;
  Seen58.QRLabel00.Caption:='영 업 일 보';
  Seen58.QRLabel72.Caption:='구 분 명:';
  Seen58.QRLabel01.Caption:=Str2+' - '+Str3;
  Seen58.QRLabel72.Enabled:=False;
  Seen58.QRLabel02.Enabled:=False;
  Seen58.QRDBText10.DataSet:=oSqry;
  Seen58.QRDBText11.DataSet:=oSqry; Seen58.QRDBText12.DataSet:=oSqry;
  Seen58.QRDBText13.DataSet:=oSqry; Seen58.QRDBText14.DataSet:=oSqry;
  Seen58.QRDBText15.DataSet:=oSqry; Seen58.QRDBText16.DataSet:=oSqry;
  Seen58.QRDBText17.DataSet:=oSqry; Seen58.QRDBText18.DataSet:=oSqry;
  Seen58.QRDBText19.DataSet:=oSqry; Seen58.QuickRep1.DataSet:=oSqry;
  Seak50.ShowModal; Seak50.PrinTing(Seen58.QuickRep1);
  Seen58.Free; }
  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
end;
end;

procedure TTong40.FormShow(Sender: TObject);
var
 Save : LongInt;
begin
  Subu00.Timer1.OnTimer:=Timer1Timer;
  {Show}
  if BorderStyle=bsNone then Exit;
  Save:=GetWindowLong(Handle,gwl_Style);
  if (Save and ws_Caption)=ws_Caption then begin
    case BorderStyle of
      bsSingle,
      bsSizeable : SetWindowLong(Handle,gwl_Style,Save and
        (not(ws_Caption)) or ws_border);
      bsDialog : SetWindowLong(Handle,gwl_Style,Save and
        (not(ws_Caption)) or ds_modalframe or ws_dlgframe);
    end;
    Height:=Height-getSystemMetrics(sm_cyCaption);
    Refresh;
  end;
end;

procedure TTong40.FormHide(Sender: TObject);
var
 Save : LongInt;
begin
  Subu00.Timer1.OnTimer:=nil;
  {Close}
{ if BorderStyle=bsNone then Exit;
  Save:=GetWindowLong(Handle,gwl_Style);
  if (Save and ws_Caption)<>ws_Caption then begin
    case BorderStyle of
      bsSingle,
      bsSizeable : SetWindowLong(Handle,gwl_Style,Save or ws_Caption or
        ws_border);
      bsDialog : SetWindowLong(Handle,gwl_Style,Save or ws_Caption or
        ds_modalframe or ws_dlgframe);
    end;
    Height:=Height+getSystemMetrics(sm_cyCaption);
    Refresh;
  end; }
end;

procedure TTong40.Timer1Timer(Sender: TObject);
begin
{ if Tong40.Color=clLime   then
     Tong40.Color:=clGreen else
  if Tong40.Color=clGreen  then
     Tong40.Color:=clOlive else
  if Tong40.Color=clOlive  then
     Tong40.Color:=clTeal  else
     Tong40.Color:=clLime; }
end;

end.
