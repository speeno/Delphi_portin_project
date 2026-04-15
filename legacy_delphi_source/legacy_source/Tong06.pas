unit Tong06;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  FR_DSet, FR_DBSet, FR_Class, frRtfExp, frexpimg, frOLEExl, FR_E_HTML2,
  FR_E_HTM, FR_E_RTF, FR_E_CSV, FR_E_TXT, FR_Cross, FR_DCtrl, FR_Shape,
  FR_BarC, FR_ChBox, FR_RRect, FR_Rich, FR_OLE, Db, Grids;

type
  TTong60 = class(TForm)
    frReport00_00: TfrReport;
    frDBDataSet00_00: TfrDBDataSet;
    frReport00_01: TfrReport;
    frDBDataSet00_01: TfrDBDataSet;
    frReport21_01: TfrReport;
    frDBDataSet21_01: TfrDBDataSet;
    frReport28_02: TfrReport;
    frDBDataSet28_02: TfrDBDataSet;
    frReport20_01: TfrReport;
    frDBDataSet20_01: TfrDBDataSet;
    frReport28_01: TfrReport;
    frDBDataSet28_01: TfrDBDataSet;
    frReport40_01: TfrReport;
    frDBDataSet40_01: TfrDBDataSet;
    frReport40_02: TfrReport;
    frDBDataSet40_02: TfrDBDataSet;
    frUserDataset21_01: TfrUserDataset;
    frUserDataset28_02: TfrUserDataset;
    frUserDataset20_01: TfrUserDataset;
    frUserDataset28_01: TfrUserDataset;
    frUserDataset40_01: TfrUserDataset;
    frUserDataset40_02: TfrUserDataset;
    frOLEObject1: TfrOLEObject;
    frRichObject1: TfrRichObject;
    frRoundRectObject1: TfrRoundRectObject;
    frCheckBoxObject1: TfrCheckBoxObject;
    frBarCodeObject1: TfrBarCodeObject;
    frShapeObject1: TfrShapeObject;
    frDialogControls1: TfrDialogControls;
    frCrossObject1: TfrCrossObject;
    frTextExport1: TfrTextExport;
    frCSVExport1: TfrCSVExport;
    frRTFExport1: TfrRTFExport;
    frHTMExport1: TfrHTMExport;
    frHTML2Export1: TfrHTML2Export;
    frOLEExcelExport1: TfrOLEExcelExport;
    frBMPExport1: TfrBMPExport;
    frJPEGExport1: TfrJPEGExport;
    frTIFFExport1: TfrTIFFExport;
    frRtfAdvExport1: TfrRtfAdvExport;
    frReport23_01: TfrReport;
    frDBDataSet23_01: TfrDBDataSet;
    frUserDataset23_01: TfrUserDataset;
    frReport1: TfrReport;
    frUserDataset1: TfrUserDataset;
    function  frReport20_00(Str: String): Integer;
    procedure frReport20_10(Str: String);
    procedure frReport21_10(Str: String);
    procedure frReport21_20(Str: String);

    procedure frReport20_01BeginPage(pgNo: Integer);
    procedure frReport20_01GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frReport21_01BeginPage(pgNo: Integer);
    procedure frReport21_01GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frReport23_01BeginPage(pgNo: Integer);
    procedure frReport23_01GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frReport28_01BeginPage(pgNo: Integer);
    procedure frReport28_01GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frReport28_02BeginPage(pgNo: Integer);
    procedure frReport28_02GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frReport40_01BeginPage(pgNo: Integer);
    procedure frReport40_01GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frReport40_02BeginPage(pgNo: Integer);
    procedure frReport40_02GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frReport99_00GetValue(const ParName: String;
      var ParValue: Variant);
    procedure frDBDataSet00_01Next(Sender: TObject);
    procedure frDBDataSet00_02Next(Sender: TObject);
    procedure frDBDataSet00_03Next(Sender: TObject);
    procedure frReport24_01GetValue(const ParName: String;
      var ParValue: Variant);
  private
  public
  end;

var
  Tong60: TTong60;
  frReport01_01: TfrReport;
  v_Scode,v_Gdate,v_Hcode,v_Gcode,v_Gname,v_Gubun,v_Jubun,v_Gjisa: String;
  v_GsumA,v_GsumB,v_GsumC: Double;
  v_Gqut1,v_Gqut2: Integer;
  v_Sline,v_Count,v_Spage,v_Pages,v_Page1,v_Page2: Integer;
  W_Count: Integer;

implementation

{$R *.DFM}

uses Base01,Tong04,TcpLib,globalCommon,
     Subu11,Subu12,Subu13,Subu14,Subu15,Subu16,Subu17,Subu18,Subu19,Subu10,
     Subu21,Subu22,Subu23,Subu24,Subu25,Subu26,Subu27,Subu28,Subu29,Subu20,
     Subu31,Subu32,Subu33,Subu34,Subu35,Subu36,Subu37,Subu38,Subu39,Subu30,
     Subu41,Subu42,Subu43,Subu44,Subu45,Subu46,Subu47,Subu48,Subu49,Subu40,
     Subu51,Subu52,Subu53,Subu54,Subu55,Subu56,Subu57,Subu58,Subu59,Subu50,
     Subu61,Subu62,Subu63,Subu64,Subu65,Subu66,Subu67,Subu68,Subu69,Subu60;

function TTong60.frReport20_00(Str: String): Integer;
var
  p_Scode,p_Gdate,p_Hcode,p_Gcode,p_Gubun,p_Jubun,p_Gjisa: String;
  p_Spage,p_Pages: Integer;
begin

  p_Spage:=0; p_Pages:=0;
  oSqry.First;
  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
      (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)and(oSqry.EOF=False)Then begin
    end else begin
      p_Scode:=oSqry.FieldByName('Scode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Hcode:=oSqry.FieldByName('Hcode').AsString;
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
      p_Gjisa:=oSqry.FieldByName('Gjisa').AsString;
      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
        (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)do begin
        p_Pages:=p_Pages+1;
        oSqry.Next;
      end;
    { if oSqry.RecordCount=1 then
      oSqry.MoveBy(-1) else
      if(oSqry.EOF=False)Then
      oSqry.MoveBy(-p_Pages) else
      oSqry.MoveBy(-p_Pages+1);
      if(oSqry.EOF=True)and(p_Pages=1)Then begin
      oSqry.MoveBy(-1);
      oSqry.MoveBy( 1);
      end; }

      v_Page1:=p_Pages mod RBand;
      if v_Page1=0 then begin
         p_Pages:=Trunc(p_Pages/RBand);
         p_Pages:=p_Pages+0;
      end else begin
         p_Pages:=Trunc(p_Pages/RBand);
         p_Pages:=p_Pages+1;
      end;
      v_Page1:=0;
    end;
    p_Spage:=p_Spage+p_Pages;
    p_Pages:=0;
  end;
  Result := p_Spage;
end;

procedure TTong60.frReport20_10(Str: String);
var
  p_Scode,p_Gdate,p_Hcode,p_Gcode,p_Gname,p_Gubun,p_Jubun,p_Gjisa,p_Gmemo,p_Cours,p_Gbigo: String;
  p_GsumA,p_GsumB: Double;
  p_GsumC,p_GsumD: Double;
  p_Cqut1,p_Cqut2,p_Cqut3: Integer;
  p_Spage,p_Pages,p_Idnum: Integer;
  p_CCCCC: Integer;
  p_Barc1,p_Barc2: String;
begin

  p_Spage:=0; p_Pages:=0; p_GsumA:=0; p_GsumB:=0;
  p_GsumC:=0; p_GsumD:=0;
  While oSqry.EOF=False do
  begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
      (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)and(oSqry.EOF=False)Then begin
    end
    else begin
      p_Scode:=oSqry.FieldByName('Scode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Hcode:=oSqry.FieldByName('Hcode').AsString;
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
      p_Gjisa:=oSqry.FieldByName('Gjisa').AsString;
      p_Gbigo:=oSqry.FieldByName('Gbigo').AsString;

      if frReport20_01.FindObject('Memo32_1').Visible=True then
        Tong40.PrinTing08(p_Scode,p_Gcode,p_Gdate,p_Gubun,p_Jubun,p_Hcode);

      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
        (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)do
      begin
        p_GsumA:=p_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
        p_GsumB:=p_GsumB+oSqry.FieldByName('Gssum').AsInteger;

        if(Base10.Database.Database='book_07_db')or
          (Hnnnn='4100')then begin
          Sqlen := 'Select Gqut1,Gqut2 From G4_Book '+
                   'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
          Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

          Base10.Socket.RunSQL(Sqlen);
          Base10.Socket.busyloop;
          if Base10.Socket.Body_Data <> 'NODATA' then begin
            Base10.Socket.MakeData;
            p_Cqut1:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 1)),0);
            p_Cqut2:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 2)),0);
            p_GsumD:=p_GsumD+(p_Cqut2*oSqry.FieldByName('Gsqut').Value);
            if (oSqry.FieldByName('Gsqut').Value<>0) and (p_Cqut1<>0) then begin
              p_Cqut3:=Trunc(oSqry.FieldByName('Gsqut').Value/p_Cqut1);
              if (oSqry.FieldByName('Gsqut').Value mod p_Cqut1) > 0 then
              p_Cqut3:=p_Cqut3+1;
              p_GsumC:=p_GsumC+p_Cqut3;
            end;
          end;
        end;

        p_Pages:=p_Pages+1;
        oSqry.Next;
      end;
      if oSqry.RecordCount=1 then
      oSqry.MoveBy(-1) else
      if(oSqry.EOF=False)Then
      oSqry.MoveBy(-p_Pages) else
      oSqry.MoveBy(-p_Pages+1);
      if(oSqry.EOF=True)and(p_Pages=1)Then begin
      oSqry.MoveBy(-1);
      oSqry.MoveBy( 1);
      end;

      v_Page1:=p_Pages mod RBand;
      if v_Page1=0 then begin
         p_Pages:=Trunc(p_Pages/RBand);
         p_Pages:=p_Pages+0;
      end else begin
         p_Pages:=Trunc(p_Pages/RBand);
         p_Pages:=p_Pages+1;
      end;
      v_Page1:=0;
      v_Page2:=p_Pages;
    end;

    p_Scode:=oSqry.FieldByName('Scode').AsString;
    p_Gname:=oSqry.FieldByName('Gname').AsString;;

    if p_Scode='X' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    if p_Scode='Y' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G2_Ggwo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    if p_Scode='Z' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    //--//
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data = 'NODATA' then begin
    if p_Scode='X' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    if p_Scode='Y' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G2_Ggwo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    if p_Scode='Z' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    end;
    //--//

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      with frReport20_01 do begin

        FindObject('Memo68_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2))+
                                      '-'+AutoFrx(Base10.Socket.GetData(1, 3));//전화번호
        FindObject('Memo69_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                      '-'+AutoFrx(Base10.Socket.GetData(1, 5));
        FindObject('Memo68_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2))+
                                      '-'+AutoFrx(Base10.Socket.GetData(1, 3));
        FindObject('Memo69_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                      '-'+AutoFrx(Base10.Socket.GetData(1, 5));
        FindObject('Memo60_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                      ' '+AutoFrx(Base10.Socket.GetData(1, 7));
        FindObject('Memo60_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                      ' '+AutoFrx(Base10.Socket.GetData(1, 7));
        p_Gname:=Base10.Socket.GetData(1, 1);

        if((Base10.Database.Database='book_01_db')and(Base10.Database.Host='115.68.7.138'))then begin
        { Sqlen := 'Select Apost From G4_Book '+
                   'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
          Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
          p_Gmemo:=Base10.Seek_Name(Sqlen); }

          Sqlen := 'Select Gnum1 From G7_Ggeo Where '+D_Select+'Gcode = ''@Gcode''';
          Translate(Sqlen, '@Gcode', oSqry.FieldByName('Hcode').AsString);
          p_Gmemo:=Base10.Seek_Name(Sqlen);

          FindObject('Memo32_1').Memo.Text:=p_Gmemo;
          FindObject('Memo32_2').Memo.Text:=p_Gmemo;
        end;

        if(Base10.Database.Database='book_kb_db')then begin
          if frReport20_01.FindObject('Memo00_1').Prop['Alignment']=9 then begin
          with frReport20_01 do begin
           FindObject('Memo71_0').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8));
         //FindObject('Memo71_1').Memo.Text:=Base10.Seek_Jisa( AutoFrx(Base10.Socket.GetData(1, 8)) ,'4');
         //FindObject('Memo71_2').Memo.Text:=Base10.Seek_Jisa( AutoFrx(Base10.Socket.GetData(1, 8)) ,'3');
           p_Gmemo:='';
           if p_Gjisa<>'' then begin
             Sqlen := 'Select Gnum1 From H2_Gbun Where '+D_Select+
                      'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
             if Copy(p_Gcode,1,1)<>'9' then
             Translate(Sqlen, '@Hcode', '') else
             Translate(Sqlen, '@Hcode', p_Hcode);
             Translate(Sqlen, '@Scode', 'X');
             Translate(Sqlen, '@Gcode', p_Gcode);
             Translate(Sqlen, '@Gname', Base10.Seek_Jisa(p_Gjisa,'3'));
             Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(p_Gjisa,'4'));
             p_Gmemo:=Base10.Seek_Name(Sqlen);
           end;
           if p_Gmemo<>'' then begin
           FindObject('Memo71_0').Memo.Text:=p_Gmemo;
         //FindObject('Memo71_1').Memo.Text:=Base10.Seek_Jisa( p_Gmemo ,'4');
         //FindObject('Memo71_2').Memo.Text:=Base10.Seek_Jisa( p_Gmemo ,'3');
           end;
          end;
          end;

          Sqlen := 'Select Gnum1 From G7_Ggeo Where '+D_Select+'Gcode = ''@Gcode''';
          Translate(Sqlen, '@Gcode', p_Hcode);
          p_Cours := Base10.Seek_Name(Sqlen);
          FindObject('Memo83_0').Memo.Text:=p_Cours;
        end;

        if(Pos('해피데이',mPrnt) > 0)then begin
          FindObject('Memo71_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8));
          FindObject('Memo71_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8));
          p_Gmemo:='';
          if p_Gjisa<>'' then begin
            Sqlen := 'Select Gnum1 From H2_Gbun Where '+D_Select+
                     'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
            if Copy(p_Gcode,1,1)<>'9' then
            Translate(Sqlen, '@Hcode', '') else
            Translate(Sqlen, '@Hcode', p_Hcode);
            Translate(Sqlen, '@Scode', 'X');
            Translate(Sqlen, '@Gcode', p_Gcode);
            Translate(Sqlen, '@Gname', Base10.Seek_Jisa(p_Gjisa,'3'));
            Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(p_Gjisa,'4'));
            p_Gmemo:=Base10.Seek_Name(Sqlen);
          end;
          if p_Gmemo<>'' then begin
          FindObject('Memo71_1').Memo.Text:=p_Gmemo;
          FindObject('Memo71_2').Memo.Text:=p_Gmemo;
          end;
        end;

        if(Pos('수레사',  mPrnt) > 0)then begin
          FindObject('Memo71_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8));
          FindObject('Memo71_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8));
          p_Gmemo:=AutoFrx(Base10.Socket.GetData(1, 8));
          if p_Gjisa<>'' then begin
            Sqlen := 'Select Gnum1 From H2_Gbun Where '+D_Select+
                     'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
            if Copy(p_Gcode,1,1)<>'9' then
            Translate(Sqlen, '@Hcode', '') else
            Translate(Sqlen, '@Hcode', p_Hcode);
            Translate(Sqlen, '@Scode', 'X');
            Translate(Sqlen, '@Gcode', p_Gcode);
            Translate(Sqlen, '@Gname', Base10.Seek_Jisa(p_Gjisa,'3'));
            Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(p_Gjisa,'4'));
            p_Gmemo:=Base10.Seek_Name(Sqlen);
          end;
          Sqlen := 'Select Gnum1 From G7_Ggeo Where '+D_Select+'Gcode = ''@Gcode''';
          Translate(Sqlen, '@Gcode', p_Hcode);
          p_Cours := Base10.Seek_Name(Sqlen);

          if p_Gmemo<>'' then begin
          FindObject('Memo71_1').Memo.Text:='( '+p_Cours+' - '+p_Gmemo+' )';
          FindObject('Memo71_2').Memo.Text:='( '+p_Cours+' - '+p_Gmemo+' )';
          end;
        end;

      end;
    end;


    Sqlen := 'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Gtel1,Gtel2,Gfax1,Gfax2 From G7_Ggeo '+
             'Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Hcode);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      if(Base10.Database.Database='book_05_db')and(p_Hcode='122')then begin
        //--동양물산기업--//
        with frReport20_01 do begin
        FindObject('Memo81_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
        FindObject('Memo82_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
        FindObject('Memo83_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
        FindObject('Memo84_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                      ' '+AutoFrx(Base10.Socket.GetData(1, 5));
        FindObject('Memo85_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 7));
        FindObject('Memo86_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 9));
        FindObject('Memo81_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
        FindObject('Memo82_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
        FindObject('Memo83_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
        FindObject('Memo84_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                      ' '+AutoFrx(Base10.Socket.GetData(1, 5));
        FindObject('Memo85_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 7));
        FindObject('Memo86_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 9));
        end;
      end else begin
        with frReport20_01 do begin
        FindObject('Memo81_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));//사업자번호
        FindObject('Memo82_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
        FindObject('Memo83_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
        FindObject('Memo84_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                      ' '+AutoFrx(Base10.Socket.GetData(1, 5));
        FindObject('Memo85_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 7));
        FindObject('Memo86_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 9));
        FindObject('Memo81_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
        FindObject('Memo82_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
        FindObject('Memo83_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
        FindObject('Memo84_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                      ' '+AutoFrx(Base10.Socket.GetData(1, 5));
        FindObject('Memo85_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 7));
        FindObject('Memo86_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                      ')'+AutoFrx(Base10.Socket.GetData(1, 9));
        end;
      end;
    end;

    if Pos('메모',frReport20_01.FindObject('Memo74_1').Memo.Text) > 0 then begin

      Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where '+D_Select+
               'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
               'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
               'Gcode=''@Gcode'' and Scode=''@Scode'' and '+
               'Gjisa=''@Gjisa'' and '+
               '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
      Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gdate', oSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gubun', oSqry.FieldByName('Gubun').AsString);
      Translate(Sqlen, '@Jubun', oSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', oSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Gjisa', oSqry.FieldByName('Gjisa').AsString);
      Translate(Sqlen, '@Ocode', 'B');
      Base10.Socket.RunSQL(Sqlen);//ddddd
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        frReport20_01.FindObject('Memo60_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
        if p_Gbigo='' then
        frReport20_01.FindObject('Memo60_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2))
        else
        //>>frReport20_01.FindObject('Memo60_2').Memo.Text:='('+p_Gbigo+')'+AutoFrx(Base10.Socket.GetData(1, 2));
        frReport20_01.FindObject('Memo60_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));

        if Base10.Database.Database='book_06_db' then
        frReport20_01.FindObject('Memo60_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));

        p_Gmemo:='';

        if Base10.Socket.GetData(1, 3)<>'' then
        p_Gmemo:=p_Gmemo+'HP:'+AutoFrx(Base10.Socket.GetData(1, 3));

        if Base10.Socket.GetData(1, 4)<>'' then
        if p_Gmemo='' then
        p_Gmemo:=p_Gmemo+'☏:'+AutoFrx(Base10.Socket.GetData(1, 4))
        else
        p_Gmemo:=p_Gmemo+', ☏:'+AutoFrx(Base10.Socket.GetData(1, 4));

        if Base10.Socket.GetData(1, 5)<>'' then
        if p_Gmemo='' then
        p_Gmemo:=p_Gmemo+'【'+AutoFrx(Base10.Socket.GetData(1, 5))+'】'
        else
        p_Gmemo:=p_Gmemo+',【'+AutoFrx(Base10.Socket.GetData(1, 5))+'】';

      { if Base10.Socket.GetData(1, 2)='' then begin
          frReport20_01.FindObject('Memo60_2').Memo.Text:=p_Gmemo;
          frReport20_01.FindObject('Memo69_1').Memo.Text:='';
        end else begin
          frReport20_01.FindObject('Memo69_1').Memo.Text:=p_Gmemo;
        end; }
          frReport20_01.FindObject('Memo69_1').Memo.Text:=p_Gmemo;
      end else begin
        if Base10.Database.Database='book_06_db' then
        frReport20_01.FindObject('Memo60_1').Memo.Text:=''
        else
        frReport20_01.FindObject('Memo60_1').Memo.Text:=p_Gbigo;
        frReport20_01.FindObject('Memo60_2').Memo.Text:='';
        frReport20_01.FindObject('Memo69_1').Memo.Text:='';
      end;

    end;

    Tong40._Gg_Magn_('7');
    with frReport20_01 do begin
      if(Base10.Database.Database='book_07_db')or(Hnnnn='4100')then begin
      FindObject('Memo32_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumC);
      FindObject('Memo33_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumD);
      FindObject('Memo32_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumC);
      FindObject('Memo33_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumD);
      end;

      if oSqry.FieldByName('Gjisa').AsString<>'' then
      p_Gname:=Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'2')+
      p_Gname+ Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'1');

      FindObject('Memo65_1').Memo.Text:=AutoFrx(p_Gname);
      if (gCompany_name = '한강물류') or (gCompany_name = '한강북') then
        FindObject('Memo70_1').Memo.Text:=AutoFrx(p_Gname);//작은 글씨
      FindObject('Memo65_2').Memo.Text:=AutoFrx(p_Gname);
      if (gCompany_name = '한강물류') or (gCompany_name = '한강북') then
        FindObject('Memo70_2').Memo.Text:=AutoFrx(p_Gname);//작은 글씨

      FindObject('Memo57_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Pubun').AsString);//"위탁" 등의 문자
      FindObject('Memo61_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gdate').AsString);
      FindObject('Memo62_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gubun').AsString);
      FindObject('Memo64_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gcode').AsString);
      FindObject('Memo66_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
      if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
        FindObject('Memo67_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end else begin
        if oSqry.FieldByName('Gcode').AsString<'9' then
        FindObject('Memo67_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end;
      if((Base10.Database.Database<>'book_01_db')and(Base10.Database.Host<>'115.68.7.138'))and
        ((Base10.Database.Database<>'book_07_db')and(Hnnnn<>'4100'))then begin
      FindObject('Memo32_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumX);
      FindObject('Memo33_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumX+p_GsumB);
      end;

      FindObject('Memo45_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
      if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
        FindObject('Memo48_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end else begin
        if oSqry.FieldByName('Gcode').AsString<'9' then
        FindObject('Memo48_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end;

      FindObject('Memo57_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Pubun').AsString);
      FindObject('Memo61_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gdate').AsString);
      FindObject('Memo62_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gubun').AsString);
      FindObject('Memo64_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gcode').AsString);
      FindObject('Memo66_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
      if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
        FindObject('Memo67_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end else begin
        if oSqry.FieldByName('Gcode').AsString<'9' then
        FindObject('Memo67_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end;
      if((Base10.Database.Database<>'book_01_db')and(Base10.Database.Host<>'115.68.7.138'))and
        ((Base10.Database.Database<>'book_07_db')and(Hnnnn<>'4100'))then begin
      FindObject('Memo32_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumX);
      FindObject('Memo33_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumX+p_GsumB);
      end;

      FindObject('Memo45_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
      if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
        FindObject('Memo48_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end else begin
        if oSqry.FieldByName('Gcode').AsString<'9' then
        FindObject('Memo48_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end;

      if FindObject('Memo71_1').Prop['Alignment']=9 then
      FindObject('Memo71_1').Memo.Text:=AutoFrx(p_Hcode);
      if FindObject('Memo71_2').Prop['Alignment']=9 then
      FindObject('Memo71_2').Memo.Text:=AutoFrx(p_Hcode);

      if FindObject('Memo58_1').Prop['Alignment']=10 then begin
        Sqlen := 'Select Idnum From S1_Ssub Where '+D_Select+'Id=@Id';
        Translate(Sqlen, '@Id', oSqry.FieldByName('Id').AsString);
        p_Idnum:=StrToIntDef(Base10.Seek_Name(Sqlen),0);
        FindObject('Memo58_1').Memo.Text:=
        FormatFloat('###,###,##0',p_Idnum);
        if FindObject('Memo58_2').Prop['Alignment']=10 then begin
        FindObject('Memo58_2').Memo.Text:=
        FormatFloat('###,###,##0',p_Idnum);
        end;
      end;

    { if FindObject('Memo76_1').Prop['Alignment']=8 then begin
        if oSqry.FieldByName('Scode').AsString='Y' then begin
          p_Barc1:='8';
          if oSqry.FieldByName('Gubun').AsString='입고' then
          p_Barc1:='8';
          if oSqry.FieldByName('Gubun').AsString='반품' then
          p_Barc1:='9';
        end else
        if oSqry.FieldByName('Scode').AsString='X' then begin
          p_Barc1:='1';
          if oSqry.FieldByName('Gubun').AsString='출고' then
          p_Barc1:='1';
          if oSqry.FieldByName('Gubun').AsString='반품' then
          p_Barc1:='2';
        end else
        if oSqry.FieldByName('Scode').AsString='Z' then begin
          p_Barc1:='4';
          if oSqry.FieldByName('Gubun').AsString='출고' then
          p_Barc1:='4';
          if oSqry.FieldByName('Gubun').AsString='반품' then
          p_Barc1:='5';
          if oSqry.FieldByName('Gubun').AsString='폐기' then
          p_Barc1:='6';
        end;
        p_Barc2:=p_Barc1;
        p_Barc2:=p_Barc2+Format('%-05s',[oSqry.FieldByName('Hcode').AsString] );
        p_Barc2:=p_Barc2+Format('%-06s',[Copy(oSqry.FieldByName('Gdate').AsString,3,2)+
                                         Copy(oSqry.FieldByName('Gdate').AsString,6,2)+
                                         Copy(oSqry.FieldByName('Gdate').AsString,9,2)] );
        p_Barc2:=p_Barc2+Format('%-05s',[oSqry.FieldByName('Gcode').AsString] );
        p_Barc2:=p_Barc2+Format('%-02s',[oSqry.FieldByName('Jubun').AsString] );
      //p_Barc2:=p_Barc2+Format('%-03s',[oSqry.FieldByName('Idnum').AsString] );
        p_Barc2:=p_Barc2+oSqry.FieldByName('Idnum').AsString;
        Translate(p_Barc2, ' ', '0');
        FindObject('Bar1').Memo.Text:=p_Barc2;
        FindObject('Bar2').Memo.Text:=p_Barc2;
      end; }
      if FindObject('Memo76_1').Prop['Alignment']=8 then begin
        if oSqry.FieldByName('Icode').AsString<>'' then begin
        FindObject('Bar1').Memo.Text:=oSqry.FieldByName('Icode').AsString;
        FindObject('Bar2').Memo.Text:=oSqry.FieldByName('Icode').AsString;
        end else begin
        FindObject('Bar1').Memo.Text:=oSqry.FieldByName('ID').AsString;
        FindObject('Bar2').Memo.Text:=oSqry.FieldByName('ID').AsString;
        end;
      end;

      if(Base10.Database.Database='chul_01_db')then begin
        if oSqry.FieldByName('Icode').AsString<>'' then begin
        FindObject('Bar1').Memo.Text:=oSqry.FieldByName('Icode').AsString;
        FindObject('Bar2').Memo.Text:=oSqry.FieldByName('Icode').AsString;
        end else begin
        FindObject('Bar1').Memo.Text:=oSqry.FieldByName('ID').AsString;
        FindObject('Bar2').Memo.Text:=oSqry.FieldByName('ID').AsString;
        end;
      end;
    end;

    if(Base10.Database.Database='book_kb_db')then begin
      if frReport20_01.FindObject('Memo00_1').Prop['Alignment']=9 then begin
      with frReport20_01 do begin
        FindObject('Memo57_0').Memo.Text:=AutoFrx(oSqry.FieldByName('Pubun').AsString);
        FindObject('Memo61_0').Memo.Text:=AutoFrx(oSqry.FieldByName('Gdate').AsString);
        FindObject('Memo68_0').Memo.Text:=FindObject('Memo68_1').Memo.Text;
        FindObject('Memo66_0').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
        FindObject('Memo67_0').Memo.Text:=FormatFloat('###,###,##0',1);
        FindObject('Memo82_0').Memo.Text:=FindObject('Memo82_2').Memo.Text;
        if Pos(')',AutoFrx(p_Gname)) > 0 then begin
          p_CCCCC:=Pos(')',AutoFrx(p_Gname));
          FindObject('Memo64_0').Memo.Text:=Copy(AutoFrx(p_Gname),1,p_CCCCC-1);
          FindObject('Memo65_0').Memo.Text:=Copy(AutoFrx(p_Gname),p_CCCCC+1,50);
        end else begin
          FindObject('Memo64_0').Memo.Text:='';
          FindObject('Memo65_0').Memo.Text:=AutoFrx(p_Gname);
        end;

        Sqlen := 'Select Gqut1 From T4_Ssub Where '+D_Select+
                 'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
                 'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
                 'Gjisa=''@Gjisa'' ';
        Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
        Translate(Sqlen, '@Gdate', oSqry.FieldByName('Gdate').AsString);
        Translate(Sqlen, '@Jubun', oSqry.FieldByName('Jubun').AsString);
        Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);
        Translate(Sqlen, '@Gjisa', oSqry.FieldByName('Gjisa').AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.busyloop;
        if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        FindObject('Memo67_0').Memo.Text:=FormatFloat('###,###,##0',StrToInt(AutoFrx(Base10.Socket.GetData(1, 1))));
        end;

      end;
      end;
    end;

    Exit;
  end;
end;

procedure TTong60.frReport21_10(Str: String);
var
  p_Scode,p_Gdate,p_Hcode,p_Gcode,p_Gname,p_Gubun,p_Jubun,p_Gjisa,p_Gmemo,p_Gbigo: String;
  t_Gtel1,t_Gtel2,t_Gadd1,t_Gadd2,t_Gpper,t_Gmemo,t_Gbigo: String;
  p_GsumA,p_GsumB: Double;
  p_GsumC,p_GsumD: Double;
  p_Cqut1,p_Cqut2,p_Cqut3: Integer;
  p_Spage,p_Pages,p_Idnum: Integer;
begin

  p_Spage:=0; p_Pages:=0; p_GsumA:=0; p_GsumB:=0;
  p_GsumC:=0; p_GsumD:=0;
  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
      (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)and(oSqry.EOF=False)Then begin
    end else begin
      p_Scode:=oSqry.FieldByName('Scode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Hcode:=oSqry.FieldByName('Hcode').AsString;
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
      p_Gjisa:=oSqry.FieldByName('Gjisa').AsString;
      p_Gbigo:=oSqry.FieldByName('Gbigo').AsString;
      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
        (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)do begin
        p_GsumA:=p_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
        p_GsumB:=p_GsumB+oSqry.FieldByName('Gssum').AsInteger;

        if(Base10.Database.Database='book_07_db')or
          (Hnnnn='4100')then begin
          Sqlen := 'Select Gqut1,Gqut2 From G4_Book '+
                   'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
          Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

          Base10.Socket.RunSQL(Sqlen);
          Base10.Socket.busyloop;
          if Base10.Socket.Body_Data <> 'NODATA' then begin
            Base10.Socket.MakeData;
            p_Cqut1:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 1)),0);
            p_Cqut2:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 2)),0);
            p_GsumD:=p_GsumD+(p_Cqut2*oSqry.FieldByName('Gsqut').Value);
            if (oSqry.FieldByName('Gsqut').Value<>0) and (p_Cqut1<>0) then begin
              p_Cqut3:=Trunc(oSqry.FieldByName('Gsqut').Value/p_Cqut1);
              if (oSqry.FieldByName('Gsqut').Value mod p_Cqut1) > 0 then
              p_Cqut3:=p_Cqut3+1;
              p_GsumC:=p_GsumC+p_Cqut3;
            end;
          end;
        end;

        p_Pages:=p_Pages+1;
        oSqry.Next;
      end;
      if oSqry.RecordCount=1 then
      oSqry.MoveBy(-1) else
      if(oSqry.EOF=False)Then
      oSqry.MoveBy(-p_Pages) else
      oSqry.MoveBy(-p_Pages+1);
      if(oSqry.EOF=True)and(p_Pages=1)Then begin
      oSqry.MoveBy(-1);
      oSqry.MoveBy( 1);
      end;

      v_Page1:=p_Pages mod RBand;
      if v_Page1=0 then begin
         p_Pages:=Trunc(p_Pages/RBand);
         p_Pages:=p_Pages+0;
      end else begin
         p_Pages:=Trunc(p_Pages/RBand);
         p_Pages:=p_Pages+1;
      end;
      v_Page1:=0;
      v_Page2:=p_Pages;
    end;

    p_Scode:=oSqry.FieldByName('Scode').AsString;
    p_Gname:=oSqry.FieldByName('Gname').AsString;;

    if p_Scode='X' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    if p_Scode='Y' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G2_Ggwo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    if p_Scode='Z' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    //--//
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data = 'NODATA' then begin
    if p_Scode='X' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    if p_Scode='Y' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G2_Ggwo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    if p_Scode='Z' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    end;
    //--//

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      p_Gname:=Base10.Socket.GetData(1, 1);

      t_Gadd1:=Base10.Socket.GetData(1, 4);
      t_Gadd2:=Base10.Socket.GetData(1, 5);
      t_Gtel1:=Base10.Socket.GetData(1, 2);
      t_Gtel2:=Base10.Socket.GetData(1, 3);
      t_Gpper:=Base10.Socket.GetData(1, 6);
      t_Gbigo:=Base10.Socket.GetData(1, 7);

      Tong40._Gg_Magn_('7');
      with frReport21_01 do begin

        if(Base10.Database.Database='book_07_db')or(Hnnnn='4100')then begin
        FindObject('Memo32_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumC);
        FindObject('Memo33_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumD);
        FindObject('Memo32_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumC);
        FindObject('Memo33_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumD);
        end;

        if oSqry.FieldByName('Gjisa').AsString<>'' then
        p_Gname:=Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'2')+
        p_Gname+ Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'1');

        FindObject('Memo65_1').Memo.Text:=AutoFrx(p_Gname);
        FindObject('Memo70_1').Memo.Text:=AutoFrx(p_Gname);//작은 글씨
        FindObject('Memo65_2').Memo.Text:=AutoFrx(p_Gname);
        FindObject('Memo70_2').Memo.Text:=AutoFrx(p_Gname);//작은 글씨

        FindObject('Memo61_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gdate').AsString);
        FindObject('Memo62_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gubun').AsString);
        FindObject('Memo64_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gcode').AsString);
        FindObject('Memo66_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
        if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
          FindObject('Memo67_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
        end else begin
          if oSqry.FieldByName('Gcode').AsString<'9' then
          FindObject('Memo67_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
        end;

        FindObject('Memo61_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gdate').AsString);
        FindObject('Memo62_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gubun').AsString);
        FindObject('Memo64_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gcode').AsString);
        FindObject('Memo66_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
        if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
          FindObject('Memo67_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
        end else begin
          if oSqry.FieldByName('Gcode').AsString<'9' then
          FindObject('Memo67_2').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
        end;
      end;
    end;

    Sqlen := 'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Gtel1,Gtel2,Gfax1,Gfax2 From G7_Ggeo '+
             'Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Hcode);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      with frReport21_01 do begin
      FindObject('Memo81_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
      FindObject('Memo82_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
      FindObject('Memo83_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
      FindObject('Memo84_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                    ' '+AutoFrx(Base10.Socket.GetData(1, 5));
      FindObject('Memo85_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 7));
      FindObject('Memo86_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 9));
      FindObject('Memo81_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
      FindObject('Memo82_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
      FindObject('Memo83_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
      FindObject('Memo84_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                    ' '+AutoFrx(Base10.Socket.GetData(1, 5));
      FindObject('Memo85_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 7));
      FindObject('Memo86_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 9));
      end;
    end;

    if Pos('메모',frReport21_01.FindObject('Memo74_1').Memo.Text) > 0 then begin

      if Base10.Database.Database='chul_04_db' then
      Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where '+D_Select+
               'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
               'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
               'Gcode=''@Gcode'' and Scode=''@Scode'' and '+
               'Gjisa=''@Gjisa'' and '+
               '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')'
      else
      Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where '+D_Select+
               'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
               'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
               'Gcode=''@Gcode'' and Scode=''@Scode'' and '+
               'Gjisa=''@Gjisa'' and '+
               '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
      Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gdate', oSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gubun', oSqry.FieldByName('Gubun').AsString);
      Translate(Sqlen, '@Jubun', oSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', oSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Gjisa', oSqry.FieldByName('Gjisa').AsString);
      Translate(Sqlen, '@Ocode', 'B');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        frReport21_01.FindObject('Memo60_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
        if p_Gbigo='' then
        frReport21_01.FindObject('Memo60_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2))
        else
        frReport21_01.FindObject('Memo60_2').Memo.Text:='('+p_Gbigo+')'+AutoFrx(Base10.Socket.GetData(1, 2));

        if Base10.Database.Database='book_06_db' then
        frReport21_01.FindObject('Memo60_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));

        p_Gmemo:='';

        if Base10.Socket.GetData(1, 3)<>'' then
        p_Gmemo:=p_Gmemo+'HP:'+AutoFrx(Base10.Socket.GetData(1, 3));

        if Base10.Socket.GetData(1, 4)<>'' then
        if p_Gmemo='' then
        p_Gmemo:=p_Gmemo+'☏:'+AutoFrx(Base10.Socket.GetData(1, 4))
        else
        p_Gmemo:=p_Gmemo+', ☏:'+AutoFrx(Base10.Socket.GetData(1, 4));

        if Base10.Socket.GetData(1, 5)<>'' then
        if p_Gmemo='' then
        p_Gmemo:=p_Gmemo+'【'+AutoFrx(Base10.Socket.GetData(1, 5))+'】'
        else
        p_Gmemo:=p_Gmemo+',【'+AutoFrx(Base10.Socket.GetData(1, 5))+'】';

        if Base10.Database.Database='chul_04_db' then begin
          frReport21_01.FindObject('Memo5').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6));
          frReport21_01.FindObject('Memo8').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6));
        end;

      { if Base10.Socket.GetData(1, 2)='' then begin
          frReport21_01.FindObject('Memo60_2').Memo.Text:=p_Gmemo;
          frReport21_01.FindObject('Memo69_1').Memo.Text:='';
        end else begin
          frReport21_01.FindObject('Memo69_1').Memo.Text:=p_Gmemo;
        end; }
          frReport21_01.FindObject('Memo69_1').Memo.Text:=p_Gmemo;
      end else begin
        if Pos('택배',p_Gname) > 0 then begin

          frReport21_01.FindObject('Memo60_1').Memo.Text:=t_Gadd1;
          if p_Gbigo='' then
          frReport21_01.FindObject('Memo60_2').Memo.Text:=t_Gadd2
          else
          frReport21_01.FindObject('Memo60_2').Memo.Text:='('+p_Gbigo+')'+t_Gadd2;

          if Base10.Database.Database='book_06_db' then
          frReport21_01.FindObject('Memo60_2').Memo.Text:=t_Gadd2;

          p_Gmemo:='';

          if t_Gbigo<>'' then
          p_Gmemo:=p_Gmemo+t_Gbigo;

          if t_Gtel2<>'' then
          if p_Gmemo='' then
          p_Gmemo:=p_Gmemo+'☏:'+t_Gtel1+'-'+t_Gtel2
          else
          p_Gmemo:=p_Gmemo+', ☏:'+t_Gtel1+'-'+t_Gtel2;

          if t_Gpper<>'' then
          if p_Gmemo='' then
          p_Gmemo:=p_Gmemo+'【'+t_Gpper+'】'
          else
          p_Gmemo:=p_Gmemo+',【'+t_Gpper+'】';

          frReport21_01.FindObject('Memo69_1').Memo.Text:=p_Gmemo;

        end else begin
          if Base10.Database.Database='book_06_db' then
          frReport21_01.FindObject('Memo60_1').Memo.Text:=''
          else
          frReport21_01.FindObject('Memo60_1').Memo.Text:=p_Gbigo;
          frReport21_01.FindObject('Memo60_2').Memo.Text:='';
          frReport21_01.FindObject('Memo69_1').Memo.Text:='';
        end;
      end;

      if frReport21_01.FindObject('Memo58_1').Prop['Alignment']=10 then begin
        Sqlen := 'Select Idnum From S1_Ssub Where '+D_Select+'Id=@Id';
        Translate(Sqlen, '@Id', oSqry.FieldByName('Id').AsString);
        p_Idnum:=StrToIntDef(Base10.Seek_Name(Sqlen),0);
        frReport21_01.FindObject('Memo58_1').Memo.Text:=
        FormatFloat('###,###,##0',p_Idnum);
        if frReport21_01.FindObject('Memo58_2').Prop['Alignment']=10 then begin
        frReport21_01.FindObject('Memo58_2').Memo.Text:=
        FormatFloat('###,###,##0',p_Idnum);
        end;
      end;

    end;

    Exit;
  end;
end;

procedure TTong60.frReport21_20(Str: String);
var
  p_Scode,p_Gdate,p_Hcode,p_Gcode,p_Gname,p_Gubun,p_Jubun,p_Gjisa: String;
  p_GsumA,p_GsumB: Double;
  p_Spage,p_Pages: Integer;
begin

  p_Spage:=0; p_Pages:=0; p_GsumA:=0; p_GsumB:=0;
  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
      (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
      (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)and(oSqry.EOF=False)Then begin
    end else begin
      p_Scode:=oSqry.FieldByName('Scode').AsString;
      p_Gdate:=oSqry.FieldByName('Gdate').AsString;
      p_Hcode:=oSqry.FieldByName('Hcode').AsString;
      p_Gcode:=oSqry.FieldByName('Gcode').AsString;
      p_Gubun:=oSqry.FieldByName('Gubun').AsString;
      p_Jubun:=oSqry.FieldByName('Jubun').AsString;
      p_Gjisa:=oSqry.FieldByName('Gjisa').AsString;
      While(oSqry.EOF=False)and
        (oSqry.FieldByName('Gdate').AsString=p_Gdate)and
        (oSqry.FieldByName('Hcode').AsString=p_Hcode)and
        (oSqry.FieldByName('Gcode').AsString=p_Gcode)and
        (oSqry.FieldByName('Gubun').AsString=p_Gubun)and
        (oSqry.FieldByName('Jubun').AsString=p_Jubun)and
        (oSqry.FieldByName('Gjisa').AsString=p_Gjisa)do begin
        p_GsumA:=p_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
        p_GsumB:=p_GsumB+oSqry.FieldByName('Gssum').AsInteger;
        p_Pages:=p_Pages+1;
        oSqry.Next;
      end;
      if oSqry.RecordCount=1 then
      oSqry.MoveBy(-1) else
      if(oSqry.EOF=False)Then
      oSqry.MoveBy(-p_Pages) else
      oSqry.MoveBy(-p_Pages+1);
      if(oSqry.EOF=True)and(p_Pages=1)Then begin
      oSqry.MoveBy(-1);
      oSqry.MoveBy( 1);
      end;
    end;

    p_Scode:=oSqry.FieldByName('Scode').AsString;
    p_Gname:=oSqry.FieldByName('Gname').AsString;;

    if p_Scode='X' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2 From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    if p_Scode='Y' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2 From G2_Ggwo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    if p_Scode='Z' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2 From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', '');
    end;
    //--//
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data = 'NODATA' then begin
    if p_Scode='X' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2 From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    if p_Scode='Y' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2 From G2_Ggwo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    if p_Scode='Z' Then begin
      Sqlen := 'Select Gname,Gtel1,Gtel2 From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', p_Gcode);
      Translate(Sqlen, '@Hcode', p_Hcode);
    end;
    end;
    //--//

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      p_Gname:=Base10.Socket.GetData(1, 1);
    end;

    if oSqry.FieldByName('Gjisa').AsString<>'' then
    p_Gname:=Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'2')+
    p_Gname+ Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'1');

    Tong40._Gg_Magn_('7');
    with frReport21_01 do begin
      FindObject('Memo61_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gdate').AsString);
      FindObject('Memo62_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gubun').AsString);
      FindObject('Memo64_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gcode').AsString);
      FindObject('Memo65_1').Memo.Text:=AutoFrx(p_Gname);
      FindObject('Memo66_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumA);
      if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
        FindObject('Memo67_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end else begin
        if oSqry.FieldByName('Gcode').AsString<'9' then
        FindObject('Memo67_1').Memo.Text:=FormatFloat('###,###,##0',p_GsumB);
      end;
    end;

    Sqlen := 'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Gtel1,Gtel2,Gfax1,Gfax2 From G7_Ggeo '+
             'Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', p_Hcode);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      with frReport21_01 do begin
      FindObject('Memo81_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
      FindObject('Memo82_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
      FindObject('Memo83_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
      FindObject('Memo84_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                    ' '+AutoFrx(Base10.Socket.GetData(1, 5));
      FindObject('Memo85_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 7));
      FindObject('Memo86_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 9));
      FindObject('Memo81_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
      FindObject('Memo82_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 2));
      FindObject('Memo83_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 3));
      FindObject('Memo84_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 4))+
                                    ' '+AutoFrx(Base10.Socket.GetData(1, 5));
      FindObject('Memo85_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 6))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 7));
      FindObject('Memo86_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 8))+
                                    ')'+AutoFrx(Base10.Socket.GetData(1, 9));
      end;
    end;

    Exit;
  end;
end;

procedure TTong60.frReport20_01BeginPage(pgNo: Integer);
begin
  if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
    (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
    (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
    (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
    (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
    (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and
    (oSqry.EOF=False)and(v_Count<>1)then begin
  end else begin
    if(v_Count<>1)then
    frReport20_10('1');
  end;
  with frReport20_01 do begin
    v_Page1:=v_Page1+1;
    FindObject('Memo63_1').Memo.Text:=IntToStr(v_Page1)+'/'+IntToStr(v_Page2);
    FindObject('Memo63_2').Memo.Text:=IntToStr(v_Page1)+'/'+IntToStr(v_Page2);
  end;
end;

procedure TTong60.frReport20_01GetValue(const ParName: String;
  var ParValue: Variant);
var  p_Spage,p_Pages: Integer;
     p_Gqut1,p_Gqut2,p_Gqut3: Integer;
begin
  if ParName = 'Pubun1' then begin
     ParValue := oSqry.FieldByName('Pubun').AsString;

     if(oSqry.EOF=False)and(v_Count<>1)then begin
       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and(oSqry.EOF=False)Then begin
       end else begin
         v_Count:=1; v_Spage:=0; v_Pages:=0;
         v_Sline:=0; v_GsumA:=0; v_GsumB:=0; v_GsumC:=0;
         p_Gqut1:=0; p_Gqut2:=0; p_Gqut3:=0; v_Gqut1:=0; v_Gqut2:=0;
         W_Count:=0;

         v_Scode:=oSqry.FieldByName('Scode').AsString;
         v_Gdate:=oSqry.FieldByName('Gdate').AsString;
         v_Hcode:=oSqry.FieldByName('Hcode').AsString;
         v_Gcode:=oSqry.FieldByName('Gcode').AsString;
         v_Gubun:=oSqry.FieldByName('Gubun').AsString;
         v_Jubun:=oSqry.FieldByName('Jubun').AsString;
         v_Gjisa:=oSqry.FieldByName('Gjisa').AsString;
         While(oSqry.EOF=False)and
           (oSqry.FieldByName('Gdate').AsString=v_Gdate)and
           (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
           (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
           (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
           (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
           (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)do begin

           if(Base10.Database.Database='book_07_db')then begin
             Sqlen := 'Select Gqut1,Gqut2 From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               p_Gqut2:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 2)),0);
               v_Gqut2:=v_Gqut2+(p_Gqut2*oSqry.FieldByName('Gsqut').Value);
             end;
           end;

           v_Pages:=v_Pages+1;
           oSqry.Next;
         end;
         if oSqry.RecordCount=1 then
         oSqry.MoveBy(-1) else
         if(oSqry.EOF=False)Then
         oSqry.MoveBy(-v_Pages) else
         oSqry.MoveBy(-v_Pages+1);
         if(oSqry.EOF=True)and(v_Pages=1)Then begin
         oSqry.MoveBy(-1);
         oSqry.MoveBy( 1);
         end;
       end;
     end;

     if(v_Sline<RBand)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and
         (oSqry.EOF=False)Then begin

         with frReport20_01 do begin
           FindObject('Memo31_1').Memo.Text:=IntToStr((v_Page1*RBand)-RBand+v_Sline);
           if gCompany_name = '해피데이' then
             FindObject('Memo22_1').Memo.Text:=AutoFrx(oSqry.FieldByName('gpost').AsString)
           else
             FindObject('Memo22_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Bcode').AsString);

           FindObject('Memo23_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Bname').AsString);
         //FindObject('Memo24_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Ocode').AsString);
           FindObject('Memo25_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gsqut').Value);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo26_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_1').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo26_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_1').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
             end;
           end;
           FindObject('Memo29_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gbigo').AsString);

           if(Base10.Database.Database='book_07_db')then begin
             FindObject('Memo31_1').Memo.Text:='';
             Sqlen := 'Select Gqut1,Gqut2 From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               p_Gqut1:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 1)),0);
             //p_Gqut2:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 2)),0);
             //v_Gqut2:=v_Gqut2+(p_Gqut2*oSqry.FieldByName('Gsqut').Value);
               if (oSqry.FieldByName('Gsqut').Value<>0) and (p_Gqut1<>0) then begin
                 p_Gqut3:=Trunc(oSqry.FieldByName('Gsqut').Value/p_Gqut1);
                 if (oSqry.FieldByName('Gsqut').Value mod p_Gqut1) > 0 then
                 p_Gqut3:=p_Gqut3+1;
                 FindObject('Memo31_1').Memo.Text:=IntToStr(p_Gqut3);
                 v_Gqut1:=v_Gqut1+p_Gqut3;
               end;
             end;
           end;

           if FindObject('Memo24_1').Visible=True then
           if FindObject('Memo24_1').Prop['Alignment']=9 then begin
             if oSqry.FieldByName('Grat1').Value=0 Then
             FindObject('Memo24_1').Memo.Text:=
             FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value)
             else
             FindObject('Memo24_1').Memo.Text:=
             FormatFloat('###,###,##0',(oSqry.FieldByName('Gdang').AsFloat*oSqry.FieldByName('Grat1').AsFloat)/100);
           end else
           if FindObject('Memo24_1').Prop['Alignment']=11 then begin
           { Sqlen := 'Select Gpost From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end; }
             if((Base10.Database.Database='book_01_db')and(Base10.Database.Host='115.68.7.138'))then
             FindObject('Memo24_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gpost').AsString)
             else
             FindObject('Memo24_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gpost').AsString);
           end else begin
             Sqlen := 'Select Gjeja From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo29_1').Visible=True then
           if FindObject('Memo29_1').Prop['Alignment']=10 then
             FindObject('Memo29_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Pubun').AsString)
           else
           if FindObject('Memo29_1').Prop['Alignment']=11 then
           if oSqry.FieldByName('Gbigo').AsString='' then begin
             Sqlen := 'Select Jubun From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo29_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

         end;

         v_GsumA:=v_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
         v_GsumB:=v_GsumB+oSqry.FieldByName('Gssum').AsInteger;
         v_GsumC:=v_GsumC+(oSqry.FieldByName('Gdang').AsInteger*oSqry.FieldByName('Gsqut').AsInteger);

         v_Spage:=v_Spage+1;
         oSqry.Next;
       end else begin
         if(v_Sline<RBand+1)then
         with frReport20_01 do begin
           ParValue := '';
           FindObject('Memo31_1').Memo.Text:='';
           FindObject('Memo22_1').Memo.Text:='';
           FindObject('Memo23_1').Memo.Text:='';
           FindObject('Memo24_1').Memo.Text:='';
           FindObject('Memo25_1').Memo.Text:='';
           FindObject('Memo26_1').Memo.Text:='';
           FindObject('Memo27_1').Memo.Text:='';
           FindObject('Memo28_1').Memo.Text:='';
           FindObject('Memo29_1').Memo.Text:='';
         end;

         if(v_Sline=RBand)and
           (frReport20_01.FindObject('Memo21_2').Visible=False)then begin
           v_Count:=0;
           v_Scode:='1';
           v_Gdate:='1';
           v_Gcode:='1';
           v_Gubun:='1';
           v_Jubun:='1';
         end;

       end;

       if(v_Sline=RBand)then begin
         with frReport20_01 do begin
           if(Base10.Database.Database='book_07_db')then begin
           FindObject('Memo32_1').Memo.Text:=FormatFloat('###,###,##0',v_Gqut1);
         //FindObject('Memo32_2').Memo.Text:=FormatFloat('###,###,##0',v_Gqut1);
           FindObject('Memo33_1').Memo.Text:=FormatFloat('###,###,##0',v_Gqut2);
         //FindObject('Memo33_2').Memo.Text:=FormatFloat('###,###,##0',v_Gqut2);
           end;

           if(Base10.Database.Database='book_03_db')then begin
             if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo32_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumC);
             FindObject('Memo32_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumC);
             end;
           end;

           FindObject('Memo35_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           FindObject('Memo35_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo38_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
             FindObject('Memo38_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo38_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
             FindObject('Memo38_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
             end;
           end;
         end;
         if(oSqry.EOF=True)Then v_Spage:=v_Spage-1;

         if(v_Sline=RBand)and
           (frReport20_01.FindObject('Memo21_2').Visible=False)then begin
            v_Sline:=0;
            v_Spage:=0;
            v_GsumA:=0;
            v_GsumB:=0;
            v_GsumC:=0;
         end else
         oSqry.MoveBy(-v_Spage);
         v_Sline:=0;

       end;
     end;
  end else
  if ParName = 'Pubun3' then begin
     ParValue := oSqry.FieldByName('Pubun').AsString;

     if(v_Sline<RBand)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and(W_Count<>1)then begin

         with frReport20_01 do begin
           FindObject('Memo31_3').Memo.Text:=IntToStr((v_Page1*RBand)-RBand+v_Sline);
           FindObject('Memo22_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Bcode').AsString);
           FindObject('Memo23_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Bname').AsString);
         //FindObject('Memo24_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Ocode').AsString);
           FindObject('Memo25_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gsqut').Value);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo26_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Grat1').AsString);
             FindObject('Memo28_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo26_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Grat1').AsString);
             FindObject('Memo28_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
             end;
           end;
           FindObject('Memo29_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Gbigo').AsString);

           if(Base10.Database.Database='book_07_db')then begin
             FindObject('Memo31_3').Memo.Text:='';
             Sqlen := 'Select Gqut1,Gqut2 From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               p_Gqut1:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 1)),0);
             //p_Gqut2:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 2)),0);
             //v_Gqut2:=v_Gqut2+(p_Gqut2*oSqry.FieldByName('Gsqut').Value);
               if (oSqry.FieldByName('Gsqut').Value<>0) and (p_Gqut1<>0) then begin
                 p_Gqut3:=Trunc(oSqry.FieldByName('Gsqut').Value/p_Gqut1);
                 if (oSqry.FieldByName('Gsqut').Value mod p_Gqut1) > 0 then
                 p_Gqut3:=p_Gqut3+1;
                 FindObject('Memo31_3').Memo.Text:=IntToStr(p_Gqut3);
                 v_Gqut1:=v_Gqut1+p_Gqut3;
               end;
             end;
           end;

           if FindObject('Memo24_3').Visible=True then
           if FindObject('Memo24_3').Prop['Alignment']=9 then begin
             if oSqry.FieldByName('Grat1').Value=0 Then
             FindObject('Memo24_3').Memo.Text:=
             FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value)
             else
             FindObject('Memo24_3').Memo.Text:=
             FormatFloat('###,###,##0',(oSqry.FieldByName('Gdang').AsFloat*oSqry.FieldByName('Grat1').AsFloat)/100);
           end else
           if FindObject('Memo24_3').Prop['Alignment']=11 then begin
           { Sqlen := 'Select Gpost From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end; }
             FindObject('Memo24_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Gpost').AsString);
           end else begin
             Sqlen := 'Select Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo29_3').Visible=True then
           if FindObject('Memo29_3').Prop['Alignment']=10 then
             FindObject('Memo29_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Pubun').AsString)
           else
           if FindObject('Memo29_3').Prop['Alignment']=11 then
           if oSqry.FieldByName('Gbigo').AsString='' then begin
             Sqlen := 'Select Jubun From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo29_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo29_3').Visible=True then
           if FindObject('Memo29_3').Prop['Alignment']=9 then begin
             Sqlen := 'Select Gbjil From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo29_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

         end;


       //v_Spage:=v_Spage+1;
         oSqry.Next;

         if(oSqry.EOF=True)Then W_Count:=1;

       end else begin
         if(v_Sline<RBand+1)then
         with frReport20_01 do begin
           ParValue := '';
           FindObject('Memo31_3').Memo.Text:='';
           FindObject('Memo22_3').Memo.Text:='';
           FindObject('Memo23_3').Memo.Text:='';
           FindObject('Memo24_3').Memo.Text:='';
           FindObject('Memo25_3').Memo.Text:='';
           FindObject('Memo26_3').Memo.Text:='';
           FindObject('Memo27_3').Memo.Text:='';
           FindObject('Memo28_3').Memo.Text:='';
           FindObject('Memo29_3').Memo.Text:='';
         end;

         if(v_Sline=RBand)and
           (frReport20_01.FindObject('Memo21_2').Visible=False)then begin
           v_Count:=0;
           v_Scode:='@';
           v_Gdate:='@';
           v_Gcode:='@';
           v_Gubun:='@';
           v_Jubun:='@';
           v_Gjisa:='@';
         end;

       end;

       if(v_Sline=RBand)then begin
       { with frReport20_01 do begin
           FindObject('Memo35_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           FindObject('Memo38_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
           FindObject('Memo35_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           FindObject('Memo38_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
         end;
         if(oSqry.EOF=True)Then v_Spage:=v_Spage-1; }

         if(v_Sline=RBand)and
           (frReport20_01.FindObject('Memo21_2').Visible=False)then begin
            v_Sline:=0;
            v_Spage:=0;
            v_GsumA:=0;
            v_GsumB:=0;
            v_GsumC:=0;
         end else
         oSqry.MoveBy(-v_Spage);
         v_Sline:=0;
       end;
     end;
  end
  else if ParName = 'Pubun2' then begin
     ParValue := oSqry.FieldByName('Pubun').AsString;

     if(v_Sline<RBand)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)Then begin

         with frReport20_01 do begin
           FindObject('Memo31_2').Memo.Text:=IntToStr((v_Page1*RBand)-RBand+v_Sline);
           FindObject('Memo22_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Bcode').AsString);
           FindObject('Memo23_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Bname').AsString);
         //FindObject('Memo24_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Ocode').AsString);
           FindObject('Memo25_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gsqut').Value);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo26_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_2').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo26_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_2').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
             end;
           end;
           if gCompany_name = '해피데이' then
             FindObject('Memo29_2').Memo.Text:=AutoFrx(oSqry.FieldByName('opost').AsString)
           else
             FindObject('Memo29_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gbigo').AsString);

           if(Base10.Database.Database='book_07_db')then begin
             FindObject('Memo31_2').Memo.Text:='';
             Sqlen := 'Select Gqut1,Gqut2 From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               p_Gqut1:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 1)),0);
             //p_Gqut2:=StrToIntDef(AutoFrx(Base10.Socket.GetData(1, 2)),0);
             //v_Gqut2:=v_Gqut2+(p_Gqut2*oSqry.FieldByName('Gsqut').Value);
               if (oSqry.FieldByName('Gsqut').Value<>0) and (p_Gqut1<>0) then begin
                 p_Gqut3:=Trunc(oSqry.FieldByName('Gsqut').Value/p_Gqut1);
                 if (oSqry.FieldByName('Gsqut').Value mod p_Gqut1) > 0 then
                 p_Gqut3:=p_Gqut3+1;
                 FindObject('Memo31_2').Memo.Text:=IntToStr(p_Gqut3);
                 v_Gqut1:=v_Gqut1+p_Gqut3;
               end;
             end;
           end;

           if FindObject('Memo24_2').Visible=True then
           if FindObject('Memo24_2').Prop['Alignment']=9 then begin
             if oSqry.FieldByName('Grat1').Value=0 Then
             FindObject('Memo24_2').Memo.Text:=
             FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value)
             else
             FindObject('Memo24_2').Memo.Text:=
             FormatFloat('###,###,##0',(oSqry.FieldByName('Gdang').AsFloat*oSqry.FieldByName('Grat1').AsFloat)/100);
           end else
           if FindObject('Memo24_2').Prop['Alignment']=11 then begin
           { Sqlen := 'Select Gpost From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end; }
             if((Base10.Database.Database='book_01_db')and(Base10.Database.Host='115.68.7.138'))then
             FindObject('Memo24_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Opost').AsString)
             else
             FindObject('Memo24_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gpost').AsString);
           end else begin
             Sqlen := 'Select Gjeja From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;
         end;

       //v_Spage:=v_Spage+1;
         oSqry.Next;

         if(oSqry.FieldByName('Gdate').AsString<>v_Gdate)or
           (oSqry.FieldByName('Hcode').AsString<>v_Hcode)or
           (oSqry.FieldByName('Gcode').AsString<>v_Gcode)or
           (oSqry.FieldByName('Gubun').AsString<>v_Gubun)or
           (oSqry.FieldByName('Jubun').AsString<>v_Jubun)or
           (oSqry.FieldByName('Gjisa').AsString<>v_Gjisa)Then begin
           v_Count:=0;
           v_Scode:='@';
           v_Gdate:='@';
           v_Hcode:='@';
           v_Gcode:='@';
           v_Gubun:='@';
           v_Jubun:='@';
           v_Gjisa:='@';
         end;

         if(oSqry.EOF=True)Then
         begin
           v_Count:=0;
           v_Scode:='1';
           v_Gdate:='1';
           v_Hcode:='1';
           v_Gcode:='1';
           v_Gubun:='1';
           v_Jubun:='1';
           v_Gjisa:='1';
         end;
       end else begin
         if(v_Sline<RBand+1)then
         with frReport20_01 do begin
           ParValue := '';
           FindObject('Memo31_2').Memo.Text:='';
           FindObject('Memo22_2').Memo.Text:='';
           FindObject('Memo23_2').Memo.Text:='';
           FindObject('Memo24_2').Memo.Text:='';
           FindObject('Memo25_2').Memo.Text:='';
           FindObject('Memo26_2').Memo.Text:='';
           FindObject('Memo27_2').Memo.Text:='';
           FindObject('Memo28_2').Memo.Text:='';
           FindObject('Memo29_2').Memo.Text:='';
         end;
         if(v_Sline=RBand)then begin
           v_Count:=0;
           v_Scode:='1';
           v_Gdate:='1';
           v_Hcode:='1';
           v_Gcode:='1';
           v_Gubun:='1';
           v_Jubun:='1';
           v_Gjisa:='1';
         end;
       end;
       if(v_Sline=RBand)then begin
          v_Sline:=0;
          v_Spage:=0;
          v_GsumA:=0;
          v_GsumB:=0;
          v_GsumC:=0;
       end;
     end;
  end;
end;

procedure TTong60.frReport21_01BeginPage(pgNo: Integer);
begin
  if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
    (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
    (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
    (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
    (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
    (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and
    (oSqry.EOF=False)and(v_Count<>1)then begin
  end else begin
    if(v_Count<>1)then
    frReport21_10('1');
  end;
  with frReport21_01 do begin
    v_Page1:=v_Page1+1;
    FindObject('Memo63_1').Memo.Text:=IntToStr(v_Page1)+'/'+IntToStr(v_Page2);
    FindObject('Memo63_2').Memo.Text:=IntToStr(v_Page1)+'/'+IntToStr(v_Page2);
  end;
end;

procedure TTong60.frReport21_01GetValue(const ParName: String;
  var ParValue: Variant);
begin
  if ParName = 'Pubun1' then begin
     ParValue := oSqry.FieldByName('Pubun').AsString;

     if(oSqry.EOF=False)and(v_Count<>1)then begin
       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and(oSqry.EOF=False)Then begin
       end else begin
         v_Count:=1; v_Spage:=0; v_Pages:=0;
         v_Sline:=0; v_GsumA:=0; v_GsumB:=0; v_GsumC:=0;
         W_Count:=1;

         v_Scode:=oSqry.FieldByName('Scode').AsString;
         v_Gdate:=oSqry.FieldByName('Gdate').AsString;
         v_Hcode:=oSqry.FieldByName('Hcode').AsString;
         v_Gcode:=oSqry.FieldByName('Gcode').AsString;
         v_Gubun:=oSqry.FieldByName('Gubun').AsString;
         v_Jubun:=oSqry.FieldByName('Jubun').AsString;
         v_Gjisa:=oSqry.FieldByName('Gjisa').AsString;
         While(oSqry.EOF=False)and
           (oSqry.FieldByName('Gdate').AsString=v_Gdate)and
           (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
           (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
           (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
           (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
           (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)do begin
           v_Pages:=v_Pages+1;
           oSqry.Next;
         end;
         if oSqry.RecordCount=1 then
         oSqry.MoveBy(-1) else
         if(oSqry.EOF=False)Then
         oSqry.MoveBy(-v_Pages) else
         oSqry.MoveBy(-v_Pages+1);
         if(oSqry.EOF=True)and(v_Pages=1)Then begin
         oSqry.MoveBy(-1);
         oSqry.MoveBy( 1);
         end;
       end;
     end;

     if(v_Sline<RBand)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and
         (oSqry.EOF=False)Then begin

         with frReport21_01 do begin
           FindObject('Memo22_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Bcode').AsString);
           FindObject('Memo23_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Bname').AsString);
         //FindObject('Memo24_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Ocode').AsString);
           FindObject('Memo25_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gsqut').Value);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo26_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_1').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo26_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_1').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_1').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
             end;
           end;
           FindObject('Memo29_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gbigo').AsString);

           if FindObject('Memo22_1').Prop['Alignment']=10 then begin
             Sqlen := 'Select Gisbn From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo22_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo24_1').Visible=True then
           if FindObject('Memo24_1').Prop['Alignment']=9 then begin
             if oSqry.FieldByName('Grat1').Value=0 Then
             FindObject('Memo24_1').Memo.Text:=
             FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value)
             else
             FindObject('Memo24_1').Memo.Text:=
             FormatFloat('###,###,##0',(oSqry.FieldByName('Gdang').AsFloat*oSqry.FieldByName('Grat1').AsFloat)/100);
           end else
           if FindObject('Memo24_1').Prop['Alignment']=11 then begin
           { Sqlen := 'Select Gpost From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end; }
             FindObject('Memo24_1').Memo.Text:=AutoFrx(oSqry.FieldByName('Gpost').AsString);
           end else begin
             Sqlen := 'Select Gjeja From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_1').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;
         end;

         v_GsumA:=v_GsumA+oSqry.FieldByName('Gsqut').AsInteger;
         v_GsumB:=v_GsumB+oSqry.FieldByName('Gssum').AsInteger;
         v_GsumC:=v_GsumC+(oSqry.FieldByName('Gdang').AsInteger*oSqry.FieldByName('Gsqut').AsInteger);

         v_Spage:=v_Spage+1;
         oSqry.Next;
       end else begin
         if(v_Sline<RBand+1)then
         with frReport21_01 do begin
           ParValue := '';
           FindObject('Memo22_1').Memo.Text:='';
           FindObject('Memo23_1').Memo.Text:='';
           FindObject('Memo24_1').Memo.Text:='';
           FindObject('Memo25_1').Memo.Text:='';
           FindObject('Memo26_1').Memo.Text:='';
           FindObject('Memo27_1').Memo.Text:='';
           FindObject('Memo28_1').Memo.Text:='';
           FindObject('Memo29_1').Memo.Text:='';
         end;
       end;

       if(v_Sline=RBand)then begin
         with frReport21_01 do begin
           if(Base10.Database.Database='book_03_db')then begin
             if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo32_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumC);
             FindObject('Memo32_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumC);
             end;
           end;

           FindObject('Memo35_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           FindObject('Memo35_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo38_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
             FindObject('Memo38_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo38_1').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
             FindObject('Memo38_2').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
             end;
           end;
         end;
         if(oSqry.EOF=True)Then v_Spage:=v_Spage-1;
         oSqry.MoveBy(-v_Spage);
         v_Sline:=0;
       end;
     end;
  end else
  if ParName = 'Pubun3' then begin
     ParValue := oSqry.FieldByName('Pubun').AsString;

     if(v_Sline<RBand)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)and(W_Count<>1)Then begin

         with frReport21_01 do begin
           FindObject('Memo22_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Bcode').AsString);
           FindObject('Memo23_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Bname').AsString);
         //FindObject('Memo24_3').Memo.Text:=oSqry.FieldByName('Ocode').AsString;
           FindObject('Memo25_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gsqut').Value);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo26_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_3').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo26_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_3').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_3').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
             end;
           end;
           FindObject('Memo29_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Gbigo').AsString);

           if FindObject('Memo22_3').Prop['Alignment']=10 then begin
             Sqlen := 'Select Gisbn From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo22_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo24_3').Visible=True then
           if FindObject('Memo24_3').Prop['Alignment']=9 then begin
             if oSqry.FieldByName('Grat1').Value=0 Then
             FindObject('Memo24_3').Memo.Text:=
             FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value)
             else
             FindObject('Memo24_3').Memo.Text:=
             FormatFloat('###,###,##0',(oSqry.FieldByName('Gdang').AsFloat*oSqry.FieldByName('Grat1').AsFloat)/100);
           end else
           if FindObject('Memo24_3').Prop['Alignment']=11 then begin
           { Sqlen := 'Select Gpost From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end; }
             FindObject('Memo24_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Gpost').AsString);
           end else begin
             Sqlen := 'Select Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo29_3').Visible=True then
           if FindObject('Memo29_3').Prop['Alignment']=10 then
             FindObject('Memo29_3').Memo.Text:=AutoFrx(oSqry.FieldByName('Pubun').AsString)
           else
           if FindObject('Memo29_3').Prop['Alignment']=11 then
           if oSqry.FieldByName('Gbigo').AsString='' then begin
             Sqlen := 'Select Jubun From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo29_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo29_3').Visible=True then
           if FindObject('Memo29_3').Prop['Alignment']=9 then begin
             Sqlen := 'Select Gbjil From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo29_3').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

         end;

       //v_Spage:=v_Spage+1;
         oSqry.Next;

         if(oSqry.EOF=True)Then W_Count:=1;

       end else begin
         if(v_Sline<RBand+1)then
         with frReport21_01 do begin
           ParValue := '';
           FindObject('Memo22_3').Memo.Text:='';
           FindObject('Memo23_3').Memo.Text:='';
           FindObject('Memo24_3').Memo.Text:='';
           FindObject('Memo25_3').Memo.Text:='';
           FindObject('Memo26_3').Memo.Text:='';
           FindObject('Memo27_3').Memo.Text:='';
           FindObject('Memo28_3').Memo.Text:='';
           FindObject('Memo29_3').Memo.Text:='';
         end;

         if(v_Sline=RBand)and
           (frReport20_01.FindObject('Memo21_2').Visible=False)then begin
           v_Count:=0;
           v_Scode:='@';
           v_Gdate:='@';
           v_Gcode:='@';
           v_Gubun:='@';
           v_Jubun:='@';
           v_Gjisa:='@';
         end;

       end;

       if(v_Sline=RBand)then begin
       { with frReport21_01 do begin
           FindObject('Memo35_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           FindObject('Memo38_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
           FindObject('Memo35_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumA);
           FindObject('Memo38_3').Memo.Text:=FormatFloat('###,###,##0',v_GsumB);
         end;
         if(oSqry.EOF=True)Then v_Spage:=v_Spage-1; }

         if(v_Sline=RBand)and
           (frReport21_01.FindObject('Memo21_2').Visible=False)then begin
            v_Sline:=0;
            v_Spage:=0;
            v_GsumA:=0;
            v_GsumB:=0;
            v_GsumC:=0;
         end else
         oSqry.MoveBy(-v_Spage);
         v_Sline:=0;
       end;
     end;
  end else
  if ParName = 'Pubun2' then begin
     ParValue := oSqry.FieldByName('Pubun').AsString;

     if(v_Sline<RBand)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gdate').AsString=v_Gdate)and
         (oSqry.FieldByName('Hcode').AsString=v_Hcode)and
         (oSqry.FieldByName('Gcode').AsString=v_Gcode)and
         (oSqry.FieldByName('Gubun').AsString=v_Gubun)and
         (oSqry.FieldByName('Jubun').AsString=v_Jubun)and
         (oSqry.FieldByName('Gjisa').AsString=v_Gjisa)Then begin

         with frReport21_01 do begin
           FindObject('Memo22_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Bcode').AsString);
           FindObject('Memo23_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Bname').AsString);
         //FindObject('Memo24_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Ocode').AsString);
           FindObject('Memo25_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gsqut').Value);
           if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([oSqry.FieldByName('Hcode').AsString,'pintx']),[loCaseInsensitive])=false then begin
             FindObject('Memo26_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_2').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           end else begin
             if oSqry.FieldByName('Gcode').AsString<'9' then begin
             FindObject('Memo26_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value);
             FindObject('Memo27_2').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
             FindObject('Memo28_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
             end;
           end;
           FindObject('Memo29_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gbigo').AsString);

           if FindObject('Memo22_2').Prop['Alignment']=10 then begin
             Sqlen := 'Select Gisbn From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo22_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;

           if FindObject('Memo24_2').Visible=True then
           if FindObject('Memo24_2').Prop['Alignment']=9 then begin
             if oSqry.FieldByName('Grat1').Value=0 Then
             FindObject('Memo24_2').Memo.Text:=
             FormatFloat('###,###,##0',oSqry.FieldByName('Gdang').Value)
             else
             FindObject('Memo24_2').Memo.Text:=
             FormatFloat('###,###,##0',(oSqry.FieldByName('Gdang').AsFloat*oSqry.FieldByName('Grat1').AsFloat)/100);
           end else
           if FindObject('Memo24_2').Prop['Alignment']=11 then begin
           { Sqlen := 'Select Gpost From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end; }
             FindObject('Memo24_2').Memo.Text:=AutoFrx(oSqry.FieldByName('Gpost').AsString);
           end else begin
             Sqlen := 'Select Gjeja From G4_Book '+
                      'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
             Translate(Sqlen, '@Gcode', oSqry.FieldByName('Bcode').AsString);
             Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);

             Base10.Socket.RunSQL(Sqlen);
             Base10.Socket.busyloop;
             if Base10.Socket.Body_Data <> 'NODATA' then begin
               Base10.Socket.MakeData;
               FindObject('Memo24_2').Memo.Text:=AutoFrx(Base10.Socket.GetData(1, 1));
             end;
           end;
         end;

       //v_Spage:=v_Spage+1;
         oSqry.Next;

         if(oSqry.FieldByName('Gdate').AsString<>v_Gdate)or
           (oSqry.FieldByName('Hcode').AsString<>v_Hcode)or
           (oSqry.FieldByName('Gcode').AsString<>v_Gcode)or
           (oSqry.FieldByName('Gubun').AsString<>v_Gubun)or
           (oSqry.FieldByName('Jubun').AsString<>v_Jubun)or
           (oSqry.FieldByName('Gjisa').AsString<>v_Gjisa)Then begin
           v_Count:=0;
           v_Scode:='@';
           v_Gdate:='@';
           v_Hcode:='@';
           v_Gcode:='@';
           v_Gubun:='@';
           v_Jubun:='@';
           v_Gjisa:='@';
         end;

         if(oSqry.EOF=True)Then begin
           v_Count:=0;
           v_Scode:='1';
           v_Gdate:='1';
           v_Hcode:='1';
           v_Gcode:='1';
           v_Gubun:='1';
           v_Jubun:='1';
           v_Gjisa:='1';
         end;
       end else begin
         if(v_Sline<RBand+1)then
         with frReport21_01 do begin
           ParValue := '';
           FindObject('Memo22_2').Memo.Text:='';
           FindObject('Memo23_2').Memo.Text:='';
           FindObject('Memo24_2').Memo.Text:='';
           FindObject('Memo25_2').Memo.Text:='';
           FindObject('Memo26_2').Memo.Text:='';
           FindObject('Memo27_2').Memo.Text:='';
           FindObject('Memo28_2').Memo.Text:='';
           FindObject('Memo29_2').Memo.Text:='';
         end;
         if(v_Sline=RBand)then begin
           v_Count:=0;
           v_Scode:='1';
           v_Gdate:='1';
           v_Hcode:='1';
           v_Gcode:='1';
           v_Gubun:='1';
           v_Jubun:='1';
           v_Gjisa:='1';
         end;
       end;
       if(v_Sline=RBand)then begin
          v_Sline:=0;
          v_Spage:=0;
          v_GsumA:=0;
          v_GsumB:=0;
          v_GsumC:=0;
       end;
     end;
  end;
end;

procedure TTong60.frReport23_01BeginPage(pgNo: Integer);
begin
//
end;

procedure TTong60.frReport23_01GetValue(const ParName: String;
  var ParValue: Variant);
var
  p_Hcode,p_Hname,p_Gname: String;
begin
  if ParName = 'Text' then begin
     ParValue := '';

     p_Hcode:=oSqry.FieldByName('Hcode').AsString;
     p_Hname:=oSqry.FieldByName('Hname').AsString;
     p_Gname:='';

     Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where '+D_Select+
              'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
              'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
              'Scode=''@Scode'' and Hcode=''@Hcode'' and '+
              'Gjisa=''@Gjisa'' and '+
              '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
     Translate(Sqlen, '@Gdate', Sobo28.Edit101.Text);
     Translate(Sqlen, '@Gubun', '출고');
     Translate(Sqlen, '@Jubun', oSqry.FieldByName('Jubun').AsString);
     Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);
     Translate(Sqlen, '@Scode', 'X');
     Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
     Translate(Sqlen, '@Gjisa', oSqry.FieldByName('Gjisa').AsString);
     Translate(Sqlen, '@Ocode', 'B');
     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.busyloop;
     if Base10.Socket.Body_Data <> 'NODATA' then begin
       p_Gname:='1';
       Base10.Socket.MakeData;
       with Tong60.frReport23_01 do begin
         FindObject('Memo101').Memo.Text:=Base10.Socket.GetData(1, 1);
         FindObject('Memo102').Memo.Text:=Base10.Socket.GetData(1, 2);
         FindObject('Memo103').Memo.Text:=Base10.Socket.GetData(1, 3);
         FindObject('Memo104').Memo.Text:=Base10.Socket.GetData(1, 4);
         FindObject('Memo105').Memo.Text:=Base10.Socket.GetData(1, 5);
       end;
     end;

     if p_Gname='' then begin
     Sqlen := 'Select Gadd1,Gadd2,Gtel1,Gtel2,Gname,Gbigo From G1_Ggeo Where '+D_Select+
              'Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
     Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);
     Translate(Sqlen, '@Hcode', '');
     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.busyloop;
     if Base10.Socket.Body_Data <> 'NODATA' then begin
       p_Gname:='1';
       Base10.Socket.MakeData;
       with Tong60.frReport23_01 do begin
         FindObject('Memo101').Memo.Text:=Base10.Socket.GetData(1, 1);
         FindObject('Memo102').Memo.Text:=Base10.Socket.GetData(1, 2);
         FindObject('Memo103').Memo.Text:=Base10.Socket.GetData(1, 3)+'-'+Base10.Socket.GetData(1, 4);
         FindObject('Memo104').Memo.Text:=Base10.Socket.GetData(1, 6);
         FindObject('Memo105').Memo.Text:=Base10.Socket.GetData(1, 5);
       end;
     end;
     end;

     if p_Gname='' then begin
     Sqlen := 'Select Gadd1,Gadd2,Gtel1,Gtel2,Gname,Gbigo From G1_Ggeo Where '+D_Select+
              'Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
     Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);
     Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.busyloop;
     if Base10.Socket.Body_Data <> 'NODATA' then begin
       p_Gname:='1';
       Base10.Socket.MakeData;
       with Tong60.frReport23_01 do begin
         FindObject('Memo101').Memo.Text:=Base10.Socket.GetData(1, 1);
         FindObject('Memo102').Memo.Text:=Base10.Socket.GetData(1, 2);
         FindObject('Memo103').Memo.Text:=Base10.Socket.GetData(1, 3)+'-'+Base10.Socket.GetData(1, 4);
         FindObject('Memo104').Memo.Text:=Base10.Socket.GetData(1, 6);
         FindObject('Memo105').Memo.Text:=Base10.Socket.GetData(1, 5);
       end;
     end;
     end;

     Sqlen := 'Select Gadd1,Gadd2,Gtel1,Gtel2,Gname,Gbigo From G7_Ggeo Where '+D_Select+
              'Gcode=''@Gcode'' ';
     Translate(Sqlen, '@Gcode', oSqry.FieldByName('Hcode').AsString);
     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.busyloop;
     if Base10.Socket.Body_Data <> 'NODATA' then begin
       Base10.Socket.MakeData;
       with Tong60.frReport23_01 do begin
         FindObject('Memo201').Memo.Text:=Base10.Socket.GetData(1, 1);
         FindObject('Memo202').Memo.Text:=Base10.Socket.GetData(1, 2);
         FindObject('Memo203').Memo.Text:=Base10.Socket.GetData(1, 3)+'-'+Base10.Socket.GetData(1, 4);
         FindObject('Memo204').Memo.Text:=Base10.Socket.GetData(1, 6);
         FindObject('Memo205').Memo.Text:=Base10.Socket.GetData(1, 5);
       end;
     end;

  // oSqry.Next;
  end;
end;

procedure TTong60.frReport28_01BeginPage(pgNo: Integer);
begin
  if(oSqry.FieldByName('Gcode').AsString=v_Gcode)and
    (oSqry.EOF=False)Then begin
  end else begin
    Sqlen :=
    'Select Gname,Gposa,Gadd1,Gadd2,Oadd1,Oadd2,Gnumb,Gnum1 '+
    'From G3_Gjeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
    //p_Gname:=Base10.Socket.GetData(1, 1);
    end;

    Tong40._Gg_Magn_('9');
    with frReport28_01 do begin
      FindObject('Memo11_2').Memo.Text:=lSqry.FieldByName('F11').AsString;
      FindObject('Memo12_2').Memo.Text:=lSqry.FieldByName('F12').AsString;
      FindObject('Memo13_2').Memo.Text:=lSqry.FieldByName('F21').AsString;
      FindObject('Memo14_2').Memo.Text:=lSqry.FieldByName('F41').AsString;
      FindObject('Memo15_2').Memo.Text:=lSqry.FieldByName('F22').AsString+' '+
                                        lSqry.FieldByName('F31').AsString+' '+
                                        lSqry.FieldByName('F32').AsString;
      FindObject('Memo21_2').Memo.Text:=Base10.Socket.GetData(1, 1);;
      FindObject('Memo22_2').Memo.Text:=Base10.Socket.GetData(1, 7);
      FindObject('Memo23_2').Memo.Text:=Base10.Socket.GetData(1, 3)+' '+
                                        Base10.Socket.GetData(1, 4);
      FindObject('Memo24_2').Memo.Text:=Base10.Socket.GetData(1, 2);
      FindObject('Memo25_2').Memo.Text:=Base10.Socket.GetData(1, 8);
      FindObject('Memo26_2').Memo.Text:=Base10.Socket.GetData(1, 5)+' '+
                                        Base10.Socket.GetData(1, 6);
      FindObject('Memo91_2').Memo.Text:=Copy(Sobo28.Edit102.Text,1,4);
      FindObject('Memo92_2').Memo.Text:=Copy(Sobo28.Edit102.Text,6,2);
      FindObject('Memo93_2').Memo.Text:=Copy(Sobo28.Edit102.Text,9,2);
      FindObject('Memo94_2').Memo.Text:=lSqry.FieldByName('F42').AsString;
      FindObject('Memo95_2').Memo.Text:=lSqry.FieldByName('F21').AsString;
    end;
  end;
end;

procedure TTong60.frReport28_01GetValue(const ParName: String;
  var ParValue: Variant);
begin
  if ParName = 'Pubun' then begin
     ParValue := oSqry.FieldByName('Gcode').AsString;

     if(oSqry.FieldByName('Gcode').AsString=v_Gcode)and
       (oSqry.EOF=False)Then begin
     end else begin
       if(v_Sline=0)then begin
          v_Sline:=0;
          v_Gcode:=oSqry.FieldByName('Gcode').AsString;
       end;
     end;

     if(v_Sline<3)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gcode').AsString=v_Gcode)Then begin

         with frReport28_01 do begin
           FindObject('Memo41_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,1,4);
           FindObject('Memo42_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,6,2);
           FindObject('Memo43_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,9,2);
           FindObject('Memo44_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,1,4);
           FindObject('Memo45_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,6,2);
           FindObject('Memo46_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           FindObject('Memo47_2').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
           FindObject('Memo48_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gisum').Value);
           FindObject('Memo49_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gosum').Value);
           FindObject('Memo50_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gbsum').Value);
         end;

         oSqry.Next;
         if(oSqry.EOF=True)Then begin
           v_Gcode:='1';
         end;
       end else begin
         if(v_Sline<4)then
         with frReport28_01 do begin
           ParValue := '';
           FindObject('Memo41_2').Memo.Text:='';
           FindObject('Memo42_2').Memo.Text:='';
           FindObject('Memo43_2').Memo.Text:='';
           FindObject('Memo44_2').Memo.Text:='';
           FindObject('Memo45_2').Memo.Text:='';
           FindObject('Memo46_2').Memo.Text:='';
           FindObject('Memo47_2').Memo.Text:='';
           FindObject('Memo48_2').Memo.Text:='';
           FindObject('Memo49_2').Memo.Text:='';
           FindObject('Memo50_2').Memo.Text:='';
         end;
         if(v_Sline=3)then begin
           v_Gcode:='1';
         end;
       end;
       if(v_Sline=3)then begin
          v_Sline:=0;
       end;
     end;
  end;
end;

procedure TTong60.frReport28_02BeginPage(pgNo: Integer);
begin
  if(oSqry.FieldByName('Gcode').AsString=v_Gcode)and
    (oSqry.EOF=False)Then begin
  end else begin
    Sqlen :=
    'Select Gname,Gposa,Gadd1,Gadd2,Oadd1,Oadd2,Gnumb,Gnum1 '+
    'From G3_Gjeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
    //p_Gname:=Base10.Socket.GetData(1, 1);
    end;

    Tong40._Gg_Magn_('9');
    with frReport28_02 do begin
      FindObject('Memo11_2').Memo.Text:=lSqry.FieldByName('F11').AsString;
      FindObject('Memo12_2').Memo.Text:=lSqry.FieldByName('F12').AsString;
      FindObject('Memo13_2').Memo.Text:=lSqry.FieldByName('F21').AsString;
      FindObject('Memo14_2').Memo.Text:=lSqry.FieldByName('F41').AsString;
      FindObject('Memo15_2').Memo.Text:=lSqry.FieldByName('F22').AsString+' '+
                                        lSqry.FieldByName('F31').AsString+' '+
                                        lSqry.FieldByName('F32').AsString;
      FindObject('Memo21_2').Memo.Text:=Base10.Socket.GetData(1, 1);;
      FindObject('Memo22_2').Memo.Text:=Base10.Socket.GetData(1, 7);
      FindObject('Memo23_2').Memo.Text:=Base10.Socket.GetData(1, 3)+' '+
                                        Base10.Socket.GetData(1, 4);
      FindObject('Memo24_2').Memo.Text:=Base10.Socket.GetData(1, 2);
      FindObject('Memo25_2').Memo.Text:=Base10.Socket.GetData(1, 8);
      FindObject('Memo26_2').Memo.Text:=Base10.Socket.GetData(1, 5)+' '+
                                        Base10.Socket.GetData(1, 6);
      FindObject('Memo91_2').Memo.Text:=Copy(Sobo28.Edit102.Text,1,4);
      FindObject('Memo92_2').Memo.Text:=Copy(Sobo28.Edit102.Text,6,2);
      FindObject('Memo93_2').Memo.Text:=Copy(Sobo28.Edit102.Text,9,2);
      FindObject('Memo94_2').Memo.Text:=lSqry.FieldByName('F42').AsString;
      FindObject('Memo95_2').Memo.Text:=lSqry.FieldByName('F21').AsString;
    end;
  end;
end;

procedure TTong60.frReport28_02GetValue(const ParName: String;
  var ParValue: Variant);
begin
  if ParName = 'Pubun' then begin
     ParValue := oSqry.FieldByName('Gcode').AsString;

     if(oSqry.FieldByName('Gcode').AsString=v_Gcode)and
       (oSqry.EOF=False)Then begin
     end else begin
       if(v_Sline=0)then begin
          v_Sline:=0;
          v_Gcode:=oSqry.FieldByName('Gcode').AsString;
       end;
     end;

     if(v_Sline<3)then begin
       v_Sline:=v_Sline+1;

       if(oSqry.FieldByName('Gcode').AsString=v_Gcode)Then begin

         with frReport28_02 do begin
           FindObject('Memo41_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,1,4);
           FindObject('Memo42_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,6,2);
           FindObject('Memo43_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,9,2);
           FindObject('Memo44_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,1,4);
           FindObject('Memo45_2').Memo.Text:=Copy(oSqry.FieldByName('Gdate').AsString,6,2);
           FindObject('Memo46_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gssum').Value);
           FindObject('Memo47_2').Memo.Text:=oSqry.FieldByName('Grat1').AsString;
           FindObject('Memo48_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gisum').Value);
           FindObject('Memo49_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gosum').Value);
           FindObject('Memo50_2').Memo.Text:=FormatFloat('###,###,##0',oSqry.FieldByName('Gbsum').Value);
         end;

         oSqry.Next;
         if(oSqry.EOF=True)Then begin
           v_Gcode:='1';
         end;
       end else begin
         if(v_Sline<4)then
         with frReport28_02 do begin
           ParValue := '';
           FindObject('Memo41_2').Memo.Text:='';
           FindObject('Memo42_2').Memo.Text:='';
           FindObject('Memo43_2').Memo.Text:='';
           FindObject('Memo44_2').Memo.Text:='';
           FindObject('Memo45_2').Memo.Text:='';
           FindObject('Memo46_2').Memo.Text:='';
           FindObject('Memo47_2').Memo.Text:='';
           FindObject('Memo48_2').Memo.Text:='';
           FindObject('Memo49_2').Memo.Text:='';
           FindObject('Memo50_2').Memo.Text:='';
         end;
         if(v_Sline=3)then begin
           v_Gcode:='1';
         end;
       end;
       if(v_Sline=3)then begin
          v_Sline:=0;
       end;
     end;
  end;
end;

procedure TTong60.frReport40_01BeginPage(pgNo: Integer);
begin
//
end;

procedure TTong60.frReport40_01GetValue(const ParName: String;
  var ParValue: Variant);
var
  p_Gdate,p_Gcode: String;
  p_Spage,p_Space,p_Gssum: Double;
begin
  if ParName = 'Text' then begin
     ParValue := '';

     p_Gcode:=oSqry.FieldByName('Gcode').AsString;
     if p_Total=1 Then
     p_Gssum:=oSqry.FieldByName('Gssum').AsInteger;
     if p_Total=2 Then
     p_Gssum:=oSqry.FieldByName('Gsusu').AsInteger;

     p_Space:=11-Length(FloatToStr(p_Gssum)); //공백

     p_Gdate:=Sobo49.Edit102.Text;

     Tong40._Gg_Magn_('8');
     with Tong60.frReport40_01 do begin
       FindObject('Memo202_1').Memo.Text:=lSqry.FieldByName('F11').AsString;
       FindObject('Memo204_1').Memo.Text:=lSqry.FieldByName('F12').AsString;
       FindObject('Memo206_1').Memo.Text:=lSqry.FieldByName('F21').AsString;
       FindObject('Memo208_1').Memo.Text:=lSqry.FieldByName('F22').AsString+
                                      ' '+lSqry.FieldByName('F31').AsString+
                                      ' '+lSqry.FieldByName('F32').AsString;
       FindObject('Memo210_1').Memo.Text:=lSqry.FieldByName('F41').AsString;
       FindObject('Memo212_1').Memo.Text:=lSqry.FieldByName('F42').AsString;
     end;

     if oSqry.FieldByName('Scode').AsString='X' Then begin
       Sqlen :=
       'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo,Gbigo '+
       'From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
       Translate(Sqlen, '@Gcode', p_Gcode);
     end;
     if oSqry.FieldByName('Scode').AsString='Y' Then begin
       Sqlen :=
       'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo,Gbigo '+
       'From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode''';
       Translate(Sqlen, '@Gcode', p_Gcode);
     end;
     if oSqry.FieldByName('Scode').AsString='Z' Then begin
       Sqlen :=
       'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo,Gbigo '+
       'From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
       Translate(Sqlen, '@Gcode', p_Gcode);
     end;

     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.busyloop;
     if Base10.Socket.Body_Data <> 'NODATA' then begin
       Base10.Socket.MakeData;
       with Tong60.frReport40_01 do begin
         FindObject('Memo215_1').Memo.Text:=Base10.Socket.GetData(1, 1);

         if FindObject('Memo217_1').Prop['Alignment']=10 then begin
           if Base10.Socket.GetData(1, 8)='' then
           FindObject('Memo217_1').Memo.Text:=Base10.Socket.GetData(1, 2)
           else
           FindObject('Memo217_1').Memo.Text:=Base10.Socket.GetData(1, 8);
         end else
           FindObject('Memo217_1').Memo.Text:=Base10.Socket.GetData(1, 2);

         FindObject('Memo219_1').Memo.Text:=Base10.Socket.GetData(1, 3);
         FindObject('Memo221_1').Memo.Text:=Base10.Socket.GetData(1, 4)+
                                        ' '+Base10.Socket.GetData(1, 5);
         FindObject('Memo223_1').Memo.Text:=Base10.Socket.GetData(1, 6);
         FindObject('Memo225_1').Memo.Text:=Base10.Socket.GetData(1, 7);
       end;
     end;

     with Tong60.frReport40_01 do begin
       FindObject('Memo320_1').Memo.Text:=Copy(p_Gdate,1,4);
       FindObject('Memo321_1').Memo.Text:=Copy(p_Gdate,6,2);
       FindObject('Memo322_1').Memo.Text:=Copy(p_Gdate,9,2);
       FindObject('Memo323_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Space)]),10,1);
       FindObject('Memo334_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),10,1);
       FindObject('Memo333_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),09,1);
       FindObject('Memo332_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),08,1);
       FindObject('Memo331_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),07,1);
       FindObject('Memo330_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),06,1);
       FindObject('Memo329_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),05,1);
       FindObject('Memo328_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),04,1);
       FindObject('Memo327_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),03,1);
       FindObject('Memo326_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),02,1);
       FindObject('Memo325_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gssum)]),01,1);
       FindObject('Memo407_1').Memo.Text:=Copy(p_Gdate,6,2);
       FindObject('Memo408_1').Memo.Text:=Copy(p_Gdate,9,2);
       FindObject('Memo409_1').Memo.Text:=lSqry.FieldByName('F51').AsString;
       FindObject('Memo413_1').Memo.Text:=Format('%10s',[FormatFloat('###,###,##0',p_Gssum)]);
       FindObject('Memo505_1').Memo.Text:=Format('%10s',[FormatFloat('###,###,##0',p_Gssum)]);
     end;
     oSqry.Next;
  end;
end;

procedure TTong60.frReport40_02BeginPage(pgNo: Integer);
begin
//
end;

procedure TTong60.frReport40_02GetValue(const ParName: String;
  var ParValue: Variant);
var
  p_Gdate,p_Gcode: String;
  p_Spage,p_Space,p_Gosum,p_Gbsum,p_Gssum: Double;
begin
  if ParName = 'Text' then begin
     ParValue := '';

     p_Gcode:=oSqry.FieldByName('Gcode').AsString;
     if p_Total=1 Then
     p_Gssum:=oSqry.FieldByName('Gssum').AsInteger;
     if p_Total=2 Then
     p_Gssum:=oSqry.FieldByName('Gsusu').AsInteger;

     p_Gosum:=oSqry.FieldByName('Gosum').AsInteger;
     p_Gbsum:=oSqry.FieldByName('Gbsum').AsInteger;
     p_Gssum:=oSqry.FieldByName('Gssum').AsInteger;

     p_Space:=11-Length(FloatToStr(p_Gosum)); //공백

     p_Gdate:=oSqry.FieldByName('Gdate').AsString;

   { Tong40._Gg_Magn_('8');
     with Tong60.frReport40_02 do begin
       FindObject('Memo202_1').Memo.Text:=lSqry.FieldByName('F11').AsString;
       FindObject('Memo204_1').Memo.Text:=lSqry.FieldByName('F12').AsString;
       FindObject('Memo206_1').Memo.Text:=lSqry.FieldByName('F21').AsString;
       FindObject('Memo208_1').Memo.Text:=lSqry.FieldByName('F22').AsString+
                                      ' '+lSqry.FieldByName('F31').AsString+
                                      ' '+lSqry.FieldByName('F32').AsString;
       FindObject('Memo210_1').Memo.Text:=lSqry.FieldByName('F41').AsString;
       FindObject('Memo212_1').Memo.Text:=lSqry.FieldByName('F42').AsString;
     end; }

     Sqlen :=
     'Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo,Gbigo '+
     'From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
     Translate(Sqlen, '@Gcode', p_Gcode);

     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.busyloop;
     if Base10.Socket.Body_Data <> 'NODATA' then begin
       Base10.Socket.MakeData;
       with Tong60.frReport40_02 do begin
         FindObject('Memo215_1').Memo.Text:=Base10.Socket.GetData(1, 1);

         if FindObject('Memo217_1').Prop['Alignment']=10 then begin
           if Base10.Socket.GetData(1, 8)='' then
           FindObject('Memo217_1').Memo.Text:=Base10.Socket.GetData(1, 2)
           else
           FindObject('Memo217_1').Memo.Text:=Base10.Socket.GetData(1, 8);
         end else
           FindObject('Memo217_1').Memo.Text:=Base10.Socket.GetData(1, 2);

         FindObject('Memo219_1').Memo.Text:=Base10.Socket.GetData(1, 3);
         FindObject('Memo221_1').Memo.Text:=Base10.Socket.GetData(1, 4)+
                                        ' '+Base10.Socket.GetData(1, 5);
         FindObject('Memo223_1').Memo.Text:=Base10.Socket.GetData(1, 6);
         FindObject('Memo225_1').Memo.Text:=Base10.Socket.GetData(1, 7);
       end;
     end;

     with Tong60.frReport40_02 do begin
       FindObject('Memo320_1').Memo.Text:=Copy(p_Gdate,1,4);
       FindObject('Memo321_1').Memo.Text:=Copy(p_Gdate,6,2);
       FindObject('Memo322_1').Memo.Text:=Copy(p_Gdate,9,2);
       FindObject('Memo323_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Space)]),10,1);
       FindObject('Memo334_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),10,1);
       FindObject('Memo333_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),09,1);
       FindObject('Memo332_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),08,1);
       FindObject('Memo331_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),07,1);
       FindObject('Memo330_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),06,1);
       FindObject('Memo329_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),05,1);
       FindObject('Memo328_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),04,1);
       FindObject('Memo327_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),03,1);
       FindObject('Memo326_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),02,1);
       FindObject('Memo325_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gosum)]),01,1);

       FindObject('Memo349_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),10,1);
       FindObject('Memo348_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),09,1);
       FindObject('Memo347_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),08,1);
       FindObject('Memo346_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),07,1);
       FindObject('Memo345_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),06,1);
       FindObject('Memo344_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),05,1);
       FindObject('Memo343_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),04,1);
       FindObject('Memo342_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),03,1);
       FindObject('Memo341_1').Memo.Text:=Copy( Format('%10s',[FormatFloat('########0',p_Gbsum)]),02,1);

       FindObject('Memo407_1').Memo.Text:=Copy(p_Gdate,6,2);
       FindObject('Memo408_1').Memo.Text:=Copy(p_Gdate,9,2);
     //FindObject('Memo409_1').Memo.Text:=lSqry.FieldByName('F51').AsString;
       FindObject('Memo413_1').Memo.Text:=Format('%10s',[FormatFloat('###,###,##0',p_Gosum)]);
       FindObject('Memo440_1').Memo.Text:=Format('%10s',[FormatFloat('###,###,##0',p_Gbsum)]);
       FindObject('Memo505_1').Memo.Text:=Format('%10s',[FormatFloat('###,###,##0',p_Gssum)]);
     end;
     oSqry.Next;
  end;
end;

procedure TTong60.frReport99_00GetValue(const ParName: String;
  var ParValue: Variant);
begin
{ if Sobo61.Edit106.Text='' Then begin
    if ParName = 'Name1' then
      ParValue := '';
    if ParName = 'Name2' then
      ParValue := '';
  end else begin
    if ParName = 'Name1' then
      ParValue := '도  서  명 :';
    if ParName = 'Name2' then
      ParValue := Sobo61.Edit104.Text+' - '+Sobo61.Edit106.Text;
  end;

  if ParName = 'Chulpan' then
    ParValue := mPrnt;
  if ParName = 'Select' then
    ParValue := Sobo61.DBGrid101.Columns.Items[5].Title.Caption;

  Tong60.frReport00_01.Dataset:=frDBDataSet00_01;
  Tong60.frReport00_01.Dataset:=frDBDataSet00_01;

  Tong60.frReport00_01.FindObject('Memo26').Memo.Clear;
  Tong60.frReport00_01.FindObject('Memo26').Memo.Add(mPrnt);
  Tong60.frReport00_01.FindObject('Memo26').Memo.Text:='Test';
  Tong60.frReport00_01.FindObject('Memo26').Visible:=False;
  Tong60.frReport00_01.FindObject('Memo26').SetBounds(0,244,0,19);
  Tong60.frReport00_01.FindObject('Memo26').SetBounds(0,296,0,19);

//Tong60.frReport00_01.BuildPage..Pages.Pages(0).BorderStyle.Form.BuildPage.
//Tong60.frReport00_01.Pages.Pages[0].pgHeight;
//Tong60.frReport00_01.Pages.Pages[0].Height;


  Tong60.frReport00_01.FindObject('Memo26').Prop['Font.Style']:=2;
  Tong60.frReport00_01.FindObject('Memo26').Prop['Font.Color']:=Tong60.Font.Color;
  Tong60.frReport00_01.FindObject('Memo26').Prop['Font.Size']:=Tong60.Font.Size;
  Tong60.frReport00_01.FindObject('Memo26').Prop['Font.Name']:=Tong60.Font.Name;

  Tong60.frReport00_01.PrepareReport; //바로출력
  Tong60.frReport00_01.PrintPreparedReport(' ',1,true, frall);//숫자 1은 1번만 출력한다
  if PrepareReport then
  PrintPreparedReport('', 1); }
end;

procedure TTong60.frDBDataSet00_01Next(Sender: TObject);
begin
  {재고현황}
  While(oSqry.EOF=False)and(oSqry.FieldByName('Goqut').AsFloat<=0)and
       (oSqry.EOF=False)and(oSqry.FieldByName('Gjqut').AsFloat<=0)do begin
    oSqry.Next;
  end;
end;

procedure TTong60.frDBDataSet00_02Next(Sender: TObject);
var p_Gjeja: String;
begin
  {출고현황}
{ While(oSqry.EOF=False)do begin
    Sqlen := 'Select Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', oSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', Hnnnn);
    p_Gjeja:=Base10.Seek_Name(Sqlen);
    if p_Gjeja<>'1' Then
      oSqry.Next
    else
      Exit;
  end; }
end;

procedure TTong60.frDBDataSet00_03Next(Sender: TObject);
begin
  {영업일보}
  While(oSqry.EOF=False)and(oSqry.FieldByName('Gosum').AsFloat=0)and
       (oSqry.EOF=False)and(oSqry.FieldByName('Giqut').AsFloat=0)and
       (oSqry.EOF=False)and(oSqry.FieldByName('Gisum').AsFloat=0)and
       (oSqry.EOF=False)and(oSqry.FieldByName('Gsusu').AsFloat=0)and
       (oSqry.EOF=False)and(oSqry.FieldByName('Gbsum').AsFloat=0)and
       (oSqry.EOF=False)and(oSqry.FieldByName('Gjsum').AsFloat=0)do begin
    oSqry.Next;
  end;
end;

procedure TTong60.frReport24_01GetValue(const ParName: String;
  var ParValue: Variant);
var St1,St2,St3,St4,St5: String;
begin
{ if ParName = 't_Gssum' then begin
     Tong40.PrinTing08(
     oSqry.FieldByName('Scode').AsString,
     oSqry.FieldByName('Gcode').AsString,
     oSqry.FieldByName('Gdate').AsString,
     oSqry.FieldByName('Gubun').AsString,
     oSqry.FieldByName('Jubun').AsString);
     with Tong60.frReport24_01 do begin
       FindObject('Memo36').Memo.Text:=FormatFloat('###,###,##0',p_GsumX);
     end;
     ParValue:=FormatFloat('###,###,##0',p_GsumX);
  end;
  if ParName = 't_Gsusu' then begin
     St1:='Gdate'+'='+#39+oSqry.FieldByName('Gdate').AsString+#39+' and '+
          'Gcode'+'='+#39+oSqry.FieldByName('Gcode').AsString+#39+' and '+
          'Scode'+'='+#39+oSqry.FieldByName('Scode').AsString+#39+' and '+
          'Hcode'+'='+#39+Hnnnn+#39;

     St4:='Gubun='+#39+'입금'+#39+' and ';
     St5:='Gubun='+#39+'출금'+#39+' and ';
     St3:='';
     St3:=St3+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
     St3:=St3+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St4+D_Select+St1+' ) as Gosum,';
     St3:=St3+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St5+D_Select+St1+' ) as Gbsum ';
     St3:=St3+' From H1_Ssub S Where '+D_Select+St1;

     if ePrnt='2' then begin
     St3:='';
     St3:=St3+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
     St3:=St3+' Sum(if('+St4+D_Select+St1+',gssum,0))as Gosum,';
     St3:=St3+' Sum(if('+St5+D_Select+St1+',gssum,0))as Gbsum ';
     St3:=St3+' From H1_Ssub S Where '+D_Select+St1;
     end;

     Sqlen := St3+' Group By Gcode ';

     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.busyloop;
     if Base10.Socket.body_data <> 'ERROR' then
        Base10.Socket.MakeGrid(SGrid)
     else ShowMessage(E_Open);

     T01:=0;
     T02:=0;
     List1:=0;
     While SGrid.RowCount-1 > List1 do begin
     List1:=List1+1;
       T01:=StrToIntDef(SGrid.Cells[ 2,List1],0);
       T02:=StrToIntDef(SGrid.Cells[ 3,List1],0);
     end;

     with Tong60.frReport24_01 do begin
       FindObject('Memo38').Memo.Text:=FormatFloat('###,###,##0',T01-T02);
     end;
     ParValue:=FormatFloat('###,###,##0',T01-T02);
  end; }
end;

end.
